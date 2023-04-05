<div align="justify">

# Ordered Binary Decision Diagrams (OBDDs) implementation in python

## Introduction

Ordered Binary Decision Diagrams (OBDDs) are a data structure used to represent boolean functions. A boolean function is
a function that takes a set of boolean inputs and returns a boolean output. OBDDs are particularly useful for
representing boolean functions with a large number of inputs, as they can provide a compact and efficient representation
of the function.

OBDDs are directed acyclic graphs (DAGs) with nodes representing sub-functions of the boolean function being
represented. The nodes in the graph are either variable nodes or terminal nodes. Variable nodes are labeled with a
variable index, and each variable node has two outgoing edges, one labeled 0 and one labeled 1(solid and dotted
according to the book). Terminal nodes are
labeled with a boolean value, either 0 or 1(T or ⊥ according to the book).

The nodes in the graph are arranged according to a total variable ordering, which is used to ensure that equivalent
boolean functions are represented by the same graph. The variable ordering is a total ordering of the variables in the
boolean function, which is used to determine the order in which the variable nodes are arranged in the graph. The
variable ordering is fixed for a given OBDD, meaning that the same variable ordering is used throughout the graph.

The construction of an OBDD involves recursively building the graph based on the boolean function being represented. At
each step, a variable node is added to the graph for the next variable in the variable ordering. The outgoing edges of
the variable node are determined by the values of the variable in the sub-functions being represented. If the values of
the variable are the same in all sub-functions, the outgoing edges of the variable node are connected to the same node
in the graph. If the values of the variable differ in the sub-functions, two new sub-graphs are recursively built for
each of the possible values of the variable, and the outgoing edges of the variable node are connected to the roots of
these sub-graphs.

OBDDs can be used for a variety of applications, including formal verification, circuit design, and optimization. They
are particularly useful in formal verification, where they can be used to verify the correctness of digital circuits or
software programs. OBDDs can also be used in circuit design and optimization to minimize the size of circuits and
improve their efficiency.

In summary, OBDDs are a powerful data structure for representing boolean functions in a compact and efficient manner.
They are based on a directed acyclic graph with nodes representing sub-functions of the boolean function. The nodes are
arranged according to a total variable ordering, and the construction of the graph is based on recursively building
sub-graphs for each variable in the variable ordering. OBDDs have many applications in computer science and logic and
can be used to optimize digital circuits, software programs, and other boolean functions.

## Implementation:

In this section, we will discuss how to implement a very simple OBDD in Python. We will start by discussing the basics
of OBDDs,
including the construction of the graph and the representation of boolean functions. We will then show how to build an
OBDD in Python and provide a sample implementation.
Basics of OBDDs:

An OBDD is a directed acyclic graph (DAG) with the following properties:

1. Every node in the graph is either a terminal node or a variable node.
2. Every variable node has two outgoing edges, corresponding to the two possible values of the variable (0 or 1).
3. Every path from the root of the graph to a terminal node corresponds to a unique assignment of values to the
   variables in the boolean function being represented.

An OBDD is ordered if the variables are assigned a total ordering, and the variable nodes are arranged in the graph
according to that ordering. This ordering is used to ensure that equivalent boolean functions are represented by the
same graph.

#### Boolean Functions Representation:

Every boolean function can be represented as a binary decision diagram. In this representation, every variable is
assigned a unique integer index, and the boolean function is represented as a DAG with the following properties:

1. The nodes in the DAG correspond to the sub-functions of the boolean function.
2. The root of the DAG corresponds to the entire boolean function.
3. Every node in the DAG is labeled with an integer index corresponding to the variable being tested.
4. Every variable in the boolean function is assigned a unique integer index.

#### Building an OBDD in Python:

To build an OBDD in Python, we need to represent the boolean function as a DAG, with each node corresponding to a
sub-function of the boolean function. We can use a dictionary to represent the nodes in the graph, with the keys of the
dictionary representing the indices of the variables being tested.

Here is a very small sample implementation of an OBDD in Python which is the base class of our code implementation:

```python
class Node:
    def __init__(self, index, low, high):
        self.index = index
        self.low = low
        self.high = high


def build_obdd(f, variables):
    node_dict = {}

    def _build_obdd(f, variables):
        if len(variables) == 0:
            return Node(None, None, None)
        index = variables[0]
        low = _build_obdd(f, variables[1:])
        high = _build_obdd(f, variables[1:])
        if (index, low.index, high.index) in node_dict:
            return node_dict[(index, low.index, high.index)]
        if f[index] == 0:
            node = Node(index, low, high)
        elif f[index] == 1:
            node = Node(index, high, low)
        else:
            node = Node(index, low, high)
        node_dict[(index, low.index, high.index)] = node
        return node

    return _build_obdd(f, variables)
```

In this implementation, f is a dictionary representing the boolean function, where the keys are the indices of the
variables and the values are either 0, 1, or None. variables is a list of the indices of the variables in the boolean
function. The function returns the root node of the OBDD.

