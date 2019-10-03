libraries <- c("ggplot2", "reshape2")

for(mylibrary in libraries){
	## [SC] installing gplots package
	if (!(mylibrary %in% rownames(installed.packages()))) {
		install.package(mylibrary)
	}
	library(mylibrary, character.only = TRUE)
}

source <- "C:/Users/Enkhbold/PycharmProjects/Test/"

relationFile <- "relation.csv"
extentFile <- "spatial_extent.csv"

whatCodesFile <- "what_codes.csv"
whatIntentFile <- "what_intents.csv"
whatAdjectivesFile <- "what_adjectives.csv"
whatObjectsFile <- "what_objects.csv"

whereCodesFile <- "where_codes.csv"
whereIntentFile <- "where_intents.csv"

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

analyzeWheres <- function(){
	whereCodesDF <- read.csv(paste0(source, whereCodesFile), stringsAsFactors=FALSE)
	whereIntentsDF <- read.csv(paste0(source, whereIntentFile), stringsAsFactors=FALSE)

	print(paste(nrow(whereCodesDF), nrow(whereIntentsDF), all(whereIntentsDF$qid %in% whereCodesDF$qid)))
	print(setdiff(whereCodesDF$qid, whereIntentsDF$qid))

	
	op <- par(mfrow=c(1, 1))

	##############################################

	whereCodesDF <- cbind(whereCodesDF, count=1)

	whereICodesDF <- aggregate(count ~ intent_code, whereCodesDF, sum)
	whereICodesDF <- whereICodesDF[order(whereICodesDF$count, decreasing=TRUE),]

	whereACodesDF <- aggregate(count ~ all_code, whereCodesDF, sum)
	whereACodesDF <- whereACodesDF[order(whereACodesDF$count, decreasing=TRUE),]

	barplot(whereICodesDF$count, names.arg=whereICodesDF$intent_code, las=2
		, main="Frequency of where intent patterns", ylab="frequency", ylim=c(0, 40)
	)
	grid(nx=15)

	#barplot(whereACodesDF$count, names.arg=whereACodesDF$all_code, las=2
	#	, main="Frequency of where whole patterns", ylab="frequency", ylim=c(0, 40)
	#)
	#grid(nx=15)

	# [SC] hierarchical clustering based on Levenshtein's distance
	#levensDistM <-- adist(whereACodesDF$all_code)
	#rownames(levensDistM) <- whereACodesDF$all_code
	#plot(hclust(as.dist(levensDistM)))

	##############################################
	
	# [SC] plurals to singular forms
	for(index in 1:nrow(whereIntentsDF)) {
		if (endsWith(whereIntentsDF$intent[index], "ies")) {
			whereIntentsDF$intent[index] <- paste0(substring(whereIntentsDF$intent[index], 1, nchar(whereIntentsDF$intent[index])-3), "y")
		}
		else if (endsWith(whereIntentsDF$intent[index], "s")) {
			whereIntentsDF$intent[index] <- substring(whereIntentsDF$intent[index], 1, nchar(whereIntentsDF$intent[index])-1)
		}
	}

	whereIntentsDF <- cbind(whereIntentsDF, count=1)
	whereIntentsDF <- aggregate(count ~ intent + code, whereIntentsDF, sum)
	
	whereObjectsDF <- subset(whereIntentsDF, whereIntentsDF$code == "o")
	whereObjectsDF <- whereObjectsDF[order(whereObjectsDF$count, decreasing=TRUE),]
	#whereObjectsDF <- subset(whereObjectsDF, whereObjectsDF$count > 1)

	whereTypesDF <- subset(whereIntentsDF, whereIntentsDF$code == "t")
	whereTypesDF <- whereTypesDF[order(whereTypesDF$count, decreasing=TRUE),]
	#whereTypesDF <- subset(whereTypesDF, whereTypesDF$count > 1)

	barplot(whereObjectsDF$count, names.arg=whereObjectsDF$intent, las=2
		, main="Frequency of where intents - objects", ylab="frequency", ylim=c(0, 10)
		, cex.names=0.8
	)
	grid(nx=15)

	barplot(whereTypesDF$count, names.arg=whereTypesDF$intent, las=2
		, main="Frequency of where intents - types", ylab="frequency", ylim=c(0, 10)
		, cex.names=0.8
	)
	grid(nx=15)


	par(op)
}

