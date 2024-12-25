import functools
from typing import Optional, Union

import immutables as immu
from pypika import analytics as an
from pypika.dialects import ClickHouseQuery
from pypika.enums import Order
from pypika.queries import AliasedQuery, QueryBuilder, Selectable, Table
from pypika.terms import Criterion, EmptyCriterion, Field

from tesseract_olap.backend import ParamManager
from tesseract_olap.common import shorthash
from tesseract_olap.query import (
    Comparison,
    DataQuery,
    FilterCondition,
    HierarchyField,
    LevelField,
    LogicOperator,
    NullityOperator,
    NumericConstraint,
    Restriction,
    TimeRestriction,
)
from tesseract_olap.schema import models as sch

from .sql_common import _get_aggregate, _transf_formula

SchemaTable = Union[sch.Table, sch.InlineTable]


def _find_timerestriction(query: DataQuery):
    gen_restriction = (
        (hiefi, lvlfi, lvlfi.time_restriction)
        for hiefi in query.fields_qualitative
        for lvlfi in hiefi.levels
        if lvlfi.time_restriction is not None
    )
    return next(gen_restriction, None)


def sql_dataquery(query: DataQuery) -> tuple[QueryBuilder, ParamManager]:
    # Manages parameters for safe SQL execution
    meta = ParamManager()

    @functools.cache
    def _convert_table(table: SchemaTable, alias: Optional[str]) -> Table:
        """Converts schema-defined tables into query tables for SQL generation."""
        if isinstance(table, sch.Table):
            return Table(table.name, schema=table.schema, alias=alias)
        else:
            meta.set_table(table)
            return Table(table.name, alias=alias)

    def _get_table(table: Optional[SchemaTable], *, alias: Optional[str] = None):
        """Returns a specified table, or the default fact table if not defined."""
        return table_fact if table is None else _convert_table(table, alias)

    table_fact = _convert_table(query.cube.table, "tfact")  # Core fact table

    qb_from = (
        ClickHouseQuery.from_(table_fact)
        .select(*_tfrom_select(query, table_fact))
        .where(_tfrom_where(query, table_fact))
    )

    qb_join = AliasedQuery("qb_from")

    time_restriction = _find_timerestriction(query)
    if time_restriction:
        restr_hiefi, restr_lvlfi, restr = time_restriction
        restr_table = _get_table(restr_hiefi.table)
        qb_join = _tjoin_timerestriction(
            qb_join, restr_table, restr_hiefi, restr_lvlfi, restr
        )

    tjoin = qb_join if isinstance(qb_join, AliasedQuery) else AliasedQuery("qb_join")
    qb_group = (
        ClickHouseQuery.from_(tjoin)
        .select(*_tgroup_select(query, tjoin))
        .groupby(*_tgroup_groupby(query, tjoin))
        .having(_tgroup_having(query))
    )

    for field, order in _tgroup_sorting(query, tjoin):
        qb_group = qb_group.orderby(field, order=order)

    qb = (
        ClickHouseQuery.with_(qb_from, "qb_from")
        .with_(qb_join, "qb_join")
        .with_(qb_group, "qb_group")
    )

    # apply pagination parameters if values are higher than zero
    limit, offset = query.pagination.as_tuple()
    if limit > 0:
        qb = qb.limit(limit)
    if offset > 0:
        qb = qb.offset(offset)

    return qb, meta


def _tfrom_select(query: DataQuery, tfrom: Selectable):
    """
    Yields the fields from the fact table that will be used later in the queries.
    """
    # ensure key_columns are being selected just once
    unique_measure_columns = {
        shorthash(measure.key_column): measure.key_column
        for msrfi in query.fields_quantitative
        for measure in msrfi.measure.and_submeasures()
        if isinstance(measure, sch.Measure)
    }
    # get the fields from the fact table which contain the values
    # to aggregate and filter; ensure to not duplicate key_column
    yield from (
        tfrom.field(key_column).as_(f"ms_{alias_key}")
        for alias_key, key_column in unique_measure_columns.items()
    )
    # also select the associated columns needed as parameters
    # for the advanced aggregation functions
    yield from (
        tfrom.field(column).as_(f"msp_{msrfi.alias_key}_{alias}")
        for msrfi in query.fields_quantitative
        for alias, column in msrfi.measure.aggregator.get_columns()
    )

    locale = query.locale

    for hiefi in query.fields_qualitative:
        if hiefi.table is None:
            # all relevant columns are in fact table
            yield from (
                tfrom.field(column.name).as_(f"lv_{column.hash}")
                for lvlfi in hiefi.drilldown_levels
                for column in lvlfi.iter_columns(locale)
            )
        else:
            # only foreign key is available
            yield tfrom.field(hiefi.foreign_key).as_(f"fk_{hiefi.alias}")


