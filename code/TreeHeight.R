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

getwd()

MyData <- read.csv("data/trees.csv")

head(MyData) #first 6 rows 
str(MyData) # column types: 120 obs of 3 variables 


#check the input 

# 1. do the three colums (Species, Distance.m, and Angle.degrees) exist 

if (!all(c("Species", "Distance.m", "Angle.degrees") %in% names (MyData))) {
  stop("Need columns Species, Distance.m and Angle.degrees")
}

# 2. Are Distance.m, and Angle.degrees numeric 

if(class(MyData$Distance.m) != "numeric" | 
   class(MyData$Angle.degrees) != "numeric") { 
  stop("Distance.m and Angle.degrees must be numeric")
}

# 3. Are Distance.m, and Angle.degrees finite - No NA, NAN, of Inf values 

if(!all(is.finite(MyData$Distance.m)) | !all(is.finite(MyData$Angle.degrees))) {
  stop("Distance.m and Angle.degrees must be finite numbers")
}


# 4. are the values for distance.m in the range (0 < Distance.m <= 100)

if(!all(MyData$Distance.m > 0 & MyData$Distance.m <= 100)) {
  stop("Distance.m must be > 0 and <= 100")
}

# 5. are the values for Angle.degrees in the range (0 < Angle.degrees < 90)

if(!all(MyData$Angle.degrees > 0 & MyData$Angle.degrees < 90)) {
  stop("Angle.degrees must be > 0 and < 90")
}



#Function calculates tree heights for all trees in the data

TreeHeight <- function(degrees, distance) {
    radians <- degrees * pi / 180
    height <- distance * tan(radians)
    print(paste("Tree height is:", height))
  
    return (height)
}

#add as a column to My Data 

height_m <- TreeHeight(MyData$Angle.degrees, MyData$Distance.m)

# build the results table 

Result <- data.frame(MyData$Species, MyData$Distance.m, MyData$Angle.degrees, height_m)
names(Result) <- c("Species", "Distance.m", "Angle.degrees", "height_m")

# save the results to results folder w/in working directory, create if it doesn't exist 

if(!file.exists("results")) {
  dir.create("results")
}
write.csv(Result, "results/TreeHts.csv", row.names = FALSE)
print("Script complete :)")

#Header and row count check 
check <- read.csv("results/TreeHts.csv")
head(check)
str(check)

#Test Calculation Check
31.66583 * tan(41.28264 * pi/ 180)
# should return 27.80212

#Rerun and recheck 


