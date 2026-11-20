#catching errors 
#Rather than letting R stop the whole analysis, you may want to catch the error 
#and continue. You can do this with try().

#First, let’s write a function: This function runs a simulation that involves 
#sampling from a synthetic population with replacement and takes its mean, but 
#only if at least 30 unique samples are obtained

doit <- function(x) {
  temp_x <- sample(x, replace = TRUE)
  if(length(unique(temp_x)) > 30) {#only take mean if sample was sufficient
    print(paste("Mean of this sample was:", as.character(mean(temp_x))))
  } 
  else {
    stop("Couldn't calculate mean: too few unique values!")
  }
}

#Now, generate your population:
set.seed(1345) # again, to get the same result for illustration

popn <- rnorm(50)

hist(popn)


result <- lapply(1:15, function(i) try(doit(popn), FALSE))

class(result)

result

result <- vector("list", 15) #Preallocate/Initialize
for(i in 1:15) {
  result[[i]] <- try(doit(popn), FALSE)
}