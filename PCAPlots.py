import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy

hapmapinfo = pd.read_table("pop_HM3_hg19_forPCA.txt", sep = r'\s*', engine = 'python', header = None, usecols=(0,2), names = ["pop", 'IID'])
fam = pd.read_table("step8_6.fam", sep = r'\s*', engine = 'python', header = None, usecols=(0,1), names = ["FID", 'IID'])
popinfo = fam.join(hapmapinfo.set_index("IID"), on = "IID")
evec = pd.read_table("step8_6.evec", sep = r'\s*', engine = 'python', header = None, skiprows = 1)
i = 0
while i < len(evec):
    x = evec[0][i].index(':')
    evec[0][i]= evec[0][i][x+1:]
    i += 1
evec.columns = ['IID', 'PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10', 'CONTROL']
PCA = evec.join(popinfo.set_index('IID'), on = 'IID') #ORDER (starting at index 1): IID PC1 PC2 PC3 PC4 PC5 PC6 PC7 PC8 PC9 PC10 CONTROL FID POP
plt.figure()
for row in PCA.itertuples():
    if row[14] == "ASN":
        A = plt.scatter(row[2], row[3], c = 'r')
    elif row[14] == "CEU":
        C = plt.scatter(row[2], row[3], c = 'b')
    elif row[14] == "YRI":
        Y = plt.scatter(row[2], row[3], c = 'm')
    else:
        G = plt.scatter(row[2], row[3], c = 'g')
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA Plot 1 (PC1 vs PC2)")
plt.legend((A, C, Y, G), ("ASN", "CEU", "YRI", "GWAS"), scatterpoints = 1, loc='center left', bbox_to_anchor=(1, 0.5), ncol = 1)
plt.savefig("PCA1.png", bbox_inches = 'tight') 

plt.figure()
for row in PCA.itertuples():
    if row[14] == "ASN":
        A = plt.scatter(row[2], row[4], c = 'r')
    elif row[14] == "CEU":
        C = plt.scatter(row[2], row[4], c = 'b')
    elif row[14] == "YRI":
        Y = plt.scatter(row[2], row[4], c = 'm')
    else:
        G = plt.scatter(row[2], row[4], c = 'g')
plt.xlabel("PC1")
plt.ylabel("PC3")
plt.title("PCA Plot 2 (PC1 vs PC3)")
plt.legend((A, C, Y, G), ("ASN", "CEU", "YRI", "GWAS"), scatterpoints = 1, loc='center left', bbox_to_anchor=(1, 0.5), ncol = 1)
plt.savefig("PCA2.png", bbox_inches = 'tight') 

plt.figure()
for row in PCA.itertuples():
    if row[14] == "ASN":
        A = plt.scatter(row[3], row[4], c = 'r')
    elif row[14] == "CEU":
        C = plt.scatter(row[3], row[4], c = 'b')
    elif row[14] == "YRI":
        Y = plt.scatter(row[3], row[4], c = 'm')
    else:
        G = plt.scatter(row[3], row[4], c = 'g')
plt.xlabel("PC2")
plt.ylabel("PC3")
plt.title("PCA Plot 3 (PC2 vs PC3)")
plt.legend((A, C, Y, G), ("ASN", "CEU", "YRI", "GWAS"), scatterpoints = 1, loc='center left', bbox_to_anchor=(1, 0.5), ncol = 1)
plt.savefig("PCA3.png", bbox_inches = 'tight') 

xvals = []
yvals = []
plt.figure()
for row in PCA.itertuples():
    if row[14] == "ASN":
        A = plt.scatter(row[2], row[3], c = 'r')
    elif row[14] == "CEU":
        C = plt.scatter(row[2], row[3], c = 'b')
    elif row[14] == "YRI":
        Y = plt.scatter(row[2], row[3], c = 'm')
        xvals.append(row[2]) #used to add bars to PCA plot
        yvals.append(row[3]) #move these two lines under desired population for bars
    else:
        G = plt.scatter(row[2], row[3], c = 'g')
xmean = sum(xvals)/float(len(xvals)) #calculate the mean
ymean = sum(yvals)/float(len(yvals)) #calculate the mean
xstd = numpy.std(xvals) #calculate std dev
ystd = numpy.std(yvals) #calculate std dev
sdn = 5 #number of standard deviations away from mean you want line to be
plt.axvline(x= xmean+xstd*sdn, color = 'k') #add line x sd away from xmean
plt.axvline(x= xmean-xstd*sdn, color = 'k')
plt.axhline(y= ymean+ystd*sdn, color = 'k') #add line x sd away from ymean
plt.axhline(y= ymean-ystd*sdn, color = 'k')
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA Plot 1 (PC1 vs PC2) with lines")
plt.legend((A, C, Y, G), ("ASN", "CEU", "YRI", "GWAS"), scatterpoints = 1, loc='center left', bbox_to_anchor=(1, 0.5), ncol = 1)
plt.savefig("PCA1Lines.png", bbox_inches = 'tight') 
