import logging
from typing import Callable, Union

from pyparsing import ParseResults
from pypika import analytics as an
from pypika import functions as fn
from pypika.enums import Arithmetic, Boolean
from pypika.queries import Selectable
from pypika.terms import (
    AggregateFunction,
    ArithmeticExpression,
    Case,
    ComplexCriterion,
    Criterion,
    Field,
    NullValue,
    Term,
    ValueWrapper,
)

from tesseract_olap.query import (
    Comparison,
    LogicOperator,
    MeasureField,
    NullityOperator,
)

from .dialect import ArrayElement, Power, Quantile, TopK

logger = logging.getLogger(__name__)


def _get_aggregate(
    table: Selectable, msrfi: MeasureField
) -> Union[fn.Function, ArithmeticExpression]:
    """Generates an AggregateFunction instance from a measure, including all its
    parameters, to be used in the SQL query.
    """
    field = table.field(f"ms_{msrfi.alias_key}")
    # alias = f"ag_{msrfi.alias_name}"
    alias = msrfi.name

    if msrfi.aggregator_type == "Sum":
        return fn.Sum(field, alias=alias)

    elif msrfi.aggregator_type == "Count":
        return fn.Count(field, alias=alias)

    elif msrfi.aggregator_type == "Average":
        return fn.Avg(field, alias=alias)

    elif msrfi.aggregator_type == "Max":
        return fn.Max(field, alias=alias)

    elif msrfi.aggregator_type == "Min":
        return fn.Min(field, alias=alias)

    elif msrfi.aggregator_type == "Mode":
        return ArrayElement(TopK(1, field), 1, alias=alias)

    # elif msrfi.aggregator_type == "BasicGroupedMedian":
    #     return fn.Abs()

    elif msrfi.aggregator_type == "WeightedSum":
        params = msrfi.aggregator_params
        weight_field = table.field(f"msp_{msrfi.alias_key}_weight")
        return fn.Sum(field * weight_field, alias=alias)

    elif msrfi.aggregator_type == "WeightedAverage":
        params = msrfi.aggregator_params
        weight_field = table.field(f"msp_{msrfi.alias_key}_weight")
        return AggregateFunction("avgWeighted", field, weight_field, alias=alias)

    # elif msrfi.aggregator_type == "ReplicateWeightMoe":
    #     return fn.Abs()

    elif msrfi.aggregator_type == "CalculatedMoe":
        params = msrfi.aggregator_params
        critical_value = ValueWrapper(params["critical_value"])
        term = fn.Sqrt(fn.Sum(Power(field / critical_value, 2)))
        return ArithmeticExpression(Arithmetic.mul, term, critical_value, alias=alias)

    elif msrfi.aggregator_type == "Median":
        return AggregateFunction("median", field, alias=alias)

    elif msrfi.aggregator_type == "Quantile":
        params = msrfi.aggregator_params
        quantile_level = float(params["quantile_level"])
        return Quantile(quantile_level, field, alias=alias)

    elif msrfi.aggregator_type == "DistinctCount":
        # Count().distinct() might use a different function, configured in Clickhouse
        return AggregateFunction("uniqExact", field, alias=alias)

    # elif msrfi.aggregator_type == "WeightedAverageMoe":
    #     return fn.Abs()

    raise NameError(
        f"Clickhouse module not prepared to handle aggregation type: {msrfi.aggregator_type}"
    )


def _get_filter_criterion(column: Field, constraint: FilterCondition) -> Criterion:
    """Apply comparison filters to query"""
    # create criterion for first constraint
    if constraint == NullityOperator.ISNULL:
        criterion = column.isnull()
    elif constraint == NullityOperator.ISNOTNULL:
        criterion = column.isnotnull()
    else:
        criterion = _get_filter_comparison(column, constraint[0])
        # add second constraint to criterion if defined
        if len(constraint) == 3:
            criterion2 = _get_filter_comparison(column, constraint[2])
            if constraint[1] == LogicOperator.AND:
                criterion &= criterion2
            elif constraint[1] == LogicOperator.OR:
                criterion |= criterion2
    return criterion


