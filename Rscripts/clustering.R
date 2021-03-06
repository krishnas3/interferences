#!/usr/bin/env Rscript
library(factoextra)
library(ggplot2)
library(ggtree)
library(phangorn)
require(cluster)
library(RootsExtremaInflections)
library(NbClust)


affByCluster = function(dIC50, dclust, prresult){
  
  
  dMCluster = NULL
  lclust = unique(dclust[,2])
  lIC50 = colnames(dIC50)
  
  for(clust in lclust){
    lval = c(clust)
    dclustIC50 = dIC50[dcluster[which(dcluster[,2] == clust),1],]
    for (i in seq(1,length(lIC50))){
      vclustIC50 = dclustIC50[-which(is.na(dclustIC50[,i])),i]
      Msp = mean(vclustIC50)
      SDsp = sd(vclustIC50)
      nchem = length(vclustIC50)
      
      lval = append(lval, Msp)
      lval = append(lval, SDsp)
      lval = append(lval, nchem)
    }
    dMCluster = rbind(dMCluster, lval)
  }
  
  
  rownames(dMCluster) = dMCluster[,1]
  dMCluster = dMCluster[,-1]
  
  lcolnames = NULL
  for(n in colnames(dIC50)){
    cname = c(paste("M", n, sep = ""), paste("SD", n, sep = ""), paste("n", n, sep = ""))
    lcolnames = append(lcolnames, cname)
  }
  
  colnames(dMCluster) = lcolnames  
  write.csv(dMCluster, paste(prresult, "clusterIC50.csv", sep = ""))
  
}







optimalCluters = function (din, prout, metcluster, metOptNB, metagregation){
  
  din = scale (din)
  # scale data in input
  #print(head(din))
  
  print(head(din))
  if (metcluster == "hclust"){
    p = fviz_nbclust(din, hcut, hcut_metho = metagregation, method = metOptNB, k.max = dim(din)[2])
    ggsave(paste(prout, metcluster, "_" , metagregation, "_", metOptNB, ".png", sep = ""), dpi=300, height = 8, width = 15)
  }else if(metcluster == "kmeans"){
    p = fviz_nbclust(din, kmeans, method = metOptNB, k.max = dim(din)[2])
    ggsave(paste(prout, metcluster, "_" , metOptNB, ".png", sep = ""), dpi=300, height = 8, width = 15)    
  }
  

  if(metOptNB == "wss"){
    dcluster = as.matrix(p$data)
    d = inflexi(as.double(dcluster[,1]),as.double(dcluster[,2]),1,length(dcluster[,1]),3,3,plots=FALSE)
    nboptimal = d$finfl[1]
    print(nboptimal)
    
  }else if (metOptNB ==   "silhouette"){
    nboptimal = which(p$data[,2] == max(p$data[,2]))
  }else if (metOptNB == "gap_stat"){
    dcluster = as.matrix(p$data)
    #distorigin = abs(scale(as.double(dcluster[,5]), 0)-scale(-1*as.double(dcluster[,6]), 0))
    d = inflexi(as.double(dcluster[,5]),-1*as.double(dcluster[,6]),1,length(dcluster[,1]),3,3,plots=FALSE)
    nboptimal = d$finfl[1]
  }
  
  
  if (metcluster == "hclust"){
    outclust = hcut(din, k = nboptimal, hc_method = metagregation)
  }else if(metcluster == "kmeans"){
    outclust = hkmeans(din, nboptimal)
  }
  
  # PCA with clusters
  fviz_cluster(outclust, labelsize = 5)
  ggsave(paste(prout, "PCA_", metcluster, "_",  metagregation, "_", metOptNB, ".png", sep = ""), dpi=300, height = 12, width = 12)
  
  
  # dendogram fviz
  if(metcluster == "hclust"){
    fviz_dend(outclust, show_labels = FALSE, type = "circular")
    ggsave(paste(prout, "dendov1_", metcluster, "_",  metagregation, "_", metOptNB, ".png", sep = ""), dpi=300, height = 12, width = 13)
  }
  
  # dendogram old
  dcluster2 = cbind(names(outclust$cluster),outclust$cluster)
  colnames(dcluster2) = c("ID", "cluster")
  dcluster2 = as.data.frame(dcluster2)
  rownames(dcluster2) = names(outclust$cluster)
  dcluster2 = dcluster2[rownames(din),]
  
  # save cluster
  write.csv(dcluster2, paste(prout, "cluster.csv", sep = ""), row.names = FALSE)
  
  
  
  d <- dist(din, method = "euc")
  tupgma2 <- upgma(d, method = metagregation)
  #tupgma2 = groupOTU(tupgma2, nboptimal)
  t4 <- ggtree(tupgma2, layout="circular", size=1)
  t4 <- t4 %<+% dcluster2 + geom_text(aes(color=cluster, label=label, angle=angle, fontface="bold"), hjust=-0.15, size=2) +
    geom_tippoint(aes(color=cluster), alpha=0.75, size=1)+
    #scale_color_continuous(low='red', high='lightgreen') +
    #scale_color_manual(values=c("grey","red")) +
    theme(legend.position="right")+
    theme(plot.margin = unit(c(0,0,0,0), "cm")) +
    geom_treescale(x = 5, y = 5, width = 10, offset = NULL,
                   color = "white", linesize = 1E-100, fontsize = 1E-100)
  #print(t4)
  ggsave(paste(prout, "dendo_", metcluster, "_",  metagregation, "_", metOptNB, ".png", sep = ""), dpi=300, height = 8, width = 15)

  
  d <- dist(din, method = "euc")
  tupgma2 <- upgma(d, method = metagregation)
  tupgma2 <- groupOTU(tupgma2, nboptimal)
  t4 <- ggtree(tupgma2, layout="circular", size=1, aes(color=cluster))
  t4 <- t4 %<+% dcluster2 + geom_text(aes(color=cluster, label=cluster, angle=angle, fontface="bold"), hjust=-0.15, size=2) +
    geom_tippoint(aes(color=cluster), alpha=0.75, size=1)+
    #scale_color_continuous(low='red', high='lightgreen') +
    #scale_color_manual(values=c("grey","red")) +
    theme(legend.position="right")+
    theme(plot.margin = unit(c(0,0,0,0), "cm")) +
    geom_treescale(x = 5, y = 5, width = 10, offset = NULL,
                   color = "white", linesize = 1E-100, fontsize = 1E-100)
  #print(t4)
  ggsave(paste(prout, "dendo_cluster", metcluster, "_",  metagregation, "_", metOptNB, ".png", sep = ""), dpi=300, height = 8, width = 15)
  return(paste(prout, "cluster.csv", sep = ""))
}



