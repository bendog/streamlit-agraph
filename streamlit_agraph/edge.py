from .node import Node


class Edge:
    """
    https://visjs.github.io/vis-network/docs/network/edges.html
    """

    def __init__(
        self,
        source: Node,
        target: Node,
        color: str = "#F7A7A6",
        # arrows_to=True,
        # arrows_from=False,
        **kwargs,
    ):
        self.source = source
        self.to = target
        self.color = color
        # self.arrows={"to": arrows_to, "from": arrows_from}
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        return {**self.__dict__, "from": self.source}
