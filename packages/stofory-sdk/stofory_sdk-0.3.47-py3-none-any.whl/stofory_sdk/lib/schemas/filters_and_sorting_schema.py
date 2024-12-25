from typing import Dict, Literal, List, Union, Optional, Any, TypeVar
import msgspec


__all__ = ('SortType', 'FieldFilter', 'SortingRulesSchema', 'FilteringRulesSchema')
T = TypeVar("T", bool, str, int, float)

SortType = Literal["asc", "desc"]


class FieldFilter[T](msgspec.Struct, forbid_unknown_fields=True):
    and_: Optional[Literal[1, 0]] = None
    ge: Optional[T] = None
    gt: Optional[T] = None
    le: Optional[T] = None
    lt: Optional[T] = None
    e: Optional[T] = None
    like: Optional[T] = None
    ilike: Optional[T] = None

    def __post_init__(self):
        self.validate_filters()

    def validate_filters(self):
        """Validate the filter rules."""
        non_empty_fields = {key for key, value in msgspec.structs.asdict(self).items() if
                            value is not None and key != "and_"}
        if self.and_ is None:
            if len(non_empty_fields) > 1:
                raise ValueError("Field 'and_' must be specified if more than one filter is present.")
        elif len(non_empty_fields) == 1:
            raise ValueError("Field 'and_' must be empty if exactly one filter is present.")
        return self


class SortingRulesSchema(msgspec.Struct, kw_only=True):
    sorting_order: Optional[Union[str, List[str]]] = None
    __sorting_rules: Dict[str, SortType] = msgspec.field(default_factory=dict)

    def __post_init__(self):
        """Populate sorting rules based on the sorting order and fields."""
        sorting_order = self.sorting_order
        if isinstance(sorting_order, str):
            sorting_order = sorting_order.split(",")

        data = {}

        for key, value in msgspec.to_builtins(self).items():
            if isinstance(value, str) and value.strip().lower() in {"asc", "desc"}:
                new_key = key.split("s__")
                if len(new_key) == 2:
                    data[new_key[1]] = value.strip().lower()

        if sorting_order:
            sorted_data = {}
            for key in sorting_order:
                if key in data:
                    sorted_data[key] = data[key]
            for key in data:
                if key not in sorted_data:
                    sorted_data[key] = data[key]
            self.__sorting_rules = sorted_data
        else:
            self.__sorting_rules = data

    def get_sorting_rules(self) -> Dict[str, SortType]:
        """Retrieve the populated sorting rules."""
        return self.__sorting_rules


class FilteringRulesSchema(msgspec.Struct):
    __filter_rules: Dict[str, Dict[str, Any]] = msgspec.field(default_factory=dict)

    def __post_init__(self):
        """Populate filter rules."""
        filters = {}
        # msgspec.structs.asdict(self).items()
        # for key, value in msgspec.to_builtins(self).items():
        #     if isinstance(value, dict):
        #         for local_key, local_value in value.items():
        #             if local_key in set(msgspec.structs.asdict(FieldFilter()).keys()):
        #                 new_key = key.split("f__")
        #                 if len(new_key) == 2:
        #                     filters[new_key[1]] = value
        for key, value in msgspec.structs.asdict(self).items():
            if isinstance(value, FieldFilter):
                value.validate_filters()
                new_key = key.split("f__")
                if len(new_key) == 2:
                    filters[new_key[1]] = value
        self.__filter_rules = filters

    def get_filter_rules(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve the populated filter rules."""
        return self.__filter_rules


class AreasOfResponsibilitiesQueryParamsSchemas(FilteringRulesSchema, kw_only=True):
    f__visibility: Optional[FieldFilter[bool]] = None
    f__coefficient: Optional[FieldFilter[float]] = None


# Usage example
schema = AreasOfResponsibilitiesQueryParamsSchemas(
    f__visibility=FieldFilter(e=True)
)
# print(schema)
schema.get_filter_rules()
# print("Sorting Rules:", schema.get_filter_rules())