## The Project

The project is implementation of OBDDs in python programming language which can be used to construct, manipulate, and
analyze Boolean functions represented as OBDDs. This project can be used to construct the binary tree structure for the
Boolean function, starting with the root node and then recursively constructing its left and right children. The project
can also include functions for manipulating and optimizing the OBDD, such as path compression(using reduce algorithm).

In addition, the project can include functionality for analyzing the OBDD, such as computing the number of nodes, the
size of the OBDD, or the number of different variable orders that can be used to represent the same function.

To make the project more practical, it can be integrated with other Python libraries or tools that are commonly used in
the field of circuit design or verification. For example, the project can be integrated with libraries that perform
model checking or theorem proving.

#### Files

The project contains several files which are responsible for different parts of the implementation in
python. `requirements.txt`
contains libraries that used inside the project(here only `graphviz`), the other files will be
discussed in the below sections:

##### _obdd.py_

Main file that implements the OBDD using an abstract way, the implementation uses a weak reference dictionary to cache
nodes and variables, so that identical nodes and variables
are reused where possible. This reduces the memory usage of the implementation, as well as speeding up the construction
of OBDDs.

The `OBDDNode` class represents an OBDD node, with a root value, a low child (lo), and a high child (hi). The root value
is an integer that represents a unique variable, and the lo and hi children are the next nodes in the graph, depending
on the value of the root variable. The `OBDDNode` class also defines the zero and one nodes, which have root values of
-1
and -2 respectively, and no children.

The `obddvar` function returns a unique Boolean variable instance represented by an ordered binary decision diagram.
Variable
instances may be used to symbolically construct larger OBDDs. The function takes a name and an optional index, and
registers the variable if it does not already exist. The implementation uses the boolean module to represent Boolean
expressions.

The `expr2obdd` function converts a Boolean expression into an OBDD by recursively building up the OBDD from its
constituent nodes. The _`expr2obddnode` function converts an expression into an OBDD node, by first checking if the
expression is zero or one, and otherwise selecting the top variable and recursively calling itself on the lo and hi
children.

The `_obddnode` function returns a unique OBDD node, either by creating a new one or returning a cached one. If the lo
and
hi children are the same node, then that node is returned, otherwise a new node is created with the given root, lo, and
hi values.

The `_obdd` function returns a unique OBDD, either by creating a new one or returning a cached one. If the node is
already
a registered OBDD, then that OBDD is returned, otherwise a new OBDD is created with the given node.

The `OrderedBinaryDecisionDiagram` class represents a Boolean function as an OBDD. The class defines methods for Boolean
operations, including logical not (~), or (|), and (&), xor (^), implication (=>), and reverse implication (<=). The
class also defines a method for restricting the function to a given point, and methods for checking if the function is
zero or one. The class uses cached_property to lazily compute and cache the input variables for the function.

##### _boolean.py_

This module implements the fundamental building blocks of Boolean variables and functions. It defines two classes:
`Variable` and `Function`, along with a helper function `var()` that returns a unique Variable instance.

Variable is a base class that represents a symbolic Boolean variable. It has two attributes: names, a tuple of variable
names in order of increasing scope, and indices, a tuple of integer indices. Each variable can have multiple names (
e.g., x[0] and y[0]), and multiple indices (e.g., x[0] and x[1]). The `__str__()` method returns a string representation
of the variable, including all names and indices.

`Function` is an abstract base class that defines an interface for a symbolic Boolean function. It has several methods
that define Boolean operators, such as `__invert__(), __or__(), __and__(), and __xor__()`, which return a new Function
object. It also has two properties: `inputs`, which returns the support set (i.e., the set of variables that appear in
the
function), and `top`, which returns the first variable in the ordered support set.

The `var()` function takes a variable name (or tuple of names) and an optional index (or tuple of indices) as arguments
and returns a unique Variable instance. If the same set of names and indices has already been seen, the function returns
the previously created Variable instance. The function raises various `TypeError` and `ValueError` exceptions if the
arguments are not of the expected type or value.

Finally, the module defines two global variables: `VARIABLES`, a dictionary that maps (names, indices) tuples to
Variable
instances, and `_UNIQIDS`, a dictionary that maps (names, indices) tuples to unique IDs used to distinguish between
variables with the same name and index. The global variable `_COUNT` is used to generate new unique IDs.

##### _facades.py_

This module defines a simplified wrapper class for using Ordered Binary Decision Diagrams (OBDDs) and manipulating
Boolean
expressions.

First, it imports the necessary modules: `typing` for specifying the types of variables and parameters, and several
classes from the `obdd` module, which provides an implementation of OBDDs and related operations.

The `OBDDVar` class provides a static method `create_variables()` that takes a list of variable names as input and
returns a
list of corresponding OBDD variables. The `obddvar()` function is imported from the `obdd` module and creates a new OBDD
variable object with the specified name.

