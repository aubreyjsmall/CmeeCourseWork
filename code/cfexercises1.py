#We can now try combining functions and the if conditional. run the following functions one by one, by pasting the block in the ipython command line. First, type all them all in a script and save it as cfexercises1.py. Then you can send them block by block easily to the command line assuming you have set your code editor to allow selections of code to be sent to terminal directly using a key binding (typically , ctrl+enter).

#Square root function
def foo_1(x):
    return x ** 0.5

#if x is bigger than y, return x, otherwise return y
def foo_2(x, y):
    if x > y:
        return x
    return y

#if x is bigger than y, swap their values; if x is bigger than z, swap their values; if y is bigger than z, swap their values - sorts the numbers x, y, z in ascending order and returns them as a list
def foo_3(x, y, z):
    if x > y:
        x, y = y, x
    if x > z:
        x, z = z, x
    if y > z:
        y, z = z, y
    return [x, y, z]

#factorial function using a for loop 
def foo_4(x):
    result = 1
    for i in range(1, x + 1):
        result = result * i
    return result

# a recursive function that calculates the factorial of x
def foo_5(x): 
    if x == 1:
        return 1
    return x * foo_5(x - 1)

# Calculate the factorial of x in a different way; no if statement involved; while loop is used instead of a for loop; the function returns 1 if x is 0, as 0! = 1      
def foo_6(x): 
    facto = 1
    while x >= 1:
        facto = facto * x
        x = x - 1
    return facto

