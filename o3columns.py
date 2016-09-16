import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import datetime as DT
from scipy.interpolate import interp2d
# Requires o3 columns prepared as follows:
# o3 = np.zeros((len(a.latitude),# to compare, len(a.day)))
# o3 = o3.tolist()
# for x in range(len(a.latitude)):
#     for y in range(len(a.day)):
#          o3[x][0][y] = a.O3COLUMN[y][x]
latitude = np.array([-8.52631607e+01,  -7.57894745e+01,  -6.63157806e+01, -5.68421059e+01,  -4.73684235e+01,  -3.78947411e+01, -2.84210606e+01,  -1.89473743e+01,  -9.47369099e+00, -6.83018834e-06,   9.47368431e+00,   1.89473515e+01, 2.84210396e+01,   3.78947296e+01,   4.73684044e+01, 5.68420982e+01,   6.63157883e+01,   7.57894592e+01, 8.52631378e+01])
latitude_edges = np.array([-90.        , -80.52631378, -71.05262756, -61.57894135,-52.10525513, -42.63156891, -33.15788269, -23.68419838,-14.21051407,  -4.73682976,   4.73685455,  14.21053886,23.68422318,  33.15790558,  42.6315918 ,  52.10527802, 61.57896423,  71.05265045,  80.52633667,  90.        ])
def volclocator(time, year = 1990):
        global volctime
    	volctime = t2dt(np.add(np.true_divide(time,365),year))

def injectnum(Cl2, So2, string):
    	global cl2, so2, stringy
	cl2 = str(Cl2)
	so2 = str(So2)
        stringy = str(string)
def plotter(o3array,dayt,lat,idxa = 0, idxb = 1, idxc = 2, idxd = 3, year=1990, ylimz = (100,350), flag = 1):
	global fig, ax
    	if flag == 0:
             plt.ioff()
        else: 
             plt.ion()
        fig, ax = plt.subplots(figsize = (10,7.5))
 	fig.set_facecolor('white')
	ax.set_ylabel('Column Ozone', fontsize = 25)
	day = []
        dayyt = np.true_divide(dayt,365)
        dayyt = np.add(dayyt, int(year))
        for x in range(len(dayt)):
              day.append(t2dt(dayyt[x]))
  	for y in range(int(ylimz[0]), int(ylimz[1]), (int(ylimz[1])-int(ylimz[0]))/10):    
              ax.plot(day, [y] *len(day), "--", lw=0.5, color="black", alpha=0.3)   
        baseline = o3array[int(lat)][idxa]
        clonly = o3array[int(lat)][idxb]
        so2only = o3array[int(lat)][idxc]   #for future use
        so2cl = o3array[int(lat)][idxd]    #change to [3] once so2 run completed
	latlabels = [roundulator(latitude_edges[int(lat)],1),roundulator(latitude_edges[int(lat)+1],1)]
        latlabelz = [0,0]
        for idx, label in enumerate(latlabels):
               if label <= 0:
                    latlabelz[idx] = str(abs(label)) + 'S'
               else:
                    latlabelz[idx] = str(label) + 'N'
        if latlabels[-1]  <=0:
               latlabelz = latlabelz[::-1]   
        latlabels = latlabelz              
        ax.plot(day,baseline, 'k-', dashes = [16,4,2,4,2,4], lw=2, label = 'No Perturbation')
        ax.plot(day,clonly, 'g-', dashes = [8,4,2,4,2,4], lw = 2, label = cl2 + ' MT Clx')
        ax.plot(day,so2only, 'y-', dashes = [8,4,2,4,2,4], lw = 2, label = so2 + ' MT SO2')
        ax.plot(day,so2cl, color = 'saddlebrown', ls ='-', lw = 2 , label = cl2 + ' MT Clx ' + so2 + ' MT SO2')     
        if 'volctime' in globals():
        	ax.axvspan(day[0],volctime, alpha = 0.5, color = 'lightblue')
                ax.axvline(x=volctime,color='k',ls='dashed')
                volcanohandle = mpatches.Patch(color = 'lightblue', linestyle = 'dashed', ec = 'black')
                volcanolegend = 'Before Eruption'
        years = mdates.YearLocator()
        months = mdates.MonthLocator()
        minorLocator = MultipleLocator(100)
        fig.autofmt_xdate()
        ax.grid(False)
        ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_major_locator(years)
        ax.yaxis.set_minor_locator(minorLocator)
        ax.set_ylim(ylimz[0],ylimz[1])
