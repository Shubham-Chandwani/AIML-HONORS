# decorator to print stuff
def wrapper_print(msg):
    def my_dec(func):
        def inner(*args, **kwargs):
            print("starting", msg)
            print("got args:", args)
            
            # run the function
            out = func(*args, **kwargs)
            
            print("done. out is:", out, "\n")
            return out
        return inner
    return my_dec

# another decorator just for fun
def log_it(func):
    def inner(*args, **kwargs):
        print("calling func named:", func.__name__)
        return func(*args, **kwargs)
    return inner

# testing functions
@wrapper_print("add")
def do_add(x, y):
    return x + y

@wrapper_print("mul")
@log_it
def do_mul(x, y):
    return x * y

# testing with strings
@wrapper_print("join")
def join_txt(t1, t2):
    return t1 + " " + t2

# testing error
@wrapper_print("div")
def do_div(x, y):
    if y == 0:
        print("cant div by 0")
        return None
    return x / y

# main part
print("test 1")
do_add(7, 12)

print("test 2")
do_mul(5, 6)

print("test 3")
join_txt("hello", "there")

print("test 4")
do_div(15, 3)

print("test 5")
do_div(8, 0)
