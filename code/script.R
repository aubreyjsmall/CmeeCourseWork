MyData <- read.csv("data/trees.csv")

ls(pattern = "My*") # Check that MyData has appeared

class(MyData)

head(MyData) # Have a quick look at the data frame

str(MyData) # Check the structure of the data frame

MyData <- read.csv("data/trees.csv", header = FALSE) # Import ignoring headers

head(MyData)

MyData <- read.table("data/trees.csv", sep = ',', header = TRUE) # Another way

head(MyData)

MyData <- read.csv("data/trees.csv", skip = 5) # Skip first 5 lines
head(MyData)

write.csv(MyData, "results/MyData.csv") # Save the data frame to a new CSV file
dir("results/") # Check if it worked

write.table(MyData[1, ], file = "results/MyData.csv", append = TRUE) # Append

write.csv(MyData, "results/MyData.csv", row.names = TRUE) # Write row names
write.table(MyData, "results/MyData.csv", col.names = FALSE) # Omit column names