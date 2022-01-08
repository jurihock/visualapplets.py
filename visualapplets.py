"""
Python bindings for Basler's VisualApplets TCL script generation.

Source
------
https://github.com/jurihock/visualapplets.py

Copyright
---------
Copyright (c) 2022, Juergen Hock juergen.hock@jurihock.de

License
-------
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""


__version__ = '1.0'


operators = {
    'ADD': {
        'I': lambda n: f'I{n:03d}',
    },
    'AND': {
        'I': lambda n: f'I{n:03d}',
    },
    'BRANCH': {
        'O': lambda n: f'O{n:03d}',
    },
    'CASE': {
        'I': lambda n: f'I{n:03d}',
        'Switch': lambda n: f'Switch',
    },
    'CMP_*': {
        'A': lambda n: f'A',
        'B': lambda n: f'B',
        'I': lambda n: f'{["A", "B"][n]}',
    },
    'DIV': {
        'I': lambda n: f'I{(n + 1)}',
        'R': lambda n: f'R',
    },
    'HierarchicalBox': {
        'I': lambda n: f'I{n:03d}',
        'O': lambda n: f'O{n:03d}',
        'INBOUND': lambda n: f'INBOUND#I{n:03d}',
        'OUTBOUND': lambda n: f'OUTBOUND#O{n:03d}',
    },
    'IF': {
        'I': lambda n: f'I{n:03d}',
        'Condition': lambda n: f'Condition{n:03d}',
        'Else': lambda n: f'ElseI',
    },
    'MergeComponents': {
        'R': lambda n: f'R',
        'G': lambda n: f'G',
        'B': lambda n: f'B',
        'I': lambda n: f'{["R", "G", "B"][n]}',
    },
    'MergeKernel': {
        'I': lambda n: f'I{n:03d}',
    },
    'MergeParallel': {
        'I': lambda n: f'I{n:03d}',
    },
    'MergePixel': {
        'I': lambda n: f'I{n:03d}',
    },
    'MULT': {
        'I': lambda n: f'I{(n + 1)}',
    },
    'OR': {
        'I': lambda n: f'I{n:03d}',
    },
    'SplitComponents': {
        'R': lambda n: f'R',
        'G': lambda n: f'G',
        'B': lambda n: f'B',
        'O': lambda n: f'{["R", "G", "B"][n]}',
    },
    'SplitKernel': {
        'O': lambda n: f'O{n:03d}',
    },
    'SplitParallel': {
        'O': lambda n: f'O{n:03d}',
    },
    'SUB': {
        'I': lambda n: f'I{(n + 1)}',
    },
    'XNOR': {
        'I': lambda n: f'I{n:03d}',
    },
    'XOR': {
        'I': lambda n: f'I{n:03d}',
    },
}


class StdoutPrinter:

    def print(self, what):

        print(what)


class FilePrinter:

    def __init__(self, path):

        self.file = open(path, 'w')

    def print(self, what):

        self.file.write(what)

        if not what.endswith('\n'):
            self.file.write('\n')


class Grid:

    def x(self, index):

        return ((index or 0) * 40 + 3) * 3 - (1 * 40 + 3)

    def y(self, index):

        return ((index or 0) * 40 + 3) * 2 - (1 * 40 + 3)


class Design:

    def __init__(self, platform, name=None, version=None, description=None):

        self.platform = platform
        self.name = name or platform
        self.version = version
        self.description = description

        printer.print(repr(self))

    def __str__(self):

        return 'Process0'

    def __repr__(self):

        return '\n'.join([
            f'CreateDesign "{self.name or ""}" "{self.platform}"',
            f'SetDesignProperty "ProjectName" "{self.name or ""}"',
            f'SetDesignProperty "Version" "{self.version or ""}"',
            f'SetDesignProperty "Description" "{self.description or ""}"'
        ])


class Module:
    """
    An instance of the specified operator type.

    Attributes
    ----------
    operator: str
        Name of the operator to create an instance from.
    parent: Design, Module, str
        Parent object or hierarchical path to the parent object of this module.
    name: str
        Unique name of this module.
    i: int, optional
        Number of input ports.
    o: int, optional
        Number of output ports.
    x: int, optional
        X position in design window.
    y: int, optional
        Y position in design window.
    """

    def __init__(self, operator, parent, name, i=None, o=None, x=None, y=None):
        """
        Creates an instance of the specified operator type.

        Parameters
        ----------
        operator: str
            Name of the operator to create an instance from.
        parent: Design, Module, str
            Parent object or hierarchical path to the parent object of this module.
        name: str
            Unique name of this module.
        i: int, optional
            Number of input ports.
        o: int, optional
            Number of output ports.
        x: int, optional
            X position in design window.
        y: int, optional
            Y position in design window.
        """

        self.operator = operator
        self.parent = parent
        self.name = name
        self.i = i
        self.o = o
        self.x = x
        self.y = y

        printer.print(repr(self))

    def __str__(self):
        """
        Returns the full hierarchical path to this module.
        """

        return '/'.join([str(self.parent), str(self.name)])

    def __repr__(self):
        """
        Generates the TCL code.
        """

        i, o = (self.i or 0), (self.o or 0)
        x, y = grid.x(self.x or 1), grid.y(self.y or 1)

        return f'CreateModule "{self.operator}" "{self}" "{i}" "{o}" "{x}" "{y}"'

    def __setitem__(self, param_name, param_value):
        """
        Sets the specified module parameter to a specific value.

        Parameters
        ----------
        param_name: str
            Name of the module parameter.
        param_value: str, int, list, tuple
            Parameter value to be assign.
        """

        return Param(self, param_name, param_value)

    def __call__(self, *port_args):
        """
        Returns either generic or specific module port descriptor.

        Parameters
        ----------
        port_args: str, int, optional
            Specific port name or number.
        """

        port_name = None
        port_number = None

        for item in port_args:

            if isinstance(item, str):
                port_name = item

            if isinstance(item, int):
                port_number = item

        return Port(self, port_name, port_number)

    def __sub__(self, other):
        """
        Connects this module with another module or a specific module port.

        Parameters
        ----------
        other: Module, Port
            Destination connection point.
        """

        assert isinstance(other, (Module, Port))

        src = self()
        dst = other() if isinstance(other, Module) else other

        return src - dst


class Port:

    def __init__(self, module, name, number):

        assert isinstance(module, Module)

        self.module = module
        self.name = name
        self.number = number

    def __str__(self):

        return str(self.module)

    def __repr__(self):

        def find1(operator):
            import fnmatch
            for key in operators.keys():
                if fnmatch.fnmatchcase(operator, key):
                    return key
            return None

        def find2(operator, port):
            for key in operators[operator].keys():
                if key.lower().startswith(port.lower()):
                    return key
            return None

        assert isinstance(self.name, str)
        assert isinstance(self.number, (int, type(None)))

        operator = find1(self.module.operator)

        if operator is None:
            return f'{self.name}'

        port = find2(operator, self.name)

        if port is None:
            return f'{self.name}'

        return operators[operator][port](self.number or 0)

    def __setitem__(self, param_name, param_value):

        return Param(self, param_name, param_value)

    def __sub__(self, other):

        assert isinstance(other, (Module, Port))

        src = self
        dst = other() if isinstance(other, Module) else other

        assert isinstance(src, Port)
        assert isinstance(dst, Port)

        if src.name is None:
            src.name = 'O'

        if dst.name is None:
            dst.name = 'I'

        if src.number is None:
            src.number = 0

        if dst.number is None:
            dst.number = 0

        return Link(src, dst)


class Link:

    def __init__(self, src, dst):

        assert isinstance(src, Port)
        assert isinstance(dst, Port)

        self.src = src
        self.dst = dst

        printer.print(repr(self))

    def __repr__(self):

        return f'ConnectModules "{str(self.src)}" "{repr(self.src)}" "{str(self.dst)}" "{repr(self.dst)}"'

    def __setitem__(self, param_name, param_value):

        return Param(self, param_name, param_value)

    def __sub__(self, other):

        assert isinstance(other, (Module, Port))

        src = self.dst.module()
        dst = other() if isinstance(other, Module) else other

        return src - dst


class Param:

    def __init__(self, instance, name, value):

        assert isinstance(instance, (Module, Port, Link))
        assert isinstance(name, str)

        self.instance = instance
        self.name = name
        self.value = value

        printer.print(repr(self))

    def __repr__(self):

        def stringify(value):
            if isinstance(value, (list, tuple)):
                return ' '.join([stringify(item) for item in value])
            return '""' if value is None else f'"{value}"'

        name = stringify(self.name)
        value = stringify(self.value)

        if isinstance(self.instance, Module):
            module = self.instance
            return f'SetModuleParam "{str(module)}" {name} {value}'

        if isinstance(self.instance, Port):
            port = self.instance
            return f'SetLinkParam "{str(port)}" "{repr(port)}" {name} {value}'

        if isinstance(self.instance, Link):
            port = self.instance.dst
            return f'SetLinkParam "{str(port)}" "{repr(port)}" {name} {value}'

        assert False


grid = Grid()
printer = StdoutPrinter()
