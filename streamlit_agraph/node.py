from typing import Annotated, Any, Literal

Shape = Annotated[
    str,
    Literal[
        "image",
        "circularImage",
        "diamond",
        "dot",
        "star",
        "triangle",
        "triangleDown",
        "hexagon",
        "square",
        "icon",
    ],
]


class Node:
    """Node class for representing a node in a graph."""

    def __init__(
        self,
        id: str,
        title: str | None = None,  # displayed if hovered"
        label: str | None = None,  # displayed inside the node
        link: str | None = None,  # link to open if double clicked
        color: str | None = None,
        shape: Shape = "dot",
        size: int = 25,
        **kwargs,
    ):
        self.id: str = id
        self.title: str = id if not title else title
        self.label: str | None = label
        self.shape: Shape = shape  # # image, circularImage, diamond, dot, star, triangle, triangleDown, hexagon, square and icon
        self.size: int = size
        self.color: str = color  # FDD2BS #F48B94 #F7A7A6 #DBEBC2
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and getattr(other, "id", None) == self.id

    def __hash__(self) -> int:
        return hash(self.id)
