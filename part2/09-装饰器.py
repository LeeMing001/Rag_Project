def log_input(func):
    def wrapper(x):
        print("-" * 20, x.to_string(), "-" * 20)
        return func(x)
    return wrapper

@log_input
def passthrough(x):
    return x

def print_fenge(func):
    def wrapper(x,y):
        print("-"*20,x,y,"-"*20)
        return func(x,y)
    return wrapper

@print_fenge
def sum(a,b):
    print(a+b)
    return a+b

s=sum(2,2)