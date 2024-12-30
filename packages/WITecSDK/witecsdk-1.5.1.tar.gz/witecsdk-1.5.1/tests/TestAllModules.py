from WITecSDK import WITecControl
from WITecSDK.Modules import WITecModules
import sys

def printerr(input):
    sys.stderr.write(str(input) + "\n")

def iterateObj(testobj, prefix: str):
    attributes = [attr for attr in dir(testobj) if not attr.startswith('_')]
    for item in attributes:
        itemobj = getattr(testobj, item)
        if callable(itemobj):
            print(prefix + item + '()')
        elif itemobj is None or isinstance(itemobj, (bool, int, float, str, tuple, list)):
            print(prefix + item + ': ' + str(itemobj))
        else:
            print(prefix + item + ': ' + str(type(itemobj)))
            iterateObj(itemobj, prefix + item + '.')

def testmodule(methodstr):
    print('')
    print('Testing: ' + methodstr)
    try:
        testmod = getattr(WITec, methodstr)
        print(type(testmod))
        iterateObj(testmod, '')

    except Exception as exc:
        printerr(type(exc))
        printerr(exc)

WITec = WITecControl()

createmethods = [func for func in dir(WITecModules) if not func.startswith("_")]

for cmethod in createmethods:
    testmodule(cmethod)
