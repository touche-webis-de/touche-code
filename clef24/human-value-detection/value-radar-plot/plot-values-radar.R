#!/usr/bin/env Rscript
library(fmsb)
library(plotrix)

args = commandArgs(trailingOnly=TRUE)

data.full <- read.csv(args[1], sep="\t", header=FALSE)
output <- "radar-plot.pdf"
if (length(args) > 1) {
  output <- args[2]
}

names <- data.full[,1]
colors <- data.full[,2]
ltys <- data.full[,3]
data <- data.full[,4:22]

dims <- 19
radar.max <- 1.00
radar.segments <- 4 

names.outer <- list(c(1.5, "Self-direction:"), c(3, "Stimulation"), c(4, "Hedonism"), c(5, "Achievement"), c(6.5, "Power:"), c(8, "Face"), c(9.5, "Security:"), c(11, "Tradition"), c(12.5, "Conformity:"), c(14, "Humility"), c(15.5, "Benevolence:"), c(18, "Universalism:"))
names.inner <- list(c(1, "thought"), c(2, "action"), c(6, "dominance"), c(7, "resources"), c(9, "personal"), c(10, "societal"), c(12, "rules"), c(13, "interpersonal"), c(15, "caring"), c(16, "dependability"), c(17, "concern"), c(18, "nature"), c(19, "tolerance"))
midlines <- list(c(66, 96), c(102, 152), c(155,189), c(213, 246), c(273.5, 305), c(328.5, 363.5))

data <- cbind(data[,1], rev(data[,2:19])) # counter-clockwise
data <- rbind(rep(radar.max,dims), rep(0,dims), data)
colnames(data) <- rep("",dims)

middle.for <- function(i) {
  return(pi/2-(2*pi/dims)*(i-1))
}
clockwise.for <- function(i) {
  middle <- middle.for(i)
  return((middle < -(0.9 * pi)) || (middle > 0))
}
arc.texts <- function(texts, ...) {
  for (tuple in texts) {
    i <- as.numeric(tuple[1])
    arctext(x=tuple[2], center=c(0,0),
      middle=middle.for(i), clockwise=clockwise.for(i),
      ...)
  }
}
arc.segments <- function (lines, ...) {
  for (tuple in lines) {
    draw.arc(x=0, y=0, deg1=tuple[1], deg2=tuple[2], ...)
  }
}

axis.labels <- sprintf("%.2f", 0:radar.segments * (radar.max/radar.segments))

cairo_pdf(output, width=5, height=5)
par(mar=c(-0,0,0,0), oma=c(0,0,0,0), family="Helvetica")
radarchart(data, pcol=colors, plty=ltys, pty=32,
  cglwd=0.5, seg=radar.segments,
  axistype=1, caxislabels=axis.labels, calcex=0.5, axislabcol="black")
arc.texts(names.inner, radius=1.05, cex=0.7)
arc.texts(names.outer, radius=1.15, cex=0.7)
arc.segments(midlines, radius=1.10)

if (sum(names != "") > 0) {
  legend("bottomleft", names[names != ""], col=colors[names != ""], lty=ltys[names != ""], lwd=1, bty="n", cex=0.7)
}
dev.off()

