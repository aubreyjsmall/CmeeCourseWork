# Pound Hill species richness analysis
# Run from the project root directory.

# Record the R version used
print(R.version.string)

# Check that the required input files exist
required_files <- c(
  "data/pound_hill_data.csv",
  "data/pound_hill_meta_data.csv"
)

missing_files <- required_files[!file.exists(required_files)]

if (length(missing_files) > 0) {
  stop(
    "Missing required input file(s): ",
    paste(missing_files, collapse = ", "),
    "\nPlease run the script from the project root."
  )
}

#check that required packages exist 




#load data 
MyData <- as.matrix(read.csv("data/pound_hill_data.csv", header = FALSE))
#check data
head(MyData) #first 6 rows 
str(MyData) # column types

#read metadata
MyMetaData <- read.csv("data/pound_hill_meta_data.csv", header = TRUE, sep = ";")
class(MyMetaData)



#convert blank spaces to 0 
MyData[MyData == ""] <- 0
#reshape to long format 
#Transpose: rows become columns, so the nested treatment labels sit in rows.
MyData <- t(MyData) 
head(MyData)
#create temp dataframe : Drops row 1 (the labels) and makes a data frame. [-1,] 
#means all rows except the first 
TempData <- as.data.frame(MyData[-1,], stringsAsFactors = FALSE)
head(TempData)
# assign column names from original data
colnames(TempData) <- MyData[1,] 
#get rid of row names 
rownames(TempData) <- NULL

#check that required package exists 
if (!requireNamespace("reshape2", quietly = TRUE)) {
  stop(
    "Package 'reshape2' is required. Install it with:\n",
    'install.packages("reshape2", ',
    'repos = "https://cloud.r-project.org")'
  )
}

library(reshape2)# load the reshape2 package



MyWrangledData <- melt(TempData, id=c("Cultivation", "Block", "Plot", "Quadrat"), 
                       variable.name = "Species", value.name = "Count")
head(MyWrangledData); tail(MyWrangledData)

#We can also now assign the correct data types to each column:
MyWrangledData[, "Cultivation"] <- as.factor(MyWrangledData[, "Cultivation"])
MyWrangledData[, "Block"] <- as.factor(MyWrangledData[, "Block"])
MyWrangledData[, "Plot"] <- as.factor(MyWrangledData[, "Plot"])
MyWrangledData[, "Quadrat"] <- as.factor(MyWrangledData[, "Quadrat"])
MyWrangledData[, "Count"] <- as.integer(MyWrangledData[, "Count"])
str(MyWrangledData)

#Confirm that counts are numeric and non-negative

stopifnot(is.integer(MyWrangledData$Count))
           
#determine the number of distinct species, quadrats and plots
SpeciesCount <- length(unique(MyWrangledData$Species))
print(SpeciesCount)

QuadratCount <- length(unique(MyWrangledData$Quadrat))
print(QuadratCount)

PlotCount <- length(unique(MyWrangledData$Plot))
print(PlotCount)

#Make a quadrat-level table containing Cultivation, Block, Plot, Quadrat and Richness.
QuadratRichness <- aggregate(
  I(Count > 0) ~ Cultivation + Block + Plot + Quadrat,
  data = MyWrangledData,
  FUN = sum
)

# Rename the calculated column
names(QuadratRichness)[names(QuadratRichness) == "I(Count > 0)"] <- "Richness"

head(QuadratRichness)
dim(QuadratRichness)
str(QuadratRichness)

#From that table, make a plot-level summary containing Cultivation, Block, 
# Plot and MeanRichness.
# Calculate mean richness across quadrats within each plot.

PlotRichness <- aggregate(
  Richness ~ Cultivation + Block + Plot,
  data = QuadratRichness,
  FUN = mean
)

# Rename the calculated column
names(PlotRichness)[names(PlotRichness) == "Richness"] <- "MeanRichness"

head(PlotRichness)
dim(PlotRichness)
str(PlotRichness)

#Save it as results/pound_hill_plot_richness.csv. 

if(!file.exists("results")) {
  dir.create("results")
}
write.csv(PlotRichness, "results/pound_hill_plot_richness.csv", row.names = FALSE)

#Draw a figure comparing plot-level mean richness among the three cultivation treatments. 
#check ggplot 2 is installed 
if (!requireNamespace("ggplot2", quietly = TRUE)) {
  stop(
    "Package 'ggplot2' is required. Install it with:\n",
    'install.packages("ggplot2", ',
    'repos = "https://cloud.r-project.org")'
  )
}

#load ggplot 
library(ggplot2)

p <- ggplot(PlotRichness, aes(x = Cultivation, y = MeanRichness)) + 
  geom_point(size=I(3), alpha = 1/2) + 
  scale_x_discrete("Cultivation month (treatment)") +
  scale_y_continuous("Mean species richness per quadrat (one point per plot)") + 
  theme_bw()
p

pdf("results/pound_hill_plot_richness.pdf")
print(p)
dev.off()

print("Script complete :)")


# Interpretation:
# Typical plot-level richness was highest in the May treatment (mean about 9.7
# species per quadrat, versus about 7.8 in March and 7.6 in October). Plots within
# each treatment varied widely (a range of roughly 4 species), so the treatments
# overlap and the differences are small relative to plot-to-plot variation.
# The figure alone cannot show that cultivation timing caused the differences:
# there are only four plots per treatment and no statistical test, and I would need
# to know how treatments were assigned to plots and whether block or site
# differences contributed.




