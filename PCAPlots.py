import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy

hapmapinfo = pd.read_table("pop_HM3_hg19_forPCA.txt", sep = r'\s*', engine = 'python', header = None, usecols=(0,2), names = ["pop", 'IID']) #read in the location of the population data
fam = pd.read_table("step8_6.fam", sep = r'\s*', engine = 'python', header = None, usecols=(0,1), names = ["FID", 'IID']) #read in the data from the fam file
popinfo = fam.join(hapmapinfo.set_index("IID"), on = "IID") #merge the two previous files using the IID values
evec = pd.read_table("step8_6.evec", sep = r'\s*', engine = 'python', header = None, skiprows = 1) #read in the evec file
i = 0
while i < len(evec): #fixes the evec IID columns
    x = evec[0][i].index(':')
    evec[0][i]= evec[0][i][x+1:]
    i += 1
evec.columns = ['IID', 'PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10', 'CONTROL'] #renames the columns
PCA = evec.join(popinfo.set_index('IID'), on = 'IID') #merges everything by IID and the order for index is as follows (starting at index 1): IID PC1 PC2 PC3 PC4 PC5 PC6 PC7 PC8 PC9 PC10 CONTROL FID POP

plt.figure() #creates a new figure
for row in PCA.itertuples(): #plots the data by the family it is from
    if row[14] == "ASN": #Plots the ASN and makes their points red
        A = plt.scatter(row[2], row[3], c = 'r')
    elif row[14] == "CEU": #Plots the CEU and makes their points blue
        C = plt.scatter(row[2], row[3], c = 'b')
    elif row[14] == "YRI": #Plots the YRI and makes their points magenta
        Y = plt.scatter(row[2], row[3], c = 'm')
    else: #Plots everything else and makes the points green
        G = plt.scatter(row[2], row[3], c = 'g')
plt.xlabel("PC1") #adds xlabel
plt.ylabel("PC2") #adds ylabel
plt.title("PCA Plot 1 (PC1 vs PC2)") #addes title
plt.legend((A, C, Y, G), ("ASN", "CEU", "YRI", "GWAS"), scatterpoints = 1, loc='center left', bbox_to_anchor=(1, 0.5), ncol = 1) #adds the legend
plt.savefig("PCA1.png", bbox_inches = 'tight') #saves the figure

plt.figure() #this code is the same as above except with different columns used to create the graph
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

plt.figure() #this code is the same as above except with different columns used to create the graph
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
plt.figure() #this code is the similar to above except it adds lines 5 std dev away from selected point
for row in PCA.itertuples():
    if row[14] == "ASN":
        A = plt.scatter(row[2], row[3], c = 'r')
    elif row[14] == "CEU":
        C = plt.scatter(row[2], row[3], c = 'b')
    elif row[14] == "YRI":
        Y = plt.scatter(row[2], row[3], c = 'm')
        xvals.append(row[2]) #used to add bars to PCA plot
        yvals.append(row[3]) #move these two lines under desired population for bars be sure to change the x and y for where the values are coming from
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
