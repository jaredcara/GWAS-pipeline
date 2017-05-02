# GWAS-pipeline  
GWAS pipeline requires .bed, .bim, and .fam input files.  
To complete PCA analysis, hapmapdata and bmerge data(bed, bim, and fam) will be required  
The bmerge data for hg19 is hosted on our github  

To run the program, enter "python gwas-pipelineQC.py file_name pop_data_for_PCA_plots bmerge_data"  
When entering the file name and bmerge data, extentions should not be entered

Other options include IBD relatedness and number of standard deviations for the heterozygosity check  
If you do not include these options the defaults will utilized

Intallation of PLINK (https://www.cog-genomics.org/plink2/) is required.   
Python modules used in pipleine: pandas, matplotlib, os, sys   
Pandas and matplotlib may need to be installed on your system  

Output Information  
---Step1: Sex Check QC---  
---Step2: SNP call rate---  
Step2_0: filters SNPS with <99% call rate QC  
Step2_1: unfiltered SNP call rate graph data  
Step2_2: filtered SNP call rate graph data  
---Step3: Person Call rate---  
Step3_0: filters persons with standard 0.1 threshold QC  
Step3_1: unfiltered person call rate graph data  
Step3_2: filtered person call rate graph data  
---Step4: Hardy-Weinberg---  
Step4_0: Hardy-Weinberg QC  
Step4_1: Hardy-Weinberg stats  
---Step5: ---  
Step5_0: Prune.in: filtered SNPs below r^2 theshold of 0.2, prune.out: filterted SNPs above threshold    
Step5_1: Heterozygosity check   
---Step6: ---  
Step6_0: Generates pairwise IBS  
Step6_1: Filters related individuals  
---Step7: ---  
Step7_0: Heterozygosity check      
Step7_1: Filters outliers      
---Step8: ---  
Step8_0: Generates missing SNPs from HAPMAP and QC files to be merged, filters SNPs that are missing     
Step8_1: filters SNPs that are missing   
Step8_2: merged genotypes  
Step8_3: filtered SNPs for pca  
Step8_4:  
Step8_5:  
