# GWAS-pipeline  
GWAS pipeline requires .bed, .bim, and .fam input files.  
To complete PCA analysis, hapmapdata and bmerge data(bed, bim, and fam) will be required  
For final imputation, HRC-1000G-check-bim.pl (http://www.well.ox.ac.uk/~wrayner/tools/) is requred,additionally for this tool to be fully functional, the unzipped tab delimited HRC reference is required (http://www.haplotype-reference-consortium.org/site).  
Hapmapdata and bmerge data for the test data for hg19 is hosted on our github  

Intallation of PLINK (https://www.cog-genomics.org/plink2/) is required.   
Python modules used in pipleine: pandas, matplotlib, os, sys, numpy, Pandas, matplotlib, and numpy must be installed on your system.  
Perl modules used in "HRC imputation": strict, warnings, Getopt::Long, IO::Uncompress::Gunzip, and Term::ReadKey must be installed on your system.  


To run the program, enter "python gwas-pipelineQC.py --fil file_name --hap pop_data_for_PCA_plots --mer bmerge_data --ref HRC_reference -c SNP_callrate -p person_callrate -i IBD_relatedness -s HET_standarddeviations  

Example:
python gwas-pipelineQC.py --fil GWAS_dataset --hap pop_HM3_hg19_forPCA.txt --mer HM3_ASN_CEU_YRI_Unrelated_hg19_noAmbig --ref HRC.r1-1.GRCh37.wgs.mac5.sites.vcf -c 0.01 -p 0.1 -i 0.125 -s 6  

Note. When entering the file name and bmerge data, extentions should not be entered  
      Be careful not to enter "." for file name and bmerge data  

SNP_callrate has a default of 0.01, if you do not enter a value, 0.01 will be used  
Person_callrate has a default of 0.1,  if you do not enter a value, 0.1 will be used  
IBD_relatedness has a default of 0.125,  if you do not enter a value, 0.125 will be used  
HET_standarddeviations has a default of 6, if you do not enter a value, 6 will be used  


The file containing the pop data for PCA plots should be similar to the .fam input file.  
Except in row 1 you should include the population data, also data should be tab delimited.  
For example, it should read: POPULATION FID IID (other info from .fam file)  


PCA plots will only be created for datasets containing ASN, CEU, and YRI as the populations being tested for.  
If there are any deviations from these populations, changes will need to be made to the code.  
GWAS points are assumed to be any point that isn't already labeled from the pop data for PCA plots file.  


All output will be found in "file_nameout/"  
Output Information  
---Final ---  
file_nameout/final/ contains the final, filtered .bed .bim and .fam files for other GWAS analysis  
file_nameout/histogram/ contains all plots and histograms from the steps specified in their names  
file_nameout/to_impute_vcf/ contains all zipped individual chromosome .vcf.gz files for upload to the Michigan Imputation Server  
file_nameout/HRC/ contails all files used in the HRC bim check  
---Step1: Sex Check QC---  
---Step2: SNP call rate---  
Step2_0 Filters SNPS with <99% call rate QC  
Step2_2 unfiltered SNP call rate graph data  
Step2_3 filtered SNP call rate graph data  
---Step3: Person Call rate---  
Step3_0 filters persons with standard 0.1 threshold QC  
Step3_1 unfiltered person call rate graph data  
Step3_2 filtered person call rate graph data  
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
Step8_4: .map and .ped files for pca  
---Step9: ---
Step
--Step10: ---
Step10_