#        ax.set_title(stringy +', '+ latlabels[0] + ' - ' + latlabels[1] , fontsize = 25)
        ax.text(day[len(day)/2], ylimz[1]- 0.01*ylimz[1], stringy + ', ' + latlabels[0] + ' - ' + latlabels[1], fontsize=25, ha="center")  
        ax.tick_params(axis = 'both', which = 'major', labelsize = 17)
        handles, labels = ax.get_legend_handles_labels()
        handles.append(volcanohandle)
        labels.append(volcanolegend)
        ax.legend(handles[::-1], labels[::-1], loc = 'best', fancybox = True, fontsize = 25) 
        ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        plt.yticks(range(int(ylimz[0]),int(ylimz[1]), (int(ylimz[1]) - int(ylimz[0]))/10), [str(x) + " DU" for x in range(int(ylimz[0]),int(ylimz[1]),(int(ylimz[1])-int(ylimz[0]))/10)], fontsize=20)
        plt.xticks(fontsize = 20)
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")  
        fig.tight_layout()  
     

def dt2t( adatetime):
            """
            Convert adatetime into a float. The integer part of the float should
            represent the year.
            Order should be preserved. If adate<bdate, then d2t(adate)<d2t(bdate)
            time distances should be preserved: If bdate-adate=ddate-cdate then
            dt2t(bdate)-dt2t(adate) = dt2t(ddate)-dt2t(cdate)
            """
            year = adatetime.year
            boy = DT.datetime(year, 1, 1)
            eoy = DT.datetime(year + 1, 1, 1)
            return year + ((adatetime - boy).total_seconds() / ((eoy - boy).total_seconds())) 
     
def roundulator(n, m): #rounds n to the nearest m
        r = n % m
        return n + m - r if r + r >= m else n - r

def t2dt( atime):
            """
            Convert atime (a float) to DT.datetime
            This is the inverse of dt2t.
            assert dt2t(t2dt(atime)) == atime
            """
            year = int(atime)
            remainder = atime - year
            boy = DT.datetime(year, 1, 1)
            eoy = DT.datetime(year + 1, 1, 1)
            seconds = remainder * (eoy - boy).total_seconds()
            return boy + DT.timedelta(seconds=seconds)

def difplotter(o3array,dayt,lat,idxa = 0, idxb = 1, idxc = 2, idxd = 3, year=1990, ylimz = (-50,5), flag = 1):
	global fig, axi
        if flag == 0:
             plt.ioff()
        else: 
             plt.ion()
    	fig, ax = plt.subplots(figsize = (10,7.5))
 	fig.set_facecolor('white')
	ax.set_ylabel('Change in Column Ozone vs. No Volcano', fontsize = 25)
	day = []
        dayyt = np.true_divide(dayt,365)
        dayyt = np.add(dayyt, int(year))
        for x in range(len(dayt)):
              day.append(t2dt(dayyt[x]))
 	for y in range(int(ylimz[0]), int(ylimz[1]), 10):    
              ax.plot(day, [y] *len(day), "--", lw=0.5, color="black", alpha=0.3)    
        novolc = o3array[int(lat)][idxa]
        clonly = o3array[int(lat)][idxb]
        so2only = o3array[int(lat)][idxc]   #for future use
        so2cl = o3array[int(lat)][idxd]    #change to [3] once so2 run completed
 #       for x in range(len(dayt)):
#		idx = int(day[x].strftime('%m')[:]) -1
#		novolc[x] = np.dot(np.true_divide(np.subtract(novolc[x], baseline[idx][lat]), baseline[idx][lat]),100)
#		clonly[x] = np.dot(np.true_divide(np.subtract(clonly[x], baseline[idx][lat]), baseline[idx][lat]),100)
#		so2only[x] = np.dot(np.true_divide(np.subtract(so2only[x], baseline[idx][lat]), baseline[idx][lat]),100)
#		so2cl[x] = np.dot(np.true_divide(np.subtract(so2cl[x], baseline[idx][lat]), baseline[idx][lat]),100)

