from typing import List

from obdd import obddvar, OBDDVariable, OrderedBinaryDecisionDiagram, expr2obdd


class OBDDVar:
    @staticmethod
    def create_variables(var_names: List[str]) -> List[OBDDVariable]:
        return list(map(obddvar, var_names))


class Expression:
    expr = None

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self):
        return self.expr


class OBDD:
    diagram: OrderedBinaryDecisionDiagram = None

    def __init__(self):
        pass

    def from_expression(self, expr: Expression) -> OrderedBinaryDecisionDiagram:
        self.diagram = expr2obdd(expr.evaluate())
        return self.diagram

    def source(self):
        return OBDD.clean_source(self.diagram.to_dot())

    @staticmethod
    def clean_source(source: str):
        return source.replace("label=0,shape=box", "label=⊥,shape=box") \
            .replace("label=1,shape=box", "label=T,shape=box").replace("label=0,", "").replace("label=1", "")
