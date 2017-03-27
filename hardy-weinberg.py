import os

#make directory for hardy-weinberg output
os.system("mkdir /home/jcara/testing/out/step4")

#write hardy-weinberg test to step4
#where SNPs with p < 1e-6 are excluded
os.system("plink --bfile /home/jcara/testing/out/step2/step2_0/step2_0 --hwe 1e-6 --make-bed -out /home/jcara/testing/out/step4/step4")

