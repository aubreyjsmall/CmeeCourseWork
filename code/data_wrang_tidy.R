install.packages("reshape2")
library(reshape2)
install.packages("tidyverse")
library(tidyverse)


# Wrangle the Pound Hill dataset.
# Run from the coursework project root with:
# Rscript code/data_wrang.R

# Load the data ----------------------------------------------------------
# The first rows describe the sampling design, so do not use one as a header yet.
MyData <- as.matrix(read.csv("data/pound_hill_data.csv", header = FALSE))

# The metadata file does have a header and uses semicolons as separators.
MyMetaData <- read.csv("data/pound_hill_meta_data.csv", header = TRUE, sep = ";")

# Inspect the data -------------------------------------------------------
head(MyData)
dim(MyData)
str(MyData)
head(MyMetaData)

# Transpose so species become columns and sampled quadrats become rows.
MyData <- t(MyData) 
head(MyData)
dim(MyData)

# For this dataset, we have been told that blanks are observed absences.
# That knowledge is what allows us to record them as zero rather than NA.
MyData[MyData == ""] <- 0

# Convert the raw matrix to a data frame --------------------------------

TempData <- as.data.frame(MyData[-1, ], stringsAsFactors = FALSE)
head(TempData)

#Now letʼs assign the original column names to the temporary dataset:
colnames(TempData) <- MyData[1, ]
head(TempData)

rownames(TempData) <- NULL
head(TempData)

# Convert from wide to long form ----------------------------------------
# This script keeps the older reshape2 route because it is still common in
# ecological code. For new work, the chapter introduces tidyr::pivot_longer().


MyWrangledData <- TempData |>
  tidyr::pivot_longer(
    cols = -c(Cultivation, Block, Plot, Quadrat),
    names_to = "Species",
    values_to = "Count"
  )

MyWrangledData[, "Cultivation"] <- as.factor(MyWrangledData[, "Cultivation"])
MyWrangledData[, "Block"] <- as.factor(MyWrangledData[, "Block"])
MyWrangledData[, "Plot"] <- as.factor(MyWrangledData[, "Plot"])
MyWrangledData[, "Quadrat"] <- as.factor(MyWrangledData[, "Quadrat"])
MyWrangledData[, "Count"] <- as.integer(MyWrangledData[, "Count"])

str(MyWrangledData)
head(MyWrangledData)
dim(MyWrangledData)

# Save a derived table while leaving the raw files unchanged.
dir.create("results", showWarnings = FALSE)
write.csv(MyWrangledData, "results/pound_hill_long.csv", row.names = FALSE)

# Explore the data below this line.

tidyverse_packages(include_self = TRUE) # the include_self = TRUE means list "tidyverse" as well 

MyWrangledData <- dplyr::as_tibble(MyWrangledData) 
MyWrangledData

#This is the same as:

MyWrangledData <- as_tibble(MyWrangledData) 
class(MyWrangledData)

glimpse(MyWrangledData) #like str(), but nicer!

#One handy thing that you can do using tidyverse is using the “pipe” %>% 
#operator to create a compact sequence of manipulations of your dataset with dplyr:

MyWrangledData %>%
  group_by(Species) %>%
  summarise(avg = mean(Count))

#This is the same as the following command using base R (not using dplyr at all):

aggregate(MyWrangledData$Count, list(MyWrangledData$Species), FUN=mean) 