optimalClutersDist = function (din, prout, metcluster, metOptNB, metagregation){
  
  minnc = 2
  maxnc = 200
  
  # remove 0 in the matrix, do not work with different index of cluster
  din[din == 0] = 0.0001# approximation for the disimilarity matrix
  ddist = as.dist(din)
  outclust = NbClust(diss = ddist, distance = NULL, min.nc = minnc, max.nc = maxnc, method = metagregation, index = metOptNB)
  nboptimal = outclust[["Best.nc"]][["Number_clusters"]]
  
  dindex = cbind(seq(minnc, maxnc), outclust$All.index)
  colnames(dindex) = c("Cluster", "Index")
  
  dindex = as.data.frame(dindex)
  
  p = ggplot(dindex, aes(Cluster, Index)) + 
    geom_point(size=1.5, colour="black", shape=21)+
    geom_line()+
    labs(x = "Number cluster", y = paste("Index ", metOptNB, sep = ""))
  print(p)
  ggsave(paste(prout, "optimisation_", metOptNB, ".png", sep = ""), width = 8, height = 8, dpi = 300)
  
  # PCA with clusters
  #fviz_cluster(outclust, labelsize = 5)
  #ggsave(paste(prout, "PCA_", metcluster, "_",  metagregation, "_", metOptNB, ".png", sep = ""), dpi=300, height = 12, width = 12)
  
  #fviz_dend(outclust, show_labels = FALSE, type = "circular")
  #ggsave(paste(prout, "dendov1_", metcluster, "_",  metagregation, "_", metOptNB, ".png", sep = ""), dpi=300, height = 12, width = 13)
  
  # dendogram old
  
  
  dcluster2 = cbind(names(outclust$Best.partition),outclust$Best.partition)
  colnames(dcluster2) = c("ID", "cluster")
  dcluster2 = as.data.frame(dcluster2)
  rownames(dcluster2) = names(outclust$cluster)
  

  
  # save cluster
  write.csv(dcluster2, paste(prout, "cluster.csv", sep = ""), row.names = FALSE)
  
  
  tupgma2 <- upgma(ddist, method = metagregation)
  #tupgma2 = groupOTU(tupgma2, nboptimal)
  t4 <- ggtree(tupgma2, layout="circular", size=1)
  t4 <- t4 %<+% dcluster2 + geom_text(aes(color=cluster, label=label, angle=angle, fontface="bold"), hjust=-0.15, size=2) +
    geom_tippoint(aes(color=cluster), alpha=0.75, size=1)+
    #scale_color_continuous(low='red', high='lightgreen') +
    #scale_color_manual(values=c("grey","red")) +
    theme(legend.position="right")+
    theme(plot.margin = unit(c(0,0,0,0), "cm")) +
    geom_treescale(x = 5, y = 5, width = 10, offset = NULL,
                   color = "white", linesize = 1E-100, fontsize = 1E-100)
  #print(t4)
  ggsave(paste(prout, "dendo_", metcluster, "_",  metagregation, "_", metOptNB, ".png", sep = ""), dpi=300, height = 8, width = 10)
  
  
  tupgma2 <- upgma(ddist, method = metagregation)
  tupgma2 <- groupOTU(tupgma2, nboptimal)
  t4 <- ggtree(tupgma2, layout="circular", size=1, aes(color=cluster))
  t4 <- t4 %<+% dcluster2 + geom_text(aes(color=cluster, label=cluster, angle=angle, fontface="bold"), hjust=-0.15, size=2) +
    geom_tippoint(aes(color=cluster), alpha=0.75, size=1)+
    #scale_color_continuous(low='red', high='lightgreen') +
    #scale_color_manual(values=c("grey","red")) +
    theme(legend.position="right")+
    theme(plot.margin = unit(c(0,0,0,0), "cm")) +
    geom_treescale(x = 5, y = 5, width = 10, offset = NULL,
                   color = "white", linesize = 1E-100, fontsize = 1E-100)
  #print(t4)
  ggsave(paste(prout, "dendo_cluster", metcluster, "_",  metagregation, "_", metOptNB, ".png", sep = ""), dpi=300, height = 8, width = 10)
  return(paste(prout, "cluster.csv", sep = ""))
}


#tree <- groupOTU(tupgma, cls)
#t4 <- ggtree(tree, layout="circular", size=0.5, branch.length="none",aes(color=group)) +
#  geom_text(aes(color=group, label=label, angle=angle, fontface="bold"), hjust=-0.15, size=3)+
#  scale_color_manual(values=c("grey",color18)) + #theme(legend.position="none")+
#  theme(plot.margin = unit(c(0,0,0,0), "cm"))+
#  geom_treescale(x = 30, y = 30, width = NULL, offset = NULL,
#                 color = "white", linesize = 1E-100, fontsize = 1E-100)
#print(t4)