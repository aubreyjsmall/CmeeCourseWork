def buggyfunc(x): 
    y = x 
    for i in range(x):
        try:
            y = y-1
            z = x/y
        except ZeroDivisionError:
            print(f"The result of dividing a number by zero is undefined")
        except: 
            print(f"this didnt work;{x= }; {y= }")
        else: 
            print(f"OK;{x= }; {y= }, {z= };")
    return z 

buggyfunc(20)

# Traceback (most recent call last): - means last function error comes first 
#ZeroDivisionError: division by zero
#turn on %pdb - python debugger 
