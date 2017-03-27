import os

#make directory step1 for output
os.system("mkdir /home/jcara/testing/out")
os.system("mkdir /home/jcara/testing/out/step1")
#runs a check sex on data, sends output to step1/step1
os.system("plink --bfile /home/jcara/testing/testdata/testdata --check-sex -out /home/jcara/testing/out/step1/step1")
#finds 'PROBLEM' in output
#this is where the check sex found an issue
os.system("grep 'PROBLEM' /home/jcara/testing/out/step1/step1.sexcheck > /home/jcara/testing/out/step1/issues.txt")

#open issues
f = open('/home/jcara/testing/out/step1/issues.txt', 'r')
s = f.readlines()
f.close()

#in each line, only return the family id and sample id
exclude = []
for each in s:
	this = each.split()
	exclude.append(this[0]+'\t'+this[1])
	
	
#write to testdata/exclude.txt, to be used for down pipe commands	
o = open('/home/jcara/testing/testdata/exclude.txt', 'w')
for each in exclude:
	o.write(each)
	o.write('\n')

o.close()