The `Expression` class is a simple wrapper around a Boolean expression. It has an `evaluate()` method that returns the
expression itself.

The `OBDD` class provides methods for creating an OBDD from a Boolean expression and returning the source code of the
resulting diagram in DOT format. It has an instance variable diagram that holds the current OBDD.
The `from_expression()`
method takes an Expression object as input, evaluates it to obtain the corresponding Boolean expression, and converts it
to an OBDD using the `expr2obdd()` function from the `obdd` module. The resulting OBDD is stored in the diagram instance
variable and returned.

The `source()` method returns the source code of the current diagram as a string in DOT format. The `clean_source()`
method
is a static method that takes a DOT string as input and replaces certain labels with more readable symbols like the one
used in the **reference book**.
Overall, this code provides a simple way to create and manipulate OBDDs from Boolean expressions.

##### _main.py_

the main code that generates an Ordered Binary Decision Diagram (OBDD) from a given logical expression and visualizes it
using `Graphviz`. Here is what the code does:

1. Import necessary classes from the facades module (OBDDVar, Expression, and OBDD) and Source from graphviz module.

2. Initialize OBDDVar.create_variables method to create a list of 11 boolean variables a, b, c, d, e, f, j, p, q, r, and
   z.

3. Create a logical expression e(which can be changed in the execution step), which is a combination of the above
   boolean variables connected by logical operators,
   such as | for OR, & for AND, and ~ for NOT. The expression is ((j | a & b | r & c | b & q | z & p) & (c ^ p ^ j) & (~
   r)).

4. Initialize an `OBDD` object.

5. Use the OBDD object to convert the logical expression e into an Ordered Binary Decision Diagram (OBDD) using the
   `from_expression()` method.

6. Use the OBDD object to get the source of the generated OBDD.

7. Use Graphviz's Source() method to create a graphviz object from the source of the generated OBDD.

8. Render the OBDD visualization using the render() method. The output will be saved in a file named 'out_bdd' in the '
   output' directory, and it will be opened automatically in the default viewer.

### Installation & Execution

Installing and running this project involves several steps, including setting up the necessary tools, installing
dependencies, and running the project. This chapter will provide you with a step-by-step process on how to install and
run project on a Windows/Linux operating system.

- Step 1: Install Python
  The first step is to install Python on your computer. You can download the latest version of Python from the official
  Python website (https://www.python.org/downloads/). Once you have downloaded the installer, run the installer and
  follow the instructions to install Python.

- Step 2: Install a Text Editor or IDE
  After installing Python, you need to install a text editor or integrated development environment (IDE) to edit and run
  your Python code. Some popular options include Visual Studio Code, PyCharm, and Sublime Text.

- Step 3: Clone the Project Repository
  Next, you need to clone the project repository from the version control system (VCS) that the project uses. For
  example, here we use git(https://git-scm.com/downloads):
   ```bash
   git clone https://github.com/sirAlireza/obdd
   ```
  Alternatively, you can use **Download Zip** button on the **GitHub** repository.


- Step 4: Install Dependencies
  Project dependencies are listed in the requirements.txt file, which you can find in the project repository. To install
  these
  dependencies, navigate to the project directory in your command prompt and run the following command:

  ```pip install -r requirements.txt```

  This command will install all the dependencies listed in the requirements.txt file(here we have only one).

- Step 5: Run the Project
  Once you have installed the necessary tools, cloned the project repository and installed dependencies you can run the
  project. You can use the following command to run the project:

  ```python main.py```

  If you faced command not found retry with replacing `python` to `python3`.

## Result

Output consists of 2 files ```out_bdd``` which is Binary Decision Diagram (BDD) in the DOT language, a graph description
language used for creating visual representations of graphs.

Each node in the BDD is represented by a unique identifier, such as "n139764640649264" or "n139764640656848", and is
labeled with either a boolean variable, such as "z" or "r", or a boolean constant, either "T" (representing true)
or "⊥" (representing false).

The edges between the nodes represent the possible assignments of the variables in the boolean function, and are labeled
with either a solid line (representing a true assignment) or a dashed line (representing a false assignment).

In addition, The file ```out_bdd.pdf``` contains the export of visualized graph into the pdf format.

## Conclusion

In this document, we discussed the basics of Ordered Binary Decision Diagrams and how implemented them in Python. We
showed how to represent boolean functions as DAGs and build an OBDD using a dictionary to represent the nodes in the
graph. The sample implementation provided shows how to recursively build an OBDD based on a boolean function represented
as a dictionary. Also, The project specification discussed completely.

OBDDs have many applications in computer science and logic, including formal verification, circuit design, and
optimization. They are particularly useful for representing boolean functions with a large number of variables, as they
can significantly reduce the size of the representation compared to other methods.

In conclusion, implementing an OBDD in Python can be a useful tool for representing boolean functions in a compact and
efficient manner. With the sample implementation provided and the understanding of OBDDs and their properties, one can
start exploring the many applications of this data structure in computer science and logic.

</div>
