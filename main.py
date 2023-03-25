from graphviz import Source

from facades import OBDDVar, Expression, OBDD

# initialize the variables
a, b, c, d, e, f, j, p, q, r, z = OBDDVar.create_variables(['a', 'b', 'c', 'd', 'e', 'f', 'j', 'p', 'q', 'r', 'z'])
# create an expression
e = Expression((j | a & b | r & c | b & q | z & p) & (c ^ p ^ j) & (~r))
# create an obdd
obdd = OBDD()
# covnert expression into obdd
obdd.from_expression(expr=e)
# get the source of obdd
gv = Source(obdd.source())
# visualize the graph
gv.render('output/out_bdd', view=True)
