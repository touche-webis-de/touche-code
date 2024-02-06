#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly=TRUE)
data.filename <- args[1]

data <- read.csv(data.filename, sep="\t", header=TRUE)
data$Language <- sub("_.*", "", data$Text.ID)
data$Is.manifesto <- regexpr("_M_", data$Text.ID) != -1

plot.barsperlanguage <- function(filename, data, ...) {
  pdf(filename, width=7, height=6)
  par(mar=c(4, 4, 0.4, 0.1))
  barplot(t(table(data[c("Language","Is.manifesto")]))[c(2,1),], xlab="language", las=1, col=c("orange", "blue"), ...)
  grid(nx=NA, ny=NULL)
  legend("topleft", legend=c("All", "Manifestos"), fill=c("blue", "orange"), bty="n")
  dev.off()
}

#files 
plot.barsperlanguage("files-per-language.pdf", data[data$Sentence.ID == 1,], ylab="Files")

# sentences
plot.barsperlanguage("sentences-per-language.pdf", data, ylab="Sentences")



plot.histsmallperlanguage <- function(filename.base, data, ...) {
  sentences.max <- max(data$Sentence.ID)
  for (language in unique(data$Language)) {
    filename <- paste(filename.base, "-", tolower(language), ".pdf", sep="")
    pdf(filename, width=7, height=3)
    par(mar=c(4, 4, 0.4, 0.1))
    hist.all <- hist(table(data[data$Language == language,]$Text.ID), breaks=(-1:sentences.max)+0.5, plot=FALSE)
    hist.manifestos <- hist(table(data[data$Language == language & data$Is.manifesto,]$Text.ID), breaks=(-1:sentences.max)+0.5, plot=FALSE)

    plot(hist.all, col="blue", xlim=c(0-0.5, sentences.max+0.5), main=NULL, ylim=c(0, 40), ...)
    plot(hist.manifestos, col="orange", xlim=c(0-0.5, sentences.max+0.5), add=TRUE)
    grid()
    text(7, 35, language, cex=2)
    legend("topright", legend=c("All", "Manifestos"), fill=c("blue", "orange"), bty="n")
    dev.off()
  }
}

plot.histsmallperlanguage("sentences-per-file", data, xlab="Files with this number of sentences")


plot.histsmallperlanguage("sentences-with-value-per-file", data[rowSums(data[3:40]) > 0,], xlab="Files with this number of sentences with values")

