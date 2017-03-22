# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 19:31:53 2017

@author: Alexa
"""

import os

#LD pruning:
os.system("plink --bfile /home/abaltsen/GWAS-pipeline/testdata --indep-pairwise 50 5 0.3 --out /home/abaltsen/GWAS-pipeline/")
#bfile:.bed file  indep-pairwise:window size in SNPs,the number of SNPs to to shift the window at each step, VIF threshold

#Relationship check:
os.system("plink --bfile /home/abaltsen/GWAS-pipeline/testdata --extract /home/abaltsen/GWAS-pipeline/plink.prune.in --genome --min 0.25 --out /home/abaltsen/GWAS-pipeline/")
#min:exclude pairs that share more than 25% of genome
os.system("plink --bfile /home/abaltsen/GWAS-pipeline/testdata --extract /home/abaltsen/GWAS-pipeline/plink.prune.in --remove hapmapDuplicateList.txt --genome --min 0.05 --out /home/abaltsen/GWAS-pipeline/")

os.system("plink --bfile /home/abaltsen/GWAS-pipeline/testdata --extract /home/abaltsen/GWAS-pipeline/plink.prune.in --remove hapmapDuplicatListFromAboveStep.txt --genome --out /home/abaltsen/GWAS-pipeline/")

#Heterozygosity check:
os.system("plink --bfile /home/abaltsen/GWAS-pipeline/testdat --het --extract plink.prune.in --remove hapmapDuplicatExclusionList.txt --out /home/abaltsen/GWAS-pipeline/")

