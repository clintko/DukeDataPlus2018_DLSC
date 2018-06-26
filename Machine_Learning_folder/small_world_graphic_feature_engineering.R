library(MASS)
library(ISLR)
library(minet)
library(Rgraphviz)
library(UpSetR)
library(ggplot2)
library(grid)
library(plyr)
library(infotheo)

syn.data <- read.csv("/Users/dzy/Desktop/变量/Programs/DATA+/DukeDataPlus2018_DLSC/data/labeled_filtered_Gland.csv")


clr.net <- minet(syn.data, "clr", "spearman", "equalfreq")
#clr.val <-validate(clr.net,syn.net)
ara.net <- minet(syn.data, "aracne", "spearman", "equalfreq")
#ara.val <-validate(ara.net,syn.net)
mr.net <- minet(syn.data, "mrnet", "spearman", "equalfreq")
#mr.val <-validate(mr.net,syn.net)

discdata <- discretize(syn.data,"equalfreq",50)
mim <- build.mim(discdata,"spearman")
mr.net <- mrnet(mim)
write.csv(mr.net, file = "/Users/dzy/Desktop/变量/Programs/DATA+/DukeDataPlus2018_DLSC/Machine_Learning_folder/unnormed_mr_confusion_matrix.csv")



write.csv(ara.net, file = "/Users/dzy/Desktop/变量/Programs/DATA+/DukeDataPlus2018_DLSC/data/ara_confusion_matrix.csv")
write.csv(clr.net, file = "/Users/dzy/Desktop/变量/Programs/DATA+/DukeDataPlus2018_DLSC/data/clr_confusion_matrix.csv")
write.csv(mr.net, file = "/Users/dzy/Desktop/变量/Programs/DATA+/DukeDataPlus2018_DLSC/data/mr_confusion_matrix.csv")

mr <- mr.net
mr <- log(mr)

par(bg = "lightgray")
hist(mr,200,col = "black",xlab = "natural logrithm of MI expression",ylab = "expression count")
grid(col = "white",lty= "solid")

mr[mr> quantile(mr,prob=25/100)] = 1
mr[mr<= quantile(mr,prob=25/100)] = 0

graph <- as(mr,"graphNEL")
plot(graph, attrs=list(node=list(fillcolor="lightgreen",size=20),edge=list(color="cyan"),graph=list(rankdir="LR")))


inf.net[inf.net<0.2468986] = 0
graph <- as(inf.net,"graphNEL")
hist(inf.net,100)
plot(graph, attrs=list(node=list(fillcolor="lightgreen",size=20),edge=list(color="cyan"),graph=list(rankdir="LR")))
graph2 <- as(syn.net,"graphNEL")
plot(graph2, attrs=list(node=list(fillcolor="lightgreen",size=20),edge=list(color="cyan"),graph=list(rankdir="LR")))
show.






#plotting pr curves with clr aracne mrnet
dev <- show.pr(clr.val,col="blue", type="l",pch = 3,cex=0.3,lwd=2)
dev <- show.pr(ara.val,col="red",device = dev, type="l",pch = 5,cex=0.3,lwd=2)
show.pr(mr.val,col="green", device = dev,type="l",pch = 7,cex=0.3,lwd=2)
grid(lty = "dotted" ,col="lightgray",lwd = par("lwd"),equilogs = TRUE)
legend("topright", 
       legend=c("CLR","ARACNe","MRNET"), 
       col = c("blue","red","green"),  
       pch = c(3,5,7), cex=1, title = "PR Curve")


#plotting roc curves with clr aracne mrnet
dev <- show.roc(clr.val,col="blue", type="l",pch = 3,lwd=2)
dev <- show.roc(ara.val,col="red",device = dev, type="l",pch = 5,lwd=2)
show.roc(mr.val,col="green", device = dev,type="l",pch = 7,lwd=2)
grid(lty = "dotted" ,col="lightgray",lwd = par("lwd"),equilogs = TRUE)
legend("bottomright", 
       legend=c("CLR","ARACNe","MRNET"), 
       col = c("blue","red","green"),  
       lwd=2,
       cex=1, title = "ROC Curve")


