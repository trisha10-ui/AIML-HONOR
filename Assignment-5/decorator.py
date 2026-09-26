# decorator used for adding two variables 
import time
def output_decorator(Parameter):
    def inner1(func):
        def inner(*args,**kwargs):
          print(Parameter)
          print("Input: ",args)
          res=func(*args,**kwargs)
          print("Output: ",res)
          return res
        return inner
    return inner1
# no return 
@output_decorator("Adding (no return)")
def add_no_return(a,b):
    a + b


# return 
@output_decorator("Adding (return)")
def add_return(a,b):
    return a + b

add_no_return(4,3)
print()
add_return(4,3)

