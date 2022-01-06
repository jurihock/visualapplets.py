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
        branch(0) - decision
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


if __name__ == '__main__':

    # dump generated TCL script to a file instead of stdout
    VA.printer = VA.FilePrinter('example.tcl')

    # create a design with an instance of the example module
    design = VA.Design('mE5-MA-VCLx', 'Example')
    example = Example(design, 'Example', x=1, y=2)