def _tfrom_where(query: DataQuery, tfact: Selectable) -> Criterion:
    """
    Yields the conditions that can be applied on the fact table to reduce the
    initial set of data, before any join and aggregation.
    """
    criterion = EmptyCriterion()

    for hiefi in query.fields_qualitative:
        tdim: Table = _convert_table(hiefi.table, alias=f"tdim_{hiefi.alias}")

        criterion_tdim = EmptyCriterion()

        for lvlfi in hiefi.levels:
            caster = lvlfi.level.key_type.get_caster()
            members_include = sorted(caster(mem) for mem in lvlfi.members_include)
            members_exclude = sorted(caster(mem) for mem in lvlfi.members_exclude)

            # here we only want cuts that can be applied on the fact table
            # ignore levels that are not primary key from other dimension tables
            if hiefi.table is None:
                key_column = tfact.field(lvlfi.key_column)
            elif lvlfi.key_column == hiefi.primary_key:
                key_column = tfact.field(hiefi.foreign_key)
            else:
                key_column = tdim.field(lvlfi.key_column)

            if members_include:
                criterion &= key_column.isin(members_include)
            if members_exclude:
                criterion &= key_column.notin(members_exclude)

        if not isinstance(criterion_tdim, EmptyCriterion):
            field_pkey = tdim.field(hiefi.primary_key)
            criterion &= tfact.field(hiefi.foreign_key).isin(
                ClickHouseQuery.from_(tdim).select(field_pkey).where(criterion_tdim)
            )

    return criterion


def _tjoin_timerestriction(
    tfrom: Selectable,
    tdim: Table,
    hiefi: HierarchyField,
    lvlfi: LevelField,
    restriction: TimeRestriction,
) -> QueryBuilder:
    # target:
    #   build a query FROM AliasedQuery(tfrom) that keeps only rows related to relevant time
    # need:
    #   criteria that can be applied on non-extended fact table that does this subquery
    #   for this needs to return the set of primary keys that globes the subset of time
    # assumption:
    #   primary keys always are the most fine-grained unit of time available; criteria
    #   always is more general, so set of primary keys is always subset of user request

    constraint = restriction.constraint

    field_fkey = tfrom.field(f"fk_{hiefi.alias}")

    if hiefi.table is None or hiefi.primary_key == lvlfi.key_column:
        field_restr = (
            tfrom.field(lvlfi.key_column) if hiefi.table is None else field_fkey
        )

        # qbA will be the query that resolves the subset of values that match the filter
        qb_a = ClickHouseQuery.from_(tfrom).select(field_restr).distinct()

        if constraint[0] is Restriction.EXPR:
            criterion = _filter_criterion(field_restr, constraint[1])
            qb_a = qb_a.where(criterion)

        else:  # Restriction.OLDEST, Restriction.LATEST
            order = Order.asc if constraint[0] == Restriction.OLDEST else Order.desc
            qb_a = qb_a.orderby(field_restr, order=order).limit(constraint[1])

        # qbB will get the subset of data that matches the time filter
        qb_b = (
            ClickHouseQuery.from_(tfrom)
            .select(tfrom.star)
            .where(field_restr.isin(qb_a))
        )

        return qb_b

    else:
        # This branch is more complicated; a translation from the dim table is needed

        field_restr = tdim.field(lvlfi.key_column)
        field_pkey = tdim.field(hiefi.primary_key)

        # First we need the set of foreign keys in tfrom to filter the possible values in tdim
        qb_a = ClickHouseQuery.from_(tfrom).select(field_fkey).distinct()

        # From tdim, we select the column of the level the user wants to filter on, and get
        # its possible values filtered by the foreign keys obtained on the previous step
        qb_b = (
            ClickHouseQuery.from_(tdim)
            .select(field_restr)
            .distinct()
            .where(field_pkey.isin(qb_a))
        )

        # We resolve and apply the user filter to this subset and get the values of the user column
        if constraint[0] is Restriction.EXPR:
            criterion = _filter_criterion(field_restr, constraint[1])
            qb_b = qb_b.having(criterion)

        else:  # Restriction.OLDEST, Restriction.LATEST
            order = Order.asc if constraint[0] == Restriction.OLDEST else Order.desc
            qb_b = qb_b.orderby(field_restr, order=order).limit(constraint[1])

        # Then we select the primary keys where the user column is in the set of the last step
        # We need to do this separatedly because we need the DISTINCT to apply to the user column
        qb_c = (
            ClickHouseQuery.from_(tdim).select(field_pkey).where(field_restr.isin(qb_b))
        )
        # And finally we filter tfrom using that set of primary keys against the foreign keys
        qb_d = (
            ClickHouseQuery.from_(tfrom).select(tfrom.star).where(field_fkey.isin(qb_c))
        )

        return qb_d


def _tgroup_select(query: DataQuery, tcore: Selectable):
    locale = query.locale

    level_columns = immu.Map(
        (column.alias, f"lv_{column.hash}")
        for hiefi in query.fields_qualitative
        for lvlfi in hiefi.levels
        for column in lvlfi.iter_columns(locale)
    )

    # Translates column names to fields in the grouping query
    def _translate_col(column: str):
        return Field(
            level_columns.get(column, column),
            table=tcore if column in level_columns else None,
        )

    for msrfi in query.fields_quantitative:
        if isinstance(msrfi.measure, sch.Measure):
            yield _get_aggregate(tcore, msrfi)

        if isinstance(msrfi.measure, sch.CalculatedMeasure):
            formula = msrfi.measure.formula
            yield _transf_formula(formula, _translate_col).as_(msrfi.name)

        # Creates Ranking columns using window functions
        if msrfi.with_ranking is not None:
            yield an.Rank(alias=f"{msrfi.name} Ranking").orderby(
                Field(msrfi.name),
                order=Order.asc if msrfi.with_ranking == "asc" else Order.desc,
            )

    yield from _tgroup_groupby(query, tcore)


