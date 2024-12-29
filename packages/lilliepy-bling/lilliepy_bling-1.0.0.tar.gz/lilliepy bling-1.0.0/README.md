# Lilliepy Bling

this function is able to run code far from the client into a private server (the server self-destructs after the function has been ran and returns value)

## _server

_server is the function, it takes 3 args:
* name
* func
* args

### name
name takes in "__name__", just slap that in there and you are good to go

### func
func is the function you want to execute away from the client, you dont put args in the function here

### args
args takes in parameters that are needed for the function in ```func``` to run, this is an optional parameter

# Example
```python
from lilliepy_bling import _server

def expensive_fibonacci(n):
    if n <= 1:
        return n
    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2)

def no_arg_function():
    return "This function takes no arguments."

result_1 = _server(__name__, no_arg_function)
result_2 = _server(__name__, no_arg_function)
print(result_1, result_2)
```