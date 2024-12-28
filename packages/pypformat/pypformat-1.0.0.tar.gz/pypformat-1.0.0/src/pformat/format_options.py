from dataclasses import MISSING, asdict, dataclass, field, fields
from typing import Any, MutableSequence, Optional

from .common_types import TypeProjectionFuncMapping
from .formatter_types import TypeFormatter
from .indentation_utility import IndentType
from .text_style import TextStyle


@dataclass
class FormatOptions:
    compact: bool = False
    width: int = 50
    indent_type: IndentType = field(default_factory=lambda: IndentType.NONE())
    text_style: TextStyle = field(default_factory=TextStyle)
    style_entire_text: bool = False
    exact_type_matching: bool = False
    projections: Optional[TypeProjectionFuncMapping] = None
    formatters: Optional[MutableSequence[TypeFormatter]] = None

    def __post_init__(self):
        if not isinstance(self.text_style, TextStyle):
            self.text_style = TextStyle.new(self.text_style)

    def asdict(self, shallow: bool = True) -> dict:
        if shallow:
            return {field.name: getattr(self, field.name) for field in fields(self)}

        return asdict(self)

    @staticmethod
    def default(opt_name: str) -> Any:
        field = FormatOptions.__dataclass_fields__[opt_name]
        if field.default_factory is not MISSING:
            return field.default_factory()
        return field.default