createCoocurenceGraph <- function(tempDF){
  intents <- unique(tempDF$intent)
  oadjectives <- unique(tempDF$adjective)
  aiCoocM <- matrix(data=0, nrow=length(oadjectives), ncol=length(intents), dimnames=list(oadjectives, intents))
  
  for(index in 1:nrow(tempDF)){
    currRow = tempDF[index,]
    aiCoocM[currRow$adjective, currRow$intent] = currRow$count
  }
  
  print(aiCoocM)
  
  longData<-melt(aiCoocM)
  longData<-longData[longData$value!=0,]
  
  ggplot(longData, aes(x = Var1, y = Var2)) + 
    geom_raster(aes(fill=value)) + 
    scale_fill_gradient(low="grey90", high="red") +
    labs(x="Adjective", y="Intent", title="Adjective - Intent Cooccurence") +
    theme_bw() + theme(axis.text.x=element_text(size=9, angle=90, vjust=0.3),
                       axis.text.y=element_text(size=9),
                       plot.title=element_text(size=11))
}

analyzeWhats <- function(){
	whatCodesDF <- read.csv(paste0(source, whatCodesFile), stringsAsFactors=FALSE)
	whatIntentsDF <- read.csv(paste0(source, whatIntentFile), stringsAsFactors=FALSE)
	whatAdjectivesDF <- read.csv(paste0(source, whatAdjectivesFile), stringsAsFactors=FALSE)
	whatObjectsDF <- read.csv(paste0(source, whatObjectsFile), stringsAsFactors=FALSE)

	print("What intents:")
	print(paste(nrow(whatCodesDF), nrow(whatIntentsDF), all(whatIntentsDF$qid %in% whatCodesDF$qid)))
	print(setdiff(whatCodesDF$qid, whatIntentsDF$qid))

	print("What adjectives:")
	print(all(whatAdjectivesDF$qid %in% whatCodesDF$qid))
	print(setdiff(whatCodesDF$qid, whatAdjectivesDF$qid))

	print("What objects:")
	print(all(whatObjectsDF$qid %in% whatCodesDF$qid))
	print(setdiff(whatCodesDF$qid, whatObjectsDF$qid))
	
	#op <- par(mfrow=c(1, 1))

	##############################################
	## [SC] plot what code frequencies 

	whatCodesDF <- cbind(whatCodesDF, count=1)
	whatCodesDF <- aggregate(count ~ code, whatCodesDF, sum)
	whatCodesDF <- whatCodesDF[order(whatCodesDF$count, decreasing=TRUE),]

	barplot(whatCodesDF$count, names.arg=whatCodesDF$code, las=2
		, main="Frequency of what intent patterns", ylab="frequency", ylim=c(0, 100)
	)
	grid(nx=15)

	##############################################
	## [SC] plot frequencies of object intents and type intents

	# [SC] plurals to singular forms
	for(index in 1:nrow(whatIntentsDF)) {
		if (endsWith(whatIntentsDF$intent[index], "ies")) {
			whatIntentsDF$intent[index] <- paste0(substring(whatIntentsDF$intent[index], 1, nchar(whatIntentsDF$intent[index])-3), "y")
		}
		else if (endsWith(whatIntentsDF$intent[index], "s")) {
			whatIntentsDF$intent[index] <- substring(whatIntentsDF$intent[index], 1, nchar(whatIntentsDF$intent[index])-1)
		}
	}

	whatIntentsDF <- cbind(whatIntentsDF, count=1)
	
	whatIntentsAggDF <- aggregate(count ~ intent + code, whatIntentsDF, sum)
	
	whatOIntentsDF <- subset(whatIntentsAggDF, whatIntentsAggDF$code == "o")
	whatOIntentsDF <- whatOIntentsDF[order(whatOIntentsDF$count, decreasing=TRUE),]

	whatTIntentsDF <- subset(whatIntentsAggDF, whatIntentsAggDF$code == "t")
	whatTIntentsDF <- whatTIntentsDF[order(whatTIntentsDF$count, decreasing=TRUE),]

	barplot(whatOIntentsDF$count, names.arg=whatOIntentsDF$intent, las=2
		, main="Frequency of what intents - objects", ylab="frequency", ylim=c(0, 15)
		, cex.names=0.8
	)
	grid(nx=15)
	print("Proportions by excluding the long tail:")
	print(sum(subset(whatOIntentsDF, whatOIntentsDF$count > 2)$count)/sum(whatOIntentsDF$count))

	barplot(whatTIntentsDF$count, names.arg=whatTIntentsDF$intent, las=2
		, main="Frequency of what intents - types", ylab="frequency", ylim=c(0, 25)
		, cex.names=0.8
	)
	grid(nx=15)
	print("Proportions by excluding the long tail:")
	print(sum(subset(whatTIntentsDF, whatTIntentsDF$count > 2)$count)/sum(whatTIntentsDF$count))
	
	##############################################
	## [SC] adjective - intent cooccurence matrix
	
	# [SC] filter by distance to the intent word
	whatAdjectivesDF <- subset(whatAdjectivesDF, whatAdjectivesDF$distance == 1)
	
	# [SC] everything to lower case
	whatAdjectivesDF$intent <- tolower(whatAdjectivesDF$intent)
	whatAdjectivesDF$adjective <- tolower(whatAdjectivesDF$adjective)
	
	# [SC] plurals to singular forms
	for(index in 1:nrow(whatAdjectivesDF)) {
		if (endsWith(whatAdjectivesDF$intent[index], "ies")) {
			whatAdjectivesDF$intent[index] <- paste0(substring(whatAdjectivesDF$intent[index], 1, nchar(whatAdjectivesDF$intent[index])-3), "y")
		}
		else if (endsWith(whatAdjectivesDF$intent[index], "s")) {
			whatAdjectivesDF$intent[index] <- substring(whatAdjectivesDF$intent[index], 1, nchar(whatAdjectivesDF$intent[index])-1)
		}

		if (endsWith(whatAdjectivesDF$adjective[index], "ies")) {
			whatAdjectivesDF$adjective[index] <- paste0(substring(whatAdjectivesDF$adjective[index], 1, nchar(whatAdjectivesDF$adjective[index])-3), "y")
		}
		else if (endsWith(whatAdjectivesDF$adjective[index], "s")) {
			whatAdjectivesDF$adjective[index] <- substring(whatAdjectivesDF$adjective[index], 1, nchar(whatAdjectivesDF$adjective[index])-1)
		}
	}

	whatAdjectivesDF <- cbind(whatAdjectivesDF, count=1)
	
	whatAdjectivesAggDF <- aggregate(count ~ intent + adjective + code, whatAdjectivesDF, sum)

	whatOAdjectivesDF <- subset(whatAdjectivesAggDF, whatAdjectivesAggDF$code == "o")
	whatOAdjectivesDF <- whatOAdjectivesDF[order(whatOAdjectivesDF$count, decreasing=TRUE),]
	#print(whatOAdjectivesDF)
	
	whatTAdjectivesDF <- subset(whatAdjectivesAggDF, whatAdjectivesAggDF$code == "t")
	whatTAdjectivesDF <- whatTAdjectivesDF[order(whatTAdjectivesDF$count, decreasing=TRUE),]
	#print(whatTAdjectivesDF)
	
	for(tempList in list(list(whatOAdjectivesDF, "Object"), list(whatTAdjectivesDF, "Type"))){
	  tempDF <- tempList[[1]]
	  
	  # [TODO] intent meaning entropy measure
	  # [TODO] unique adjectives
	  tempTwoDF <- aggregate(count ~ intent, tempDF, sum)
	  tempTwoDF <- tempTwoDF[order(tempTwoDF$count, decreasing=TRUE),]
	  barplot(tempTwoDF$count, names.arg=tempTwoDF$intent, las=2
	          , main=paste0("Frequency of what ", tempList[[2]], " intents with adjectives"), ylab="frequency"
	          , cex.names=0.8
	  )
	  grid(nx=15)
	  
  	intents <- unique(tempDF$intent)
  	adjectives <- unique(tempDF$adjective)
  	aiCoocM <- matrix(data=0, nrow=length(adjectives), ncol=length(intents), dimnames=list(adjectives, intents))
  	
  	for(index in 1:nrow(tempDF)){
  	  currRow = tempDF[index,]
  	  aiCoocM[currRow$adjective, currRow$intent] = currRow$count
  	}
  	
  	longData<-melt(aiCoocM)
  	longData<-longData[longData$value!=0,]
  	
  	# [SC] print is necessary if ggplotn is inside a loop
  	print(ggplot(longData, aes(x = Var1, y = Var2)) +
  	  geom_raster(aes(fill=value)) +
  	  #scale_fill_gradient(low="grey90", high="red") +
  	  labs(x="Adjective", y="Intent", title=paste0("Adjective - ", tempList[[2]], " Intent Cooccurence")) +
  	  theme_bw() + theme(axis.text.x=element_text(size=9, angle=90, vjust=0.3),
  	                     axis.text.y=element_text(size=9),
  	                     plot.title=element_text(size=11)))
	}
	
	for(tempList in list(list(whatOAdjectivesDF, "Object"), list(whatTAdjectivesDF, "Type"))){
	  tempDF <- tempList[[1]]
	  
	  tempDF <- aggregate(count ~ adjective, tempDF, sum)
	  tempDF <- tempDF[order(tempDF$count, decreasing = TRUE),]
	  
	  barplot(tempDF$count, names.arg=tempDF$adjective, las=2
	          , main=paste0("Frequency of what adjectives - ", tempList[[2]]), ylab="frequency"
	          , cex.names=0.8
	  )
	  grid(nx=15)
	}
	
	##############################################
	## [SC] intent - object cooccurence matrix
	
	# [SC] filter by distance to the intent word
	whatObjectsDF <- subset(whatObjectsDF, whatObjectsDF$distance == 1)

	# [SC] everything to lower case
	whatObjectsDF$intent <- tolower(whatObjectsDF$intent)
	whatObjectsDF$relation <- tolower(whatObjectsDF$relation)
	whatObjectsDF$object <- tolower(whatObjectsDF$object)
	
	# [SC] plurals to singular forms
	for(index in 1:nrow(whatObjectsDF)) {
	  if (endsWith(whatObjectsDF$intent[index], "ies")) {
	    whatObjectsDF$intent[index] <- paste0(substring(whatObjectsDF$intent[index], 1, nchar(whatObjectsDF$intent[index])-3), "y")
	  }
	  else if (endsWith(whatObjectsDF$intent[index], "s")) {
	    whatObjectsDF$intent[index] <- substring(whatObjectsDF$intent[index], 1, nchar(whatObjectsDF$intent[index])-1)
	  }
	  
	  if (endsWith(whatObjectsDF$object[index], "ies")) {
	    whatObjectsDF$object[index] <- paste0(substring(whatObjectsDF$object[index], 1, nchar(whatObjectsDF$object[index])-3), "y")
	  }
	  else if (endsWith(whatObjectsDF$object[index], "s")) {
	    whatObjectsDF$object[index] <- substring(whatObjectsDF$object[index], 1, nchar(whatObjectsDF$object[index])-1)
	  }
	}
	
	whatObjectsDF <- cbind(whatObjectsDF, count=1)
	
	whatObjectsAggDF <- aggregate(count ~ intent + object + code, whatObjectsDF, sum)
	
	whatOObjectsDF <- subset(whatObjectsAggDF, whatObjectsAggDF$code == "o")
	whatOObjectsDF <- whatOObjectsDF[order(whatOObjectsDF$count, decreasing=TRUE),]
	#print(whatOObjectsDF)
	
	whatTObjectsDF <- subset(whatObjectsAggDF, whatObjectsAggDF$code == "t")
	whatTObjectsDF <- whatTObjectsDF[order(whatTObjectsDF$count, decreasing=TRUE),]
	#print(whatTObjectsDF)
	
	for(tempList in list(list(whatOObjectsDF, "Object"), list(whatTObjectsDF, "Type"))){
	  tempDF <- tempList[[1]]
	  intents <- unique(tempDF$intent)
	  objects <- unique(tempDF$object)
	  aiCoocM <- matrix(data=0, nrow=length(objects), ncol=length(intents), dimnames=list(objects, intents))
	  
	  for(index in 1:nrow(tempDF)){
	    currRow = tempDF[index,]
	    aiCoocM[currRow$object, currRow$intent] = currRow$count
	  }
	  
	  longData<-melt(aiCoocM)
	  longData<-longData[longData$value!=0,]
	  
	  # [SC] print is necessary if ggplotn is inside a loop
	  print(ggplot(longData, aes(x = Var1, y = Var2)) +
	          geom_raster(aes(fill=value)) +
	          #scale_fill_gradient(low="grey90", high="red") +
	          labs(x="Object", y="Intent", title=paste0("Object - ", tempList[[2]], " Intent Cooccurence")) +
	          theme_bw() + theme(axis.text.x=element_text(size=9, angle=90, vjust=0.3),
	                             axis.text.y=element_text(size=9),
	                             plot.title=element_text(size=11)))
	}
	
	for(tempList in list(list(whatOObjectsDF, "Object"), list(whatTObjectsDF, "Type"))){
	  tempDF <- tempList[[1]]
	  
	  tempDF <- aggregate(count ~ object, tempDF, sum)
	  tempDF <- tempDF[order(tempDF$count, decreasing = TRUE),]
	  
	  barplot(tempDF$count, names.arg=tempDF$object, las=2
	          , main=paste0("Frequency of what objects - ", tempList[[2]]), ylab="frequency"
	          , cex.names=0.8
	  )
	  grid(nx=15)
	}
	
	for(tempList in list(list(whatOObjectsDF, "Object"), list(whatTObjectsDF, "Type"))){
	  tempDF <- tempList[[1]]
	  
	  tempDF <- aggregate(count ~ intent, tempDF, sum)
	  tempDF <- tempDF[order(tempDF$count, decreasing = TRUE),]
	  
	  barplot(tempDF$count, names.arg=tempDF$intent, las=2
	          , main=paste0("Frequency of what ", tempList[[2]], " intents with objects"), ylab="frequency"
	          , cex.names=0.8
	  )
	  grid(nx=15)
	}
	
	##############################################
	## [SC] intent - object relation cooccurence matrix
	
	whatObjectsAggDF <- aggregate(count ~ intent + relation + code, whatObjectsDF, sum)
	
	whatOObjectsDF <- subset(whatObjectsAggDF, whatObjectsAggDF$code == "o")
	whatOObjectsDF <- whatOObjectsDF[order(whatOObjectsDF$count, decreasing=TRUE),]
	#print(whatOObjectsDF)
	
	whatTObjectsDF <- subset(whatObjectsAggDF, whatObjectsAggDF$code == "t")
	whatTObjectsDF <- whatTObjectsDF[order(whatTObjectsDF$count, decreasing=TRUE),]
	#print(whatTObjectsDF)
	
	for(tempList in list(list(whatOObjectsDF, "Object"), list(whatTObjectsDF, "Type"))){
	  tempDF <- tempList[[1]]
	  intents <- unique(tempDF$intent)
	  relations <- unique(tempDF$relation)
	  aiCoocM <- matrix(data=0, nrow=length(intents), ncol=length(relations), dimnames=list(intents, relations))
	  
	  for(index in 1:nrow(tempDF)){
	    currRow = tempDF[index,]
	    aiCoocM[currRow$intent, currRow$relation] = currRow$count
	  }
	  
	  longData<-melt(aiCoocM)
	  longData<-longData[longData$value!=0,]
	  
	  # [SC] print is necessary if ggplotn is inside a loop
	  print(ggplot(longData, aes(x = Var1, y = Var2)) +
	          geom_raster(aes(fill=value)) +
	          #scale_fill_gradient(low="grey90", high="red") +
	          labs(x="Intent", y="Relation", title=paste0("Relation - ", tempList[[2]], " Intent Cooccurence")) +
	          theme_bw() + theme(axis.text.x=element_text(size=9, angle=90, vjust=0.3),
	                             axis.text.y=element_text(size=9),
	                             plot.title=element_text(size=11)))
	}
	
	for(tempList in list(list(whatOObjectsDF, "Object"), list(whatTObjectsDF, "Type"))){
	  tempDF <- tempList[[1]]
	  
	  tempDF <- aggregate(count ~ relation, tempDF, sum)
	  tempDF <- tempDF[order(tempDF$count, decreasing = TRUE),]
	  
	  barplot(tempDF$count, names.arg=tempDF$relation, las=2
	          , main=paste0("Frequency of what relations - ", tempList[[2]]), ylab="frequency"
	          , cex.names=0.8
	  )
	  grid(nx=15)
	}
	
	
	##############################################
	## [SC] intent - object relationcooccurence matrix
	
	#whatIntentsDF
	aggDF <- whatAdjectivesDF[,c("intent","adjective","code","count")]
	colnames(aggDF)[colnames(aggDF)=="adjective"] <- "term"
	aggDF <- cbind(aggDF, type="adjective")

	tempDF <- whatObjectsDF[,c("intent","object","code","count")]
	colnames(tempDF)[colnames(tempDF)=="object"] <- "term"
	tempDF <- cbind(tempDF, type="object")
	
	aggDF <- rbind(aggDF, tempDF)
	aggDF <- aggregate(count ~ intent + term + code + type, aggDF, sum)
	aggDF <- aggDF[order(aggDF$intent),]
	
	print(aggDF)
	
	#par(op)
}




plotRelationFrequencies()

#analyzeWhats()

#analyzeWheres()

# spatial extent 
# 	- with multiple in
# 	- in/of quality
# what is/are the -> quality
# for by of per each every