source <- "./"

relationFile <- "relation.csv"
extentFile <- "spatial_extent.csv"

whatCodesFile <- "what_codes.csv"
whatTermFile <- "what_terms.csv"


plotRelationFrequencies <- function() {
	extentDF <- read.csv(paste0(source, extentFile))
	extentDF$count <- as.numeric(extentDF$count)
	extentDF <- subset(extentDF, extentDF$count > 0)
	extentDF <- extentDF[order(extentDF$count, decreasing=TRUE),]

	relationDF <- read.csv(paste0(source, relationFile))
	relationDF$count <- as.numeric(relationDF$count)
	relationDF <- subset(relationDF, relationDF$count > 0)
	relationDF <- relationDF[order(relationDF$count, decreasing=TRUE),]

	op <- par(mfrow=c(1, 2))
	
	barplot(extentDF$count, names.arg=paste(extentDF$relation, extentDF$code), las=2
		, main="relations at the sentence end", ylab="frequency", ylim=c(0, 150)
	)
	grid(nx=15)
	barplot(relationDF$count, names.arg=paste(relationDF$relation, relationDF$code), las=2
		, main="relations eslewhere", ylab="frequency", ylim=c(0, 150)
	)
	grid(nx=15)

	print(extentDF)
	print(relationDF)

	par(op)
}

analyzeWhats <- function(){
	whatCodesDF <- read.csv(paste0(source, whatCodesFile))
	whatCodesDF <- cbind(whatCodesDF, count=1)
	whatCodesDF <- aggregate(count ~ code, whatCodesDF, sum)
	whatCodesDF <- whatCodesDF[order(whatCodesDF$count, decreasing=TRUE),]

	whatTermsDF <- read.csv(paste0(source, whatTermFile))
	whatTermsDF <- cbind(whatTermsDF, count=1)
	whatTermsDF <- aggregate(count ~ term, whatTermsDF, sum)
	whatTermsDF <- whatTermsDF[order(whatTermsDF$count, decreasing=TRUE),]
	whatTermsDF <- subset(whatTermsDF, whatTermsDF$count > 1)

	op <- par(mfrow=c(1, 1), ask=TRUE)

	barplot(whatCodesDF$count, names.arg=whatCodesDF$code, las=2
		, main="frequency of what intent patterns", ylab="frequency", ylim=c(0, 100)
	)
	grid(nx=15)

	barplot(whatTermsDF$count, names.arg=whatTermsDF$term, las=2
		, main="frequency of what intents - objects", ylab="frequency", ylim=c(0, 15)
	)
	grid(nx=15)

	print(whatCodesDF)

}

plotRelationFrequencies()

analyzeWhats()