#Author : ANURAJ R
#GitHub :  https://github.com/Anuraj-CodeHaven

# Dictionary to store constants
constants = {}

def const_i(variable_name, value):
    """Declare an integer constant."""
    if variable_name in constants:
        raise ValueError(f"Constant '{variable_name}' has already been assigned.")
    if not isinstance(value, int):
        raise TypeError(f"Value for '{variable_name}' must be an integer.")
    constants[variable_name] = value

def const_s(variable_name, value):
    """Declare a string constant."""
    if variable_name in constants:
        raise ValueError(f"Constant '{variable_name}' has already been assigned.")
    if not isinstance(value, str):
        raise TypeError(f"Value for '{variable_name}' must be a string.")
    constants[variable_name] = value

def const_f(variable_name, value):
    """Declare a floating-point constant."""
    if variable_name in constants:
        raise ValueError(f"Constant '{variable_name}' has already been assigned.")
    if not isinstance(value, float):
        raise TypeError(f"Value for '{variable_name}' must be a float.")
    constants[variable_name] = value

def get_constant(variable_name):
    """Retrieve the value of a constant."""
    if variable_name not in constants:
        raise KeyError(f"Constant '{variable_name}' is not defined.")
    return constants[variable_name]

def delete_constant(variable_name):
    """Delete a constant."""
    if variable_name in constants:
        del constants[variable_name]
    else:
        raise KeyError(f"Constant '{variable_name}' is not defined.")

# Define __getattr__ to access constants directly
def __getattr__(name):
    if name in constants:
        return constants[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
