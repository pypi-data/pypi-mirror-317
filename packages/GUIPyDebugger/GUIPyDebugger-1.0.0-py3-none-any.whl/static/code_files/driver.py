#ENTRY
import inspect
from pprint import pprint

# the two user defined modules for import
import dummy_module as dm
import another_one

# Important methods:
    # getsource: grabs the source python code from an object
        # can be used on import module, cannot be used on variables

    # signature: grabs the signature of a callable
        # really only grabs parameters, could be used to turn params into a tuple
        # This line makes a tuple after str cast: test.lstrip("(").rstrip(")").split(", ")
        # signature returns an OrderedDict object which can be cast to dict cause iterable
        # using .keys on the dict object is another way to get an iterable of the param names

    # getmembers: gets all members of an object
        # This is useful for class variables, and for getting function scoped variables
        # calling getmembers on function.__code__ returns a list
            # That list can be cast to a dict and queried for things like:
                # function name
                # definition line number
                # constant values
                # argument count
                # file name
                # local variable count (including args)
                # variable names
            # getmembers also takes a predicate argument which can filter based on true/false conditions
                # something like inspect.isfunction can be used to get only functions from a class

    # getmodule: returns the module and file path to the file an object was defined in
        # works for import aliases as well as functions

    # classify_class_atts: returns name, kind of attr, class that defined attr and the object
        # example: Attribute(name='exp_y', kind='method', defining_class=<class 'dummy_module.SomeClass'>, object=<function SomeClass.exp_y at 0x0000024F68565260>)

    # getblock: returns a list of lines in the first logical block of a python file
        # could be used in iteration to get every block

    # getdoc: returns the documenation string for an object
        # This could be useful for displaying comments in the debugger

    # currentframe: returns the caller of a context
        # requires some finagling to actually get the name of the caller
        # f_locals attr returns local var memory dest, file path, line number, and code block name
        # f_back returns info on caller frame like: memory dest, file path, line number, and module
            # f_back can be combined with the other f_ attrs to get more info about the caller frame

    # stack: returns a list of FrameInfo objects going back to the root caller
        # each FrameInfo includes:
            # frame=frame memory destination
                # file=file path
                # line=line number
                # code=caller name
            # filename=file path
            # lineno=line number
            # function=function name
            # code_context=body of caller definition
            # index=not sure
            # positions=specific info like line and columns


print(inspect.getsource(dm))


print(inspect.signature(another_one.func1))


print(inspect.getmembers(dm.SomeClass))


print(inspect.getmembers(another_one.func1.__code__))


print(inspect.getmodule(dm))


print(inspect.classify_class_attrs(dm.SomeClass))


lines = []

with open("another_one.py", "r") as another_one_contents:
    lines = another_one_contents.readlines()

print(inspect.getblock(lines))


print(inspect.getdoc(dm.SomeClass))

class Test:
    '''Testing The 
    Docstring'''
    attr = "wassup"
    def __init__(self):
	    pass

def test_currentframe():
    """
    Docstring
    but with double quotes
    """
    frame = inspect.currentframe()
    another_var = "can you see me?"
    print(f"called from: {frame.f_back.f_locals}")
    # result: called from: test_currentframe

test_currentframe()


def test_stack1():
    pprint(inspect.stack())
    # result: a list of frames

def test_stack2():
    test_stack1()

test_stack2()