def _tgroup_groupby(query: DataQuery, tcore: Selectable):
    locale = query.locale

    for hiefi in query.fields_qualitative:
        if hiefi.table is None:
            yield from (
                tcore.field(f"lv_{column.hash}")
                for lvlfi in hiefi.drilldown_levels
                for column in lvlfi.iter_columns(locale)
            )
        else:
            yield tcore.field(f"fk_{hiefi.foreign_key}")


def _tgroup_having(query: DataQuery):
    """Applies user-defined filters on aggregated data."""
    criterion = EmptyCriterion()

    for msrfi in query.fields_quantitative:
        if msrfi.constraint:
            criterion &= _filter_criterion(Field(msrfi.name), msrfi.constraint)

    return criterion


def _tgroup_sorting(query: DataQuery, tcore: Selectable):
    if not query.sorting:
        return None

    locale = query.locale
    sort_field, sort_order = query.sorting.as_tuple()

    for hiefi in query.fields_qualitative:
        for lvlfi in hiefi.drilldown_levels:
            for column in lvlfi.iter_columns(locale):
                if sort_field == column.alias:
                    order = Order.asc if sort_order == "asc" else Order.desc
                    yield tcore.field(f"lv_{column.hash}"), order

    for msrfi in query.fields_quantitative:
        for measure in msrfi.measure.and_submeasures():
            if isinstance(measure, sch.Measure) and sort_field == measure.name:
                order = Order.asc if sort_order == "asc" else Order.desc
                yield tcore.field(f"ms_{shorthash(measure.key_column)}"), order

    yield from (
        (tcore.field(f"lv_{column.hash}"), Order.asc)
        for hiefi in query.fields_qualitative
        if (not query.topk or hiefi.deepest_level.name in query.topk.levels)
        for lvlfi in hiefi.drilldown_levels
        for index, column in enumerate(lvlfi.iter_columns(locale))
        if index == 0
    )


def _trich_pagination(query: DataQuery, tgroup: Selectable):
    pass


def _tnext_topk(query: DataQuery, tprev: Selectable) -> Optional[QueryBuilder]:
    """
    Builds the query which will perform the grouping by drilldown members,
    and then the aggregation over the resulting groups.
    """

    qb: QueryBuilder = ClickHouseQuery.from_(tprev)

    if query.topk is None:
        return None

    topk_fields = [Field(x) for x in query.topk.levels]
    topk_colname = f"Top {query.topk.measure}"
    topk_order = Order.asc if query.topk.order == "asc" else Order.desc

    subquery = (
        qb.select(tprev.star)
        .select(
            an.RowNumber()
            .over(*topk_fields)
            .orderby(Field(query.topk.measure), order=topk_order)
            .as_(topk_colname),
        )
        .orderby(Field(topk_colname), order=Order.asc)
    )

    return (
        ClickHouseQuery.from_(subquery)
        .select(subquery.star)
        .where(subquery.field(topk_colname) <= query.topk.amount)
    )


def _filter_criterion(column: Field, constraint: FilterCondition) -> Criterion:
    """Apply comparison filters to query"""
    # create criterion for first constraint
    if constraint == NullityOperator.ISNULL:
        return column.isnull()
    if constraint == NullityOperator.ISNOTNULL:
        return column.isnotnull()

    criterion = _filter_comparison(column, constraint[0])

    # add second constraint to criterion if defined
    if len(constraint) == 1:
        return criterion
    elif constraint[1] == LogicOperator.AND:
        return criterion & _filter_comparison(column, constraint[2])
    elif constraint[1] == LogicOperator.OR:
        return criterion | _filter_comparison(column, constraint[2])
    elif constraint[1] == LogicOperator.XOR:
        return criterion ^ _filter_comparison(column, constraint[2])

    raise ValueError(f"Invalid constraint: {constraint}")


def _filter_comparison(field: Field, constr: NumericConstraint) -> Criterion:
    """Retrieves the comparison operator for the provided field."""
    comparison, scalar = constr

    # Note we must use == to also compare Enums values to strings
    if comparison == Comparison.GT:
        return field.gt(scalar)
    if comparison == Comparison.GTE:
        return field.gte(scalar)
    if comparison == Comparison.LT:
        return field.lt(scalar)
    if comparison == Comparison.LTE:
        return field.lte(scalar)
    if comparison == Comparison.EQ:
        return field.eq(scalar)
    if comparison == Comparison.NEQ:
        return field.ne(scalar)

    raise ValueError(f"Invalid criterion type: {comparison}")
