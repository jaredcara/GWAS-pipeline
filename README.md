# GWAS-pipeline
GWAS pipeline requires .bed, .bim, and .fam files.   
To run the program, enter "python wrapper.py fle_location

Out info
Step1: Sex Check QC
Step2: SNP call rate
Step2_0: filters SNPS with <99% call rate QC
Step2_1: unfiltered SNP call rate graph data
Step2_2: filtered SNP call rate graph data
Step3: Person Call rate
Step3_0: filters persons with standard 0.1 threshold QC
Step3_1: unfiltered person call rate graph data
Step3_2: filtered person call rate graph data
Step4_0: Hardy-weinberg QC
Step4_1: Hardy-weinberg stats
Step5:
