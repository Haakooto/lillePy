import sys
import inspect
import types


class CallableModule(types.ModuleType):
    """
    Proxy module that implements __call__, allowing you to call the module
    """

    def __init__(self, name, method_name):
        """
        Initialize a new proxy module
        :param name: The name of the proxy module
        :param method_name: The name of the method to call on the original module
        """
        super(CallableModule, self).__init__(name)
        self._original_module = name + "_ORIGINAL"
        self._method_name = method_name

    def __getattr__(self, name):
        # Get the value from the original module
        return getattr(sys.modules[self._original_module], name)

    def __call__(self, *args, **kwargs):
        # Call the method on the original module
        return getattr(sys.modules[self._original_module], self._method_name)(
            *args, **kwargs
        )


def get_caller_module_name(depth=2):
    """
    Gets the name of the module that caused this method to be called
    :param depth: The depth of this call
    :return: The name of the module
    """
    # Get one level up
    back = inspect.currentframe().f_back
    # Go up levels until you reach the requested depth
    for i in range(depth - 1):
        back = back.f_back
    # Return the name from the frame globals
    return back.f_globals["__name__"]


def patch(module_name=None, method_name="__call__"):
    """
    Patches a module to allow it to be callable
    :param module_name: The name of the module
    :param method_name: The method to call when the module is called
    """
    # If no module name is provided, use the name of the module that is calling this method
    if module_name is None:
        module_name = get_caller_module_name()

    # Create a backup of the existing module
    original_module = sys.modules[module_name]
    # Replace the module with a proxy module that implements __call__
    sys.modules[module_name] = CallableModule(module_name, method_name)
    # Restore the original module to <module_name>_ORIGINAL
    sys.modules[module_name + "_ORIGINAL"] = original_module


def unpatch(module_name=None):
    """
    Unpatches a module
    :param module_name: The name of the module
    """
    # If no module name is provided, use the name of the module that is calling this method
    if module_name is None:
        module_name = get_caller_module_name()

    # Replace the proxy module with the original module
    sys.modules[module_name] = sys.modules[module_name + "_ORIGINAL"]
    # Delete the backup copy
    del sys.modules[module_name + "_ORIGINAL"]


def _callable_patch(module_name=None, method_name="__call__"):
    """
    Patches a module to allow it to be callable
    :param module_name: The name of the module
    :param method_name: The method to call when the module is called
    """
    # If no module name is provided, use the name of the module that is two levels back
    # This method -> proxy module -> caller module
    if module_name is None:
        module_name = get_caller_module_name(depth=3)
    # Patch the module
    patch(module_name, method_name)


# Patch this module, so you can use a callable module to make your modules callable
patch(module_name="CallableModules", method_name="_callable_patch")
