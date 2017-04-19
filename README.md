# GWAS-pipeline
GWAS pipeline requires .bed, .bim, and .fam files.   
To run the program, enter "python wrapper.py fle_location

Out info  
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
Step5_1: Prune.in: filtered SNPs below r^2 theshold of 0.2, prune.out: filterted SNPs above threshold    
Step5_2: Heterozygosity check   
---Step6: ---  
Step6_1: Generates pairwise IBS  
Step6_2: Filters related individuals  
---Step7: ---  
Step7_1: Heterozygosity check      
Step7_2: Filters outliers      
---Step8: ---  
Step8_1: Generates missing SNPs from HAPMAP and QC files to be merged, filters SNPs that are missing     
Step8_2: filters SNPs that are missing   
Step8_3: merged genotypes  
Step8_4: filtered SNPs for pca 
