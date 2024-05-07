#!/usr/bin/env Rscript

values <- c("Self-direction\nthought", "Self-direction\naction", "Stimulation", "Hedonism", "Achievement", "Power\ndominance", "Power\nresources", "Face", "Security\npersonal", "Security\nsocietal", "Tradition", "Conformity\nrules", "Conformity\ninterpersonal", "Humility", "Benevolence\ncaring", "Benevolence\ndependability", "Universalism\nconcern", "Universalism\nnature", "Universalism\ntolerance")

args <- commandArgs(trailingOnly=TRUE)
data.filename <- args[1]

data <- read.csv(data.filename, sep="\t", header=TRUE)
data$Language <- factor(sub("_.*", "", data$Text.ID))
data$Is.manifesto <- regexpr("_M_", data$Text.ID) != -1

plot.barsperlanguage <- function(filename, data, ...) {
  pdf(filename, width=7, height=6)
  par(mar=c(4, 4, 0.4, 0.1))
  barplot(t(table(data[c("Language","Is.manifesto")]))[c(2,1),], xlab="Language", las=1, col=c("orange", "blue"), ...)
  grid(nx=NA, ny=NULL)
  legend("topleft", legend=c("All", "Manifestos"), fill=c("blue", "orange"), bty="n")
  dev.off()
}

#files 
plot.barsperlanguage("files-per-language.pdf", data[data$Sentence.ID == 1,], ylab="Texts")

# sentences
plot.barsperlanguage("sentences-per-language.pdf", data, ylab="Sentences")

# fraction of sentences with at least one value
col <- rev(c("#edf8fb", "#ccece6", "#99d8c9", "#66c2a4", "#2ca25f", "#006d2c"))
pdf("fraction-sentences-with-value-per-language.pdf", width=7, height=6)
par(mar=c(4, 4, 0.4, 0.1))
barplot(t(sapply(rev(1:6), function(x) {return(table(data[rowSums(data[3:40]) == x,]$Language) / table(data$Language))})), xlab="Language", ylab="Fraction of sentences with at least that many values", las=1, col=col, ylim=c(0,1))
legend("topleft", legend=1:6, fill=rev(col), bty="n")
grid(nx=NA, ny=NULL)
dev.off()

pdf("fraction-sentences-with-value-per-language-zoomed.pdf", width=7, height=6)
par(mar=c(4, 4, 0.4, 0.1))
barplot(t(sapply(rev(1:6), function(x) {return(table(data[rowSums(data[3:40]) == x,]$Language) / table(data$Language))})), xlab="Language", ylab="Fraction of sentences with at least that many values", las=1, col=col, ylim=c(0,0.005))
legend("topleft", legend=1:6, fill=rev(col), bty="n")
grid(nx=NA, ny=NULL)
dev.off()


plot.histsmallperlanguage <- function(filename.base, data, subset=rep(TRUE, dim(data)[1]), ...) {
  sentences.max <- max(data$Sentence.ID)
  for (language in unique(data$Language)) {
    filename <- paste(filename.base, "-", tolower(language), ".pdf", sep="")
    pdf(filename, width=7, height=3)
    par(mar=c(4, 4, 0.4, 0.1))

    sentences.all <- factor(data[data$Language == language,]$Text.ID)
    sentences.manifestos <- factor(data[data$Language == language & data$Is.manifesto,]$Text.ID)
    hist.all <- hist(table(sentences.all[subset[data$Language == language]]), breaks=(-1:sentences.max)+0.5, plot=FALSE)
    hist.manifestos <- hist(table(sentences.manifestos[subset[data$Language == language & data$Is.manifesto]]), breaks=(-1:sentences.max)+0.5, plot=FALSE)

    plot(hist.all, col="blue", xlim=c(0-0.5, sentences.max+0.5), main=NULL, ylim=c(0, 50), ...)
    plot(hist.manifestos, col="orange", xlim=c(0-0.5, sentences.max+0.5), add=TRUE)
    grid()
    text(7, 45, language, cex=2)
    legend("topright", legend=c("All", "Manifestos"), fill=c("blue", "orange"), bty="n")
    dev.off()
  }
}

plot.histsmallperlanguage("sentences-per-file", data, xlab="Texts with this number of sentences")

sentences.withvalue <- rowSums(data[3:40]) > 0
plot.histsmallperlanguage("sentences-with-value-per-file", data, subset=sentences.withvalue, xlab="Texts with this number of sentences with values")
write(gsub("_", "\\\\_", paste(setdiff(data$Text.ID, data$Text.ID[rowSums(data[3:40]) > 0]), collapse=", ")), "files-without-values.txt")


plot.fractionsentencespervalue <- function(sentences, genre, language) {
  filename.base <- "fraction-sentences-per-value"
  sentences.num <- dim(sentences)[1]
  sums.attained <- colSums(sentences[,(1:19*2+1)])
  sums.constrained <- colSums(sentences[,(1:19*2+2)])
  filename <- paste(filename.base, "-", tolower(genre), "-", tolower(language), ".pdf", sep="")
  pdf(filename, width=7, height=3)
  par(mar=c(0.3, 4, 0.4, 0.1))
  plot(1:19, sums.attained / sentences.num, type="b", col="green", pch=3, xlab="", xaxt="n", ylab="Sentences with value", las=2, ylim=c(0,0.3))
  lines(1:19, sums.constrained / sentences.num, type="b", col="red", pch=4)
  lines(1:19, (sums.attained + sums.constrained) / sentences.num, type="b", col="blue", pch=8)
  grid(nx=NA, ny=NULL)
  abline(v=1:19, col="lightgray", lty="dotted")
  text(1, 0.29, paste(genre, language), cex=1, adj=0)
  text(1, 0.265, paste("(", length(unique(sentences$Text.ID)), " texts, ", sentences.num, " sentences)", sep=""), col="darkgray", cex=0.8, adj=0)
  # legend("topright", legend=c("Constrained", "Attained"), fill=c("red", "green"), bty="n")
  dev.off()
}

plots.fractionsentencepervalue <- function(sentences, genre) {
  plot.fractionsentencespervalue(sentences, genre, "all")
  for (language in unique(sentences$Language)) {
    sentences.language <- sentences[sentences$Language == language,]
    plot.fractionsentencespervalue(sentences.language, genre, language)
  }
}

plots.fractionsentencepervalue(data[data$Is.manifesto,], "Manifestos")
plots.fractionsentencepervalue(data[data$Is.manifesto == FALSE,], "News")

