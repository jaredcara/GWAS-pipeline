import os


#make directory for person call rate check output
os.system("mkdir /home/jcara/testing/out/step3")
#person call rate with standard 0.1 threshold
#write output to step5/step5
os.system("plink --bfile /home/jcara/testing/out/step2/step2_0/step2_0 --mind 0.1 --make-bed --out /home/jcara/testing/out/step3/step3")

