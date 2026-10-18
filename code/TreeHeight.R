# This function calculates heights of trees given distance of each tree 
# from its base and angle to its top, using  the trigonometric formula 
#
# height = distance * tan(radians)
#
# ARGUMENTS
# degrees:   The angle of elevation of tree
# distance:  The distance from base of tree (e.g., meters)
#
# OUTPUT
# The heights of the tree, same units as "distance"

#Loads trees.csv

MyData <- read.csv("data/trees.csv",header = FALSE)

write.table(MyData, "data/trees.csv", col.names = FALSE) # Omit column names

#calculates tree heights for all trees in the data

TreeHeight <- function(degrees, distance) {
    radians <- degrees * pi / 180
    height <- distance * tan(radians)
    print(paste("Tree height is:", height))
  
    return (height)
}

TreeHeight("MyData")

