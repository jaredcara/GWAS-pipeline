
# coding: utf-8

# In[36]:

import matplotlib.pyplot as plt
import pandas as pd

x = "step2_2" #insert file name here
ftype = ".imiss" #insert file type here

data = pd.read_table(x + ftype, sep= r'\s*') #use panda to read in the data from specified file

plt.figure() #create a new figure
plt.hist(data["F_MISS"], bins = 100) #add a histogram to the figure
plt.xlabel("F_MISS") #add the x label
plt.ylabel("Frequency") #add the y label
plt.title("F_MISS Frequncy Histogram") #add the title
plt.savefig(x + '_histogram.png') #save the file to specified file name as a .png


# In[ ]:



