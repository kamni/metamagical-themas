"""
J Leadbetter <j@jleadbetter.com>
MIT License

This is a module that is callable and returns itself. To try out the code,
go into a python shell and import self_referencing_module. Then do something
like:

>>> self_referencing_module
<self_referencing_module.IndirectModuleReference object at 0x101502cf8>
>>> self_referencing_module()
<self_referencing_module.IndirectModuleReference object at 0x101502cf8>
>>> self_referencing_module.self_referencing_lambda()
<function <lambda> at 0x10108e620>
>>> self_referencing_module.self_referencing_function()
<function self_referencing_function at 0x10108e6a8>
"""

import sys


# IndirectModuleReferenceSubstitute is intentionally left out to avoid
# causing more havoc than we really want.
__all__ = ['self_referencing_lambda', 'self_referencing_function']


# A lambda that returns itself
self_referencing_lambda = lambda: globals()['self_referencing_lambda']


def self_referencing_function():
    """A function that returns itself"""

    return globals()['self_referencing_function']


class IndirectModuleReference(object):
    """
    Class to reference the existing module in an indirect fashion.

    Python doesn't allow adding methods like '__call__' to a module, so we're
    going to create a class that will have the call method we want and then
    overwrite the existing module.
    """

    def __init__(self):
        super(IndirectModuleReference, self).__init__()

        # Let's bring in the attributes from the existing module
        for attr in dir(sys.modules[__name__]):
            setattr(self, attr, getattr(sys.modules[__name__], attr))

    def __call__(self):
        """Allows the module to return itself when called"""

        return sys.modules[__name__]


sys.modules[__name__] = IndirectModuleReference()
