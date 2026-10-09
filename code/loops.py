#for loops 
for i in range(5):
       print(i)
#return 0
#      1
#      2
#      3
#      4

my_list = [0, 2, "geronimo!", 3.0, True, False]
for k in my_list:
       print(k)
#returns 0
#      2
#      geronimo!
#      3.0
#      True
#      False

total = 0 
summands = [0, 1, 11, 111, 1111]
for s in summands: 
       total = total + s
       print(total)   
#returns 0
#      1
#      12
#      123
#      1234


# WHILE loop
z = 0 
while z < 100: 
       z = z + 1 
       print(z)
#returns numbers 1 through 100, each on a new line

# WHILE loop 
# can also be written using the += operator
z = 0 
while z < 100: 
       z += 1
       print(z)
#returns numbers 1 through 100, each on a new line


#Let’s start with the if statement, which allows you to control when to execute a statement. This is the basic syntax:

#if <expr>: 
#       <statement>

#<expr> is the (boolean) condition (True / False) that needs to be met for the <statement> to be executed.

x = 0; y = 2
if x > y: 
       print('yes')

if x: 
       print('yes')
#No output here because x is NOT an integer

if x==0:
       print('yes')
if y: 
       print('yes')
if y==2:
       print('yes')
x = True # make x boolean

if x: 
       print('yes')

if x == True: 
       print('yes')
