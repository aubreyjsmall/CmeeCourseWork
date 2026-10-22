#accept exactly one readable CSV path

input_path <- commandArgs(trailingOnly = TRUE)
# commmandArgs() returns everything written on the command line 
# trailingOnly = TRUE specifies the command to only include what was written after the script name aka the name of the csv 
# input <- stores it as as a variable, input 

# next make sure it is only one file 

if (length(input_path) !=1 ) {
       stop("give exactly one file")
}

# make sure the file is readable 

if(!file.exists(input_path)) {
       stop("cannot find file")
}

#load data 

MyData <- read.csv(input_path)

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

#add as a column 

height_m <- TreeHeight(MyData$Angle.degrees, MyData$Distance.m)

# build the results table 

Result <- data.frame(MyData$Species, MyData$Distance.m, MyData$Angle.degrees, height_m)
names(Result) <- c("Species", "Distance.m", "Angle.degrees", "height_m")

# build the name of the output file from the input file 

#drop the folder, strsplit splits the input path by "/" and creates a list, [[1]] returns the contents of the list to a vector, v 
v <- strsplit(input_path, "/")[[1]]
#saves the name of the file by selecting the last item of the vector 
file_name <- v[length(v)]
#drop the ".csv" by separting file_name by ".csv" and using [[1]] to store the parts as a vector and [1] to select the first item and store it as base_name 
base_name <- strsplit(file_name, ".csv")[[1]][1]
#paste the basename onto the output path and store as variable, output 
output_path <- paste("results/",base_name, "_treeheight.csv", sep = "" )

# save the results to results folder w/in working directory, create if it doesn't exist 

if(!file.exists("results")) {
  dir.create("results")
}
write.csv(Result, output_path, row.names = FALSE)
print("Script complete :)")

