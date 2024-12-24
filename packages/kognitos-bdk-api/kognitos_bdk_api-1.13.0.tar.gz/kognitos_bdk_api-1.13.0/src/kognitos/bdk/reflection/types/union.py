from typing import List

from .base import ConceptType
from .self import ConceptSelfType


class ConceptUnionType(ConceptType):
    def __init__(self, inners: List[ConceptType]):
        self.inners = inners

    def simplify(self) -> ConceptType:
        seen = set()
        result = set()
        for inner in [inner.simplify() for inner in self.inners]:
            if inner not in seen:
                seen.add(inner)
                result.add(inner)

        if len(result) == 1:
            return next(iter(self.inners)).simplify()

        simplified_union = ConceptUnionType(list(result))

        inner_unions = simplified_union.find(ConceptUnionType)
        if inner_unions:
            for inner_union in inner_unions:
                new_simplified_union = simplified_union.replace(inner_union, ConceptSelfType())
                if new_simplified_union == inner_union:
                    simplified_union = new_simplified_union

        return simplified_union

    def __repr__(self) -> str:
        return f"Union[{','.join([inner.__repr__() for inner in self.inners])}]"

    def __str__(self) -> str:
        return " or ".join([f"`{inner.__str__()}`" for inner in list(self.inners)])

    def children(self) -> List[ConceptType]:
        return self.inners

    def replace(self, old: ConceptType, new: ConceptType) -> ConceptType:
        if self == old:
            return new
        replaced_inners = [inner.replace(old, new) for inner in self.inners]
        return ConceptUnionType(replaced_inners)

    def __eq__(self, other) -> bool:
        if isinstance(other, ConceptUnionType):
            return set(self.inners) == set(other.inners)
        return False

    def __hash__(self) -> int:
        combined_hash = hash("Union")
        for inner in self.inners:
            combined_hash ^= hash(inner)
        return combined_hash
