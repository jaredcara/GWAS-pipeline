import os

os.system("plink --bfile /home/jcara/testdata/testdata --check-sex -out /home/jcara/step1/step1")
os.system("grep 'PROBLEM' /home/jcara/step1/step1.sexcheck > /home/jcara/step1/issues.txt")

f = open('/home/jcara/step1/issues.txt', 'r')
s = f.readlines()
f.close()

exclude = []
for each in s:
	this = each.split()
	exclude.append(this[0]+'\t'+this[1])
	
	
	
o = open('/home/jcara/testdata/exclude.txt', 'w')
for each in exclude:
	o.write(each)
	o.write('\n')

o.close()