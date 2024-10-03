#!/usr/bin/env Rscript

values <- c("Self-direction\nthought", "Self-direction\naction", "Stimulation", "Hedonism", "Achievement", "Power\ndominance", "Power\nresources", "Face", "Security\npersonal", "Security\nsocietal", "Tradition", "Conformity\nrules", "Conformity\ninterpersonal", "Humility", "Benevolence\ncaring", "Benevolence\ndependability", "Universalism\nconcern", "Universalism\nnature", "Universalism\ntolerance")

col.constrained="#db58d3"
col.combined="#58dbab"
col.attained="#db5992"
col.news=col.attained
col.manifestos=col.constrained

args <- commandArgs(trailingOnly=TRUE)
data.filename <- args[1]

data <- read.csv(data.filename, sep="\t", header=TRUE)
data$Language <- factor(sub("_.*", "", data$Text.ID))
data$Is.manifesto <- regexpr("_M_", data$Text.ID) != -1

plot.barsperlanguage <- function(filename, data, ...) {
  pdf(filename, width=7, height=6)
  par(mar=c(4, 4, 0.4, 0.1))
  barplot(t(table(data[c("Language","Is.manifesto")]))[c(2,1),], xlab="", las=1, col=rev(c(col.combined, col.manifestos)), ...)
  mtext("Language", side=1, line=2.5)
  grid(nx=NA, ny=NULL)
  legend("topleft", legend=c("All", "Manifestos"), fill=c(col.combined, col.manifestos), bty="n")
  dev.off()
}

#files 
plot.barsperlanguage("files-per-language.pdf", data[data$Sentence.ID == 1,], ylab="Texts")

# sentences
plot.barsperlanguage("sentences-per-language.pdf", data, ylab="Sentences")

# fraction of sentences with at least one value
col <- rev(c("white", "#edf8fb", "#ccece6", "#99d8c9", "#66c2a4", "#2ca25f", "#006d2c"))
col <- rev(c("white", "#d3db57", "#92db59", "#59db61", "#59d3db", "#6159db", "#a259db"))
plot.fraction.sentences <- function(ylim.max, box.ytop=ylim.max) {
  par(mar=c(4, 4, 0.4, 0.1))
  barplot(t(sapply(rev(0:6), function(x) {return(table(data[rowSums(data[3:40]) == x,]$Language) / table(data$Language))})), xlab="", ylab="Percentage of sentences with at least that many values", yaxt="n", col=col, ylim=c(0,ylim.max))
  mtext("Language", side=1, line=2.5)
  at <- (0:5)/5*ylim.max
  labels <- sprintf("%.1f%%", at*100)
  if (at[2] * 100 >= 1) {
    labels <- sprintf("%d%%", at*100)
  }
  axis(2, at=at, labels=labels, line=-0.25, las=1)
  grid(nx=NA, ny=NULL)
  rect(xleft=0, xright=11, ybottom=-0.0001, ytop=box.ytop+0.0001, lwd=2, xpd=TRUE, border="orange")
  legend("topright", legend=0:6, fill=rev(col), bg="white", box.col="white")
}
pdf("fraction-sentences-with-value-per-language.pdf", width=7, height=6)
plot.fraction.sentences(1, box.ytop=0.025)
dev.off()
pdf("fraction-sentences-with-value-per-language-zoomed.pdf", width=7, height=6)
plot.fraction.sentences(0.025)
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

    plot(hist.all, col=col.combined, xlim=c(0-0.5, sentences.max+0.5), main=NULL, ylim=c(0, 50), ...)
    plot(hist.manifestos, col=col.manifestos, xlim=c(0-0.5, sentences.max+0.5), add=TRUE)
    grid()
    text(7, 45, language, cex=2)
    legend("topright", legend=c("All", "Manifestos"), fill=c(col.combined, col.manifestos), bty="n")
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
  plot(1:19, sums.attained / sentences.num, type="b", col=col.attained, pch=3, xlab="", xaxt="n", ylab="Sentences with value", las=2, ylim=c(0,0.3))
  lines(1:19, sums.constrained / sentences.num, type="b", col=col.constrained, pch=4)
  lines(1:19, (sums.attained + sums.constrained) / sentences.num, type="b", col=col.combined, pch=8)
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

