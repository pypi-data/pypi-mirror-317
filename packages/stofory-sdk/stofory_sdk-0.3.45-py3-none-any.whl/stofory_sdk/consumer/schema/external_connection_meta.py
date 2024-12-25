from typing import List

import msgspec


class ExternalOptionMapping(msgspec.Struct):
    external_option_id: int
    internal_option_id: int


class ExternalParameterMapping(msgspec.Struct):
    external_parameter_id: int
    internal_parameter_id: int

    options: List[ExternalOptionMapping] | None
