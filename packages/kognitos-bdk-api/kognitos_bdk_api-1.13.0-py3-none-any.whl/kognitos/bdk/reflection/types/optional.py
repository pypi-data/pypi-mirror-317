from typing import List

from .base import ConceptType


class ConceptOptionalType(ConceptType):
    def __init__(self, inner: ConceptType):
        self.type = inner

    def simplify(self) -> ConceptType:
        return ConceptOptionalType(self.type.simplify())

    def children(self) -> List[ConceptType]:
        return [self.type]

    def replace(self, old: ConceptType, new: ConceptType) -> ConceptType:
        if self == old:
            return new
        return ConceptOptionalType(self.type.replace(old, new))

    def __eq__(self, other) -> bool:
        if isinstance(other, ConceptOptionalType):
            return self.type == other.type
        return False

    def __repr__(self) -> str:
        return f"Optional[{self.type.name}]"

    def __str__(self) -> str:
        return f"{self.type.name}?"

    def __hash__(self) -> int:
        combined_hash = hash("Optional")
        combined_hash ^= hash(self.type)
        return combined_hash
