observations <- read.csv(
  "data/bootcamp_observations.csv",
  colClasses = "character", na.strings = "", check.names = FALSE
)

#colClasses = "character" stops R from silently changing values. na.strings = "" turns empty cells into NA.



str(observations)
print(observations)

# Write read_observations(path)

# Read the file as in Step 1.
# Check the column names are exactly site, date, count, in that order. If not, stop("...") with a clear message.
#Check no site or date is empty (NA). If one is, stop().
#For each count that isn’t NA, check it matches the pattern for a non-negative whole number:


read_observations <- function(path) { 
       observations <- read.csv(
          path,
          colClasses = "character", na.strings = "", check.names = FALSE
)
#is it true that not all of the observations are named "site", "date", "count" , if so stop 
       if (!all(names(observations) == c("site", "date", "count"))) {
    stop("Columns must be exactly: site, date, count (in that order)") #is it true that not all of the observations are named "site", "date", "count" , if so stop 
  } 
#Check no site or date is empty (NA). If one is, stop().
#is it true that not all of the observtaions of site are not NA , if so stop 
       if(any(is.na(observations$site))) { 
              stop("Every row needs a site, but at least one site is empty")
  }
#is it true that not all of the observtaions of date are not NA , if so stop  
 if(any(is.na(observations$date))) { 
       stop("Every row needs a site, but at least one site is empty")
  }
#Step 4: Check the counts, ignoring the missing ones. 
#remove the missing counts 
 counts <- observations$count[!is.na(observations$count)]

#Test each count against the pattern - does this text match this pattern?
# The text must start here -- "^ -- The text is exactly the digit zero --  0  -- or -- | -- A first digit from 1 to 9 (not zero) -- [1-9] --Followed by any number of digits, including none --[0-9]* --  The text must end here (nothing after it) -- $" --


valid <- grepl("^(0|[1-9][0-9]*)$", counts)
if(!all(valid)) {
       bad <- counts[!valid]  
       stop(paste("Count must be a non-negative integer, but found:", bad[1]))
  }
  observations$count <- as.integer(observations$count)
   return(observations)
}

read_observations("data/bootcamp_observations.csv")
#output: 
# site       date count
#1    A 2026-10-01     2
#2    B 2026-10-01     0
#3    A 2026-10-02    NA
#4    A 2026-10-01     2
#Warning message:
#In read.table(file = file, header = header, sep = sep, quote = quote,  :
#  incomplete final line found by readTableHeader on 'data/bootcamp_observations.csv'

read_observations("data/bootcamp_observations_invalid.csv")

#output : Error in read_observations("data/bootcamp_observations_invalid.csv") : 
#  Count must be a non-negative integer, but found: -1
#In addition: Warning message:
#In read.table(file = file, header = header, sep = sep, quote = quote,  :
#  incomplete final line found by readTableHeader on 'data/bootcamp_observations_invalid.csv'

#Independent: deduplicate and summarise
#Step 1: Create the function shell and remove duplicates.
summarise_observations <- function(data) {
  data <- unique(data)

#Step 2: Calculate total_known for each site.
total_known <- tapply(data$count, data$site, function(x) {
       if (all(is.na(x))) {
              return(NA) 
       }
       return(sum(x[!is.na(x)]))
})
#Step 3: Calculate missing_count for each site.
  missing_count <- tapply(data$count, data$site, function(x) sum(is.na(x)))

#Step 4: Combine into one table and return it.
 result <- data.frame(
    site = names(total_known),
    total_known = total_known,
    missing_count = missing_count
  )
  return(result)
}

observations <- read_observations("data/bootcamp_observations.csv")
summary_table <- summarise_observations(observations)
print(summary_table)

#output: > print(summary_table)
#      site total_known missing_count
#      A    A           2             1
#      B    B           0             0