def _get_filter_comparison(field: Field, constr: NumericConstraint) -> Criterion:
    """Retrieves the comparison operator for the provided field."""
    comparison, scalar = constr

    # Note we must use == to also compare Enums values to strings
    if comparison == Comparison.GT:
        return field.gt(scalar)
    elif comparison == Comparison.GTE:
        return field.gte(scalar)
    elif comparison == Comparison.LT:
        return field.lt(scalar)
    elif comparison == Comparison.LTE:
        return field.lte(scalar)
    elif comparison == Comparison.EQ:
        return field.eq(scalar)
    elif comparison == Comparison.NEQ:
        return field.ne(scalar)

    raise NameError(f"Invalid criterion type: {comparison}")


def _transf_formula(tokens, field_builder: Callable[[str], Field]) -> Term:
    if isinstance(tokens, ParseResults):
        if len(tokens) == 1:
            return _transf_formula(tokens[0], field_builder)

        if tokens[0] == "CASE":
            case = Case()

            for item in tokens[1:]:
                if item[0] == "WHEN":
                    clauses = _transf_formula(item[1], field_builder)
                    expr = _transf_formula(item[3], field_builder)
                    case = case.when(clauses, expr)
                elif item[0] == "ELSE":
                    expr = _transf_formula(item[1], field_builder)
                    case = case.else_(expr)
                    break

            return case

        if tokens[0] == "NOT":
            # 2 tokens: ["NOT", A]
            return _transf_formula(tokens[1], field_builder).negate()

        if tokens[1] in ("AND", "OR", "XOR"):
            # 2n + 1 tokens: [A, "AND", B, "OR", C]
            left = _transf_formula(tokens[0], field_builder)
            for index in range(len(tokens) // 2):
                comparator = Boolean(tokens[index * 2 + 1])
                right = _transf_formula(tokens[index * 2 + 2], field_builder)
                left = ComplexCriterion(comparator, left, right)
            return left

        column = tokens[1]
        assert isinstance(column, str), f"Malformed formula: {tokens}"

        if tokens[0] == "ISNULL":
            return field_builder(column).isnull()

        if tokens[0] == "ISNOTNULL":
            return field_builder(column).isnotnull()

        if tokens[0] == "TOTAL":
            return an.Sum(field_builder(column)).over()

        if tokens[0] == "SQRT":
            return fn.Sqrt(field_builder(column))

        if tokens[0] == "POW":
            return field_builder(column) ** tokens[2]

        operator = column

        if operator in ">= <= == != <>":
            branch_left = _transf_formula(tokens[0], field_builder)
            branch_right = _transf_formula(tokens[2], field_builder)

            if operator == ">":
                return branch_left > branch_right
            elif operator == "<":
                return branch_left < branch_right
            elif operator == ">=":
                return branch_left >= branch_right
            elif operator == "<=":
                return branch_left <= branch_right
            elif operator == "==":
                return branch_left == branch_right
            elif operator in ("!=", "<>"):
                return branch_left != branch_right

            raise ValueError(f"Operator '{operator}' is not supported")

        if operator in "+-*/%":
            branch_left = _transf_formula(tokens[0], field_builder)
            branch_right = _transf_formula(tokens[2], field_builder)

            if operator == "+":
                return branch_left + branch_right
            elif operator == "-":
                return branch_left - branch_right
            elif operator == "*":
                return branch_left * branch_right
            elif operator == "/":
                return branch_left / branch_right
            elif operator == "%":
                return branch_left % branch_right

            raise ValueError(f"Operator '{operator}' is not supported")

    elif isinstance(tokens, (int, float)):
        return ValueWrapper(tokens)

    elif isinstance(tokens, str):
        if tokens.startswith("'") and tokens.endswith("'"):
            return ValueWrapper(tokens[1:-1])
        elif tokens.startswith('"') and tokens.endswith('"'):
            return ValueWrapper(tokens[1:-1])
        elif tokens == "NULL":
            return NullValue()
        else:
            return field_builder(tokens)

    logger.debug("Couldn't parse formula: <%s %r>", type(tokens).__name__, tokens)
    raise ValueError(f"Expression '{tokens!r}' can't be parsed")