#	novolc = np.dot(np.true(divide(np.subtract(novolc, baseline), baseline), 100)
	clonly = np.dot(np.true_divide(np.subtract(clonly, novolc),novolc),100)
        so2only = np.dot(np.true_divide(np.subtract(so2only, novolc),novolc),100)
        so2cl = np.dot(np.true_divide(np.subtract(so2cl, novolc), novolc), 100)
#	novolc = np.asarray(novolc)
#	clonly = np.asarray(clonly)        
#	so2only = np.asarray(so2only)
#	so2cl = np.asarray(so2cl)
#	novolc = novolc.flatten()
 #       clonly = clonly.flatten()
  #      so2only = so2only.flatten()
   #     so2cl = so2cl.flatten()
        latlabels = [roundulator(latitude_edges[int(lat)],1),roundulator(latitude_edges[int(lat)+1],1)]
        latlabelz = [0,0]
        for idx, label in enumerate(latlabels):
               if label <= 0:
                    latlabelz[idx] = str(abs(label)) + 'S'
               else:
                    latlabelz[idx] = str(label) + 'N'
        if latlabels[-1]  <=0:
               latlabelz = latlabelz[::-1]   
        latlabels = latlabelz              
#        ax.plot(day,novolc, 'ko-', dashes = [8,4,2,4,2,4], lw=2, label = 'No Perturbation')
        ax.plot(day,clonly, 'g-', dashes = [8,4,2,4,2,4], lw = 2, label = cl2 + ' MT Clx')
        ax.plot(day,so2only, 'y-', dashes = [4,4,2,4,2,4], lw = 2, label = so2 + ' MT SO2')
        ax.plot(day,so2cl, color = 'saddlebrown', ls ='-', lw = 2 , label = cl2 + ' MT Clx ' + so2 + ' MT SO2')     
        if 'volctime' in globals():
        	ax.axvspan(day[0],volctime, alpha = 0.5, color = 'lightblue')
                ax.axvline(x=volctime,color='k',ls='dashed')
                volcanohandle = mpatches.Patch(color = 'lightblue', ec = 'k', ls = 'dashed')
                volcanolegend = 'Before Eruption'
        years = mdates.YearLocator()
        months = mdates.MonthLocator()
        minorLocator = MultipleLocator(2.5)
        fig.autofmt_xdate()
        ax.grid(False)
        ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_major_locator(years)
        ax.yaxis.set_minor_locator(minorLocator)
        ax.set_ylim(ylimz[0],ylimz[1])
#        ax.set_title(stringy +', '+ latlabels[0] + ' - ' + latlabels[1] , fontsize = 25)
        ax.text(day[len(day)/2], ylimz[1]/2, stringy + ', ' + latlabels[0] + ' - ' + latlabels[1], fontsize=25, ha="center")  
        ax.tick_params(axis = 'both', which = 'major', labelsize = 17)
        handles, labels = ax.get_legend_handles_labels()
        handles.append(volcanohandle)
        labels.append(volcanolegend)
        ax.legend(handles[::-1], labels[::-1], loc = 'best', fancybox = True, fontsize = 25) 
        ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        plt.yticks(range(int(ylimz[0]),int(ylimz[1]), 10), [str(x) + "%" for x in range(int(ylimz[0]),int(ylimz[1]), 10)], fontsize=20)
        plt.xticks(fontsize = 20)
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")  
        fig.tight_layout()

def baselineextractor(filename):
	global avgs, baseline
  	avgs = np.fromfile(filename, dtype = '>f4')
	avgs = avgs[2:].reshape((37,50,324), order = "FORTRAN")
        avgs[ avgs > 1e10] = 0
        baseline = np.zeros((37,12)).tolist()
	evenList = np.linspace(0,36,37, dtype = 'int')
	evenlist = [x for x in evenList if x % 2 == 0]
        monthlist = np.linspace(12,23,12, dtype = 'int')
        for x in range(37):
		for y in range(len(monthlist)):
			monthavgs = []
			for z in range(50):
				monthavgs.append(avgs[x][z][monthlist[y]])
				baseline[x][y] = np.sum(monthavgs)
     	X , Y = np.meshgrid(np.linspace(-90,90,37),range(0,12))
        f = interp2d(X, Y, baseline)
        xnew = latitude	
        months = range(0,12,1)
        baseline = f(xnew, months)
        
