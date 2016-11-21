##setwd("~/research/trump")

library(ggplot2)

df <- read.csv("correls.csv")
df <- subset(df, !(word %in% c("am")))
df$word <- factor(df$word, levels=df$word[order(df$correl)])

df$polar <- sign(df$correl)
df$polar[df$polar == -1] <- "Against Trump"
df$polar[df$polar == 1] <- "For Trump"
df$polar <- factor(df$polar, levels=c("For Trump", "Against Trump"))

ggplot(subset(df, abs(correl) > .5), aes(x=word, y=abs(correl), fill=polar)) +
    geom_bar(stat="identity") + coord_flip() +
    scale_fill_discrete(name="Polarization: ") +
    scale_y_continuous(expand=c(0, 0)) +
    ylab("Correlation") + xlab("") + theme_bw() + theme(legend.position="top")
