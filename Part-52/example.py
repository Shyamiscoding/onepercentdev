import functools
def my_decorator(func):
    @functools.wraps(func)      
    def wrapper1(*args, **kwargs):
        """Greet a user by name 12121."""
        return func(*args, **kwargs)
    return wrapper1

@my_decorator
def greet(name):
    """Greet a user by name."""
    return f"Hello, {name}!"

print(greet.__name__)   # wrapper  <- wrong! it should say "greet"
print(greet.__doc__)    # None     <- the docstring is gone