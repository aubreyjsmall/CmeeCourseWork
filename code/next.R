#Using next. You can also skip to next iteration of a loop. Both next and break can be used within other loops ( while, for). Try this (type into next.R and save in code):

for (i in 1:10) {
  if ((i %% 2) == 0) # check if the number is odd
    next # pass to next iteration of loop 
  print(i)
}

#This code checks if a number is odd using the “modulo” operation and prints it if it is.
