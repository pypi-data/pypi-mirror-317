#Author : ANURAJ R
#GitHub :  https://github.com/Anuraj-CodeHaven

class setconstant:
    _initialized = False  # Track whether the constants have been reset

    def __new__(cls, *args, **kwargs):
        if not cls._initialized:
            #print("Resetting constants...")
            for attr in list(cls.__dict__.keys()):
                if not attr.startswith('__') and not callable(getattr(cls, attr)):
                    delattr(cls, attr)
            cls._initialized = True  # Mark as initialized
        return super().__new__(cls)

    @classmethod
    def _check_existing(cls, const_name):
        """Check if the constant already exists."""
        if hasattr(cls, const_name):
            raise ValueError(f"Constant '{const_name}' has already been assigned and cannot be redefined.")

    @classmethod
    def const_i(cls, const_name, value):
        """Declare an integer constant."""
        cls._check_existing(const_name)
        if not isinstance(value, int):
            raise TypeError(f"Value for '{const_name}' must be an integer.")
        setattr(cls, const_name, value)

    @classmethod
    def const_f(cls, const_name, value):
        """Declare a floating-point constant."""
        cls._check_existing(const_name)
        if not isinstance(value, float):
            raise TypeError(f"Value for '{const_name}' must be a float.")
        setattr(cls, const_name, value)

    @classmethod
    def const_s(cls, const_name, value):
        """Declare a string constant."""
        cls._check_existing(const_name)
        if not isinstance(value, str):
            raise TypeError(f"Value for '{const_name}' must be a string.")
        setattr(cls, const_name, value)

    @classmethod
    def get_constant(cls, const_name):
        """Retrieve the value of a constant."""
        if not hasattr(cls, const_name):
            raise AttributeError(f"Constant '{const_name}' is not defined.")
        return getattr(cls, const_name)

    @classmethod
    def delete_constant(cls, const_name):
        """Delete a constant."""
        if hasattr(cls, const_name):
            delattr(cls, const_name)
        else:
            raise AttributeError(f"Constant '{const_name}' is not defined.")