library(ggplot2)
library(readxl)
library(tidyr)
library(cowplot)
library(scales)
library(viridis)

#### Plot A ####
## All studies combined and only facetted by closest species (Only CRC and Control)

growth_rate_CRC_healthy <- read_excel('/Volumes/External_Drive/CRC_Read_metadata/Sorted_Growth_Rate_Sheets/Raw_Graph_Data/PlotA_raw_data.xlsx')

growth_rate_CRC_healthy$`Disease Status` <- as.character(growth_rate_CRC_healthy$`Disease Status`)
growth_rate_CRC_healthy$`Disease Status` <- factor(growth_rate_CRC_healthy$`Disease Status`, levels=c("Healthy", "CRC"))
growth_rate_CRC_healthy$`Closest Species` <- with(growth_rate_CRC_healthy, sub(" ", "\n", `Closest Species`))

pd = position_dodge(width = 0.5)
plotA <- ggplot(growth_rate_CRC_healthy, aes(x=`Disease Status`, y=`un-filtered index of replication (iRep)`, group=`Disease Status`)) + stat_boxplot(geom="errorbar", position=pd, width = 0.1) + geom_boxplot(width=0.5, position=pd, aes(fill=`Closest Species`)) +
  facet_grid(cols = vars(`Closest Species`), scales="free_y") + theme_bw() + theme(axis.text.x = element_text(angle=90, vjust = 0.5, hjust = 1), text = element_text(size=15), panel.grid = element_blank(),
                                                                                   strip.text = element_text(face = "italic"), strip.background = element_blank(), panel.border = element_rect(colour = "black", fill=NA), 
                                                                                   panel.background = element_blank(), legend.position = "none") + scale_fill_viridis(discrete=TRUE, option="B")

plotA

#### Supplementary Plot ####
## All genomes facetted by species and study (Adenoma, CRC, Control | YuJ, FengQ, HanniganGD, ZellerG)

#Importing growth rate excel spreadsheet to be used in plot creation
growth_rate_all <- read_excel('/Volumes/External_Drive/CRC_Read_metadata/Sorted_Growth_Rate_Sheets/Raw_Graph_Data/Supp_Plot_raw_data.xlsx')

growth_rate_all$`Disease Status` <- as.character(growth_rate_all$`Disease Status`)
growth_rate_all$`Disease Status` <- factor(growth_rate_all$`Disease Status`, levels=c("Healthy", "Adenoma","CRC"))
growth_rate_all$`Closest Species` <- with(growth_rate_all, sub(" ", "\n", `Closest Species`))

growth_rate_all$Study <- as.character(growth_rate_all$Study)
growth_rate_all$Study <- factor(growth_rate_all$Study, levels=c("Yu J. 2015", "Feng Q. 2015", "Hannigan GD. 2017", "Zeller G. 2014"))

pd = position_dodge(width = 0.5)
supp_plot <- ggplot(growth_rate_all, aes(x=`Disease Status`, y=`un-filtered index of replication (iRep)`, group=`Disease Status`)) + stat_boxplot(geom="errorbar", position=pd, width = 0.1) + geom_boxplot(width=0.5, position=pd, aes(fill=`Closest Species`)) +
  facet_grid(cols = vars(`Closest Species`), rows = vars(`Study`), scales="free_y") + theme_bw() + theme(axis.text.x = element_text(angle=90, vjust = 0.5, hjust = 1), text = element_text(size=15), legend.position = "none", strip.text.y = element_text(angle=0, hjust=0),
                                                                                                         strip.text.x = element_text(face = "italic"), strip.background = element_blank(), panel.border = element_rect(colour = "black", fill=NA), 
                                                                                                         panel.background = element_blank(), panel.grid = element_blank()) + scale_fill_viridis(discrete=TRUE, option="B")

supp_plot
