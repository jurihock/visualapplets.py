# About visualapplets.py

The [Basler AG](https://www.baslerweb.com) company provides a [TCL](https://docs.baslerweb.com/visualapplets/files/documents/TCL/Content/4_VisualApplets/TCL/Intro.htm) scripting engine to automatize the creation of [VisualApplets](https://www.baslerweb.com/en/products/frame-grabber-portfolio/visualapplets) designs (a former Silicon Software GmbH technology), which is a nice and useful feature but not nice enough, in my opinion.

The main idea of the `visualapplets.py` project is to introduce an additional scripting abstraction and to script the creation of TCL scripts via Python.

Huh, to script a script? Too much meta? Let's study an example...

## Example

In this example we will implement the [ReLU](https://en.wikipedia.org/wiki/Rectifier_(neural_networks)) operator, which functionally corresponds to `y(x) = max(0, x)`.

Just for practical reasons, we encapsulate the operator logic in a `HierarchicalBox`. So it can be reused many times in a VisualApplets design. Consequently we also create a class in our Python script, for the same purpose of course.

We begin with the first part of the Python script [example.py](example.py):

```python
import visualapplets as VA

class Example(VA.Module):

    def __init__(self, parent, name, x, y):

        # initialize the HierarchicalBox (e.g. super)
        super().__init__('HierarchicalBox', parent, name, i=1, o=1, x=x, y=y)

        # create required modules inside the HierarchicalBox (e.g. self)
        branch = VA.Module('BRANCH', self, 'Branch', o=3, x=1, y=1)
        condition = VA.Module('IS_GreaterThan', self, 'Condition', x=2, y=2)
        value = VA.Module('CONST', self, 'Value', x=2, y=3)
        decision = VA.Module('IF', self, 'Decision', x=3, y=1)

        # link created modules together, from left to right
        self('INBOUND') - branch
        branch(0) - decision('I')
        branch(1) - condition - decision('C')
        branch(2) - value - decision('E')
        decision - self('OUTBOUND')

        # for instance, set desired link properties
        branch('I')['Bit Width'] = 16        # input link of the BRANCH
        branch('I')['Arithmetic'] = 'signed'
        value('O')['Bit Width'] = 16         # output link of the CONST
        value('O')['Arithmetic'] = 'signed'  # (needs to match the input link)

        # for instance, set desired module properties
        condition['Number'] = 0  # input value threshold
        value['Value'] = 0       # output value below threshold
```

Now the second part of our Python script:

```python
# dump generated TCL script to a file instead of stdout
VA.printer = VA.FilePrinter('example.tcl')

# create a design with an instance of the example module
design = VA.Design('mE5-MA-VCLx', 'Example')
example = Example(design, 'Example', x=1, y=2)
```

Finally import the generated [example.tcl](example.tcl) file in the VisualApplets IDE or execute something like this in the TCL console:

```
CloseDesign Discard
source "C:/foo/bar/example.tcl"
```

The resulting design should look similar to this one:

![](example.png)

Obviously there are multiple possibilities to implement the ReLU function, e.g. you can replace the fallback value by the `XOR` result or also only check the sign bit of the input value. But the best way is probably to utilize the built-in `ClipLow` operator instead... ;-)

# Basics

With the help of the previous example imagine now, how custom algorithms could be implemented without a deep [TCL](https://en.wikipedia.org/wiki/Tcl) knowledge, but of course not without a certain amount of [Python](https://www.python.org/doc/essays/comparisons) experience.

There are a few basic concepts to understand how the `visualapplets.py` works.

## Module

An instance of the Python module actually triggers the `CreateModule` TCL command as well forwards the specified parameters as is:

```python
Module(operator, parent, name, i, o, x, y)
```

Only `x` and `y` arguments will be converted from the grid cell index to the absolute coordinates via `visualapplets.grid` instance. So you don't have to mess up with pixels, just place modules discretely in grid cells.

Furthermore each module instance provides an access to

* module port descriptor via `__call__` method and
* module parameter descriptor via `__setitem__` method.

Modules with unambiguous assignable output-input port combination can be directly connected without specifying the source and destination port, like `CONST - BRANCH`. Reciprocal connection `BRANCH - CONST` is not necessarily unambiguous, since the branch can have multiple outputs, so you have to specify which one.

## Port

A port descriptor has a little magic inside. Conventionally call the module instance to access either input or output port descriptor:

```
module('I') # default input port
module('I', 0) # same
module(0, 'I') # same

module('O') # default output port
module('o', 0) # same (since case invariant)
module(0, 'o') # same

module('O', 1) # second output port of branch
module('A') # first input of comparator
module('R') # rest of division output

module() # either default I or O port, which is only detectable in connection context
```

There are particular operator specific variations like in case of `DIV`, `MULT` or `SUB`, where the input index begins with `1` instead of `0` and has no specific `%03d` string format. Such delicacies are specified in the operator port dictionary `visualapplets.operators`. The port descriptor looks up for the matching dictionary entry. If there is no matching entry, it keeps the specified port name string as is.

## Link

...

## Param

...
