#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

data <- read.csv(args[1], sep="\t", header=FALSE)
output <- "radar-plot.pdf"
if (length(args) > 1) {
  output <- args[2]
}


library("grImport")
radar <- readPicture("values-radar-empty.ps.xml")[-1]
# created by:
# $ pdftops values-radar-empty.ai values-radar-empty.ps
# $ Rscript -e 'library("grImport");PostScriptTrace("values-radar-empty.ps")'

radar.line <- function(values, col="black", pch=21, cex=0.5) {
  values.extended <- c(values, values[1])

  xcorrection <- 0.0045
  ycorrection <- -0.005
  radius.start <- 0.17
  radius <- 0.67
  start <- 99
  step <- 18

  for (i in 1:20) {
    if (!is.na(values.extended[i])) {
      r <- values.extended[i] * radius + radius.start
      px <- r * cos((start - i * step) * pi / 180) - xcorrection
      py <- r * sin((start - i * step) * pi / 180) - ycorrection
      # points(x=px, y=py, col=FALSE, bg=col, pch=pch, cex=cex)
      if (!is.na(values.extended[i+1])) {
        r2 <- values.extended[i+1] * radius + radius.start
        px2 <- r2 * cos((start - (i+1) * step) * pi / 180) - xcorrection
        py2 <- r2 * sin((start - (i+1) * step) * pi / 180) - ycorrection
        lines(x=c(px, px2), y=c(py, py2), col=col)
      }
    }
  }
}

radar.lines <- function(data, ...) {
  colors <- data[,1]
  values <- as.matrix(suppressWarnings(sapply(data[,-1], as.numeric)))
  for (i in 1:length(colors)) {
    radar.line(values[i,], col=colors[i], ...)
  }
}

pdf(output, width=4, height=4)
par(mar=c(0,0,0,0), oma=c(0,0,0,0))
plot(0, xlim=c(-1,1), ylim=c(-1,1), type="n", bty="n", axes=FALSE)
grid.picture(radar)
radar.lines(data)
dev.off()
