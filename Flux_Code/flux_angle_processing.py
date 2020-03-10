import os
import numpy as np
import file_management as fm
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats

DATA_FOLDER = "../Week2Flux"

angles = [-5,-4,-3,-2.5,-2,-1.5,-1,0.0,1,1.5,2,2.5,3,4,5] # non equal jumps

#gets angle from file name
def get_angle(filename):
    filename = filename.split("_")
    return float(filename[2])

def normal_dist(x, mean, sigma, A):
    return A*(1/np.sqrt(2*np.pi*sigma**2))*np.exp(-(((x-mean)**2)/2*sigma**2))

datadict = {}

# counting angle counts
for angle in angles:
    ccounts = []
    for filename in fm.file_generator(DATA_FOLDER,".txt"):
        if "flux" not in filename:
            continue
        
        if get_angle(filename) ==  angle:
            with open(DATA_FOLDER+"/"+filename) as f:
                line0 = f.readline()
                splitline = line0.split("\t")
                counts = int(float(splitline[1][0:-2]))
            ccounts.append(counts)

    datadict[angle] = [np.mean(ccounts),np.std(ccounts)]


X = list(datadict.keys())
Y = [datadict[key][0] for key in X]
Yerror = [np.sqrt(datadict[key][0])/np.sqrt(100) for key in X]
print("X:",X,"\n")
print("Y:",Y,"\n")
print("Y_error:",np.array(Yerror).round(2))

mean, sigma, A = curve_fit(normal_dist, X, Y, sigma = Yerror)[0]
Xspan = np.arange(min(X),max(X),0.01)
Yfit = [normal_dist(x,mean,sigma,A) for x in Xspan]
plt.plot(Xspan,Yfit)
plt.errorbar(X,Y,yerr=Yerror,fmt='.')
plt.show()

#statisitical analysis
chi_squared = sum([(Y[i]-normal_dist(X[i],mean,sigma,A))**2/normal_dist(X[i],mean,sigma,A) for i in range(len(X))])
print("p-value =",stats.chi2.pdf(chi_squared , len(X)-4))

print("Write extracted data to file? (yes/no)")
inputed = input()

if inputed == "yes":
    f = open("undoubled.txt", "w")
    for i in range(len(X)):
        print("wroteline")
        f.write(str(X[i])+"\t"+str(Y[i])+"\t"+str(Yerror[i])+"\n")
    f.close()
