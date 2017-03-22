#wrapper code

import os                           #imports os module to allow the code to use the command line
import argparse                     #imports the argparse module which accepts input from the command line to use in the running of the code
parser = argparse.ArgumentParser()  #creates the parser list for argparse
#parser.add_argument("test", help="simply a test") #testing argument
args = parser.parse_args()          #creates the list of aruments called args

#run Step 1-sex_check.py from Jared (still needs to be not hardcoded)
os.system("python check_sex.py")    #runs check_sex.py but will need to be changed so it is not hard coded
print ("Sex check complete.")            #tells the user when the process is complete


# run Step 5-step5.py from Alexa (still needs to be not hardcoded)
os.system("python step5.py")
print ("LD prune relationship check and heterozygosity complete.")