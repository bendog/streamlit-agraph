from .edge import Edge
from .node import Node


class Triple:
    def __init__(self, subj: Node, pred: Edge, obj: Node) -> None:
        self.subj = subj
        self.pred = pred
        self.obj = obj
