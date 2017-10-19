from __future__ import unicode_literals
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import matplotlib.gridspec as gridspec
import datetime as DT
from scipy.interpolate import interp2d
import matplotlib as mpl
from matplotlib import dates
import math

mpl.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.unicode'] = True
mpl.use("pgf")
pgf_with_custom_preamble = {
    #"font.family": "serif", # use serif/main font for text elements
    #"text.usetex": True,    # use inline math for ticks
    #"pgf.rcfonts": False,   # don't setup fonts from rc parameters
    "pgf.preamble": [
         "\\usepackage{units}",         # load additional packages
         "\\usepackage{amsmath}",
         "\\usepackage{unicode-math}",  # unicode math setup
         r"\setmathfont{xits-math.otf}",
         #r"\setmainfont{}", # serif font via preamble
         ]}
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
	return volctime

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
        
def globeplotter(o3arrray,yr, dayt,idxa = 0, idxb = 1, idxc = 2, idxd = 3, year=1990,  ylimz = (-50,5), tickah = 5, flag = 1):
	global fig, ax
        if flag == 0:
             plt.ioff()
        else: 
             plt.ion()
	o3array = np.zeros((19,4,len(dayt)))
	for x in range(0,18):
		for y in range(len(dayt)):
			o3array[x][0][y] = o3arrray[int(yr)][x][idxa][y]
			o3array[x][1][y] = o3arrray[int(yr)][x][idxb][y]
			o3array[x][2][y] = o3arrray[int(yr)][x][idxc][y]
			o3array[x][3][y] = o3arrray[int(yr)][x][idxd][y]
    	fig, ax = plt.subplots(figsize = (10,7.5))
 	fig.set_facecolor('white')
	ax.set_ylabel('Change in Column Ozone vs. No Volcano', fontsize = 35)
	day = []
        dayyt = np.true_divide(dayt,365)
        dayyt = np.add(dayyt, int(year))
        for x in range(len(dayt)):
              day.append(t2dt(dayyt[x]))
 	for y in range(int(ylimz[0]), int(ylimz[1]), int(tickah)):    
              ax.plot(day, [y] *len(day), "--", lw=0.5, color="black", alpha=0.3)
        novolc = np.zeros(( len(dayt))).tolist()
        clonly = np.zeros((len(dayt))).tolist()
        so2only = np.zeros(( len(dayt))).tolist()
        so2cl = np.zeros((len(dayt))).tolist()    
        so2pluscl = np.zeros((len(dayt))).tolist()
	for lat in range(3,15):
		novolc = np.add(novolc, o3array[int(lat)][0])
        	clonly = np.add(clonly, o3array[int(lat)][1])
        	so2only =np.add(so2only, o3array[int(lat)][2])   #for future use
        	so2cl = np.add(so2cl, o3array[int(lat)][3])    #change to [3] once so2 run completed
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
	so2pluscl = np.add(so2only, clonly)


#	novolc = np.asarray(novolc)
#	clonly = np.asarray(clonly)        
#	so2only = np.asarray(so2only)
#	so2cl = np.asarray(so2cl)
#	novolc = novolc.flatten()
 #       clonly = clonly.flatten()
  #      so2only = so2only.flatten()
   #     so2cl = so2cl.flatten()
#        ax.plot(day,novolc, 'ko-', dashes = [8,4,2,4,2,4], lw=2, label = 'No Perturbation')
       # ax.plot(day,clonly, 'g-', dashes = [8,4,2,4,2,4], lw = 2, label = cl2 + '$\mbox{\ Tg\ Cl}_\mbox{y}$')
        ax.plot(day,clonly, 'g-', ls='-', lw = 3, label = 'Cl$_y$ only')
        ax.plot(day,so2only, 'y-', ls='-', lw = 3, label ='SO$_2$ only')
	ax.plot(day, so2pluscl, color = 'darkslategray', ls = '-', lw= 3, label = 'SO$_2$ only + Cl$_y$ only')
        ax.plot(day,so2cl, color = 'saddlebrown', ls ='-', lw = 3 , label = 'SO$_2$ and Cl$_y$ co-injection')     
       # ax.plot(day,so2only, 'y-', dashes = [4,4,2,4,2,4], lw = 2, label = so2 + '$\mbox{\ Tg\ SO}_\mbox{2}$')
	#ax.plot(day, so2pluscl, color = 'darkslategray', ls = '--', lw= 2, label = '$\mbox{SO}_{\mbox{2}}\ \mbox{only}\ \mbox{+}\ \mbox{Cl}_{\mbox{y}}\ \mbox{only}$')
        #ax.plot(day,so2cl, color = 'saddlebrown', ls ='-', lw = 2 , label = cl2 + '$\mbox{\ Tg\ Cl}_{\mbox{y}}\ $'+ ' + ' + so2 + '$\mbox{\ Tg\ SO}_\mbox{2}$')     
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
    #    ax.text(day[3*len(day)/5 - 3], ylimz[1]/2, stringy + ', 60S - 60N', fontsize=40, ha="center")  
        ax.tick_params(axis = 'both', which = 'major', labelsize = 17)
        handles, labels = ax.get_legend_handles_labels()
        handles.append(volcanohandle)
        labels.append(volcanolegend)
        ax.legend(handles[::-1], labels[::-1], loc = 4, fancybox = True, fontsize = 35) 
        ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
#	ax.fill_between(day,so2cl, so2pluscl, facecolor = 'whitesmoke', interpolate = True)
#	ax.fill_between(day,clonly, so2only, where = so2only <= clonly, facecolor = 'palegoldenrod', interpolate = True)
#	ax.fill_between(day,clonly, so2only, where = so2only >= clonly, facecolor = 'yellowgreen', interpolate = True)
        plt.yticks(range(int(ylimz[0]),int(ylimz[1]), int(tickah)), [str(x) + "\%" for x in range(int(ylimz[0]),int(ylimz[1]), int(tickah))], fontsize=35)
        plt.xticks(fontsize = 35)
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")  
        fig.tight_layout() 
        
def norplotter(o3arrray,yr, dayt,idxa = 0, idxb = 1, idxc = 2, idxd = 3, year=1990,  ylimz = (-50,5), tickah = 5, flag = 1):
	global fig, ax
        if flag == 0:
             plt.ioff()
        else: 
             plt.ion()
	o3array = np.zeros((19,4,len(dayt)))
	for x in range(0,18):
		for y in range(len(dayt)):
			o3array[x][0][y] = o3arrray[int(yr)][x][idxa][y]
			o3array[x][1][y] = o3arrray[int(yr)][x][idxb][y]
			o3array[x][2][y] = o3arrray[int(yr)][x][idxc][y]
			o3array[x][3][y] = o3arrray[int(yr)][x][idxd][y]
    	fig, ax = plt.subplots(figsize = (10,7.5))
 	fig.set_facecolor('white')
	ax.set_ylabel('Change in Column Ozone vs. No Volcano', fontsize = 35)
	day = []
        dayyt = np.true_divide(dayt,365)
        dayyt = np.add(dayyt, int(year))
        for x in range(len(dayt)):
              day.append(t2dt(dayyt[x]))
 	for y in range(int(ylimz[0]), int(ylimz[1]), int(tickah)):    
              ax.plot(day, [y] *len(day), "--", lw=0.5, color="black", alpha=0.3)
        novolc = np.zeros(( len(dayt))).tolist()
        clonly = np.zeros((len(dayt))).tolist()
        so2only = np.zeros(( len(dayt))).tolist()
        so2cl = np.zeros((len(dayt))).tolist()    
        so2pluscl = np.zeros((len(dayt))).tolist()
	for lat in range(14,15):
		novolc = np.add(novolc, o3array[int(lat)][0])
        	clonly = np.add(clonly, o3array[int(lat)][1])
        	so2only =np.add(so2only, o3array[int(lat)][2])   #for future use
        	so2cl = np.add(so2cl, o3array[int(lat)][3])    #change to [3] once so2 run completed
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
	so2pluscl = np.add(so2only, clonly)


#	novolc = np.asarray(novolc)
#	clonly = np.asarray(clonly)        
#	so2only = np.asarray(so2only)
#	so2cl = np.asarray(so2cl)
#	novolc = novolc.flatten()
 #       clonly = clonly.flatten()
  #      so2only = so2only.flatten()
   #     so2cl = so2cl.flatten()
        ax.plot(day,novolc, 'ko-', dashes = [8,4,2,4,2,4], lw=2, label = 'No Perturbation')
        ax.plot(day,clonly, 'g-', dashes = [8,4,2,4,2,4], lw = 2, label = cl2 + '$\mbox{\ Tg\ Cl}_\mbox{y}$')
        ax.plot(day,so2only, 'y-', dashes = [4,4,2,4,2,4], lw = 2, label = so2 + '$\mbox{\ Tg\ SO}_\mbox{2}$')
	ax.plot(day, so2pluscl, color = 'darkslategray', ls = '--', lw= 2, label = '$\mbox{SO}_{\mbox{2}}\ \mbox{only}\ \mbox{+}\ \mbox{Cl}_{\mbox{y}}\ \mbox{only}$')
        ax.plot(day,so2cl, color = 'saddlebrown', ls ='-', lw = 2 , label = cl2 + '$\mbox{\ Tg\ Cl}_{\mbox{y}}\ }$'+ '\&  ' + so2 + '$\mbox{\ Tg\ SO}_\mbox{2}$')     
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
        ax.text(day[3*len(day)/5 - 3], ylimz[1]/2, stringy + ', 43N - 52N', fontsize=40, ha="center")  
        ax.tick_params(axis = 'both', which = 'major', labelsize = 17)
        handles, labels = ax.get_legend_handles_labels()
        handles.append(volcanohandle)
        labels.append(volcanolegend)
        ax.legend(handles[::-1], labels[::-1], loc = 4, fancybox = True, fontsize = 25) 
        ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
#	ax.fill_between(day,so2cl, so2pluscl, facecolor = 'whitesmoke', interpolate = True)
#	ax.fill_between(day,clonly, so2only, where = so2only <= clonly, facecolor = 'palegoldenrod', interpolate = True)
#	ax.fill_between(day,clonly, so2only, where = so2only >= clonly, facecolor = 'yellowgreen', interpolate = True)
        plt.yticks(range(int(ylimz[0]),int(ylimz[1]), int(tickah)), [str(x) + "\%" for x in range(int(ylimz[0]),int(ylimz[1]), int(tickah))], fontsize=20)
        plt.xticks(fontsize = 20)
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")  
        fig.tight_layout() 


def twodgraph(var, dayt,yr,idxa = 0, idx=1, year = 1991, num=10, flag=0):
	global Z, X , Y, XX, CS, ax, fig
	X = []
	XX = []
	day = []
        dayyt = np.true_divide(dayt,365)
	dayyyt = dayyt
        dayyt = np.add(dayyt, int(year))
	X,Y = np.meshgrid(dayyt, latitude)
	XX = X.tolist()
        for y in range(len(Y)):
		for x in range(len(X[0])):
              		XX[y][x] = t2dt(X[y][x])
	#XX = dates.date2num(XX)
	XX = np.asarray(XX)
	fig, ax = plt.subplots()
	Z = np.zeros((19, len(dayyyt))).tolist()
	C = np.zeros((19, len(dayyyt))).tolist()
	for x in range(19):
		for y in range(len(dayt)):
			Z[x][y] = var[yr][x][idx][y]
			C[x][y] = var[yr][x][idxa][y]
	Z = np.dot(np.divide(np.subtract(Z,C),C),100)
	Z = np.asarray(Z)
	if abs(Z.min()) > abs(Z.max()):
		levels = np.linspace(Z[3:16].min() + (Z[3:16].min()/10), abs(Z[3:16].min() + (Z[3:16].min()/10)), int(num)) 
	else:
		levels = np.linspace(-(Z[3:16].max() +Z[3:16].max() / 5), Z[3:16].max() + Z[3:16].max()/5, int(num))
	ax.set_xlabel('date (year)', fontsize = 20)
	ax.set_ylabel('latitude (degrees)', fontsize = 20)
	ax.set_title('Ozone Depletion for '+ str(year + 1) +' Pinatubo Scenario', fontsize = 25)
	if flag == 1:
		CS = plt.contour(X,Y,Z, colors = 'k')

	if flag == 0: 
		CS = plt.contourf(XX,Y,Z,levels, cmap = plt.cm.seismic_r)
		cbar = plt.colorbar(CS)
                cbar.ax.set_ylabel('percent difference')
        years = mdates.YearLocator()
        months = mdates.MonthLocator()
        minorLocator = MultipleLocator(2.5)
        ax.xaxis.set_minor_locator(months)
        ax.xaxis.set_major_locator(years)
        ax.yaxis.set_minor_locator(minorLocator)
	fig.set_facecolor('white')
        ax.axvline(x=volctime,color='k',ls='dashed')
        fig.autofmt_xdate()
	ax.set_ylim(-60,60)
	ax.set_xlim(XX[0][13], XX[0][-1])
	ax.get_yaxis().tick_left()
        plt.xticks(fontsize = 20)
	plt.yticks(fontsize = 20)
        stringy = []
	for x in range(-60, 0, 15):
		stringy.append(str(abs(x)) + ' $^{\circ}$S')
	stringy.append(str(0) + ' $^{\circ}$')
	for x in range(15,75,15):
		stringy.append(str(x) + ' $^{\circ}$N')
	plt.yticks(range(-60,75, 15), [stringy[x] for x in range(len(stringy))], fontsize=20)
        ax.scatter(volctime, 15.9, s = 100,color = 'k', marker= '^')			 
 	for y in range(-60, 60, 15):    
              ax.plot(XX[0], [y] *len(XX[0]), "--", lw=0.5, color="black", alpha=0.3)
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
        fig.tight_layout() 

def datamodulator(var, dayt,yr,idxa = 0, idx=1, year = 1991, num=10, flag=0):
	global Z, X , Y, XX, CS, ax, fig, stringy
	X = []
	XX = []
	day = []
        dayyt = np.true_divide(dayt,365)
	dayyyt = dayyt
        dayyt = np.add(dayyt, int(year))
	X,Y = np.meshgrid(dayyt, latitude)
	XX = X.tolist()
        for y in range(len(Y)):
		for x in range(len(X[0])):
              		XX[y][x] = t2dt(X[y][x])
	#XX = dates.date2num(XX)
	XX = np.asarray(XX)
	Z = np.zeros((19, len(dayyyt))).tolist()
	C = np.zeros((19, len(dayyyt))).tolist()
	for x in range(19):
		for y in range(len(dayt)):
			Z[x][y] = var[yr][x][idx][y]
			C[x][y] = var[yr][x][idxa][y]
	Z = np.dot(np.divide(np.subtract(Z,C),C),100)
	Z = np.asarray(Z)
	return [XX, Y, Z]

def fourgraph(var, dayt,idxa=0, idx=1, num=10, flag=0):
	global ax1,ax2,ax3,ax4, fig1, plt, levels, datas, volcinjectlats
	datas = []
	CS = []
	zmax = []
	years = [1990, 2000, 2017, 2070]
	volctimes = []
	for x in range(4):
		datas.append(datamodulator(var, dayt, x, idxa,idx, years[x], num, flag))
		volctimes.append(volclocator(531, years[x]))
		zmax.append([datas[x][2][3:16].min(), datas[x][2][3:16].max()])
	zmax = np.asarray(zmax)	
	if idx < 10:
		volctimes[2] = volclocator(896,2017)
	volclathigh = latitude_edges[12] - 15.9
	volclatlow =  15.9 - latitude_edges[10]
	
	if abs(zmax.min()) > abs(zmax.max()):
		levels = np.linspace(int(zmax.min() + (zmax.min()/10)), abs(int(zmax.min() + (zmax.min()/10))), int(num)) 
	else:
		levels = np.linspace(int(-(zmax.max() +zmax.max() / 10)),int( zmax.max() + zmax.max()/10), int(num))
	plt.figure
	ax1 = plt.subplot(221)
	ax2 = plt.subplot(222)
	ax3 = plt.subplot(223)
	ax4 = plt.subplot(224)
	fig = plt.gcf()
	fig.set_facecolor('white')
	plt.subplot(2,2,1)
	
	CS1 =plt.contourf(datas[0][0],datas[0][1],datas[0][2],levels, cmap = plt.cm.seismic_r)
	plt.subplot(2,2,2)
	
	CS2 = plt.contourf(datas[1][0],datas[1][1],datas[1][2],levels, cmap = plt.cm.seismic_r)
	plt.subplot(2,2,3)
	CS3 =plt.contourf(datas[2][0],datas[2][1],datas[2][2],levels, cmap = plt.cm.seismic_r)
	plt.subplot(2,2,4)
	CS4 = plt.contourf(datas[3][0],datas[3][1],datas[3][2],levels, cmap = plt.cm.seismic_r)
        stringy = []
	for x in range(-60, 0, 15):
		stringy.append(str(abs(x)) + '$^{\circ}$S')
	stringy.append(str(0) + '$^{\circ}$   ')
	for x in range(15,75,15):
		stringy.append(str(x) + '$^{\circ}$N')
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	plt.subplot(2,2,1)
#	ax1.xaxis.set_minor_locator(months)
#	ax1.xaxis.set_major_locator(years)
#	ax1.yaxis.set_minor_locator(minorLocator)
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_ylim(-60,60)
	ax1.set_xlim(datas[0][0][0][13], datas[0][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax1.plot(datas[0][0][0], [z] *len(datas[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
#	ax1.errorbar(volctimes[0],15.9,yerr=[volcinjectlats[0], volcinjectlats[1]], ecolor = 'k', capthick =1)	 
	plt.subplot(2,2,2)
#	ax2.xaxis.set_minor_locator(months)
#	ax2.xaxis.set_major_locator(years)
#	ax2.yaxis.set_minor_locator(minorLocator)
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_ylim(-60,60)
	ax2.set_xlim(datas[1][0][0][13], datas[1][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax2.plot(datas[1][0][0], [z] *len(datas[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
        ax2.scatter(volctimes[1], 15.9, s = 100,color = 'k', marker= '^')		
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.tick_params(axis='y', pad = 13)
	plt.subplot(2,2,3)
#	ax3.xaxis.set_minor_locator(months)
#	ax3.xaxis.set_major_locator(years)
#	ax3.yaxis.set_minor_locator(minorLocator)
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_ylim(-60,60)
	ax3.set_xlim(datas[2][0][0][13], datas[2][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax3.plot(datas[2][0][0], [z] *len(datas[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax3.scatter(volctimes[2], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.subplot(2,2,4)
#	ax4.xaxis.set_minor_locator(months)
#	ax4.xaxis.set_major_locator(years)
#	ax4.yaxis.set_minor_locator(minorLocator)
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_ylim(-60,60)
	ax4.set_xlim(datas[3][0][0][13], datas[3][0][0][-1])
        ax4.scatter(volctimes[3], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax4.plot(datas[3][0][0], [z] *len(datas[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
#	ax.set_xticklabels(labels,rotation=30, ha='right')
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	ax4.tick_params(axis='y', pad = 13)
	cbar_ax = fig.add_axes([0.03, 0.15, 0.03, 0.7])
	fmt = '%1.0f'
	cbar = fig.colorbar(CS1, cax = cbar_ax, format =fmt)
	cbar.set_label('Percent Change', fontsize = 15, labelpad = -65)
	
def sixgraph(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global ax1,ax2,ax3,ax4, ax5, ax6, fig,cbar, plt, levels, datas, volcinjectlats

	datas = []
	CS = []
	zmax = []
	years = [1950, 1990, 2000, 2017, 2070, 2100]
	volctimes = []

	for x in range(6):
		datas.append(datamodulator(var, dayt, x, idxa,idx, years[x], num, flag))
		volctimes.append(volclocator(531, years[x]))
		zmax.append([datas[x][2][3:16].min(), datas[x][2][3:16].max()])

	zmax = np.asarray(zmax)	
	volclathigh = latitude_edges[12] - 15.9
	volclatlow =  15.9 - latitude_edges[10]
	if flagg ==0:
		if abs(zmax.min()) > abs(zmax.max()):
			levels = np.linspace(int(zmax.min() + (zmax.min()/10)), abs(int(zmax.min() + (zmax.min()/10))), int(num)) 
		else:
			levels = np.linspace(int(-(zmax.max() +zmax.max() / 10)),int( zmax.max() + zmax.max()/10), int(num))
	else:
		levels = np.linspace(int(zmax.min()), 0, int(num))
	plt.figure
	ax1 = plt.subplot(321)
	ax2 = plt.subplot(322)
	ax3 = plt.subplot(323)
	ax4 = plt.subplot(324)
	ax5 = plt.subplot(325)
	ax6 = plt.subplot(326)
	fig = plt.gcf()
	fig.set_facecolor('white')
	plt.subplot(3,2,1)
	
	CS1 =plt.contourf(datas[0][0],datas[0][1],datas[0][2],levels, cmap = cma)
	plt.subplot(3,2,2)
	CS2 = plt.contourf(datas[1][0],datas[1][1],datas[1][2],levels, cmap = cma)
	plt.subplot(3,2,3)
	CS3 =plt.contourf(datas[2][0],datas[2][1],datas[2][2],levels, cmap = cma)
	plt.subplot(3,2,4)
	CS4 = plt.contourf(datas[3][0],datas[3][1],datas[3][2],levels, cmap = cma)
	plt.subplot(3,2,5)
	CS5 = plt.contourf(datas[4][0],datas[4][1],datas[4][2],levels, cmap = cma)
	plt.subplot(3,2,6)
	CS6 = plt.contourf(datas[5][0],datas[5][1],datas[5][2],levels, cmap = cma)
        stringy = []
	
	for x in range(-60, 0, 15):
		stringy.append(str(abs(x)) + '$^{\circ}$S')
	stringy.append(str(0) + '$^{\circ}$   ')
	for x in range(15,75,15):
		stringy.append(str(x) + '$^{\circ}$N')
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	
	plt.subplot(3,2,1)
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_ylim(-60,60)
	ax1.set_xlim(datas[0][0][0][13], datas[0][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax1.plot(datas[0][0][0], [z] *len(datas[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(3,2,2)
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_ylim(-60,60)
	ax2.set_xlim(datas[1][0][0][13], datas[1][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax2.plot(datas[1][0][0], [z] *len(datas[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
        ax2.scatter(volctimes[1], 15.9, s = 100,color = 'k', marker= '^')		
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.tick_params(axis='y', pad = 13)
	
	plt.subplot(3,2,3)
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_ylim(-60,60)
	ax3.set_xlim(datas[2][0][0][13], datas[2][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax3.plot(datas[2][0][0], [z] *len(datas[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax3.scatter(volctimes[2], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(3,2,4)
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_ylim(-60,60)
	ax4.set_xlim(datas[3][0][0][13], datas[3][0][0][-1])
        ax4.scatter(volctimes[3], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax4.plot(datas[3][0][0], [z] *len(datas[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	ax4.tick_params(axis='y', pad = 13)
	
	plt.subplot(3,2,5)
	ax5.axvline(x=volctimes[4],color='k',ls='dashed')
	ax5.set_ylim(-60,60)
	ax5.set_xlim(datas[4][0][0][13], datas[4][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax5.plot(datas[4][0][0], [z] *len(datas[4][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax5.scatter(volctimes[4], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[4],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(3,2,6)
	ax6.axvline(x=volctimes[5],color='k',ls='dashed')
	ax6.set_ylim(-60,60)
	ax6.set_xlim(datas[5][0][0][13], datas[5][0][0][-1])
        ax6.scatter(volctimes[5], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[5],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax6.plot(datas[5][0][0], [z] *len(datas[5][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	ax6.tick_params(axis='y', pad = 13)

	cbar_ax = fig.add_axes([0.03, 0.15, 0.03, 0.7])
	fmt = '%1.0f'
	tix =  np.linspace(levels.min(), levels.max(), 9, endpoint=True)
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt)
	cbar.set_label('Percent Change', fontsize = 15, labelpad = -65)
	
def eightgraph(dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global ax1,ax2,ax3,ax4, ax5, ax6,ax7, ax8, fig, plt, levels, datas, volcinjectlats, strongy, cbar, zmax, CS1, tix, cbar_ax
	var = [b26, b45, b60, b85]
	datas = []
	CS = []
	zmax = []
	years = [2070, 2100]
	volctimes = []
	for y in range(4):
		for x in range(2):
			datas.append(datamodulator(var[y], dayt, x+4, idxa,idx, years[x], num, flag))
			volctimes.append(volclocator(531, years[x]))
			zmax.append([datas[2*y+x][2][2:16].min(), datas[2*y+x][2][2:16].max()])
	zmax = np.asarray(zmax)	
	volclathigh = latitude_edges[12] - 15.9
	volclatlow =  15.9 - latitude_edges[10]
#	if flagg ==0:
#		if abs(zmax.min()) > abs(zmax.max()):
#			levels = np.linspace(int(math.floor(zmax.min())), abs(int(math.floor(zmax.min()))), int(num)) 
#		else:
#			levels = np.linspace(-int(math.ceil(zmax.max())),int(math.ceil(zmax.max())), int(num))
#	else:
#		levels = np.linspace(int(zmax.min()), 0, int(num))
	plt.figure
	ax1 = plt.subplot(421)
	ax2 = plt.subplot(422)
	ax3 = plt.subplot(423)
	ax4 = plt.subplot(424)
	ax5 = plt.subplot(425)
	ax6 = plt.subplot(426)
	ax7 = plt.subplot(427)
	ax8 = plt.subplot(428)
	fig = plt.gcf()
	fig.set_facecolor('white')
	
	plt.subplot(4,2,1)
	CS1 =plt.contourf(datas[0][0],datas[0][1],datas[0][2],levels, cmap = cma)
	plt.subplot(4,2,2)
	CS2 = plt.contourf(datas[1][0],datas[1][1],datas[1][2],levels, cmap = cma)
	plt.subplot(4,2,3)
	CS3 =plt.contourf(datas[2][0],datas[2][1],datas[2][2],levels, cmap = cma)
	plt.subplot(4,2,4)
	CS4 = plt.contourf(datas[3][0],datas[3][1],datas[3][2],levels, cmap = cma)
	plt.subplot(4,2,5)
	CS5 = plt.contourf(datas[4][0],datas[4][1],datas[4][2],levels, cmap = cma)
	plt.subplot(4,2,6)
	CS6 = plt.contourf(datas[5][0],datas[5][1],datas[5][2],levels, cmap = cma)
	plt.subplot(4,2,7)
	CS7 = plt.contourf(datas[6][0],datas[6][1],datas[6][2],levels, cmap = cma)
	plt.subplot(4,2,8)
	CS8 = plt.contourf(datas[7][0],datas[7][1],datas[7][2],levels, cmap = cma)
       
	stringy = []
	strongy = [str('RCP2.6'), str('RCP4.5'), str('RCP6.0'), str('RCP8.5')]
	for x in range(-60, 0, 15):
		stringy.append(str(abs(x)) + '$^{\circ}$S')
	stringy.append(str(0) + '$^{\circ}$   ')
	for x in range(15,75,15):
		stringy.append(str(x) + '$^{\circ}$N')
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	
	plt.subplot(4,2,1)
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_ylim(-60,60)
	ax1.set_xlim(datas[0][0][0][13], datas[0][0][0][-1])
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax1.plot(datas[0][0][0], [z] *len(datas[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=90)
        ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax1.set_ylabel(strongy[0], fontsize = 25)
	
	plt.subplot(4,2,2)
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_ylim(-60,60)
	ax2.set_xlim(datas[1][0][0][13], datas[1][0][0][-1])
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax2.plot(datas[1][0][0], [z] *len(datas[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=90)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
        ax2.scatter(volctimes[1], 15.9, s = 100,color = 'k', marker= '^')		
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.tick_params(axis='y', pad = 13)
	
	plt.subplot(4,2,3)
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_ylim(-60,60)
	ax3.set_xlim(datas[2][0][0][13], datas[2][0][0][-1])
	#plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="off", top="on", labelbottom="off", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax3.plot(datas[2][0][0], [z] *len(datas[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	#plt.xticks(rotation=30)
        ax3.scatter(volctimes[2], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax3.set_ylabel(strongy[1], fontsize = 25)

	plt.subplot(4,2,4)
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_ylim(-60,60)
	ax4.set_xlim(datas[3][0][0][13], datas[3][0][0][-1])
        ax4.scatter(volctimes[3], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	#plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="off", top="on", labelbottom="off", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax4.plot(datas[3][0][0], [z] *len(datas[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	#plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	ax4.tick_params(axis='y', pad = 13)
	
	plt.subplot(4,2,5)
	ax5.axvline(x=volctimes[4],color='k',ls='dashed')
	ax5.set_ylim(-60,60)
	ax5.set_xlim(datas[4][0][0][13], datas[4][0][0][-1])
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax5.plot(datas[4][0][0], [z] *len(datas[4][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=90)
        ax5.scatter(volctimes[4], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[4],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax5.set_ylabel(strongy[2], fontsize = 25)
	
	plt.subplot(4,2,6)
	ax6.axvline(x=volctimes[5],color='k',ls='dashed')
	ax6.set_ylim(-60,60)
	ax6.set_xlim(datas[5][0][0][13], datas[5][0][0][-1])
        ax6.scatter(volctimes[5], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[5],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.xticks(fontsize = 12)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax6.plot(datas[5][0][0], [z] *len(datas[5][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=90)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	ax6.tick_params(axis='y', pad = 13)

	plt.subplot(4,2,7)
	ax7.axvline(x=volctimes[6],color='k',ls='dashed')
	ax7.set_ylim(-60,60)
	ax7.set_xlim(datas[6][0][0][13], datas[6][0][0][-1])
	#plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="off", top="on", labelbottom="off", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax7.plot(datas[6][0][0], [z] *len(datas[6][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	#plt.xticks(rotation=30)
        ax7.scatter(volctimes[6], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[6],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax7.set_ylabel(strongy[3], fontsize = 25)	

	plt.subplot(4,2,8)
	ax8.axvline(x=volctimes[5],color='k',ls='dashed')
	ax8.set_ylim(-60,60)
	ax8.set_xlim(datas[7][0][0][13], datas[7][0][0][-1])
        ax8.scatter(volctimes[7], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[7],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	#plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="off", top="on", labelbottom="off", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax8.plot(datas[7][0][0], [z] *len(datas[7][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	#plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	ax8.tick_params(axis='y', pad = 13)

	cbar_ax = fig.add_axes([0.03, 0.15, 0.03, 0.7])
	fmt = '%1.0f'
	#tix =  np.linspace(levels.min(), levels.max(), 9, endpoint=True)
	tix = [-15,-9,-6,-3,0]
	#tix = [-65,-45,-25,-5,0]
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt)
	cbar.set_label('Percent Change', fontsize = 15, labelpad = -65)
	
def fourfourgraph(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global zmax,ax1,ax2,ax3,ax4, fig,cbar, plt, levels, datas, volcinjectlats

	datas = []
	CS = []
	zmax = []
	years = [1950, 1990, 2000, 2017, 2070, 2100]
	volctimes = []

	for x in range(6):
		datas.append(datamodulator(var, dayt, x, idxa,idx, years[x], num, flag))
		volctimes.append(volclocator(531, years[x]))
		zmax.append([datas[x][2][3:16].min(), datas[x][2][3:16].max()])

	zmax = np.asarray(zmax)	
	volclathigh = latitude_edges[12] - 15.9
	volclatlow =  15.9 - latitude_edges[10]
	#if flagg ==0:
	#	if abs(zmax.min()) > abs(zmax.max()):
	#		levels = np.linspace(int(zmax.min() + (zmax.min()/10)), abs(int(zmax.min() + (zmax.min()/10))), int(num)) 
	#	else:
	#		levels = np.linspace(int(-(zmax.max() +zmax.max() / 10)),int( zmax.max() + zmax.max()/10), int(num))
	#else:
	#	levels = np.linspace(int(zmax.min()), 0, int(num))
	plt.figure
	ax1 = plt.subplot(221)
	ax2 = plt.subplot(222)
	ax3 = plt.subplot(223)
	ax4 = plt.subplot(224)
	fig = plt.gcf()
	fig.set_facecolor('white')
	plt.subplot(2,2,1)
	
	CS1 =plt.contourf(datas[0][0],datas[0][1],datas[0][2],levels, cmap = cma)
	plt.subplot(2,2,2)
	CS2 = plt.contourf(datas[1][0],datas[1][1],datas[1][2],levels, cmap = cma)
	plt.subplot(2,2,3)
	CS3 =plt.contourf(datas[2][0],datas[2][1],datas[2][2],levels, cmap = cma)
	plt.subplot(2,2,4)
	CS4 = plt.contourf(datas[3][0],datas[3][1],datas[3][2],levels, cmap = cma)
        stringy = []
	
	for x in range(-60, 0, 15):
		stringy.append(str(abs(x)) + '$^{\circ}$S')
	stringy.append(str(0) + '$^{\circ}$   ')
	for x in range(15,75,15):
		stringy.append(str(x) + '$^{\circ}$N')
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	
	plt.subplot(2,2,1)
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_ylim(-60,60)
	ax1.set_xlim(datas[0][0][0][13], datas[0][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax1.plot(datas[0][0][0], [z] *len(datas[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(2,2,2)
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_ylim(-60,60)
	ax2.set_xlim(datas[1][0][0][13], datas[1][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax2.plot(datas[1][0][0], [z] *len(datas[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
        ax2.scatter(volctimes[1], 15.9, s = 100,color = 'k', marker= '^')		
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.tick_params(axis='y', pad = 13)
	
	plt.subplot(2,2,3)
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_ylim(-60,60)
	ax3.set_xlim(datas[2][0][0][13], datas[2][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax3.plot(datas[2][0][0], [z] *len(datas[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax3.scatter(volctimes[2], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(2,2,4)
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_ylim(-60,60)
	ax4.set_xlim(datas[3][0][0][13], datas[3][0][0][-1])
        ax4.scatter(volctimes[3], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax4.plot(datas[3][0][0], [z] *len(datas[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	ax4.tick_params(axis='y', pad = 13)
	
	cbar_ax = fig.add_axes([0.03, 0.15, 0.03, 0.7])
	fmt = '%1.0f'
	#tix =  np.linspace(levels.min(), levels.max(), 9, endpoint=True)
	tix = [-15,-12, -9, -6, -3, 0]
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt)
	cbar.set_label('Percent Change', fontsize = 15, labelpad = -65)

def fourtwograph(var, dayt,idxa=0,idxb=1, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global zmax,ax1,ax2,ax3,ax4, fig,cbar, plt, levels, datas, volcinjectlats

	datas = []
	databs = []
	CS = []
	zmax = []
	years = [1950, 1990, 2000, 2017, 2070, 2100]
	volctimes = []

	for x in range(6):
		datas.append(datamodulator(var, dayt, x, idxa,idx, years[x], num, flag))
		volctimes.append(volclocator(531, years[x]))
		zmax.append([datas[x][2][3:16].min(), datas[x][2][3:16].max()])

	for x in range(6):
		databs.append(datamodulator(var, dayt, x, idxa,idxb, years[x], num, flag))
		volctimes.append(volclocator(531, years[x]))
		zmax.append([databs[x][2][3:16].min(), databs[x][2][3:16].max()])
	zmax = np.asarray(zmax)	
	volclathigh = latitude_edges[12] - 15.9
	volclatlow =  15.9 - latitude_edges[10]
	#if flagg ==0:
	#	if abs(zmax.min()) > abs(zmax.max()):
	#		levels = np.linspace(int(zmax.min() + (zmax.min()/10)), abs(int(zmax.min() + (zmax.min()/10))), int(num)) 
	#	else:
	#		levels = np.linspace(int(-(zmax.max() +zmax.max() / 10)),int( zmax.max() + zmax.max()/10), int(num))
	#else:
	#	levels = np.linspace(int(zmax.min()), 0, int(num))
	plt.figure
	ax1 = plt.subplot(221)
	ax2 = plt.subplot(222)
	ax3 = plt.subplot(223)
	ax4 = plt.subplot(224)
	fig = plt.gcf()
	fig.set_facecolor('white')
	plt.subplot(2,2,1)
	
	CS1 =plt.contourf(datas[1][0],datas[1][1],datas[1][2],levels, cmap = cma)
	plt.subplot(2,2,2)
	CS2 = plt.contourf(datas[3][0],datas[3][1],datas[3][2],levels, cmap = cma)
	plt.subplot(2,2,3)
	CS3 =plt.contourf(databs[1][0],databs[1][1],databs[1][2],levels, cmap = cma)
	plt.subplot(2,2,4)
	CS4 = plt.contourf(databs[3][0],databs[3][1],databs[3][2],levels, cmap = cma)
        stringy = []
	
	for x in range(-60, 0, 15):
		stringy.append(str(abs(x)) + '$^{\circ}$S')
	stringy.append(str(0) + '$^{\circ}$   ')
	for x in range(15,75,15):
		stringy.append(str(x) + '$^{\circ}$N')
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	
	plt.subplot(2,2,1)
	ax1.axvline(x=volctimes[1],color='k',ls='dashed')
	ax1.set_ylim(-60,60)
	ax1.set_xlim(datas[1][0][0][13], datas[1][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax1.plot(datas[1][0][0], [z] *len(datas[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax1.scatter(volctimes[1], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(2,2,2)
	ax2.axvline(x=volctimes[3],color='k',ls='dashed')
	ax2.set_ylim(-60,60)
	ax2.set_xlim(datas[3][0][0][13], datas[3][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax2.plot(datas[3][0][0], [z] *len(datas[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
        ax2.scatter(volctimes[3], 15.9, s = 100,color = 'k', marker= '^')		
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.tick_params(axis='y', pad = 13)
	
	plt.subplot(2,2,3)
	ax3.axvline(x=volctimes[1],color='k',ls='dashed')
	ax3.set_ylim(-60,60)
	ax3.set_xlim(databs[1][0][0][13], databs[1][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax3.plot(databs[1][0][0], [z] *len(databs[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax3.scatter(volctimes[1], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(2,2,4)
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_ylim(-60,60)
	ax4.set_xlim(databs[3][0][0][13], databs[3][0][0][-1])
        ax4.scatter(volctimes[3], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax4.plot(databs[3][0][0], [z] *len(databs[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	ax4.tick_params(axis='y', pad = 13)
	
	cbar_ax = fig.add_axes([0.03, 0.15, 0.03, 0.7])
	fmt = '%1.0f'
	#tix =  np.linspace(levels.min(), levels.max(), 9, endpoint=True)
	tix = [-40,-30, -20, -10, 0]
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt)
	cbar.set_label('Percent Change', fontsize = 15, labelpad = -65)

def globeplotyear(o3arrray,yr, dayt,idxa = 0, idxb = 1, year=1990,  ylimz = (-50,5), tickah = 5, flag = 1):
	global fig, ax
        if flag == 0:
             plt.ioff()
        else: 
             plt.ion()
	o3array = np.zeros((19,12,len(dayt)))
	for x in range(0,18):
		for y in range(len(dayt)):
			o3array[x][0][y] = o3arrray[0][x][idxa][y]
			o3array[x][1][y] = o3arrray[1][x][idxa][y]
			o3array[x][2][y] = o3arrray[2][x][idxa][y]
			o3array[x][3][y] = o3arrray[3][x][idxa][y]
			o3array[x][4][y] = o3arrray[4][x][idxa][y]
			o3array[x][5][y] = o3arrray[5][x][idxa][y]
			o3array[x][6][y] = o3arrray[0][x][idxb][y]
			o3array[x][7][y] = o3arrray[1][x][idxb][y]
			o3array[x][8][y] = o3arrray[2][x][idxb][y]
			o3array[x][9][y] = o3arrray[3][x][idxb][y]
			o3array[x][10][y] = o3arrray[4][x][idxb][y]
			o3array[x][11][y] = o3arrray[5][x][idxb][y]
    	fig, ax = plt.subplots(figsize = (10,7.5))
 	fig.set_facecolor('white')
	ax.set_ylabel('Change in Column Ozone vs. No Volcano', fontsize = 35)
	day = []
        dayyt = np.true_divide(dayt,365)
        dayyt = np.add(dayyt, int(year))
	delta = DT.timedelta(days = 364)
        for x in range(len(dayt)):
              day.append(t2dt(dayyt[x]) - delta)
 	for y in range(int(ylimz[0]), int(ylimz[1]), int(tickah)):    
              ax.plot(day, [y] *len(day), "--", lw=0.5, color="black", alpha=0.3)
        novolca = np.zeros(( len(dayt))).tolist()
        novolcb = np.zeros(( len(dayt))).tolist()
        novolcc = np.zeros(( len(dayt))).tolist()
        novolcd = np.zeros(( len(dayt))).tolist()
        novolce = np.zeros(( len(dayt))).tolist()
        novolcf = np.zeros(( len(dayt))).tolist()
        volca = np.zeros((len(dayt))).tolist()
        volcb = np.zeros(( len(dayt))).tolist()
        volcc = np.zeros((len(dayt))).tolist()    
        volcd = np.zeros((len(dayt))).tolist()
        volce = np.zeros((len(dayt))).tolist()
        volcf = np.zeros((len(dayt))).tolist()
	
	for lat in range(3,15):
		novolca = np.add(novolca, o3array[int(lat)][0])
		novolcb = np.add(novolcb, o3array[int(lat)][1])
		novolcc = np.add(novolcc, o3array[int(lat)][2])
		novolcd = np.add(novolcd, o3array[int(lat)][3])
		novolce = np.add(novolce, o3array[int(lat)][4])
		novolcf = np.add(novolcf, o3array[int(lat)][5])
        	volca = np.add(volca, o3array[int(lat)][6])
        	volcb = np.add(volcb, o3array[int(lat)][7])
        	volcc =np.add(volcc, o3array[int(lat)][8])   #for future use
        	volcd = np.add(volcd, o3array[int(lat)][9])
		volce = np.add(volce, o3array[int(lat)][10])
		volcf = np.add(volcf, o3array[int(lat)][11])    #change to [3] once so2 run completed
 #       for x in range(len(dayt)):
#		idx = int(day[x].strftime('%m')[:]) -1
#		novolc[x] = np.dot(np.true_divide(np.subtract(novolc[x], baseline[idx][lat]), baseline[idx][lat]),100)
#		clonly[x] = np.dot(np.true_divide(np.subtract(clonly[x], baseline[idx][lat]), baseline[idx][lat]),100)
#		so2only[x] = np.dot(np.true_divide(np.subtract(so2only[x], baseline[idx][lat]), baseline[idx][lat]),100)
#		so2cl[x] = np.dot(np.true_divide(np.subtract(so2cl[x], baseline[idx][lat]), baseline[idx][lat]),100)

#	novolc = np.dot(np.true(divide(np.subtract(novolc, baseline), baseline), 100)
	volca = np.dot(np.true_divide(np.subtract(volca, novolca),novolca),100)
        volcb = np.dot(np.true_divide(np.subtract(volcb, novolcb),novolcb),100)
        volcc = np.dot(np.true_divide(np.subtract(volcc, novolcc), novolcc), 100)
	volcd = np.dot(np.true_divide(np.subtract(volcd, novolcd), novolcd),100)
	volce = np.dot(np.true_divide(np.subtract(volce, novolce), novolce),100)
	volcf = np.dot(np.true_divide(np.subtract(volcf, novolcf), novolcf),100)


#	novolc = np.asarray(novolc)
#	clonly = np.asarray(clonly)        
#	so2only = np.asarray(so2only)
#	so2cl = np.asarray(so2cl)
#	novolc = novolc.flatten()
 #       clonly = clonly.flatten()
  #      so2only = so2only.flatten()
   #     so2cl = so2cl.flatten()
#        ax.plot(day,novolc, 'ko-', dashes = [8,4,2,4,2,4], lw=2, label = 'No Perturbation')
       # ax.plot(day,clonly, 'g-', dashes = [8,4,2,4,2,4], lw = 2, label = cl2 + '$\mbox{\ Tg\ Cl}_\mbox{y}$')
        #	clonly = np.add(clonly, o3array[int(lat)][1])
        ax.plot(day,volcf, color = 'saddlebrown', ls ='-', lw = 2 , label = '4 PPT VSL / 4 PPT Bry ')
        ax.plot(day,volce, color = 'mediumorchid', ls ='-', lw = 2 , label = '4 PPT VSL / 2 PPT Bry')
        ax.plot(day,volcd, color = 'darkgoldenrod', ls ='-', lw = 2 , label = '4 PPT VSL / 0 PPT Bry')
	ax.plot(day, volcc, color = 'forestgreen', ls = '-', lw= 2, label = '0 PPT VSL / 4 PPT Bry')
        ax.plot(day,volcb, 'dodgerblue', ls='-', lw = 2, label ='0 PPT VSL / 2 PPT Bry')
        ax.plot(day,volca, 'firebrick', ls = '-', lw = 2, label = '0 PPT VSL / 0 PPT Bry')
       # ax.plot(day,so2only, 'y-', dashes = [4,4,2,4,2,4], lw = 2, label = so2 + '$\mbox{\ Tg\ SO}_\mbox{2}$')
	#ax.plot(day, so2pluscl, color = 'darkslategray', ls = '--', lw= 2, label = '$\mbox{SO}_{\mbox{2}}\ \mbox{only}\ \mbox{+}\ \mbox{Cl}_{\mbox{y}}\ \mbox{only}$')
        #ax.plot(day,so2cl, color = 'saddlebrown', ls ='-', lw = 2 , label = cl2 + '$\mbox{\ Tg\ Cl}_{\mbox{y}}\ $'+ ' + ' + so2 + '$\mbox{\ Tg\ SO}_\mbox{2}$')     
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
    #    ax.text(day[3*len(day)/5 - 3], ylimz[1]/2, stringy + ', 60S - 60N', fontsize=40, ha="center")  
        ax.tick_params(axis = 'both', which = 'major', labelsize = 35)
        handles, labels = ax.get_legend_handles_labels()
        handles.append(volcanohandle)
        labels.append(volcanolegend)
        ax.legend(handles[::-1], labels[::-1], loc = 4, fancybox = True, fontsize = 25) 
        ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
	ax.spines['left'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
#	ax.fill_between(day,so2cl, so2pluscl, facecolor = 'whitesmoke', interpolate = True)
#	ax.fill_between(day,clonly, so2only, where = so2only <= clonly, facecolor = 'palegoldenrod', interpolate = True)
#	ax.fill_between(day,clonly, so2only, where = so2only >= clonly, facecolor = 'yellowgreen', interpolate = True)
        plt.yticks(range(int(ylimz[0]),int(ylimz[1]), int(tickah)), [str(x) + "\%" for x in range(int(ylimz[0]),int(ylimz[1]), int(tickah))], fontsize=35)
        plt.xticks(fontsize = 35)
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")  
        fig.tight_layout()

def salagraph(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global ax1,ax2,ax3,ax4, ax5, ax6, fig,cbar, plt, levels, datas, volcinjectlats

	datas = []
	CS = []
	zmax = []
	years = [2100, 2100, 2100, 2100, 2100, 2100]
	volctimes = []

	for x in range(6):
		datas.append(datamodulator(var, dayt, x, idxa,idx, years[x], num, flag))
		volctimes.append(volclocator(531, years[x]))
		zmax.append([datas[x][2][3:16].min(), datas[x][2][3:16].max()])

	zmax = np.asarray(zmax)	
	volclathigh = latitude_edges[12] - 15.9
	volclatlow =  15.9 - latitude_edges[10]
	if flagg ==0:
		if abs(zmax.min()) > abs(zmax.max()):
			levels = np.linspace(int(zmax.min() + (zmax.min()/10)), abs(int(zmax.min() + (zmax.min()/10))), int(num)) 
		else:
			levels = np.linspace(int(-(zmax.max() +zmax.max() / 10)),int( zmax.max() + zmax.max()/10), int(num))
	else:
		levels = np.linspace(int(zmax.min()), 0, int(num))
	plt.figure
	ax1 = plt.subplot(321)
	ax2 = plt.subplot(322)
	ax3 = plt.subplot(323)
	ax4 = plt.subplot(324)
	ax5 = plt.subplot(325)
	ax6 = plt.subplot(326)
	fig = plt.gcf()
	fig.set_facecolor('white')
	plt.subplot(3,2,1)
	
	CS1 =plt.contourf(datas[0][0],datas[0][1],datas[0][2],levels, cmap = cma)
	plt.subplot(3,2,2)
	CS2 = plt.contourf(datas[3][0],datas[3][1],datas[3][2],levels, cmap = cma)
	plt.subplot(3,2,3)
	CS3 =plt.contourf(datas[1][0],datas[1][1],datas[1][2],levels, cmap = cma)
	plt.subplot(3,2,4)
	CS4 = plt.contourf(datas[4][0],datas[4][1],datas[4][2],levels, cmap = cma)
	plt.subplot(3,2,5)
	CS5 = plt.contourf(datas[2][0],datas[2][1],datas[2][2],levels, cmap = cma)
	plt.subplot(3,2,6)
	CS6 = plt.contourf(datas[5][0],datas[5][1],datas[5][2],levels, cmap = cma)
        stringy = []
	
	for x in range(-60, 0, 15):
		stringy.append(str(abs(x)) + '$^{\circ}$S')
	stringy.append(str(0) + '$^{\circ}$   ')
	for x in range(15,75,15):
		stringy.append(str(x) + '$^{\circ}$N')
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	
	plt.subplot(3,2,1)
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_ylim(-60,60)
	ax1.set_xlim(datas[0][0][0][13], datas[0][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax1.plot(datas[0][0][0], [z] *len(datas[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(3,2,2)
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_ylim(-60,60)
	ax2.set_xlim(datas[1][0][0][13], datas[1][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax2.plot(datas[1][0][0], [z] *len(datas[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
        ax2.scatter(volctimes[1], 15.9, s = 100,color = 'k', marker= '^')		
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.tick_params(axis='y', pad = 13)
	
	plt.subplot(3,2,3)
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_ylim(-60,60)
	ax3.set_xlim(datas[2][0][0][13], datas[2][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax3.plot(datas[2][0][0], [z] *len(datas[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax3.scatter(volctimes[2], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(3,2,4)
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_ylim(-60,60)
	ax4.set_xlim(datas[3][0][0][13], datas[3][0][0][-1])
        ax4.scatter(volctimes[3], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax4.plot(datas[3][0][0], [z] *len(datas[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	ax4.tick_params(axis='y', pad = 13)
	
	plt.subplot(3,2,5)
	ax5.axvline(x=volctimes[4],color='k',ls='dashed')
	ax5.set_ylim(-60,60)
	ax5.set_xlim(datas[4][0][0][13], datas[4][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax5.plot(datas[4][0][0], [z] *len(datas[4][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax5.scatter(volctimes[4], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[4],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(3,2,6)
	ax6.axvline(x=volctimes[5],color='k',ls='dashed')
	ax6.set_ylim(-60,60)
	ax6.set_xlim(datas[5][0][0][13], datas[5][0][0][-1])
        ax6.scatter(volctimes[5], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[5],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax6.plot(datas[5][0][0], [z] *len(datas[5][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	ax6.tick_params(axis='y', pad = 13)

	cbar_ax = fig.add_axes([0.03, 0.15, 0.03, 0.7])
	fmt = '%1.0f'
	tix =  np.linspace(levels.min(), levels.max(), 9, endpoint=True)
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt)
	cbar.set_label('Percent Change', fontsize = 15, labelpad = -65)

def salaavg(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global ax1,ax2,ax3,ax4, ax5, ax6, fig,cbar, plt, levels, datas, volcinjectlats

	datas = []
	CS = []
	zmax = []
	years = [2100, 2100, 2100, 2100, 2100, 2100]
	volctimes = []
	dataflat = []

	for x in range(6):
		datas.append(datamodulator(var, dayt, x, idxa,idx, years[x], num, flag))
		zmax.append([datas[x][2][3:16].min(), datas[x][2][3:16].max()])
		volctimes.append(volclocator(531, years[x]))


	zmax = np.asarray(zmax)	
	volclathigh = latitude_edges[12] - 15.9
	volclatlow =  15.9 - latitude_edges[10]
	if flagg ==0:
		if abs(zmax.min()) > abs(zmax.max()):
			levels = np.linspace(int(zmax.min() + (zmax.min()/10)), abs(int(zmax.min() + (zmax.min()/10))), int(num)) 
		else:
			levels = np.linspace(int(-(zmax.max() +zmax.max() / 10)),int( zmax.max() + zmax.max()/10), int(num))
	else:
		levels = np.linspace(int(zmax.min()), 0, int(num))
	plt.figure
	ax1 = plt.subplot(321)
	ax2 = plt.subplot(322)
	ax3 = plt.subplot(323)
	ax4 = plt.subplot(324)
	ax5 = plt.subplot(325)
	ax6 = plt.subplot(326)
	fig = plt.gcf()
	fig.set_facecolor('white')
	plt.subplot(3,2,1)
	
	CS1 =plt.contourf(datas[0][0],datas[0][1],datas[0][2],levels, cmap = cma)
	plt.subplot(3,2,2)
	CS2 = plt.contourf(datas[3][0],datas[3][1],datas[3][2],levels, cmap = cma)
	plt.subplot(3,2,3)
	CS3 =plt.contourf(datas[1][0],datas[1][1],datas[1][2],levels, cmap = cma)
	plt.subplot(3,2,4)
	CS4 = plt.contourf(datas[4][0],datas[4][1],datas[4][2],levels, cmap = cma)
	plt.subplot(3,2,5)
	CS5 = plt.contourf(datas[2][0],datas[2][1],datas[2][2],levels, cmap = cma)
	plt.subplot(3,2,6)
	CS6 = plt.contourf(datas[5][0],datas[5][1],datas[5][2],levels, cmap = cma)
        stringy = []
	
	for x in range(-60, 0, 15):
		stringy.append(str(abs(x)) + '$^{\circ}$S')
	stringy.append(str(0) + '$^{\circ}$   ')
	for x in range(15,75,15):
		stringy.append(str(x) + '$^{\circ}$N')
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	
	plt.subplot(3,2,1)
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_ylim(-60,60)
	ax1.set_xlim(datas[0][0][0][13], datas[0][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax1.plot(datas[0][0][0], [z] *len(datas[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(3,2,2)
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_ylim(-60,60)
	ax2.set_xlim(datas[1][0][0][13], datas[1][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax2.plot(datas[1][0][0], [z] *len(datas[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
        ax2.scatter(volctimes[1], 15.9, s = 100,color = 'k', marker= '^')		
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.tick_params(axis='y', pad = 13)
	
	plt.subplot(3,2,3)
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_ylim(-60,60)
	ax3.set_xlim(datas[2][0][0][13], datas[2][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax3.plot(datas[2][0][0], [z] *len(datas[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax3.scatter(volctimes[2], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(3,2,4)
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_ylim(-60,60)
	ax4.set_xlim(datas[3][0][0][13], datas[3][0][0][-1])
        ax4.scatter(volctimes[3], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax4.plot(datas[3][0][0], [z] *len(datas[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	ax4.tick_params(axis='y', pad = 13)
	
	plt.subplot(3,2,5)
	ax5.axvline(x=volctimes[4],color='k',ls='dashed')
	ax5.set_ylim(-60,60)
	ax5.set_xlim(datas[4][0][0][13], datas[4][0][0][-1])
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	for z in range(-60, 60, 15):    
	      ax5.plot(datas[4][0][0], [z] *len(datas[4][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
        ax5.scatter(volctimes[4], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[4],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.subplot(3,2,6)
	ax6.axvline(x=volctimes[5],color='k',ls='dashed')
	ax6.set_ylim(-60,60)
	ax6.set_xlim(datas[5][0][0][13], datas[5][0][0][-1])
        ax6.scatter(volctimes[5], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[5],15.9, yerr=np.array([[volclatlow,volclathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	for z in range(-60, 60, 15):    
	      ax6.plot(datas[5][0][0], [z] *len(datas[5][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	plt.xticks(rotation=30)
	plt.yticks(range(-60,75, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	ax6.tick_params(axis='y', pad = 13)

	cbar_ax = fig.add_axes([0.03, 0.15, 0.03, 0.7])
	fmt = '%1.0f'
	tix =  np.linspace(levels.min(), levels.max(), 9, endpoint=True)
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt)
	cbar.set_label('Percent Change', fontsize = 15, labelpad = -65)

def latseas(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global ax1,ax2,ax3,ax4, ax5, ax6, fig,cbar, plt, levels, datas, volcinjectlats

	datas = []
	CS = []
	zmax = []
	years = [2017, 2017, 2017, 2017, 2017, 2017]
	volcdays = [531, 714, 531, 714, 531, 714] 
	volctimes = []
	dataflat = []

	for x in range(6):
		datas.append(datamodulator(var, dayt, x, idxa,idx, years[x], num, flag))
		zmax.append([datas[x][2].min(), datas[x][2].max()])
		volctimes.append(volclocator(volcdays[x], years[x]))


	zmax = np.asarray(zmax)	
	volclathigh = [latitude_edges[18] - 72, latitude_edges[18] - 72, latitude_edges[15] - 41, latitude_edges[15] - 41, latitude_edges[12] - 15.9, latitude_edges[12] - 15.9]
	volclatlow =  [72 - latitude_edges[16], 72 - latitude_edges[16], 41 - latitude_edges[13], 41 - latitude_edges[13], 15.9 - latitude_edges[10], 15.9 - latitude_edges[10]]
#	if flagg ==0:
#		if abs(zmax.min()) > abs(zmax.max()):
#			levels = np.linspace(int(zmax.min() + (zmax.min()/10)), abs(int(zmax.min() + (zmax.min()/10))), int(num)) 
#		else:
#			levels = np.linspace(int(-(zmax.max() +zmax.max() / 10)),int( zmax.max() + zmax.max()/10), int(num))
#	else:
#		levels = np.linspace(int(zmax.min()), 0, int(num))
	plt.figure
	ax1 = plt.subplot(311)
	#ax2 = plt.subplot(322)
	ax3 = plt.subplot(312)
	#ax4 = plt.subplot(324)
	ax5 = plt.subplot(313)
	#ax6 = plt.subplot(326)
	fig = plt.gcf()
	fig.set_facecolor('white')
	plt.subplot(3,1,1)
	
	CS1 =plt.contourf(datas[0][0],datas[0][1],datas[0][2],levels, cmap = cma)
	#plt.subplot(3,2,2)
	#CS2 = plt.contourf(datas[1][0],datas[1][1],datas[1][2],levels, cmap = cma)
	plt.subplot(3,1,2)
	CS3 =plt.contourf(datas[2][0],datas[2][1],datas[2][2],levels, cmap = cma)
	#plt.subplot(3,2,4)
	#CS4 = plt.contourf(datas[3][0],datas[3][1],datas[3][2],levels, cmap = cma)
	plt.subplot(3,1,3)
	CS5 = plt.contourf(datas[4][0],datas[4][1],datas[4][2],levels, cmap = cma)
	#plt.subplot(3,2,6)
	#CS6 = plt.contourf(datas[5][0],datas[5][1],datas[5][2],levels, cmap = cma)
	stringy = []
	stringy = ['','75$^{\circ}$S','', '45$^{\circ}$S','', '15$^{\circ}$S','', '15$^{\circ}$N','', '45$^{\circ}$N','', '75$^{\circ}$N', '']
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	
	plt.subplot(3,1,1)
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_ylim(-90,90)
	ax1.set_xlim(datas[0][0][0][13], datas[0][0][0][-1])
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="on", labeltop="off", labelbottom="off", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,0,30,60,90]:    
	      ax1.plot(datas[0][0][0], [z] *len(datas[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax1.plot(datas[0][0][0][0:65], [z] *len(datas[0][0][0][0:65]), "--", lw=0.5, color="black", alpha=0.3)
	ax1.scatter(volctimes[0], 66,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],66, yerr=np.array([[volclatlow[0],volclathigh[0]]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.yticks(range(-90,105, 15), [stringy[w] for w in range(len(stringy))], fontsize=14)
	for tick in ax1.yaxis.get_major_ticks():
		tick.set_pad(-35)
		tick.label2.set_horizontalalignment('left')
	#plt.xticks(fontsize = 15,rotation = 90)
	#plt.subplot(3,2,2)
	#ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	#ax2.set_ylim(-90,90)
	#ax2.set_xlim(datas[1][0][0][13], datas[1][0][0][-1])
	#plt.xticks(fontsize = 15)
	#plt.yticks(fontsize = 20)
	#plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	#for z in range(-90, 90, 15):    
	#      ax2.plot(datas[1][0][0], [z] *len(datas[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	#plt.xticks(rotation=30)
	#plt.yticks(range(-90,105, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	#ax2.scatter(volctimes[1], 66, s = 100,color = 'k', marker= '^')		
	#plt.errorbar(volctimes[1],66, yerr=np.array([[volclatlow[1],volclathigh[1]]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	#ax2.tick_params(axis='y', pad = 13)
	
	plt.subplot(3,1,2)
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_ylim(-90,90)
	ax3.set_xlim(datas[2][0][0][13], datas[2][0][0][-1])
	#plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="on", labelbottom="on", labeltop = "on", left="off", right="off", labelright = "on", labelleft="off")
	for z in [-90,-60,-30,0,30,60,90]:    
	      ax3.plot(datas[2][0][0], [z] *len(datas[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax3.plot(datas[2][0][0][0:65], [z] *len(datas[2][0][0][0:65]), "--", lw=0.5, color="black", alpha=0.3)
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%n%Y'))
	plt.xticks(rotation=0, fontsize = 13)
	ax3.scatter(volctimes[2], 38, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[2],38, yerr=np.array([[volclatlow[2],volclathigh[2]]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	plt.yticks(range(-90,105, 15), [stringy[w] for w in range(len(stringy))], fontsize=14)
	for tick in ax3.yaxis.get_major_ticks():
		tick.set_pad(-35)
		tick.label2.set_horizontalalignment('left')
	#plt.subplot(3,2,4)
	#ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	#ax4.set_ylim(-90,90)
	#ax4.set_xlim(datas[3][0][0][13], datas[3][0][0][-1])
	#ax4.scatter(volctimes[3], 38, s = 100,color = 'k', marker= '^')		 
	#plt.errorbar(volctimes[3],38, yerr=np.array([[volclatlow[3],volclathigh[3]]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	#plt.xticks(fontsize = 15)
	#plt.yticks(fontsize = 20)
	#plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	#for z in range(-90, 90, 15):    
	#      ax4.plot(datas[3][0][0], [z] *len(datas[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	#plt.xticks(rotation=30)
	#plt.yticks(range(-90,105, 15), [stringy[w] for w in range(len(stringy))], fontsize=15)
	#ax4.tick_params(axis='y', pad = 13)
	
	plt.subplot(3,1,3)
	ax5.axvline(x=volctimes[4],color='k',ls='dashed')
	ax5.set_ylim(-90,90)
	ax5.set_xlim(datas[4][0][0][13], datas[4][0][0][-1])
#	plt.xticks(fontsize = 15)
	plt.yticks(fontsize = 20)
	plt.tick_params(axis="both", which="both", bottom="on", top="on", labelbottom="off", left="off", right="off", labelright = "on", labelleft="off")
	for z in [-90,-60,-30,0,30,60,90]:    
	      ax5.plot(datas[4][0][0], [z] *len(datas[4][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax5.plot(datas[4][0][0][0:65], [z] *len(datas[4][0][0][0:65]), "--", lw=0.5, color="black", alpha=0.3)
	#plt.xticks(rotation=90)
	ax5.scatter(volctimes[4], 15.9, s = 100,color = 'k', marker= '^')		 
	plt.errorbar(volctimes[4],15.9, yerr=np.array([[volclatlow[4],volclathigh[4]]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	#plt.subplot(3,2,6)
	#ax6.axvline(x=volctimes[5],color='k',ls='dashed')
	#ax6.set_ylim(-90,90)
	#ax6.set_xlim(datas[5][0][0][13], datas[5][0][0][-1])
	#ax6.scatter(volctimes[5], 15.9, s = 100,color = 'k', marker= '^')		 
	#plt.errorbar(volctimes[5],15.9, yerr=np.array([[volclatlow[5],volclathigh[5]]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	#plt.xticks(fontsize = 15)
	#plt.yticks(fontsize = 20)
	#plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on")
	#for z in range(-90, 90, 15):    
	#      ax6.plot(datas[5][0][0], [z] *len(datas[5][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	#plt.xticks(rotation=30)
	plt.yticks(range(-90,105, 15), [stringy[w] for w in range(len(stringy))], fontsize=14)
	#ax6.tick_params(axis='y', pad = 13)
	for tick in ax5.yaxis.get_major_ticks():
		tick.set_pad(-34)
		tick.label2.set_horizontalalignment('left')

	cbar_ax = fig.add_axes([0.12, 0.03, 0.78, 0.03])
	fmt = '%1.0f'
	tix =  np.linspace(levels.min(), levels.max(), 10, endpoint=True)
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt, orientation = 'horizontal')
	cbar_ax.tick_params(labelsize = 15)
	cbar.set_label('Percent Change', fontsize = 15, labelpad = -65)



def latfig(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global ax1,ax2,ax3,ax4, ax5, ax6,ax7,ax8,ax9, ax10, ax11, ax12,fig,cbar, plt, levels, datas0,datas1,datas2, volcinjectlats

	datas0 = []
	datas1 = []
	datas2 = []
	datas3 = []
	dateflat = []
	CS = []
	zmax = []
	years = [2017]
	volcdays = [531] 
	volctimes = []
	

	for x in range(6):
		datas0.append(datamodulator(var, dayt, x, 0,1, 2017, num, flag))
		datas1.append(datamodulator(var, dayt, x, 0,2, 2017, num, flag))
		datas2.append(datamodulator(var, dayt, x, 0,3, 2017, num, flag))
		zmax.append([datas2[x][2].min(), datas2[x][2].max()])
		volctimes.append(volclocator(531, 2017))
	
	datas3.append(datas0[4][2][13:14].mean(0))
	datas3.append(datas0[2][2][13:14].mean(0))
	datas3.append(datas0[0][2][13:14].mean(0))
	datas3.append(datas1[4][2][13:14].mean(0))
	datas3.append(datas1[2][2][13:14].mean(0))
	datas3.append(datas1[0][2][13:14].mean(0))
	datas3.append(datas2[4][2][13:14].mean(0))
	datas3.append(datas2[2][2][13:14].mean(0))
	datas3.append(datas2[0][2][13:14].mean(0))
	dateflat.append(datas0[4][0][0])
	dateflat.append(datas0[2][0][0])
	dateflat.append(datas0[0][0][0])
	dateflat.append(datas1[4][0][0])
	dateflat.append(datas1[2][0][0])
	dateflat.append(datas1[0][0][0])
	dateflat.append(datas2[4][0][0])
	dateflat.append(datas2[2][0][0])
	dateflat.append(datas2[2][0][0])


	zmax = np.asarray(zmax)	
	volclatarctichigh = latitude_edges[18] - 72
	volclatmidlathigh = latitude_edges[15] - 41
	volclattropichigh = latitude_edges[12] - 15.9
	volclatarcticlow = 72 - latitude_edges[16]
	volclatmidlatlow = 41 - latitude_edges[13]
	volclattropiclow = 15.9 - latitude_edges[10]
	levels =  np.array([-70,-60,-50,-40,-30,-25,-20, -15,-10,-8, -6,-4,-2,-1,0])
	
	plt.figure
	G = gridspec.GridSpec(3,5)
	ax1 = plt.subplot(G[0,0])
	ax2 = plt.subplot(G[0,1])
	ax3 = plt.subplot(G[0,2])
	ax4 = plt.subplot(G[1,0])
	ax5 = plt.subplot(G[1,1])
	ax6 = plt.subplot(G[1,2])
	ax7 = plt.subplot(G[2,0])
	ax8 = plt.subplot(G[2,1])
	ax9 = plt.subplot(G[2,2])
	ax10 = plt.subplot(G[0,3:])
	ax11 = plt.subplot(G[1,3:])
	ax12 = plt.subplot(G[2,3:])

	fig = plt.gcf()
	fig.set_facecolor('white')
	plt.subplot(G[0,0])
	
	CS1 =plt.contourf(datas0[4][0],datas0[4][1],datas0[4][2],levels, cmap = cma)
	CS1.cmap.set_over('white')
	CS1.cmap.set_under((0.267004, 0.004874, 0.329415))
	plt.subplot(G[0,1])
	CS2 = plt.contourf(datas0[2][0],datas0[2][1],datas0[2][2],levels, cmap = cma)
	CS2.cmap.set_over('white')
	CS2.cmap.set_under((0.267004, 0.004874, 0.329415))
	plt.subplot(G[0,2])
	CS3 =plt.contourf(datas0[0][0],datas0[0][1],datas0[0][2],levels, cmap = cma)
	CS3.cmap.set_over('white')
	CS3.cmap.set_under((0.267004, 0.004874, 0.329415))
	plt.subplot(G[1,0])
	CS4 = plt.contourf(datas1[4][0],datas1[4][1],datas1[4][2],levels, cmap = cma)
	CS4.cmap.set_over('white')
	CS4.cmap.set_under((0.267004, 0.004874, 0.329415))
	plt.subplot(G[1,1])
	CS5 = plt.contourf(datas1[2][0],datas1[2][1],datas1[2][2],levels, cmap = cma)
	CS5.cmap.set_over('white')
	CS5.cmap.set_under((0.267004, 0.004874, 0.329415))
	plt.subplot(G[1,2])
	CS6 = plt.contourf(datas1[0][0],datas1[0][1],datas1[0][2],levels, cmap = cma)
	CS6.cmap.set_over('white')
	CS6.cmap.set_under((0.267004, 0.004874, 0.329415))
	plt.subplot(G[2,0])
	CS7 = plt.contourf(datas2[4][0],datas2[4][1],datas2[4][2],levels, cmap = cma)
	CS7.cmap.set_over('white')
	CS7.cmap.set_under((0.267004, 0.004874, 0.329415))
	plt.cla()
	CS7 = plt.contourf(datas2[4][0],datas2[4][1],datas2[4][2],levels, cmap = cma)
	plt.subplot(G[2,1])
	CS8 = plt.contourf(datas2[2][0],datas2[2][1],datas2[2][2],levels, cmap = cma)
	CS8.cmap.set_over('white')
	CS8.cmap.set_under((0.267004, 0.004874, 0.329415))
	plt.subplot(G[2,2])
	CS9 = plt.contourf(datas2[0][0],datas2[0][1],datas2[0][2],levels, cmap = cma)
	CS9.cmap.set_over('white')
	CS9.cmap.set_under((0.267004, 0.004874, 0.329415))
	

	stringy = []
	stringy = ['','75$^{\circ}$S','', '45$^{\circ}$S','', '15$^{\circ}$S','', '15$^{\circ}$N','', '45$^{\circ}$N','', '75$^{\circ}$N', '']
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	labstring = ['a','b','c','d','e','f','g','h','i','j','k','l']
	labellocation = (DT.date(2018,1,25), -75)
	plt.subplot(G[0,0])
	
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_ylim(-85,85)
	ax1.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="on", labeltop="off", labelbottom="off", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax1.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax1.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	ax1.plot(datas2[0][0][0],[0]*len(datas2[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax1.xaxis.set_major_locator(years)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax1.xaxis.set_minor_locator(months)
	ax1.annotate(labstring[0],xy = labellocation, fontsize = 10)
	ax1.set_title('Tropical eruptions', fontsize = 10)
	ax1.set_ylabel('Sulfur dioxide only', fontsize = 10)
	plt.subplot(G[0,1])
	
	ax2.axvline(x=volctimes[0],color='k',ls='dashed')
	ax2.set_ylim(-85,85)
	ax2.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="on", labeltop="off", labelbottom="off", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax2.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax2.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	ax2.plot(datas0[0][0][0],[0]*len(datas0[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax2.scatter(volctimes[0], 41,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],41, yerr=np.array([[volclatmidlatlow,volclatmidlathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.xaxis.set_major_locator(years)
	ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax2.xaxis.set_minor_locator(months)
	ax2.annotate(labstring[1],xy = labellocation, fontsize = 10)
	ax2.set_title('Mid-latitude eruptions', fontsize = 10)
	
	plt.subplot(G[0,2])
	
	ax3.axvline(x=volctimes[0],color='k',ls='dashed')
	ax3.set_ylim(-85,85)
	ax3.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="on", labeltop="off", labelbottom="off", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax3.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax3.plot(datas0[0][0][0][0:60], [z] *len(datas0[0][0][0][0:60]), "--", lw=0.5, color="black", alpha=0.3)
	ax3.plot(datas2[0][0][0],[0]*len(datas2[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax3.scatter(volctimes[0], 72,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],72, yerr=np.array([[volclatarcticlow,volclatarctichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	#plt.yticks(range(-90,105, 15), [stringy[w] for w in range(len(stringy))], fontsize=10)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,73,90], [stringy[w] for w in range(len(stringy))], fontsize=10)
	for tick in ax3.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax3.set_ylim(-85,85)
	ax3.xaxis.set_major_locator(years)
	ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax3.xaxis.set_minor_locator(months)
	ax3.annotate(labstring[2],xy = labellocation, fontsize = 10)
	ax3.set_title('Arctic eruptions', fontsize = 10)
	
	plt.subplot(G[1,0])
	
	ax4.axvline(x=volctimes[0],color='k',ls='dashed')
	ax4.set_ylim(-85,85)
	ax4.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="on", labeltop="on", labelbottom="on", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax4.plot(datas1[0][0][0], [z] *len(datas1[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax4.plot(datas1[0][0][0], [z] *len(datas1[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	ax4.plot(datas2[0][0][0],[0]*len(datas2[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax4.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	ax4.xaxis.set_major_locator(years)
	ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax4.xaxis.set_minor_locator(months)
	plt.xticks(rotation=15, fontsize = 10)
	ax4.annotate(labstring[3],xy = labellocation, fontsize = 10)
	ax4.set_ylabel('Co-injected halogen', fontsize = 10)
	plt.subplot(G[1,1])
	
	ax5.axvline(x=volctimes[0],color='k',ls='dashed')
	ax5.set_ylim(-85,85)
	ax5.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="on", labeltop="on", labelbottom="on", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax5.plot(datas1[0][0][0], [z] *len(datas1[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax5.plot(datas1[0][0][0], [z] *len(datas1[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	ax5.plot(datas2[0][0][0],[0]*len(datas2[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax5.scatter(volctimes[0], 41,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],41, yerr=np.array([[volclatmidlatlow,volclatmidlathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	ax5.xaxis.set_major_locator(years)
	ax5.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax5.xaxis.set_minor_locator(months)
	plt.xticks(rotation=15, fontsize = 10)
	ax5.annotate(labstring[4],xy = labellocation, fontsize = 10)
	plt.subplot(G[1,2])
	
	ax6.axvline(x=volctimes[0],color='k',ls='dashed')
	ax6.set_ylim(-85,85)
	ax6.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="on", labeltop="on", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax6.plot(datas1[0][0][0], [z] *len(datas1[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax6.plot(datas1[0][0][0][0:60], [z] *len(datas1[0][0][0][0:60]), "--", lw=0.5, color="black", alpha=0.3)
	ax6.plot(datas2[0][0][0],[0]*len(datas2[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax6.scatter(volctimes[0], 72,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],72, yerr=np.array([[volclatarcticlow,volclatarctichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
#	plt.yticks(range(-90,105, 15), [stringy[w] for w in range(len(stringy))], fontsize=10)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,73,90], [stringy[w] for w in range(len(stringy))], fontsize=10)
	for tick in ax6.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')

	ax6.xaxis.set_major_locator(years)
	ax6.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax6.xaxis.set_minor_locator(months)
	plt.xticks(rotation=15, fontsize = 10)
	ax6.set_ylim(-85,85)
	ax6.annotate(labstring[5],xy = labellocation, fontsize = 10)
	plt.subplot(G[2,0])
	
	ax7.axvline(x=volctimes[0],color='k',ls='dashed')
	ax7.set_ylim(-85,85)
	ax7.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="on", labeltop="off", labelbottom="off", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax7.plot(datas2[0][0][0], [z] *len(datas2[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax7.plot(datas2[0][0][0], [z] *len(datas2[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	ax7.plot(datas2[0][0][0],[0]*len(datas2[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax7.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax7.xaxis.set_major_locator(years)
	ax7.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax7.xaxis.set_minor_locator(months)
	ax7.annotate(labstring[6],xy = labellocation, fontsize = 10)
	ax7.set_ylabel('High co-injected halogen', fontsize = 10)
	plt.subplot(G[2,1])
	
	ax8.axvline(x=volctimes[0],color='k',ls='dashed')
	ax8.set_ylim(-85,85)
	ax8.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="on", labeltop="off", labelbottom="off", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax8.plot(datas2[0][0][0], [z] *len(datas2[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax8.plot(datas2[0][0][0], [z] *len(datas2[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	ax8.plot(datas2[0][0][0],[0]*len(datas2[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax8.scatter(volctimes[0], 41,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],41, yerr=np.array([[volclatmidlatlow,volclatmidlathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax8.xaxis.set_major_locator(years)
	ax8.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax8.xaxis.set_minor_locator(months)
	ax8.annotate(labstring[7],xy = labellocation, fontsize = 10)
	
	plt.subplot(G[2,2])
	
	ax9.axvline(x=volctimes[0],color='k',ls='dashed')
	ax9.set_ylim(-85,85)
	ax9.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="on", labeltop="off", labelbottom="off", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax9.plot(datas2[0][0][0], [z] *len(datas2[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	ax9.plot(datas2[0][0][0],[0]*len(datas2[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax9.plot(datas2[0][0][0][0:60], [z] *len(datas2[0][0][0][0:60]), "--", lw=0.5, color="black", alpha=0.3)
	ax9.scatter(volctimes[0], 72,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],72, yerr=np.array([[volclatarcticlow,volclatarctichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	#plt.yticks(range(-90,105, 15), [stringy[w] for w in range(len(stringy))], fontsize=10)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,73,90], [stringy[w] for w in range(len(stringy))], fontsize=10)
	for tick in ax9.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax9.set_ylim(-85,85)
	ax9.xaxis.set_major_locator(years)
	ax9.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax9.xaxis.set_minor_locator(months)
	ax9.annotate(labstring[8],xy = labellocation, fontsize = 10)





	

	cbar_ax = fig.add_axes([0.02, 0.03, 0.56, 0.03])
	fmt = '%1.0f'
	tix =  np.array([-70,-60,-50,-40,-30,-25,-20, -15,-10,-8, -6,-4,-2,-1,0])
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt, orientation = 'horizontal')
	cbar_ax.tick_params(labelsize = 10)
	cbar.set_label('Percent change in column ozone', fontsize = 10, labelpad = -40)


	plt.subplot(G[0,3:])
	ax10.plot(dateflat[0], datas3[0], 'k-', lw = 2, label = 'Tropical sulfate')
	ax10.plot(dateflat[1], datas3[1], 'r-', lw = 2, label = 'Mid-latitude sulfate')
	ax10.plot(dateflat[2], datas3[2], 'b-', lw = 2, label = 'Arctic sulfate')
	ax10.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	ax10.grid(False)
        ax10.xaxis.set_minor_locator(months)
        ax10.xaxis.set_major_locator(years)
        ax10.yaxis.set_minor_locator(minorLocator)
        ax10.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax10.spines['top'].set_visible(False)
	ax10.spines['right'].set_visible(False)
	ax10.spines['bottom'].set_visible(False)
	ax10.spines['left'].set_visible(False)
        ax10.get_xaxis().tick_bottom()
        ax10.get_yaxis().tick_left()
	ax10.axvline(x=volctimes[0],color='k',ls='dashed')
	ax10.set_ylim(-12,2)
        plt.yticks(range(-12,2,3), [str(x) + "\%" for x in range(-12,2,3)], fontsize=10)
        plt.tick_params(axis="both", which="both", bottom="on", top="on", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in range(-12,2,3):    
              ax10.plot(datas2[0][0][13], [y] *len(datas2[0][0][13]), "--", lw=0.5, color="black", alpha=0.3)
	ax10.set_title('Scenario mid-latitude column ozone deviations (33N - 53N)', fontsize = 10)
       	ax10.axvspan(datas0[0][0][13][0],volctimes[0], alpha = 0.5, color = 'lightblue')
	ax10.annotate(labstring[9],xy = (DT.date(2018,1,25),-11.2), fontsize = 10)
	ax10.set_ylabel('Sulfur dioxide only', fontsize = 10)	
	plt.subplot(G[1,3:])
	ax11.plot(dateflat[3], datas3[3], 'k-', lw = 2, label = 'Tropical halogen')
	ax11.plot(dateflat[4], datas3[4], 'r-', lw = 2, label = 'Mid-latitude halogen')
	ax11.plot(dateflat[5], datas3[5], 'b-', lw = 2, label = 'Arctic halogen')
	ax11.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	ax11.grid(False)
        ax11.xaxis.set_minor_locator(months)
        ax11.xaxis.set_major_locator(years)
        ax11.yaxis.set_minor_locator(minorLocator)
        ax11.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax11.spines['top'].set_visible(False)
	ax11.spines['right'].set_visible(False)
	ax11.spines['bottom'].set_visible(False)
	ax11.spines['left'].set_visible(False)
        ax11.get_xaxis().tick_bottom()
        ax11.get_yaxis().tick_left()
	ax11.axvline(x=volctimes[0],color='k',ls='dashed')
	ax11.set_ylim(-16,2)
        plt.yticks(range(-16,2,4), [str(x) + "\%" for x in range(-16,2,4)], fontsize=10)
        plt.tick_params(axis="both", which="both", bottom="on", top="on", labelbottom="on", labeltop = "on", left="off", right="off", labelleft="off", labelright = "on")  
	plt.xticks(rotation=15, fontsize = 10)
 	for y in range(-16,2,4):    
              ax11.plot(datas2[0][0][13], [y] *len(datas2[0][0][13]), "--", lw=0.5, color="black", alpha=0.3)
       	ax11.axvspan(datas1[0][0][13][0],volctimes[0], alpha = 0.5, color = 'lightblue')
	ax11.annotate(labstring[10],xy = (DT.date(2018,1,25),-14.94), fontsize = 10)
	ax11.set_ylabel('Co-injected halogen', fontsize = 10)
	plt.subplot(G[2,3:])
	ax12.plot(dateflat[6], datas3[6], 'k-', lw = 2, label = 'Tropical eruptions')
	ax12.plot(dateflat[7], datas3[7], 'r-', lw = 2, label = 'Mid-latitude eruptions')
	ax12.plot(dateflat[8], datas3[8], 'b-', lw = 2, label = 'Arctic eruptions')
	ax12.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	ax12.grid(False)
        ax12.xaxis.set_minor_locator(months)
        ax12.xaxis.set_major_locator(years)
        ax12.yaxis.set_minor_locator(minorLocator)
        ax12.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax12.spines['top'].set_visible(False)
	ax12.spines['right'].set_visible(False)
	ax12.spines['bottom'].set_visible(False)
	ax12.spines['left'].set_visible(False)
        ax12.get_xaxis().tick_bottom()
        ax12.get_yaxis().tick_left()
	ax12.axvline(x=volctimes[0],color='k',ls='dashed')
	ax12.set_ylim(-40,2)
	ax12.set_ylabel('High co-injected halogen', fontsize = 10)
        plt.yticks(range(-40,2,10), [str(x) + "\%" for x in range(-40,2,10)], fontsize=10)
        plt.tick_params(axis="both", which="both", bottom="on", top="on", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in range(-40,2,10):    
              ax12.plot(datas2[0][0][13], [y] *len(datas2[0][0][13]), "--", lw=0.5, color="black", alpha=0.3)
        handles, labels = ax12.get_legend_handles_labels()
       	ax12.axvspan(datas2[0][0][13][0],volctimes[0], alpha = 0.5, color = 'lightblue')
        volcanohandle = mpatches.Patch(color = 'lightblue', ec = 'k', ls = 'dashed')
        volcanolegend = 'Before eruption'
        handles.append(volcanohandle)
        labels.append(volcanolegend)
        ax12.legend(handles[::-1], labels[::-1], bbox_to_anchor=(0.54,-0.35),frameon = False, loc = 'lower center', ncol = 2, fancybox = False, fontsize = 10, columnspacing = 4) 

	ax12.annotate(labstring[11],xy = (DT.date(2018,1,25),-37.5), fontsize = 10)

def figure1(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global ax1,ax2,ax3,ax4, ax5, ax6,ax7,ax8,ax9, ax10, ax11, ax12,ax19,fig,cbar, plt, levels, datas0,datas1,datas2, volcinjectlats, Gs, G2017, G2050, G2060, G2070, G2100

	datas0 = []
	datas1 = []
	datas2 = []
	dateflat = []
	CS = []
	years = [2017]
	volcdays = [531] 
	volctimes = []
	dataslat=[]
	totalcol = []	


	datas0.append(datamodulator(var, dayt, 2, 0,1, 2017, num, flag))
	datas0.append(datamodulator(var, dayt, 2, 2,3, 2050, num, flag))
	datas0.append(datamodulator(var, dayt, 2, 4,5, 2060, num, flag))
	datas0.append(datamodulator(var, dayt, 2, 7,6, 2070, num, flag))
	datas0.append(datamodulator(var, dayt, 2, 8,9, 2100, num, flag))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2050))
	volctimes.append(volclocator(531, 2060))
	volctimes.append(volclocator(531, 2070))
	volctimes.append(volclocator(531, 2100))
	datas1.append(datas0[0][2].mean(0))
	datas1.append(datas0[1][2].mean(0))
	datas1.append(datas0[2][2].mean(0))
	datas1.append(datas0[3][2].mean(0))
	datas1.append(datas0[4][2].mean(0))
	dateflat.append(datas0[0][0][0])
	dateflat.append(datas0[1][0][0])
	dateflat.append(datas0[2][0][0])
	dateflat.append(datas0[3][0][0])
	dateflat.append(datas0[4][0][0])
	
	for x in range(len(datas0)):
		latarray = []
		for y in range(len(datas0[0][0])):
			latarray.append(datas0[x][2][y][20:72].mean())
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))
	lats = datas0[0][1].mean(1)
	
	volclattropichigh = latitude_edges[12] - 15.9
	volclattropiclow = 15.9 - latitude_edges[10]
	levels =  np.array([-13,-11,-9,-7,-5,-3,-1,1,3,5,7])
#	levels = np.array([-10,0,10,20])
	plt.figure
	Gs = gridspec.GridSpec(5,1, hspace = 0)
	G2017 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[0])
	G2050 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[1])
	G2060 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[2])
	G2070 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[3])
	G2100 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[4])
	ax1 = plt.subplot(G2017[1:3,0:9])
	ax2 = plt.subplot(G2050[1:3,0:9])
	ax3 = plt.subplot(G2060[1:3,0:9])
	ax4 = plt.subplot(G2070[1:3,0:9])
	ax5 = plt.subplot(G2100[1:3,0:9])
	ax6 = plt.subplot(G2017[0,0:9])
	ax7 = plt.subplot(G2050[0,0:9])
	ax8 = plt.subplot(G2060[0,0:9])
	ax9 = plt.subplot(G2070[0,0:9])
	ax10 = plt.subplot(G2100[0,0:9])
	ax11 = plt.subplot(G2017[1:3,9])
	ax12 = plt.subplot(G2050[1:3,9])
	ax13 = plt.subplot(G2060[1:3,9])
	ax14 = plt.subplot(G2070[1:3,9])
	ax15 = plt.subplot(G2100[1:3,9])
	ax16 = plt.subplot(G2017[0,9])
	ax17 = plt.subplot(G2050[0,9])
	ax18 = plt.subplot(G2060[0,9])
	ax19 = plt.subplot(G2070[0,9])
	ax20 = plt.subplot(G2100[0,9])

	
	fig = plt.gcf()
	fig.set_facecolor('white')
	plt.subplot(G2017[1:3,0:9])
	
	CS1 =plt.contourf(datas0[0][0],datas0[0][1],datas0[0][2],levels, cmap = cma, extend = "both")
	plt.subplot(G2050[1:3,0:9])
	CS2 = plt.contourf(datas0[1][0],datas0[1][1],datas0[1][2],levels, cmap = cma)
	plt.subplot(G2060[1:3,0:9])
	CS3 =plt.contourf(datas0[2][0],datas0[2][1],datas0[2][2],levels, cmap = cma, extend = "both")
	plt.subplot(G2070[1:3,0:9])
	CS4 = plt.contourf(datas0[3][0],datas0[3][1],datas0[3][2],levels, cmap = cma, extend = "both")
	plt.subplot(G2100[1:3,0:9])
	CS5 = plt.contourf(datas0[4][0],datas0[4][1],datas0[4][2],levels, cmap = cma, extend = "both")
	

	stringy = []
	stringy = ['','75$^{\circ}$S','', '45$^{\circ}$S','', '15$^{\circ}$S','', '15$^{\circ}$N','', '45$^{\circ}$N','', '75$^{\circ}$N', '']
	labstring = ['a','b','c','d','e','f','g','h','i','j','k','l']
	
	plt.subplot(G2017[1:3,0:9])
	
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	labellocation = (DT.date(2018,1,25), -75)
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	ax1.xaxis.set_major_locator(years)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax1.xaxis.set_minor_locator(months)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax1.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax1.plot(datas0[0][0][0][0:70], [z] *len(datas0[0][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax1.plot(datas0[0][0][0],[0]*len(datas0[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax1.annotate(labstring[0],xy = labellocation, fontsize=18, fontweight='heavy')
	plt.xticks(rotation=0, fontsize=12, fontweight='heavy')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	for tick in ax1.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax1.set_ylim(-85,85)
	ax1.set_ylabel('Latitudinal column deviations', fontsize = 12, fontweight = 'heavy')	
	ax1.yaxis.set_label_coords(-0.035,0.7)

	
	plt.subplot(G2050[1:3,0:9])
	years2 = mdates.YearLocator()
	months2 = mdates.MonthLocator()
	minorLocator2 = MultipleLocator(2.5)
	labellocation = (DT.date(2051,1,25), -75)
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_xlim(DT.date(2051,1,1), DT.date(2055,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax2.plot(datas0[1][0][0], [z] *len(datas0[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax2.plot(datas0[1][0][0][0:70], [z] *len(datas0[1][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax2.plot(datas0[1][0][0],[0]*len(datas0[1][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax2.scatter(volctimes[1], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.xaxis.set_major_locator(years2)
	ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax2.xaxis.set_minor_locator(months2)
	ax2.annotate(labstring[1],xy = labellocation, fontsize=18, fontweight='heavy')
	plt.xticks(rotation=0, fontsize=12, fontweight='heavy')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	
	for tick in ax2.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax2.set_ylim(-85,85)
	plt.subplot(G2060[1:3,0:9])
	
	labellocation = (DT.date(2061,1,25), -75)
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_xlim(DT.date(2061,1,1), DT.date(2065,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax3.plot(datas0[2][0][0], [z] *len(datas0[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax3.plot(datas0[2][0][0][0:70], [z] *len(datas0[2][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax3.plot(datas0[2][0][0],[0]*len(datas0[2][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax3.scatter(volctimes[2], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	ax3.set_ylim(-85,85)
	for tick in ax3.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	years3 = mdates.YearLocator()
	months3 = mdates.MonthLocator()
	minorLocator3 = MultipleLocator(2.5)
	ax3.xaxis.set_major_locator(years3)
	ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax3.xaxis.set_minor_locator(months3)
	plt.xticks(rotation=0, fontsize=12, fontweight='heavy')
	ax3.annotate(labstring[2],xy = labellocation, fontsize=18, fontweight='heavy')
	ax3.set_ylim(-85,85)
	
	plt.subplot(G2070[1:3,0:9])
	
	years3a = mdates.YearLocator()
	months3a = mdates.MonthLocator()
	minorLocator3 = MultipleLocator(2.5)
	labellocation = (DT.date(2071,1,25), -75)
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_xlim(DT.date(2071,1,1), DT.date(2075,7,1))
	ax4.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax4.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax4.plot(datas0[3][0][0][0:70], [z] *len(datas0[3][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax4.plot(datas0[3][0][0],[0]*len(datas0[3][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax4.scatter(volctimes[3], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	ax4.xaxis.set_major_locator(years3a)
	ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax4.xaxis.set_minor_locator(months3a)
	plt.xticks(rotation=0, fontsize=12, fontweight='heavy')
	ax4.annotate(labstring[3],xy = labellocation, fontsize=18, fontweight='heavy')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	for tick in ax4.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax4.set_ylim(-85,85)

	plt.subplot(G2100[1:3,0:9])
	labellocation = (DT.date(2101,1,25), -75)
	ax5.axvline(x=volctimes[4],color='k',ls='dashed')
	ax5.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax5.plot(datas0[4][0][0], [z] *len(datas0[4][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax5.plot(datas0[4][0][0][0:70], [z] *len(datas0[4][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax5.plot(datas0[4][0][0],[0]*len(datas0[4][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax5.scatter(volctimes[4], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[4],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	years4 = mdates.YearLocator()
	months4 = mdates.MonthLocator()
	minorLocator4 = MultipleLocator(2.5)
	ax5.xaxis.set_major_locator(years4)
	ax5.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax5.xaxis.set_minor_locator(months4)
	plt.xticks(rotation=0, fontsize=12, fontweight='heavy')
	ax5.annotate(labstring[4],xy = labellocation, fontsize=18, fontweight='heavy')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	for tick in ax5.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax5.set_ylim(-85,85)	

	ax5.set_xlabel('Model year', fontsize =12, fontweight = 'heavy', horizontalalignment='center')
	#ax5.xaxis.set_label_coords(0,-0.2)

	cbar_ax = fig.add_axes([0.025, 0.97, 0.967, 0.01])
	fmt = '%1.0f'
	tix =  levels
	cbar = fig.colorbar(CS2, cax = cbar_ax, ticks = tix, format =fmt, orientation = 'horizontal')
	cbar_ax.tick_params(labelsize = 12)
	cbar.set_label('Percent change in column ozone', fontsize=12, fontweight='heavy', labelpad = -40)


	plt.subplot(G2017[0,0:9])
	ax6.plot(dateflat[0][16:], datas1[0][16:], 'k-', lw = 2, label = 'Tropical sulfate')
	years5 = mdates.YearLocator()
	months5 = mdates.MonthLocator()
	minorLocator5 = MultipleLocator(2.5)
	ax6.set_xlim(DT.date(2018,1,1), DT.date(2022,7,1))
	ax6.grid(False)
        ax6.xaxis.set_minor_locator(months5)
        ax6.xaxis.set_major_locator(years5)
        ax6.yaxis.set_minor_locator(minorLocator5)
        ax6.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax6.spines['top'].set_visible(True)
	ax6.spines['right'].set_visible(True)
	ax6.spines['bottom'].set_visible(True)
	ax6.spines['left'].set_visible(True)
        ax6.get_xaxis().tick_bottom()
        ax6.get_yaxis().tick_left()
	ax6.axvline(x=volctimes[0],color='k',ls='dashed')
	ax6.set_ylim(-9.5,2.5)
	ax6.set_xlabel('Temporal column ozone deviations', fontsize = 12, horizontalalignment = 'left', fontweight = 'heavy')	
	ax6.xaxis.set_label_coords(0,1.34)
	plt.yticks(range(-8,2,4), [str(x) + "\%" for x in range(-8,2,4)], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", labeltop='off',right="off", labelleft="on", labelright = "off")  
 	for y in range(-8,2,4):    
              ax6.plot(dateflat[0][16:], [y] *len(dateflat[0][16:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax6.yaxis.get_major_ticks():
		tick.set_pad(-18)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2050[0,0:9])
	years6 = mdates.YearLocator()
	months6 = mdates.MonthLocator()
	minorLocator6 = MultipleLocator(2.5)
	ax7.plot(dateflat[1][16:], datas1[1][16:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax7.set_xlim(DT.date(2051,1,1), DT.date(2055,7,1))
	ax7.grid(False)
        ax7.xaxis.set_minor_locator(months6)
        ax7.xaxis.set_major_locator(years6)
        ax7.yaxis.set_minor_locator(minorLocator6)
        ax7.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax7.spines['top'].set_visible(True)
	ax7.spines['right'].set_visible(True)
	ax7.spines['bottom'].set_visible(True)
	ax7.spines['left'].set_visible(True)
        ax7.get_xaxis().tick_bottom()
        ax7.get_yaxis().tick_left()
	ax7.axvline(x=volctimes[1],color='k',ls='dashed')
	ax7.set_ylim(-7.5,2.5)
        plt.yticks(range(-6,2,3), [str(x) + "\%" for x in range(-6,2,3)], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in range(-6,2,3):    
              ax7.plot(dateflat[1][16:], [y] *len(dateflat[1][16:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax7.yaxis.get_major_ticks():
		tick.set_pad(-18)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2060[0,0:9])
	years8 = mdates.YearLocator()
	months8 = mdates.MonthLocator()
	minorLocator8 = MultipleLocator(2.5)
	ax8.plot(dateflat[2][16:], datas1[2][16:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax8.set_xlim(DT.date(2061,1,1), DT.date(2065,7,1))
	ax8.grid(False)
        ax8.xaxis.set_minor_locator(months8)
        ax8.xaxis.set_major_locator(years8)
        ax8.yaxis.set_minor_locator(minorLocator8)
        ax8.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax8.spines['top'].set_visible(True)
	ax8.spines['right'].set_visible(True)
	ax8.spines['bottom'].set_visible(True)
	ax8.spines['left'].set_visible(True)
        ax8.get_xaxis().tick_bottom()
        ax8.get_yaxis().tick_left()
	ax8.axvline(x=volctimes[2],color='k',ls='dashed')
	ax8.set_ylim(-4.75,1.5)
        plt.yticks(range(-4,2,2), [str(x) + "\%" for x in range(-4,2,2)], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in range(-4,2,2):    
              ax8.plot(dateflat[2][16:], [y] *len(dateflat[2][16:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax8.yaxis.get_major_ticks():
		tick.set_pad(-18)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2070[0,0:9])
	years9 = mdates.YearLocator()
	months9 = mdates.MonthLocator()
	minorLocator9 = MultipleLocator(2.5)
	ax9.plot(dateflat[3][16:], datas1[3][16:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax9.set_xlim(DT.date(2071,1,1), DT.date(2075,7,1))
	ax9.grid(False)
        ax9.xaxis.set_minor_locator(months9)
        ax9.xaxis.set_major_locator(years9)
        ax9.yaxis.set_minor_locator(minorLocator9)
        ax9.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax9.spines['top'].set_visible(True)
	ax9.spines['right'].set_visible(True)
	ax9.spines['bottom'].set_visible(True)
	ax9.spines['left'].set_visible(True)
        ax9.get_xaxis().tick_bottom()
        ax9.get_yaxis().tick_left()
	ax9.axvline(x=volctimes[3],color='k',ls='dashed')
	ax9.set_ylim(-2.5,0.75)
        plt.yticks(range(-2,1,1), [str(x) + "\%" for x in range(-2,1,1)], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in range(-2,1,1):    
              ax9.plot(dateflat[3][16:], [y] *len(dateflat[3][16:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax9.yaxis.get_major_ticks():
		tick.set_pad(-18)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2100[0,0:9])
	years10 = mdates.YearLocator()
	months10 = mdates.MonthLocator()
	minorLocator10 = MultipleLocator(2.5)
	ax10.plot(dateflat[4][16:], datas1[4][16:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax10.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax10.grid(False)
        ax10.xaxis.set_minor_locator(months10)
        ax10.xaxis.set_major_locator(years10)
        ax10.yaxis.set_minor_locator(minorLocator10)
        ax10.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax10.spines['top'].set_visible(True)
	ax10.spines['right'].set_visible(True)
	ax10.spines['bottom'].set_visible(True)
	ax10.spines['left'].set_visible(True)
        ax10.get_xaxis().tick_bottom()
        ax10.get_yaxis().tick_left()
	ax10.axvline(x=volctimes[4],color='k',ls='dashed')
	ax10.set_ylim(-1.5,1.5)
        plt.yticks(range(-1,2,1), [str(x) + "\%" for x in range(-1,2,1)], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in range(-1,2,1):    
              ax10.plot(dateflat[4][16:], [y] *len(dateflat[4][16:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax10.yaxis.get_major_ticks():
		tick.set_pad(-18)

		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2017[1:3,9])
	ax11.plot(dataslat[0], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax11.grid(False)
        ax11.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax11.spines['top'].set_visible(True)
	ax11.spines['right'].set_visible(True)
	ax11.spines['bottom'].set_visible(True)
	ax11.spines['left'].set_visible(True)
        ax11.get_xaxis().tick_bottom()
        ax11.get_yaxis().tick_left()
	ax11.set_ylim(-85,85)
	ax11.set_xlim(-7, 1.5)
	ax11.set_xlabel('EESC(3 year): 1991 pptv', fontsize = 12, fontweight = 'heavy', horizontalalignment='right')
	ax11.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-6,0], [str(x) + "\%" for x in [-6,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in range(-6,1,3):    
              ax11.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax11.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2017[0,9])
	ax16.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax16.set_xlim(-1,1)
	ax16.set_ylim(-1,1)
	ax16.annotate(str(totalcol[0])[0:4] + '\%', xy = (-0.75,-0.20), fontsize = 14, fontweight = 'heavy')
	ax16.set_xlabel('Global-temporal \n average', fontsize = 12, fontweight = 'heavy', horizontalalignment = 'right')
	ax16.xaxis.set_label_coords(1,1.635)

	plt.subplot(G2050[1:3,9])
	ax12.plot(dataslat[1], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax12.grid(False)
        ax12.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax12.spines['top'].set_visible(True)
	ax12.spines['right'].set_visible(True)
	ax12.spines['bottom'].set_visible(True)
	ax12.spines['left'].set_visible(True)
        ax12.get_xaxis().tick_bottom()
        ax12.get_yaxis().tick_left()
	ax12.set_ylim(-85,85)
	ax12.set_xlim(-5.5, 1.6)
	ax12.set_xlabel('1304 pptv', fontsize = 12, fontweight = 'heavy', horizontalalignment='right')
	ax12.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-5,0.5], [str(x) + "\%" for x in [-5,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-5,-2.5,0]:    
              ax12.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax12.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2050[0,9])
	ax17.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax17.set_xlim(-1,1)
	ax17.set_ylim(-1,1)
	ax17.annotate(str(totalcol[1])[0:4] + '\%', xy = (-0.75,-0.20), fontsize = 14, fontweight = 'heavy')
	ax17.xaxis.set_label_coords(0.45,1.525)
	
	plt.subplot(G2060[1:3,9])
	ax13.plot(dataslat[2], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax13.grid(False)
        ax13.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax13.spines['top'].set_visible(True)
	ax13.spines['right'].set_visible(True)
	ax13.spines['bottom'].set_visible(True)
	ax13.spines['left'].set_visible(True)
        ax13.get_xaxis().tick_bottom()
        ax13.get_yaxis().tick_left()
	ax13.set_ylim(-85,85)
	ax13.set_xlim(-4.5, 1.1)
	ax13.set_xlabel('1199 pptv', fontsize = 12, fontweight = 'heavy', horizontalalignment='right')
	ax13.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-4,0], [str(x) + "\%" for x in [-4,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in range(-4,1,2):    
              ax13.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax13.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2060[0,9])
	ax18.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax18.set_xlim(-1,1)
	ax18.set_ylim(-1,1)
	ax18.annotate(str(totalcol[2])[0:4] + '\%', xy = (-0.75,-0.20), fontsize = 14, fontweight = 'heavy')
	ax18.xaxis.set_label_coords(0.45,1.525)
	
	plt.subplot(G2070[1:3,9])
	ax14.plot(dataslat[3], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax14.grid(False)
        ax14.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax14.spines['top'].set_visible(True)
	ax14.spines['right'].set_visible(True)
	ax14.spines['bottom'].set_visible(True)
	ax14.spines['left'].set_visible(True)
        ax14.get_xaxis().tick_bottom()
        ax14.get_yaxis().tick_left()
	ax14.set_ylim(-85,85)
	ax14.set_xlim(-3.5, 0.7)
	ax14.set_xlabel('1104 pptv', fontsize = 12, fontweight = 'heavy', horizontalalignment='right')
	ax14.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-3,0], [str(x) + "\%" for x in [-3,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-3,-1.5,0]:    
              ax14.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax14.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2070[0,9])
	ax19.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax19.set_xlim(-1,1)
	ax19.set_ylim(-1,1)
	ax19.annotate(str(totalcol[3])[0:4] + '\%', xy = (-0.75,-0.20), fontsize = 14, fontweight = 'heavy')
	ax19.xaxis.set_label_coords(0.45,1.525)
	
	plt.subplot(G2100[1:3,9])
	ax15.plot(dataslat[4], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax15.grid(False)
        ax15.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax15.spines['top'].set_visible(True)
	ax15.spines['right'].set_visible(True)
	ax15.spines['bottom'].set_visible(True)
	ax15.spines['left'].set_visible(True)
        ax15.get_xaxis().tick_bottom()
        ax15.get_yaxis().tick_left()
	ax15.set_ylim(-85,85)
	ax15.set_xlim(-2.5, 0.5)
	ax15.set_xlabel('944 pptv', fontsize = 12, fontweight = 'heavy', horizontalalignment='right')
	ax15.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-2,0], [str(x) + "\%" for x in [-2,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in range(-2,1,1):    
              ax15.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax15.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2100[0,9])
	ax20.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax20.set_xlim(-1,1)
	ax20.set_ylim(-1,1)
	ax20.annotate(str(totalcol[4])[0:4] + '\%', xy = (-0.75,-0.20), fontsize = 14, fontweight = 'heavy')
	ax20.xaxis.set_label_coords(0.45,1.525)

def figure2(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global ax1,ax2,ax3,ax4, ax5, ax6,ax7,ax8,ax9, ax10,dataslat, totalcol,ax11, ax12,fig,cbar, plt, levels, datas0,datas1,datas2, volcinjectlats, Gs, G2017, G2050, G2060, G2070, G2100

	datas0 = []
	datas1 = []
	datas2 = []
	dateflat = []
	CS = []
	years = [2100]
	volcdays = [531] 
	volctimes = []	
	dataslat = []
	totalcol = []

	datas0.append(datamodulator(var, dayt, 0, 0,1, 2100, num, flag))
	datas0.append(datamodulator(var, dayt, 1, 0,1, 2100, num, flag))
	datas0.append(datamodulator(var, dayt, 2, 8,9, 2100, num, flag))
	datas0.append(datamodulator(var, dayt, 3, 0,1, 2100, num, flag))
	datas1.append(datamodulator(var, dayt, 4, 0,1, 2100, num, flag))
	datas1.append(datamodulator(var, dayt, 4, 2,3, 2100, num, flag))
	datas1.append(datamodulator(var, dayt, 4, 4,5, 2100, num, flag))
	datas1.append(datamodulator(var, dayt, 4, 6,7, 2100, num, flag))
	datas1.append(datamodulator(var, dayt, 4, 8,9, 2100, num, flag))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	datas2.append(datas0[0][2].mean(0))
	datas2.append(datas0[1][2].mean(0))
	datas2.append(datas0[2][2].mean(0))
	datas2.append(datas0[3][2].mean(0))
	datas2.append(datas1[0][2].mean(0))
	datas2.append(datas1[1][2].mean(0))
	datas2.append(datas1[2][2].mean(0))
	datas2.append(datas1[3][2].mean(0))
	datas2.append(datas1[4][2].mean(0))
	dateflat.append(datas0[0][0][0])
	dateflat.append(datas0[1][0][0])
	dateflat.append(datas0[2][0][0])
	dateflat.append(datas0[3][0][0])
	dateflat.append(datas1[0][0][0])
	dateflat.append(datas1[1][0][0])
	dateflat.append(datas1[2][0][0])
	dateflat.append(datas1[3][0][0])
	dateflat.append(datas1[4][0][0])
	
	for x in range(len(datas0)):
		latarray = []
		for y in range(len(datas0[0][0])):
			latarray.append(datas0[x][2][y][20:72].mean())
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))
	lats = datas0[0][1].mean(1)
	for x in range(len(datas1)):
		latarray = []
		for y in range(len(datas1[0][0])):
			latarray.append(np.nanmean(datas1[x][2][y][20:]))
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))

	volclattropichigh = latitude_edges[12] - 15.9
	volclattropiclow = 15.9 - latitude_edges[10]
	
	levels =  np.array([-13,-11,-9,-7,-5,-3,-1,1,3,5,7])
	plt.figure
	Gs = gridspec.GridSpec(3,2, hspace = 0.05, wspace =0.05)
	G26 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[0], hspace = 0)
	G45 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[1], hspace = 0)
	G60 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[2], hspace = 0)
	G85 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[3], hspace = 0)
	Gsal = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[4:6], hspace=0, wspace = 0)
	ax1 = plt.subplot(G26[1:3,0:9])
	ax2 = plt.subplot(G45[1:3,0:9])
	ax3 = plt.subplot(G60[1:3,0:9])
	ax4 = plt.subplot(G85[1:3,0:9])
	ax5 = plt.subplot(Gsal[1:3,0:5])
	ax23 = plt.subplot(Gsal[1:3,5:])
	ax6 = plt.subplot(G26[0,0:9])
	ax7 = plt.subplot(G45[0,0:9])
	ax8 = plt.subplot(G60[0,0:9])
	ax9 = plt.subplot(G85[0,0:9])
	ax10 = plt.subplot(Gsal[0,0:2])
	ax11 = plt.subplot(Gsal[0,2:4])
	ax12 = plt.subplot(Gsal[0,4:6])
	ax13 = plt.subplot(Gsal[0,6:8])
	ax14 = plt.subplot(Gsal[0,8:])
	ax15 = plt.subplot(G26[1:3,9])
	ax16 = plt.subplot(G45[1:3,9])
	ax17 = plt.subplot(G60[1:3,9])
	ax18 = plt.subplot(G85[1:3,9])
	ax19 = plt.subplot(G26[0,9])
	ax20 = plt.subplot(G45[0,9])
	ax21 = plt.subplot(G60[0,9])
	ax22 = plt.subplot(G85[0,9])
	fig = plt.gcf()
	fig.set_facecolor('white')
	
	plt.subplot(G26[1:3,0:9])
	CS1 =plt.contourf(datas0[0][0],datas0[0][1],datas0[0][2],levels, cmap = cma)
	
	plt.subplot(G45[1:3,0:9])
	CS2 = plt.contourf(datas0[1][0],datas0[1][1],datas0[1][2],levels, cmap = cma)
	
	plt.subplot(G60[1:3,0:9])
	CS3 =plt.contourf(datas0[2][0],datas0[2][1],datas0[2][2],levels, cmap = cma)
	
	plt.subplot(G85[1:3,0:9])
	CS4 = plt.contourf(datas0[3][0],datas0[3][1],datas0[3][2],levels, cmap = cma)
	
	plt.subplot(Gsal[0,0:2])
	CS5 = plt.contourf(datas1[0][0], datas1[0][1],datas1[0][2], levels, cmap = cma)
	
	plt.subplot(Gsal[0,2:4])
	CS6 = plt.contourf(datas1[1][0], datas1[1][1],datas1[1][2], levels, cmap = cma)
	
	plt.subplot(Gsal[0,4:6])
	CS7 = plt.contourf(datas1[2][0], datas1[2][1],datas1[2][2], levels, cmap = cma)
	
	plt.subplot(Gsal[0,6:8])
	CS8 = plt.contourf(datas1[3][0], datas1[3][1],datas1[3][2], levels, cmap = cma, exgtend = "both")
	
	plt.subplot(Gsal[0,8:])
	CS9 = plt.contourf(datas1[4][0], datas1[4][1],datas1[4][2], levels, cmap = cma, extend="both")
	stringy = []
	stringy = ['','75$^{\circ}$S','', '45$^{\circ}$S','', '15$^{\circ}$S','', '15$^{\circ}$N','', '45$^{\circ}$N','', '75$^{\circ}$N', '']
	labstring = ['a','b','c','d','e','f','g','h','i','j','k','l']
	stringgy = []
	stringgy = ['','','', '45$^{\circ}$S','', '','', '','', '45$^{\circ}$N','', '', '']
	plt.subplot(G26[1:3,0:9])
	
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax1.xaxis.set_major_locator(years)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax1.xaxis.set_minor_locator(months)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax1.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75,-45, -15, 15, 45]:    
	      ax1.plot(datas0[0][0][0][0:68], [z] *len(datas0[0][0][0][0:68]), "--", lw=0.5, color="black", alpha=0.3)
	ax1.plot(datas0[0][0][0],[0]*len(datas0[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax1.plot(datas0[0][0][0][0:68], [75] *len(datas0[0][0][0][0:68]), "--", lw=0.5, color="black", alpha=0.3)
	ax1.set_ylabel('Latitudinal column deviations\n RCP 2.6', fontsize=12, fontweight='bold')
	ax1.yaxis.set_label_coords(0, 0.72)
	ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax1.annotate(labstring[0],xy = labellocation, fontsize=18, fontweight='bold')
	plt.xticks(rotation=0, fontsize=12, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax1.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax1.set_ylim(-85,85)
	ax1.set_xlabel('Temporal column ozone deviations', fontsize = 12, fontweight = 'heavy', horizontalalignment = 'left')
	ax1.xaxis.set_label_coords(0,1.63)	
	
	plt.subplot(G45[1:3,0:9])
	years2 = mdates.YearLocator()
	months2 = mdates.MonthLocator()
	minorLocator2 = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax2.plot(datas0[1][0][0], [z] *len(datas0[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45]:    
	      ax2.plot(datas0[1][0][0][0:68], [z] *len(datas0[1][0][0][0:68]), "--", lw=0.5, color="black", alpha=0.3)
	ax2.plot(datas0[1][0][0],[0]*len(datas0[1][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax2.plot(datas0[0][0][0][0:68], [75] *len(datas0[0][0][0][0:68]), "--", lw=0.5, color="black", alpha=0.3)
	ax2.set_ylabel('RCP 4.5', fontsize=12, fontweight='bold')
	ax2.yaxis.set_label_coords(0, 0.7)
	ax2.scatter(volctimes[1], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.xaxis.set_major_locator(years2)
	ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax2.xaxis.set_minor_locator(months2)
	ax2.annotate(labstring[1],xy = labellocation, fontsize=18, fontweight='bold')
	plt.xticks(rotation=0, fontsize=12, fontweight='bold')
	
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax2.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax2.set_ylim(-85,85)
	
	
	plt.subplot(G60[1:3,0:9])
	labellocation = (DT.date(2101,1,25), -75)
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax3.plot(datas0[2][0][0], [z] *len(datas0[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45]:    
	      ax3.plot(datas0[2][0][0][0:68], [z] *len(datas0[2][0][0][0:68]), "--", lw=0.5, color="black", alpha=0.3)
	ax3.plot(datas0[2][0][0],[0]*len(datas0[2][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax3.plot(datas0[0][0][0][0:68], [75] *len(datas0[0][0][0][0:68]), "--", lw=0.5, color="black", alpha=0.3)
	ax3.set_ylabel('RCP 6.0', fontsize=12, fontweight='bold')
	ax3.yaxis.set_label_coords(0, 0.7)
	ax3.scatter(volctimes[2], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	ax3.set_ylim(-85,85)
	for tick in ax3.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	years3 = mdates.YearLocator()
	months3 = mdates.MonthLocator()
	minorLocator3 = MultipleLocator(2.5)
	ax3.xaxis.set_major_locator(years3)
	ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax3.xaxis.set_minor_locator(months3)
	plt.xticks(rotation=0, fontsize=12, fontweight='bold')
	ax3.annotate(labstring[2],xy = labellocation, fontsize=18, fontweight='bold')
	ax3.set_ylim(-85,85)
	
	plt.subplot(G85[1:3,0:9])
	years3a = mdates.YearLocator()
	months3a = mdates.MonthLocator()
	minorLocator3 = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax4.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax4.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45]:    
	      ax4.plot(datas0[3][0][0][0:68], [z] *len(datas0[3][0][0][0:68]), "--", lw=0.5, color="black", alpha=0.3)
	ax4.plot(datas0[3][0][0],[0]*len(datas0[3][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax4.plot(datas0[0][0][0][0:68], [75] *len(datas0[0][0][0][0:68]), "--", lw=0.5, color="black", alpha=0.3)
	ax4.set_ylabel('RCP 8.5', fontsize=12, fontweight='bold')
	ax4.yaxis.set_label_coords(0, 0.7)
	ax4.scatter(volctimes[3], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	ax4.xaxis.set_major_locator(years3a)
	ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax4.xaxis.set_minor_locator(months3a)
	plt.xticks(rotation=0, fontsize=12, fontweight='bold')
	ax4.annotate(labstring[3],xy = labellocation, fontsize=18, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax4.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax4.set_ylim(-85,85)

	plt.subplot(Gsal[0,0:2])
	
	yearssala = mdates.YearLocator()
	monthssala = mdates.MonthLocator()
	minorLocatorsala = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax10.axvline(x=volctimes[3],ymin = 0, ymax = 0.8,color='k',ls='dashed')
	ax10.set_xlim(DT.date(2101,1,1), DT.date(2105,1,1))
	ax10.tick_params(axis="both", which="both", bottom="off", top="off", labeltop="off", labelbottom="off", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-75, -45, -15, 15, 45]:    
	      ax10.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	ax10.plot(datas0[3][0][0][38:],[75]*len(datas0[3][0][0][38:]), "--", lw= 0.5, color = "black", alpha=0.3)	
	ax10.xaxis.set_major_locator(yearssala)
	ax10.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax10.xaxis.set_minor_locator(monthssala)
	plt.xticks(rotation=0, fontsize=12, fontweight='bold')
	ax10.annotate(labstring[4],xy = labellocation, fontsize=18, fontweight='bold')
	ax10.set_ylim(-85,85)
	ax10.annotate('+' + str(0.8) + '\% $\Delta$Column O3', xy = (DT.date(2101,2,1),55), fontsize = 10, fontweight = 'heavy')
	plt.subplot(Gsal[0,2:4])
	
	yearssala = mdates.YearLocator()
	monthssala = mdates.MonthLocator()
	minorLocatorsala = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax11.axvline(x=volctimes[3],ymin = 0, ymax = 0.8,color='k',ls='dashed')
	ax11.set_xlim(DT.date(2101,1,1), DT.date(2105,1,1))
	ax11.tick_params(axis="both", which="both", bottom="off", top="off", labeltop="off", labelbottom="off", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-75, -45, -15, 15, 45]:    
	      ax11.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	
	ax11.plot(datas0[3][0][0][21:],[75]*len(datas0[3][0][0][21:]), "--", lw= 0.5, color = "black", alpha=0.3)	
	ax11.xaxis.set_major_locator(yearssala)
	ax11.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax11.xaxis.set_minor_locator(monthssala)
	plt.xticks(rotation=0, fontsize=12, fontweight='bold')
	ax11.annotate(labstring[5],xy = labellocation, fontsize=18, fontweight='bold')
	ax11.set_ylim(-85,85)
	ax11.annotate(str(0.3) + '\%', xy = (DT.date(2101,2,1),55), fontsize = 10, fontweight = 'heavy')
	plt.subplot(Gsal[0,4:6])
	
	yearssala = mdates.YearLocator()
	monthssala = mdates.MonthLocator()
	minorLocatorsala = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax12.axvline(x=volctimes[3],ymin = 0, ymax = 0.8,color='k',ls='dashed')
	ax12.set_xlim(DT.date(2101,1,1), DT.date(2105,1,1))
	ax12.tick_params(axis="both", which="both", bottom="off", top="off", labeltop="off", labelbottom="off", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-75, -45, -15, 15, 45]:    
	      ax12.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	
	ax12.plot(datas0[3][0][0][22:],[75]*len(datas0[3][0][0][22:]), "--", lw= 0.5, color = "black", alpha=0.3)	
	ax12.xaxis.set_major_locator(yearssala)
	ax12.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax12.xaxis.set_minor_locator(monthssala)
	plt.xticks(rotation=0, fontsize=12, fontweight='bold')
	ax12.annotate(labstring[6],xy = (DT.date(2101,1,25),-65), fontsize=18, fontweight='bold')
	ax12.set_ylim(-85,85)
	ax12.annotate(str(-0.2) + '\%', xy = (DT.date(2101,2,1),55), fontsize = 10, fontweight = 'heavy')
	plt.subplot(Gsal[0,6:8])
	
	yearssala = mdates.YearLocator()
	monthssala = mdates.MonthLocator()
	minorLocatorsala = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax13.axvline(x=volctimes[3],ymin = 0, ymax = 0.8,color='k',ls='dashed')
	ax13.set_xlim(DT.date(2101,1,1), DT.date(2105,1,1))
	ax13.tick_params(axis="both", which="both", bottom="off", top="off", labeltop="off", labelbottom="off", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-75, -45, -15, 15, 45]:    
	      ax13.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	
	ax13.plot(datas0[3][0][0][22:],[75]*len(datas0[3][0][0][22:]), "--", lw= 0.5, color = "black", alpha=0.3)	
	ax13.xaxis.set_major_locator(yearssala)
	ax13.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax13.xaxis.set_minor_locator(monthssala)
	plt.xticks(rotation=0, fontsize=12, fontweight='bold')
	ax13.annotate(labstring[7],xy = labellocation, fontsize=18, fontweight='bold')
	ax13.set_ylim(-85,85)
	ax13.annotate(str(-0.8) + '\%', xy = (DT.date(2101,2,1),55), fontsize = 10, fontweight = 'heavy')
	plt.subplot(Gsal[0,8:])
	
	yearssala = mdates.YearLocator()
	monthssala = mdates.MonthLocator()
	minorLocatorsala = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax14.axvline(x=volctimes[3], ymin=0, ymax = 0.8,color='k',ls='dashed')
	ax14.set_xlim(DT.date(2101,1,1), DT.date(2105,1,1))
	ax14.tick_params(axis="both", which="both", bottom="off", top="off", labeltop="off", labelbottom="off", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-45, 45]:    
	      ax14.plot(datas0[3][0][0][0:60], [z] *len(datas0[3][0][0][0:60]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -15, 15]:    
	      ax14.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	
	ax14.plot(datas0[3][0][0][22:],[75]*len(datas0[3][0][0][22:]), "--", lw= 0.5, color = "black", alpha=0.3)	
	ax14.xaxis.set_major_locator(yearssala)
	ax14.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax14.xaxis.set_minor_locator(monthssala)
	plt.xticks(rotation=0, fontsize=12, fontweight='bold')
	ax14.annotate(labstring[8],xy = labellocation, fontsize=18, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,73,90], [stringgy[w] for w in range(len(stringgy))], fontsize=9)
	for tick in ax14.yaxis.get_major_ticks():
		tick.set_pad(-22)
		tick.label2.set_horizontalalignment('left')
	ax14.set_ylim(-85,85)

	ax14.annotate(str(-1.3) + '\%', xy = (DT.date(2101,2,1),55),alpha = 1, fontsize = 10, fontweight = 'heavy')
	cbar_ax = fig.add_axes([0.025, 0.97, 0.97, 0.01])
	fmt = '%1.0f'
	tix =  levels
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt, orientation = 'horizontal')
	cbar_ax.tick_params(labelsize = 12)
	cbar.set_label('Percent change in column ozone', fontsize=12, fontweight='bold', labelpad = -33.3)


	plt.subplot(G26[0,0:9])
	ax6.plot(dateflat[0][17:], datas2[0][17:], 'k-', lw = 2, label = 'Tropical sulfate')
	years5 = mdates.YearLocator()
	months5 = mdates.MonthLocator()
	minorLocator5 = MultipleLocator(2.5)
	ax6.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax6.grid(False)
        ax6.xaxis.set_minor_locator(months5)
        ax6.xaxis.set_major_locator(years5)
        ax6.yaxis.set_minor_locator(minorLocator5)
        ax6.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax6.spines['top'].set_visible(True)
	ax6.spines['right'].set_visible(True)
	ax6.spines['bottom'].set_visible(True)
	ax6.spines['left'].set_visible(True)
        ax6.get_xaxis().tick_bottom()
        ax6.get_yaxis().tick_left()
	ax6.axvline(x=volctimes[0],color='k',ls='dashed')
	ax6.set_ylim(-3.5,0.75)
        plt.yticks([-3,-1.5,0], [str(x) + "\%" for x in [-3,-1.5,0]], fontsize=10, fontweight='bold', horizontalalignment = 'left')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in [-3,-1.5,0]:    
              ax6.plot(dateflat[0][18:], [y] *len(dateflat[0][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax6.yaxis.get_major_ticks():
		tick.set_pad(-1)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G45[0,0:9])
	years6 = mdates.YearLocator()
	months6 = mdates.MonthLocator()
	minorLocator6 = MultipleLocator(2.5)
	ax7.plot(dateflat[1][17:], datas2[1][17:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax7.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax7.grid(False)
        ax7.xaxis.set_minor_locator(months6)
        ax7.xaxis.set_major_locator(years6)
        ax7.yaxis.set_minor_locator(minorLocator6)
        ax7.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax7.spines['top'].set_visible(True)
	ax7.spines['right'].set_visible(True)
	ax7.spines['bottom'].set_visible(True)
	ax7.spines['left'].set_visible(True)
        ax7.get_xaxis().tick_bottom()
        ax7.get_yaxis().tick_left()
	ax7.axvline(x=volctimes[1],color='k',ls='dashed')
	ax7.set_ylim(-2.5,0.5)
        plt.yticks(range(-2,1,1), [str(x) + "\%" for x in range(-2,1,1)], fontsize=10, fontweight='bold', horizontalalignment = 'left')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in range(-2,1,1):    
              ax7.plot(dateflat[1][18:], [y] *len(dateflat[1][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax7.yaxis.get_major_ticks():
		tick.set_pad(-1)
		tick.label2.set_horizontalalignment('left')

	plt.subplot(G60[0,0:9])
	years8 = mdates.YearLocator()
	months8 = mdates.MonthLocator()
	minorLocator8 = MultipleLocator(2.5)
	ax8.plot(dateflat[2][17:], datas2[2][17:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax8.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax8.grid(False)
        ax8.xaxis.set_minor_locator(months8)
        ax8.xaxis.set_major_locator(years8)
        ax8.yaxis.set_minor_locator(minorLocator8)
        ax8.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax8.spines['top'].set_visible(True)
	ax8.spines['right'].set_visible(True)
	ax8.spines['bottom'].set_visible(True)
	ax8.spines['left'].set_visible(True)
        ax8.get_xaxis().tick_bottom()
        ax8.get_yaxis().tick_left()
	ax8.axvline(x=volctimes[0],color='k',ls='dashed')
	ax8.set_ylim(-1.5,1.5)
        plt.yticks(range(-1,2,1), [str(x) + "\%" for x in range(-1,2,1)], fontsize=10, horizontalalignment= 'left', fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in range(-1,2,1):    
              ax8.plot(dateflat[2][18:], [y] *len(dateflat[2][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax8.yaxis.get_major_ticks():
		tick.set_pad(-1)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G85[0,0:9])
	years9 = mdates.YearLocator()
	months9 = mdates.MonthLocator()
	minorLocator9 = MultipleLocator(2.5)
	ax9.plot(dateflat[3][17:], datas2[3][17:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax9.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax9.grid(False)
        ax9.xaxis.set_minor_locator(months9)
        ax9.xaxis.set_major_locator(years9)
        ax9.yaxis.set_minor_locator(minorLocator9)
        ax9.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax9.spines['top'].set_visible(True)
	ax9.spines['right'].set_visible(True)
	ax9.spines['bottom'].set_visible(True)
	ax9.spines['left'].set_visible(True)
        ax9.get_xaxis().tick_bottom()
        ax9.get_yaxis().tick_left()
	ax9.axvline(x=volctimes[3],color='k',ls='dashed')
	ax9.set_ylim(-0.35,1.25)
        plt.yticks([0,0.5,1], [str(x) + "\%" for x in [0,0.5,1]], fontsize=10, horizontalalignment= 'left', fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in [0,0.5,1]:    
              ax9.plot(dateflat[3][18:], [y] *len(dateflat[3][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax9.yaxis.get_major_ticks():
		tick.set_pad(-1)
		tick.label2.set_horizontalalignment('left')

	plt.subplot(Gsal[1:3,0:5])
	years10 = mdates.YearLocator()
	labellocation = (DT.date(2101,3,15), -3.1)
	months10 = mdates.MonthLocator()
	minorLocator10 = MultipleLocator(2.5)
	ax5.plot(dateflat[4][18:], datas2[4][18:], 'b-', lw = 2, label = '0 pptv VSL Br\nEESC: 704 pptv')
	ax5.plot(dateflat[5][18:], datas2[5][18:], 'g-', lw = 2, label = '2 pptv VSL Br\n824 pptv')
	ax5.plot(dateflat[6][18:], datas2[6][18:], 'k-', lw = 2, label = '4 pptv VSL Br\n944 pptv')
	ax5.plot(dateflat[7][18:], datas2[7][18:], 'orange', lw = 2, label = '6 pptv VSL Br\n1064 pptv')
	ax5.plot(dateflat[8][18:], datas2[8][18:], 'r-', lw = 2, label = '8 pptv VSL Br\n1184 pptv')
	ax5.set_xlim(DT.date(2101,3,1), DT.date(2105,1,1))
	ax5.grid(False)
        ax5.xaxis.set_minor_locator(months10)
        ax5.xaxis.set_major_locator(years10)
        ax5.yaxis.set_minor_locator(minorLocator10)
        ax5.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax5.spines['top'].set_visible(True)
	ax5.spines['right'].set_visible(True)
	ax5.spines['bottom'].set_visible(True)
	ax5.spines['left'].set_visible(True)
        ax5.get_xaxis().tick_bottom()
        ax5.get_yaxis().tick_left()
	ax5.axvline(x=volctimes[4],color='k',ls='dashed')
	ax5.set_ylim(-3.5,2.4)
	ax5.set_ylabel('VSL Br sensitivity\n  RCP 6.0', fontsize=12, fontweight='bold')
	ax5.yaxis.set_label_coords(0, 0.7)
        plt.yticks([-2,0,2], [str(x) + "\%" for x in [-2,0,2]], fontsize=10, fontweight='bold', horizontalalignment = 'left')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on", labelright = "off")  
	plt.xticks(rotation=0, fontsize=12, fontweight='bold')
 	for y in range(-2,3,1):    
              ax5.plot(dateflat[4][18:], [y] *len(dateflat[4][18:]), "--", lw=1, color="black", alpha=0.3)
       	ax5.plot(dateflat[4][18:], [0]*len(dateflat[4][18:]), "--", lw=2, color = "black", alpha = 0.3)
       	ax5.plot(dateflat[4][18:47], [-3]*len(dateflat[4][18:47]), "--", lw=1, color = "black", alpha = 0.3)
#	ax5.axvspan(dateflat[4][0], volctimes[4], alpha = 0.5, color = 'lightblue')
	for tick in ax5.yaxis.get_major_ticks():
		tick.set_pad(-1)
		tick.label2.set_horizontalalignment('left')       
	ax5.annotate(labstring[9],xy = labellocation, fontsize=18, fontweight='bold')
        handles, labels = ax5.get_legend_handles_labels()
        ax5.legend(handles, labels, bbox_to_anchor=(1,1.87),frameon = False, loc = 'upper center',ncol = 5, fancybox = False, fontsize=11, columnspacing = 4.75,  handletextpad = 0.15) 
	ax5.set_xlabel('Model year', fontsize=12, fontweight='bold')	
	ax5.annotate('Column ozone deviation', xy = (DT.date(2103,7,25), -3), fontsize = 12,verticalalignment= 'center', fontweight = 'heavy')

	plt.subplot(G26[1:3,9])
	ax15.plot(dataslat[0], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax15.grid(False)
        ax15.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax15.spines['top'].set_visible(True)
	ax15.spines['right'].set_visible(True)
	ax15.spines['bottom'].set_visible(True)
	ax15.spines['left'].set_visible(True)
        ax15.get_xaxis().tick_bottom()
        ax15.get_yaxis().tick_left()
	ax15.set_ylim(-85,85)
	ax15.set_xlim(-3.5, 0.7)
	ax15.set_xlabel('EESC(3 year): 996 pptv', fontsize = 12, fontweight = 'heavy', horizontalalignment='right')
	ax15.xaxis.set_label_coords(1,-0.17)
        plt.xticks([-3,0], [str(x) + "\%" for x in [-3,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-3,-1.5,0]:    
              ax15.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax15.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G26[0,9])
	ax19.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax19.set_xlim(-1,1)
	ax19.set_ylim(-1,1)
	ax19.annotate(str(totalcol[0])[0:4] + '\%', xy = (0,0), fontsize = 12, horizontalalignment = 'center', verticalalignment = 'center', fontweight = 'heavy')
	ax19.xaxis.set_label_coords(1,1.525)
	ax19.set_xlabel('Global-temporal\n average', fontsize = 12, fontweight = 'heavy', horizontalalignment = 'right')
	ax19.xaxis.set_label_coords(1,1.53)	

	plt.subplot(G45[1:3,9])
	ax16.plot(dataslat[1], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax16.grid(False)
        ax16.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax16.spines['top'].set_visible(True)
	ax16.spines['right'].set_visible(True)
	ax16.spines['bottom'].set_visible(True)
	ax16.spines['left'].set_visible(True)
        ax16.get_xaxis().tick_bottom()
        ax16.get_yaxis().tick_left()
	ax16.set_ylim(-85,85)
	ax16.set_xlim(-2.5, 0.5)
	ax16.set_xlabel('921 pptv', fontsize = 12, fontweight = 'heavy', horizontalalignment='right')
	ax16.xaxis.set_label_coords(1,-0.17)
        plt.xticks([-2,0], [str(x) + "\%" for x in [-2,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-2,-1,0]:    
              ax16.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax16.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G45[0,9])
	ax20.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax20.set_xlim(-1,1)
	ax20.set_ylim(-1,1)
	ax20.annotate(str(totalcol[1])[0:4] + '\%', xy = (0,0), fontsize = 12, horizontalalignment = 'center', verticalalignment = 'center', fontweight = 'heavy')
	ax20.xaxis.set_label_coords(1,1.525)
	
	plt.subplot(G60[1:3,9])
	ax17.plot(dataslat[2], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax17.grid(False)
        ax17.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax17.spines['top'].set_visible(True)
	ax17.spines['right'].set_visible(True)
	ax17.spines['bottom'].set_visible(True)
	ax17.spines['left'].set_visible(True)
        ax17.get_xaxis().tick_bottom()
        ax17.get_yaxis().tick_left()
	ax17.set_ylim(-85,85)
	ax17.set_xlim(-2.25,0.5)
	ax17.set_xlabel('944 pptv', fontsize = 12, fontweight = 'heavy', horizontalalignment='right')
	ax17.xaxis.set_label_coords(1,-0.17)
        plt.xticks([-2, 0], [str(x) + "\%" for x in [-2,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-2,-1, 0]:    
              ax17.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax17.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G60[0,9])
	ax21.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax21.set_xlim(-1,1)
	ax21.set_ylim(-1,1)
	ax21.annotate(str(totalcol[2])[0:4] + '\%', xy = (0,0), horizontalalignment = 'center', verticalalignment = 'center', fontsize = 12, fontweight = 'heavy')
	ax21.xaxis.set_label_coords(1,1.525)
	
	plt.subplot(G85[1:3,9])
	ax18.plot(dataslat[3], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax18.grid(False)
        ax18.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax18.spines['top'].set_visible(True)
	ax18.spines['right'].set_visible(True)
	ax18.spines['bottom'].set_visible(True)
	ax18.spines['left'].set_visible(True)
        ax18.get_xaxis().tick_bottom()
        ax18.get_yaxis().tick_left()
	ax18.set_ylim(-85,85)
	ax18.set_xlim(-1.25, 1.45)
	ax18.set_xlabel('932 pptv', fontsize = 12, fontweight = 'heavy', horizontalalignment='right')
	ax18.xaxis.set_label_coords(1,-0.17)
        plt.xticks([-1,1], [str(x) + "\%" for x in [-1,1]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-1,0,1]:    
              ax18.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax18.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G85[0,9])
	ax22.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax22.set_xlim(-1,1)
	ax22.set_ylim(-1,1)
	ax22.annotate( '+0.2' + '\%', xy = (0,0), fontsize = 12,horizontalalignment = 'center', verticalalignment= 'center', fontweight = 'heavy')
	ax22.xaxis.set_label_coords(1,1.525)

	plt.subplot(Gsal[1:3,5:])
	labellocation = (-3.4,-80)
	ax23.plot(dataslat[4], lats, 'b-', lw = 2, label = '0 pptv VSL Br')
	ax23.plot(dataslat[5], lats, 'g-', lw = 2, label = '2 pptv VSL Br')
	ax23.plot(dataslat[6], lats, 'k-', lw = 2, label = '4 pptv VSL Br')
	ax23.plot(dataslat[7], lats, 'orange', lw = 2, label = '6 pptv VSL Br')
	ax23.plot(dataslat[8], lats, 'r-', lw = 2, label = '8 pptv VSL Br')
	ax23.grid(False)
        ax23.tick_params(axis = 'both', which = 'major', labelsize = 10, zorder = 10)
        ax23.spines['top'].set_visible(True)
	ax23.spines['right'].set_visible(True)
	ax23.spines['bottom'].set_visible(True)
	ax23.spines['left'].set_visible(True)
        ax23.get_xaxis().tick_bottom()
        ax23.get_yaxis().tick_left()
	ax23.set_ylim(-85,85)
	ax23.set_xlim(-3.5, 2)
	ax23.set_xlabel('Time-averaged column ozone deviation', fontsize = 12, fontweight = 'heavy')
        plt.xticks([-3,-2,-1,0,1], [str(x) + "\%" for x in [-3,-2,-1,0,1]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-3,-2,-1,0,1]:    
              ax23.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax23.xaxis.get_major_ticks():
		tick.set_pad(1)
		tick.label2.set_horizontalalignment('left')
	ax23.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	
	ax23.annotate(labstring[10],xy = labellocation, fontsize=18, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold', zorder = 10)
	for tick in ax23.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax23.set_ylim(-85,85)
	for z in [-90,-60,-30,30,60,90]:    
	      ax23.plot(lats, [z] *len(lats), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45,75]:    
	      ax23.plot(lats, [z] *len(lats), "--", lw=0.5, color="black", alpha=0.3, zorder = 0)
	ax23.plot(lats,[0]*len(lats), "--", lw = 2, color = "black", alpha = 0.3)
       	ax23.axvspan(1.75, 3, alpha = 1, color = 'white', zorder = 1)


def figure3(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global ax1,ax2,ax3,ax4, ax5, ax6,ax7,ax8,ax9, ax10, ax11, ax12,fig,cbar, plt, levels, datas0,datas1,datas2, dataslat, volcinjectlats

	datas0 = []
	datas1 = []
	datas2 = []
	dateflat = []
	CS = []
	volctimes = []
	latarray = []
	dataslat = []	
	totalcol = []

	datas0.append(datamodulator(var, dayt, 5, 0,1, 2100, num, flag))
	datas0.append(datamodulator(var, dayt, 5, 0,3, 2100, num, flag))
	datas0.append(datamodulator(var, dayt, 5, 0,5, 2100, num, flag))
	datas2.append(datamodulator(var, dayt, 3, 0,1, 2017, num, flag))
	datas2.append(datamodulator(var, dayt, 3, 0,3, 2017, num, flag))
	datas2.append(datamodulator(var, dayt, 3, 0,5, 2017, num, flag))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	
	datas1.append(datas0[0][2].mean(0))
	datas1.append(datas0[1][2].mean(0))
	datas1.append(datas0[2][2].mean(0))
	datas1.append(datas2[0][2].mean(0))
	datas1.append(datas2[1][2].mean(0))
	datas1.append(datas2[2][2].mean(0))

	dateflat.append(datas0[0][0][0])
	dateflat.append(datas0[1][0][0])
	dateflat.append(datas0[2][0][0])
	dateflat.append(datas2[0][0][0])
	dateflat.append(datas2[1][0][0])
	dateflat.append(datas2[2][0][0])

	for x in range(len(datas0)):
		latarray = []
		for y in range(len(datas0[0][0])):
			latarray.append(datas0[x][2][y][20:72].mean())
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))

	lats = datas0[0][1].mean(1)

	for x in range(len(datas2)):
		latarray = []
		for y in range(len(datas2[0][0])):
			latarray.append(np.nanmean(datas2[x][2][y][20:72]))
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))

	volclattropichigh = latitude_edges[12] - 15.9
	volclattropiclow = 15.9 - latitude_edges[10]
	levels =  np.array([-80,-70,-60,-50,-40,-30,-25,-20, -15,-10,-8, -6,-4,-2,-1,1,2,])
#	levels =  np.array([-80,-70,-60,-50,-40,-30,-20,-10,0,10,20])
	
	plt.figure
	Gs = gridspec.GridSpec(3,2, hspace = 0.15)
	G0 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[0,1], hspace =0, wspace = 0)
	G1 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[1,1],hspace = 0, wspace = 0)
	G2 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[2,1], hspace = 0, wspace =0)

	G3 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[0,0], hspace =0, wspace = 0)
	G4 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[1,0],hspace = 0, wspace = 0)
	G5 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[2,0], hspace = 0, wspace = 0)
	ax1 = plt.subplot(G0[2:,0:6])
	ax2= plt.subplot(G1[2:,0:6])
	ax3 = plt.subplot(G2[2:,0:6])
	
	ax4 = plt.subplot(G3[2:,0:6])
	ax5= plt.subplot(G4[2:,0:6])
	ax6 = plt.subplot(G5[2:,0:6])
	ax10 = plt.subplot(G0[0:2,0:6])
	ax11 = plt.subplot(G1[0:2,0:6])
	ax12 = plt.subplot(G2[0:2,0:6])

	ax7 = plt.subplot(G3[0:2,0:6])
	ax8 = plt.subplot(G4[0:2,0:6])
	ax9 = plt.subplot(G5[0:2,0:6])
	
	ax13 = plt.subplot(G0[2:,6])
	ax14 = plt.subplot(G1[2:,6])
	ax15 = plt.subplot(G2[2:,6])
	ax16 = plt.subplot(G3[2:,6])
	ax17 = plt.subplot(G4[2:,6])
	ax18 = plt.subplot(G5[2:,6])

	ax19 = plt.subplot(G0[0:2,6])
	ax20 = plt.subplot(G1[0:2,6])
	ax21 = plt.subplot(G2[0:2,6])
	ax22 = plt.subplot(G3[0:2,6])
	ax23 = plt.subplot(G4[0:2,6])
	ax24 = plt.subplot(G5[0:2,6])

	
	fig = plt.gcf()
	fig.set_facecolor('white')
	
	plt.subplot(G0[2:,0:6])
	CS1 =plt.contourf(datas0[0][0],datas0[0][1],datas0[0][2],levels, cmap = cma)
	
	plt.subplot(G1[2:,0:6])
	CS2 = plt.contourf(datas0[1][0],datas0[1][1],datas0[1][2],levels, cmap = cma)
	
	plt.subplot(G2[2:,0:6])
	CS3 =plt.contourf(datas0[2][0],datas0[2][1],datas0[2][2],levels, cmap = cma)

	plt.subplot(G3[2:,0:6])
	CS4 =plt.contourf(datas2[0][0],datas2[0][1],datas2[0][2],levels, cmap = cma)
	
	plt.subplot(G4[2:,0:6])
	CS5 = plt.contourf(datas2[1][0],datas2[1][1],datas2[1][2],levels, cmap = cma)
	
	plt.subplot(G5[2:,0:6])
	CS6 =plt.contourf(datas2[2][0],datas2[2][1],datas2[2][2],levels, cmap = cma)
	
	label2100location = (DT.date(2101,1,25), -75)
	years2100 = mdates.YearLocator()
	months2100 = mdates.MonthLocator()
	minorLocator2100 = MultipleLocator(2.5)

	label2018location = (DT.date(2018,1,25), -75)
	years2018 = mdates.YearLocator()
	months2018 = mdates.MonthLocator()
	minorLocator2018 = MultipleLocator(2.5)
	stringy = []
	stringy = ['','75$^{\circ}$S','', '45$^{\circ}$S','', '15$^{\circ}$S','', '15$^{\circ}$N','', '45$^{\circ}$N','', '75$^{\circ}$N', '']
	labstring = ['b', 'd', 'f','a','c','e','g','h','i','j','k','l']
	
	plt.subplot(G0[2:,0:6])

	
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_xlim(DT.date(2100,11,1), DT.date(2105,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax1.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax1.plot(datas0[2][0][0][0:67], [z] *len(datas0[2][0][0][0:67]), "--", lw=0.5, color="black", alpha=0.3)
	ax1.plot(datas0[0][0][0],[0]*len(datas0[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax1.xaxis.set_major_locator(years2100)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax1.xaxis.set_minor_locator(months2100)
	ax1.annotate(labstring[0],xy = label2100location, fontsize = 18, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax1.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')
	ax1.set_ylim(-85,85)

	plt.subplot(G1[2:,0:6])
	
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_xlim(DT.date(2100,11,1), DT.date(2105,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax2.plot(datas0[1][0][0], [z] *len(datas0[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax2.plot(datas0[2][0][0][0:67], [z] *len(datas0[2][0][0][0:67]), "--", lw=0.5, color="black", alpha=0.3)
	ax2.plot(datas0[1][0][0],[0]*len(datas0[1][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax2.scatter(volctimes[1], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.xaxis.set_major_locator(years2100)
	ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax2.xaxis.set_minor_locator(months2100)
	ax2.annotate(labstring[1],xy = label2100location, fontsize = 18, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,73,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax2.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')	
	ax2.set_ylim(-85,85)

	plt.subplot(G2[2:,0:6])
	
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_xlim(DT.date(2100,11,1), DT.date(2105,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax3.plot(datas0[2][0][0], [z] *len(datas0[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax3.plot(datas0[2][0][0][0:67], [z] *len(datas0[2][0][0][0:67]), "--", lw=0.5, color="black", alpha=0.3)
	ax3.plot(datas0[2][0][0],[0]*len(datas0[2][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax3.scatter(volctimes[2], 15.9,  s = 100,color = 'k', marker= '^')
#	ax3.set_xlabel('Model year (RCP 6.0)', fontsize = 10, fontweight='bold')
#	ax3.xaxis.set_label_coords(0.5, -0.22)
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax3.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax3.set_ylim(-85,85)
	ax3.xaxis.set_major_locator(years2100)
	ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax3.xaxis.set_minor_locator(months2100)
	ax3.annotate(labstring[2],xy = label2100location, fontsize = 18, fontweight = 'bold')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')
	ax3.set_ylim(-85,85)

	plt.subplot(G0[0:2,0:6])
	ax10.plot(dateflat[0][17:], datas1[0][17:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax10.set_xlim(DT.date(2100,11,1), DT.date(2105,7,1))
	ax10.grid(False)
        ax10.xaxis.set_minor_locator(months2100)
        ax10.xaxis.set_major_locator(years2100)
        ax10.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax10.spines['top'].set_visible(True)
	ax10.spines['right'].set_visible(True)
	ax10.spines['bottom'].set_visible(True)
	ax10.spines['left'].set_visible(True)
        ax10.get_xaxis().tick_bottom()
        ax10.get_yaxis().tick_left()
	ax10.axvline(x=volctimes[0],color='k',ls='dashed')
	ax10.set_ylim(-1.6,1.6)
        plt.yticks([-1, 0,1], [str(x) + "\%" for x in [-1,0, 1]], fontsize=10, horizontalalignment = 'left',  fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-1,0,1]:    
              ax10.plot(dateflat[0][17:], [y] *len(dateflat[0][17:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax10.yaxis.get_major_ticks():
		tick.set_pad(-285)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G1[0:2,0:6])
	ax11.plot(dateflat[1][17:], datas1[1][17:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax11.set_xlim(DT.date(2100,11,1), DT.date(2105,7,1))
	ax11.grid(False)
        ax11.xaxis.set_minor_locator(months2100)
        ax11.xaxis.set_major_locator(years2100)
        ax11.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax11.spines['top'].set_visible(True)
	ax11.spines['right'].set_visible(True)
	ax11.spines['bottom'].set_visible(True)
	ax11.spines['left'].set_visible(True)
        ax11.get_xaxis().tick_bottom()
        ax11.get_yaxis().tick_left()
	ax11.axvline(x=volctimes[1],color='k',ls='dashed')
	ax11.set_ylim(-5,1.5)

        plt.yticks([-4,-2,0], [str(x) + "\%" for x in [-4,-2,0]],horizontalalignment = 'left', fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-4,-2,0]:    
              ax11.plot(dateflat[1][17:], [y] *len(dateflat[1][17:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax11.yaxis.get_major_ticks():
		tick.set_pad(-285)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G2[0:2,0:6])
	ax12.plot(dateflat[2][17:], datas1[2][17:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax12.set_xlim(DT.date(2100,11,1), DT.date(2105,7,1))
	ax12.grid(False)
        ax12.xaxis.set_minor_locator(months2100)
        ax12.xaxis.set_major_locator(years2100)
        ax12.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax12.spines['top'].set_visible(True)
	ax12.spines['right'].set_visible(True)
	ax12.spines['bottom'].set_visible(True)
	ax12.spines['left'].set_visible(True)
        ax12.get_xaxis().tick_bottom()
        ax12.get_yaxis().tick_left()
	ax12.axvline(x=volctimes[2],color='k',ls='dashed')
	ax12.set_ylim(-27,7)
        plt.yticks([-20,-10,0], [str(x) + "\%" for x in [-20,-10,0]], horizontalalignment = 'left', fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-20,-10,0]:    
              ax12.plot(dateflat[2][17:], [y] *len(dateflat[2][17:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax12.yaxis.get_major_ticks():
		tick.set_pad(-285)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G3[2:,0:6])

	
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax4.plot(datas2[0][0][0], [z] *len(datas2[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax4.plot(datas2[2][0][0][0:67], [z] *len(datas2[2][0][0][0:67]), "--", lw=0.5, color="black", alpha=0.3)
	ax4.plot(datas2[0][0][0],[0]*len(datas2[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax4.scatter(volctimes[3], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax4.xaxis.set_major_locator(years2018)
	ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax4.xaxis.set_minor_locator(months2018)
	ax4.annotate(labstring[3],xy = label2018location, fontsize = 18, fontweight = 'bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax4.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')
	ax4.set_ylabel('Latitudinal column deviations \n Sulfur dioxide only', fontsize = 12, fontweight = 'bold')
	ax4.yaxis.set_label_coords(-0.002, 0.70)
	ax4.set_xlabel('Temporal column ozone deviations', fontsize = 12, fontweight = 'heavy', horizontalalignment = 'left')
	ax4.xaxis.set_label_coords(0,1.5)
	ax4.set_ylim(-85,85)

	plt.subplot(G4[2:,0:6])
	
	ax5.axvline(x=volctimes[4],color='k',ls='dashed')
	ax5.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax5.plot(datas2[1][0][0], [z] *len(datas2[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax5.plot(datas2[2][0][0][0:67], [z] *len(datas2[2][0][0][0:67]), "--", lw=0.5, color="black", alpha=0.3)
	ax5.plot(datas2[1][0][0],[0]*len(datas2[1][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax5.scatter(volctimes[4], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[4],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax5.xaxis.set_major_locator(years2018)
	ax5.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax5.xaxis.set_minor_locator(months2018)
	ax5.annotate(labstring[4],xy = label2018location, fontsize = 18, fontweight = 'bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax5.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')	
	ax5.set_ylabel('Co-injected halogen', fontsize = 12, fontweight = 'bold')
	ax5.yaxis.set_label_coords(-0.002, 0.70)
	ax5.set_ylim(-85,85)
	
	plt.subplot(G5[2:,0:6])
	
	ax6.axvline(x=volctimes[5],color='k',ls='dashed')
	ax6.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax6.plot(datas2[2][0][0], [z] *len(datas2[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax6.plot(datas2[2][0][0][0:67], [z] *len(datas2[2][0][0][0:67]), "--", lw=0.5, color="black", alpha=0.3)
	ax6.plot(datas2[2][0][0],[0]*len(datas2[2][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax6.scatter(volctimes[5], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[5],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax6.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax6.set_ylim(-85,85)
	ax6.xaxis.set_major_locator(years2018)
	ax6.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax6.xaxis.set_minor_locator(months2018)
	ax6.annotate(labstring[5],xy = label2018location, fontsize = 18, fontweight = 'bold')
	ax6.set_ylabel('High co-injected halogen', fontsize = 12, fontweight = 'bold')
	ax6.yaxis.set_label_coords(-0.002, 0.70)
#	ax6.set_xlabel('Model year', fontsize = 12, fontweight='bold', horizontalalignment = 'left')
	ax6.xaxis.set_label_coords(-0.02, -0.2)
	ax6.set_ylim(-85,85)
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')

	plt.subplot(G3[0:2,0:6])
	ax7.plot(dateflat[3][17:], datas1[3][17:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax7.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax7.grid(False)
        ax7.xaxis.set_minor_locator(months2018)
        ax7.xaxis.set_major_locator(years2018)
        ax7.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax7.spines['top'].set_visible(True)
	ax7.spines['right'].set_visible(True)
	ax7.spines['bottom'].set_visible(True)
	ax7.spines['left'].set_visible(True)
        ax7.get_xaxis().tick_bottom()
        ax7.get_yaxis().tick_left()
	ax7.axvline(x=volctimes[3],color='k',ls='dashed')
	ax7.set_ylim(-7.5,2)
	plt.yticks([-6, -3,0], [str(x) + "\%" for x in [-6,-3, 0]], fontsize=10, horizontalalignment = 'left', fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-6,-3,0]:    
              ax7.plot(dateflat[3][17:], [y] *len(dateflat[3][17:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax7.yaxis.get_major_ticks():
		tick.set_pad(-285)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G4[0:2,0:6])
	ax8.plot(dateflat[4][17:], datas1[4][17:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax8.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax8.grid(False)
        ax8.xaxis.set_minor_locator(months2018)
        ax8.xaxis.set_major_locator(years2018)
        ax8.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax8.spines['top'].set_visible(True)
	ax8.spines['right'].set_visible(True)
	ax8.spines['bottom'].set_visible(True)
	ax8.spines['left'].set_visible(True)
        ax8.get_xaxis().tick_bottom()
        ax8.get_yaxis().tick_left()
	ax8.axvline(x=volctimes[4],color='k',ls='dashed')
	ax8.set_ylim(-10,3)
        plt.yticks([-8,-4], [str(x) + "\%" for x in [-8,-4]], fontsize=10, fontweight='bold')
	plt.yticks([-8,-4, 0], ['-8\%', '-4\%', '0\%\  '], fontsize = 10, fontweight = 'bold', horizontalalignment = 'left')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-8,-4,0]:    
              ax8.plot(dateflat[4][17:], [y] *len(dateflat[4][17:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax8.yaxis.get_major_ticks():
		tick.set_pad(-285)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G5[0:2,0:6])
	ax9.plot(dateflat[5][17:], datas1[5][17:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax9.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax9.grid(False)
        ax9.xaxis.set_minor_locator(months2018)
        ax9.xaxis.set_major_locator(years2018)
        ax9.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax9.spines['top'].set_visible(True)
	ax9.spines['right'].set_visible(True)
	ax9.spines['bottom'].set_visible(True)
	ax9.spines['left'].set_visible(True)
        ax9.get_xaxis().tick_bottom()
        ax9.get_yaxis().tick_left()
	ax9.axvline(x=volctimes[5],color='k',ls='dashed')
	ax9.set_ylim(-26,7)
        plt.yticks([-20,-10, 0],['-20\%','-10\%','$\ $0\%'], fontsize=10,horizontalalignment = 'left', fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-20,-10,0]:    
              ax9.plot(dateflat[5][17:], [y] *len(dateflat[5][17:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax9.yaxis.get_major_ticks():
		tick.set_pad(-285)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G0[2:,6])
	ax13.plot(dataslat[0], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax13.grid(False)
        ax13.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax13.spines['top'].set_visible(True)
	ax13.spines['right'].set_visible(True)
	ax13.spines['bottom'].set_visible(True)
	ax13.spines['left'].set_visible(True)
        ax13.get_xaxis().tick_bottom()
        ax13.get_yaxis().tick_left()
	ax13.set_ylim(-85,85)
	ax13.set_xlim(-2.25,0.6)
	ax13.xaxis.set_label_coords(1,1.6)
        plt.xticks([-2, 0], [str(x) + "\%" for x in [-2,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-2,-1, 0]:    
              ax13.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax13.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G0[0:2,6])
	ax19.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax19.set_xlim(-1,1)
	ax19.set_ylim(-1,1)
	ax19.annotate(str(totalcol[0])[0:4] + '\%', xy = (0,0), fontsize = 14, horizontalalignment='center',verticalalignment='center',fontweight = 'heavy')
	ax19.xaxis.set_label_coords(1,1.525)

	plt.subplot(G1[2:,6])
	ax14.plot(dataslat[1], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax14.grid(False)
        ax14.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax14.spines['top'].set_visible(True)
	ax14.spines['right'].set_visible(True)
	ax14.spines['bottom'].set_visible(True)
	ax14.spines['left'].set_visible(True)
        ax14.get_xaxis().tick_bottom()
        ax14.get_yaxis().tick_left()
	ax14.set_ylim(-85,85)
	ax14.set_xlim(-9,2.5)
	ax14.xaxis.set_label_coords(1,2.5)
        plt.xticks([-8, 0], [str(x) + "\%" for x in [-8,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-8,-4, 0]:    
              ax14.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax14.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G1[0:2,6])
	ax20.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax20.set_xlim(-1,1)
	ax20.set_ylim(-1,1)
	ax20.annotate(str(totalcol[1])[0:4] + '\%', xy = (0,0), horizontalalignment='center', verticalalignment='center',fontsize = 14, fontweight = 'heavy')
	ax20.xaxis.set_label_coords(1,1.525)


	plt.subplot(G2[2:,6])
	ax15.plot(dataslat[2], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax15.grid(False)
        ax15.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax15.spines['top'].set_visible(True)
	ax15.spines['right'].set_visible(True)
	ax15.spines['bottom'].set_visible(True)
	ax15.spines['left'].set_visible(True)
        ax15.get_xaxis().tick_bottom()
        ax15.get_yaxis().tick_left()
	ax15.set_ylim(-85,85)
	ax15.set_xlim(-30,8)
	ax15.xaxis.set_label_coords(-2.5,-0.17)
	ax15.set_xlabel('Future scenarios', fontsize = 12, fontweight = 'heavy', horizontalalignment = 'center')
        plt.xticks([-25, 0], [str(x) + "\%" for x in [-25,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-25,-12.5, 0]:    
              ax15.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax15.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2[0:2,6])
	ax21.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax21.set_xlim(-1,1)
	ax21.set_ylim(-1,1)
	ax21.annotate('-12\%', xy = (0,0), fontsize = 14,horizontalalignment = 'center', verticalalignment = 'center', fontweight = 'heavy')
	ax21.xaxis.set_label_coords(1,1.525)


	plt.subplot(G3[2:,6])
	ax16.plot(dataslat[3], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax16.grid(False)
        ax16.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax16.spines['top'].set_visible(True)
	ax16.spines['right'].set_visible(True)
	ax16.spines['bottom'].set_visible(True)
	ax16.spines['left'].set_visible(True)
        ax16.get_xaxis().tick_bottom()
        ax16.get_yaxis().tick_left()
	ax16.set_ylim(-85,85)
	ax16.set_xlim(-6,1.5)
	ax16.xaxis.set_label_coords(1,1.6)
        plt.xticks([-5, 0], [str(x) + "\%" for x in [-5,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-5,-2.5, 0]:    
              ax16.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax16.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G3[0:2,6])
	ax22.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax22.set_xlim(-1,1)
	ax22.set_ylim(-1,1)
	ax22.annotate(str(totalcol[3])[0:4] + '\%', xy = (0,0), fontsize = 14, fontweight = 'heavy', horizontalalignment = 'center', verticalalignment = 'center')
	ax22.xaxis.set_label_coords(1,1.525)

	ax22.set_xlabel('Global-temporal\naverage', fontsize = 12, horizontalalignment='right', fontweight = 'heavy')
	ax22.xaxis.set_label_coords(1,1.5)

	plt.subplot(G4[2:,6])
	ax17.plot(dataslat[4], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax17.grid(False)
        ax17.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax17.spines['top'].set_visible(True)
	ax17.spines['right'].set_visible(True)
	ax17.spines['bottom'].set_visible(True)
	ax17.spines['left'].set_visible(True)
        ax17.get_xaxis().tick_bottom()
        ax17.get_yaxis().tick_left()
	ax17.set_ylim(-85,85)
	ax17.set_xlim(-10,3)
	ax17.xaxis.set_label_coords(1,1.6)
        plt.xticks([-9, 0], [str(x) + "\%" for x in [-8,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-8,-4, 0]:    
              ax17.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax17.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G4[0:2,6])
	ax23.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax23.set_xlim(-1,1)
	ax23.set_ylim(-1,1)
	ax23.annotate(str(totalcol[4])[0:4] + '\%', xy = (0,0), horizontalalignment = 'center', verticalalignment = 'center',fontsize = 14, fontweight = 'heavy')
	ax23.xaxis.set_label_coords(1,1.525)


	plt.subplot(G5[2:,6])
	ax18.plot(dataslat[5], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax18.grid(False)
        ax18.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax18.spines['top'].set_visible(True)
	ax18.spines['right'].set_visible(True)
	ax18.spines['bottom'].set_visible(True)
	ax18.spines['left'].set_visible(True)
        ax18.get_xaxis().tick_bottom()
        ax18.get_yaxis().tick_left()
	ax18.set_ylim(-85,85)
	ax18.set_xlim(-30,8)
	ax18.xaxis.set_label_coords(-2.5,-0.17)
	ax18.set_xlabel('Contemporary scenarios', fontsize = 12, fontweight = 'heavy', horizontalalignment = 'center')
        plt.xticks([-25, 0], [str(x) + "\%" for x in [-25,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-25,-12.5, 0]:    
              ax18.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax18.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G5[0:2,6])
	ax24.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax24.set_xlim(-1,1)
	ax24.set_ylim(-1,1)
	ax24.annotate('-14\%', xy = (0.0,0),verticalalignment = 'center', horizontalalignment = 'center',fontsize = 14, fontweight = 'heavy')
	ax24.xaxis.set_label_coords(1,1.525)


	cbar_ax = fig.add_axes([0.025, 0.95, 0.962, 0.02])
	fmt = '%2.0f'
	tix =  levels
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt, orientation = 'horizontal')
	cbar_ax.tick_params(labelsize = 12)
	cbar.set_label('Percent change in column ozone', fontsize = 12, fontweight = 'bold', labelpad = -43)

def figure4(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global Gs, ax1,ax2,ax3,ax4, ax5, ax6,ax7,ax8,ax9, ax10, ax11, ax12,fig,cbar, plt, levels, datas0,datas1,datas2, volcinjectlats



	datas0 = []
	datas1 = []
	datas2 = []
	datas3 = []
	dateflat = []
	CS = []
	years = [2017]
	volcdays = [531] 
	volctimes = []
	

	
	datas0.append(datamodulator(var, dayt, 4, 0,1, 2017, num, flag))
	datas0.append(datamodulator(var, dayt, 2, 0,1, 2017, num, flag))
	datas0.append(datamodulator(var, dayt, 0, 0,1, 2017, num, flag))
	
	datas1.append(datamodulator(var, dayt, 4, 0,2, 2017, num, flag))
	datas1.append(datamodulator(var, dayt, 2, 0,2, 2017, num, flag))
	datas1.append(datamodulator(var, dayt, 0, 0,2, 2017, num, flag))


	datas2.append(datamodulator(var, dayt, 4, 0,3, 2017, num, flag))
	datas2.append(datamodulator(var, dayt, 2, 0,3, 2017, num, flag))
	datas2.append(datamodulator(var, dayt, 0, 0,3, 2017, num, flag))
	
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	



	volclatarctichigh = latitude_edges[18] - 72
	volclatmidlathigh = latitude_edges[15] - 41
	volclattropichigh = latitude_edges[12] - 15.9
	volclatarcticlow = 72 - latitude_edges[16]
	volclatmidlatlow = 41 - latitude_edges[13]
	volclattropiclow = 15.9 - latitude_edges[10]


	latarray = []
	dataslat = []	
	totalcol = []

	
	datas3.append(datas0[0][2].mean(0))
	datas3.append(datas1[0][2].mean(0))
	datas3.append(datas2[0][2].mean(0))
	datas3.append(datas0[1][2].mean(0))
	datas3.append(datas1[1][2].mean(0))
	datas3.append(datas2[1][2].mean(0))
	datas3.append(datas0[2][2].mean(0))
	datas3.append(datas1[2][2].mean(0))
	datas3.append(datas2[2][2].mean(0))

	dateflat.append(datas0[0][0][0])
	dateflat.append(datas0[1][0][0])
	dateflat.append(datas0[2][0][0])
	dateflat.append(datas1[0][0][0])
	dateflat.append(datas1[1][0][0])
	dateflat.append(datas1[2][0][0])
	dateflat.append(datas2[0][0][0])
	dateflat.append(datas2[1][0][0])
	dateflat.append(datas2[2][0][0])

	for x in range(len(datas0)):
		latarray = []
		for y in range(len(datas0[0][0])):
			latarray.append(datas0[x][2][y][20:72].mean())
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))

	for x in range(len(datas1)):
		latarray = []
		for y in range(len(datas1[0][0])):
			latarray.append(datas1[x][2][y][20:72].mean())
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))
	for x in range(len(datas2)):
		latarray = []
		for y in range(len(datas2[0][0])):
			latarray.append(datas2[x][2][y][20:72].mean())
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))

	lats = datas0[0][1].mean(1)


	levels =  np.array([-70,-60,-50,-40,-30,-25,-20, -15,-10,-8, -6,-4,-2,-1,0])
	
	plt.figure
	Gs = gridspec.GridSpec(3,3, hspace = 0.15, wspace = 0.05)
	G0 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[0,0], hspace =0, wspace = 0)
	G1 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[1,0],hspace = 0, wspace = 0)
	G2 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[2,0], hspace = 0, wspace =0)

	G3 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[0,1], hspace =0, wspace = 0)
	G4 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[1,1],hspace = 0, wspace = 0)
	G5 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[2,1], hspace = 0, wspace = 0)

	G6 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[0,2], hspace =0, wspace = 0)
	G7 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[1,2],hspace = 0, wspace = 0)
	G8 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[2,2], hspace = 0, wspace = 0)

	ax1 = plt.subplot(G0[2:,0:6])
	ax2= plt.subplot(G1[2:,0:6])
	ax3 = plt.subplot(G2[2:,0:6])
	
	ax4 = plt.subplot(G3[2:,0:6])
	ax5= plt.subplot(G4[2:,0:6])
	ax6 = plt.subplot(G5[2:,0:6])
	
	ax25 = plt.subplot(G6[2:,0:6])
	ax26= plt.subplot(G7[2:,0:6])
	ax27 = plt.subplot(G8[2:,0:6])

	ax10 = plt.subplot(G0[0:2,0:6])
	ax11 = plt.subplot(G1[0:2,0:6])
	ax12 = plt.subplot(G2[0:2,0:6])

	ax7 = plt.subplot(G3[0:2,0:6])
	ax8 = plt.subplot(G4[0:2,0:6])
	ax9 = plt.subplot(G5[0:2,0:6])
	
	ax28 = plt.subplot(G6[0:2,0:6])
	ax29 = plt.subplot(G7[0:2,0:6])
	ax30 = plt.subplot(G8[0:2,0:6])
	
	ax13 = plt.subplot(G0[2:,6])
	ax14 = plt.subplot(G1[2:,6])
	ax15 = plt.subplot(G2[2:,6])

	ax16 = plt.subplot(G3[2:,6])
	ax17 = plt.subplot(G4[2:,6])
	ax18 = plt.subplot(G5[2:,6])

	ax31 = plt.subplot(G6[2:,6])
	ax32 = plt.subplot(G7[2:,6])
	ax33 = plt.subplot(G8[2:,6])
	
	ax19 = plt.subplot(G0[0:2,6])
	ax20 = plt.subplot(G1[0:2,6])
	ax21 = plt.subplot(G2[0:2,6])

	ax22 = plt.subplot(G3[0:2,6])
	ax23 = plt.subplot(G4[0:2,6])
	ax24 = plt.subplot(G5[0:2,6])

	ax34 = plt.subplot(G6[0:2,6])
	ax35 = plt.subplot(G7[0:2,6])
	ax36 = plt.subplot(G8[0:2,6])
	
	fig = plt.gcf()
	fig.set_facecolor('white')
	
	plt.subplot(G0[2:,0:6])
	CS1 =plt.contourf(datas0[0][0],datas0[0][1],datas0[0][2],levels, cmap = cma)
	
	plt.subplot(G1[2:,0:6])
	CS2 = plt.contourf(datas1[0][0],datas1[0][1],datas1[0][2],levels, cmap = cma)
	
	plt.subplot(G2[2:,0:6])
	CS3 =plt.contourf(datas2[0][0],datas2[0][1],datas2[0][2],levels, cmap = cma)

	plt.subplot(G3[2:,0:6])
	CS4 =plt.contourf(datas0[1][0],datas0[1][1],datas0[1][2],levels, cmap = cma)
	
	plt.subplot(G4[2:,0:6])
	CS5 = plt.contourf(datas1[1][0],datas1[1][1],datas1[1][2],levels, cmap = cma)
	
	plt.subplot(G5[2:,0:6])
	CS6 =plt.contourf(datas2[1][0],datas2[1][1],datas2[1][2],levels, cmap = cma)
	
	plt.subplot(G6[2:,0:6])
	CS7 =plt.contourf(datas0[2][0],datas0[2][1],datas0[2][2],levels, cmap = cma)
	
	plt.subplot(G7[2:,0:6])
	CS8 =plt.contourf(datas1[2][0],datas1[2][1],datas1[2][2],levels, cmap = cma)
	
	plt.subplot(G8[2:,0:6])
	CS9 =plt.contourf(datas2[2][0],datas2[2][1],datas2[2][2],levels, cmap = cma)
	

	label2018location = (DT.date(2018,1,25), -75)
	years2018 = mdates.YearLocator()
	months2018 = mdates.MonthLocator()
	minorLocator2018 = MultipleLocator(2.5)
	stringy = []
	stringy = ['','75$^{\circ}$S','', '45$^{\circ}$S','', '15$^{\circ}$S','', '15$^{\circ}$N','', '45$^{\circ}$N','', '75$^{\circ}$N', '']
	labstring = ['a', 'b', 'c','d','e','f','g','h','i','j','k','l']
	
	plt.subplot(G0[2:,0:6])

	
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax1.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax1.plot(datas0[2][0][0][0:70], [z] *len(datas0[2][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax1.plot(datas0[0][0][0],[0]*len(datas0[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax1.xaxis.set_major_locator(years2018)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax1.xaxis.set_minor_locator(months2018)
	ax1.annotate(labstring[0],xy = label2018location, fontsize = 18, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax1.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')
	ax1.set_ylim(-85,85)
	ax1.set_ylabel('Sulfur dioxide only', fontsize = 14, fontweight = 'bold')
	ax1.yaxis.set_label_coords(-0.02, 0.70)

	plt.subplot(G1[2:,0:6])
	
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax2.plot(datas1[0][0][0], [z] *len(datas1[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax2.plot(datas1[0][0][0][0:70], [z] *len(datas1[0][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax2.plot(datas1[0][0][0],[0]*len(datas1[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax2.scatter(volctimes[1], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.xaxis.set_major_locator(years2018)
	ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax2.xaxis.set_minor_locator(months2018)
	ax2.annotate(labstring[3],xy = label2018location, fontsize = 18, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,73,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	ax2.set_ylabel('Co-injected halogen', fontsize = 14, fontweight = 'bold')
	ax2.yaxis.set_label_coords(-0.02, 0.70)
	for tick in ax2.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')	
	ax2.set_ylim(-85,85)

	plt.subplot(G2[2:,0:6])
	
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax3.plot(datas2[0][0][0], [z] *len(datas2[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax3.plot(datas2[0][0][0][0:70], [z] *len(datas2[0][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax3.plot(datas2[0][0][0],[0]*len(datas2[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax3.scatter(volctimes[2], 15.9,  s = 100,color = 'k', marker= '^')
	ax3.set_xlabel('Tropical eruption scenarios', fontsize = 14, fontweight='bold')
	ax3.set_ylabel('High co-injected halogen', fontsize = 14, fontweight = 'bold')
	ax3.yaxis.set_label_coords(-0.02, 0.70)
	ax3.xaxis.set_label_coords(0.5, -0.12)
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax3.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax3.set_ylim(-85,85)
	ax3.xaxis.set_major_locator(years2018)
	ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax3.xaxis.set_minor_locator(months2018)
	ax3.annotate(labstring[6],xy = label2018location, fontsize = 18, fontweight = 'bold')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')
	ax3.set_ylim(-85,85)

	plt.subplot(G0[0:2,0:6])
	ax10.plot(dateflat[0][18:], datas3[0][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax10.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax10.grid(False)
        ax10.xaxis.set_minor_locator(months2018)
        ax10.xaxis.set_major_locator(years2018)
        ax10.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax10.spines['top'].set_visible(True)
	ax10.spines['right'].set_visible(True)
	ax10.spines['bottom'].set_visible(True)
	ax10.spines['left'].set_visible(True)
        ax10.get_xaxis().tick_bottom()
        ax10.get_yaxis().tick_left()
	ax10.axvline(x=volctimes[0],color='k',ls='dashed')
	ax10.set_ylim(-7.5,1.5)
        plt.yticks([-6, -3,0], [str(x) + "\%" for x in [-6,-3, 0]], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-6,-3,0]:    
              ax10.plot(dateflat[0][18:], [y] *len(dateflat[0][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax10.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G1[0:2,0:6])
	ax11.plot(dateflat[1][18:], datas3[1][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax11.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax11.grid(False)
        ax11.xaxis.set_minor_locator(months2018)
        ax11.xaxis.set_major_locator(years2018)
        ax11.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax11.spines['top'].set_visible(True)
	ax11.spines['right'].set_visible(True)
	ax11.spines['bottom'].set_visible(True)
	ax11.spines['left'].set_visible(True)
        ax11.get_xaxis().tick_bottom()
        ax11.get_yaxis().tick_left()
	ax11.axvline(x=volctimes[1],color='k',ls='dashed')
	ax11.set_ylim(-10,2)

        plt.yticks([-8,-4,0], [str(x) + "\%" for x in [-8,-4,0]], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-8,-4,0]:    
              ax11.plot(dateflat[1][18:], [y] *len(dateflat[1][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax11.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G2[0:2,0:6])
	ax12.plot(dateflat[2][18:], datas3[2][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax12.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax12.grid(False)
        ax12.xaxis.set_minor_locator(months2018)
        ax12.xaxis.set_major_locator(years2018)
        ax12.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax12.spines['top'].set_visible(True)
	ax12.spines['right'].set_visible(True)
	ax12.spines['bottom'].set_visible(True)
	ax12.spines['left'].set_visible(True)
        ax12.get_xaxis().tick_bottom()
        ax12.get_yaxis().tick_left()
	ax12.axvline(x=volctimes[2],color='k',ls='dashed')
	ax12.set_ylim(-25,5)
        plt.yticks([-20,-10,0], [str(x) + "\%" for x in [-20,-10,0]], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-20,-10,0]:    
              ax12.plot(dateflat[2][18:], [y] *len(dateflat[2][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax12.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G3[2:,0:6])

	
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax4.plot(datas0[1][0][0], [z] *len(datas0[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax4.plot(datas0[1][0][0][0:70], [z] *len(datas0[1][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax4.plot(datas0[1][0][0],[0]*len(datas0[1][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax4.scatter(volctimes[0], 41,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],41, yerr=np.array([[volclatmidlatlow,volclatmidlathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax4.xaxis.set_major_locator(years2018)
	ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax4.xaxis.set_minor_locator(months2018)
	ax4.annotate(labstring[1],xy = label2018location, fontsize = 18, fontweight = 'bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax4.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')
	ax4.set_ylim(-85,85)

	plt.subplot(G4[2:,0:6])
	
	ax5.axvline(x=volctimes[4],color='k',ls='dashed')
	ax5.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax5.plot(datas1[1][0][0], [z] *len(datas1[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax5.plot(datas1[1][0][0][0:70], [z] *len(datas1[1][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax5.plot(datas1[1][0][0],[0]*len(datas1[1][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax5.scatter(volctimes[4], 41,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[4],41, yerr=np.array([[volclatmidlatlow,volclatmidlathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax5.xaxis.set_major_locator(years2018)
	ax5.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax5.xaxis.set_minor_locator(months2018)
	ax5.annotate(labstring[4],xy = label2018location, fontsize = 18, fontweight = 'bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax5.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')	
	ax5.set_ylim(-85,85)
	
	plt.subplot(G5[2:,0:6])
	
	ax6.axvline(x=volctimes[5],color='k',ls='dashed')
	ax6.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax6.plot(datas2[1][0][0], [z] *len(datas2[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax6.plot(datas2[1][0][0][0:70], [z] *len(datas2[1][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax6.plot(datas2[1][0][0],[0]*len(datas2[1][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax6.scatter(volctimes[5], 41,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[5],41, yerr=np.array([[volclatmidlatlow,volclatmidlathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax6.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax6.set_ylim(-85,85)
	ax6.xaxis.set_major_locator(years2018)
	ax6.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax6.xaxis.set_minor_locator(months2018)
	ax6.annotate(labstring[7],xy = label2018location, fontsize = 18, fontweight = 'bold')
	ax6.yaxis.set_label_coords(-0.02, 0.70)
	ax6.set_xlabel('Mid-latitude eruption scenarios', fontsize = 14, fontweight='bold')
	ax6.xaxis.set_label_coords(0.5, -0.12)
	ax6.set_ylim(-85,85)
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')

	plt.subplot(G3[0:2,0:6])
	ax7.plot(dateflat[3][18:], datas3[3][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax7.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax7.grid(False)
        ax7.xaxis.set_minor_locator(months2018)
        ax7.xaxis.set_major_locator(years2018)
        ax7.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax7.spines['top'].set_visible(True)
	ax7.spines['right'].set_visible(True)
	ax7.spines['bottom'].set_visible(True)
	ax7.spines['left'].set_visible(True)
        ax7.get_xaxis().tick_bottom()
        ax7.get_yaxis().tick_left()
	ax7.axvline(x=volctimes[3],color='k',ls='dashed')
	ax7.set_ylim(-7.5,1.5)
	plt.yticks([-6, -3,0], [str(x) + "\%" for x in [-6,-3, 0]], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-6,-3,0]:    
              ax7.plot(dateflat[3][18:], [y] *len(dateflat[3][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax7.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G4[0:2,0:6])
	ax8.plot(dateflat[4][18:], datas3[4][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax8.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax8.grid(False)
        ax8.xaxis.set_minor_locator(months2018)
        ax8.xaxis.set_major_locator(years2018)
        ax8.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax8.spines['top'].set_visible(True)
	ax8.spines['right'].set_visible(True)
	ax8.spines['bottom'].set_visible(True)
	ax8.spines['left'].set_visible(True)
        ax8.get_xaxis().tick_bottom()
        ax8.get_yaxis().tick_left()
	ax8.axvline(x=volctimes[4],color='k',ls='dashed')
	ax8.set_ylim(-10,2)
        plt.yticks([-8,-4], [str(x) + "\%" for x in [-8,-4]], fontsize=10, fontweight='bold')
	plt.yticks([-8,-4, 0], ['-8\%', '-4\%', '0\%\  '], fontsize = 10, fontweight = 'bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-8,-4,0]:    
              ax8.plot(dateflat[4][18:], [y] *len(dateflat[4][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax8.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G5[0:2,0:6])
	ax9.plot(dateflat[5][18:], datas3[5][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax9.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax9.grid(False)
        ax9.xaxis.set_minor_locator(months2018)
        ax9.xaxis.set_major_locator(years2018)
        ax9.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax9.spines['top'].set_visible(True)
	ax9.spines['right'].set_visible(True)
	ax9.spines['bottom'].set_visible(True)
	ax9.spines['left'].set_visible(True)
        ax9.get_xaxis().tick_bottom()
        ax9.get_yaxis().tick_left()
	ax9.axvline(x=volctimes[5],color='k',ls='dashed')
	ax9.set_ylim(-25,5)
        plt.yticks([-20,-10, 0],['-20\%','-10\%','$\ $0\%'], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-20,-10,0]:    
              ax9.plot(dateflat[5][19:], [y] *len(dateflat[5][19:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax9.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G6[2:,0:6])

	
	ax25.axvline(x=volctimes[6],color='k',ls='dashed')
	ax25.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax25.plot(datas0[2][0][0], [z] *len(datas0[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax25.plot(datas0[2][0][0][0:70], [z] *len(datas0[2][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax25.plot(datas0[2][0][0],[0]*len(datas0[2][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax25.scatter(volctimes[0], 72,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],72, yerr=np.array([[volclatarcticlow,volclatarctichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax25.xaxis.set_major_locator(years2018)
	ax25.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax25.xaxis.set_minor_locator(months2018)
	ax25.annotate(labstring[2],xy = label2018location, fontsize = 18, fontweight = 'bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax25.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')
	ax25.yaxis.set_label_coords(-0.02, 0.70)
	ax25.set_ylim(-85,85)

	plt.subplot(G7[2:,0:6])
	
	ax26.axvline(x=volctimes[4],color='k',ls='dashed')
	ax26.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax26.plot(datas1[2][0][0], [z] *len(datas1[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax26.plot(datas1[2][0][0][0:70], [z] *len(datas1[2][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax26.plot(datas1[2][0][0],[0]*len(datas1[2][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax26.scatter(volctimes[4], 72,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[4],72, yerr=np.array([[volclatarcticlow,volclatarctichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax26.xaxis.set_major_locator(years2018)
	ax26.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax26.xaxis.set_minor_locator(months2018)
	ax26.annotate(labstring[5],xy = label2018location, fontsize = 18, fontweight = 'bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax26.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')	
	ax26.yaxis.set_label_coords(-0.02, 0.70)
	ax26.set_ylim(-85,85)
	
	plt.subplot(G8[2:,0:6])
	
	ax27.axvline(x=volctimes[5],color='k',ls='dashed')
	ax27.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax27.plot(datas2[2][0][0], [z] *len(datas2[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax27.plot(datas2[2][0][0][0:70], [z] *len(datas2[2][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax27.plot(datas2[2][0][0],[0]*len(datas2[2][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax27.scatter(volctimes[5], 72,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[5],72, yerr=np.array([[volclatarcticlow,volclatarctichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax27.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax27.set_ylim(-85,85)
	ax27.xaxis.set_major_locator(years2018)
	ax27.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax27.xaxis.set_minor_locator(months2018)
	ax27.annotate(labstring[8],xy = label2018location, fontsize = 18, fontweight = 'bold')
	ax27.yaxis.set_label_coords(-0.02, 0.70)
	ax27.set_xlabel('Arctic eruption scenarios', fontsize = 14, fontweight='bold')
	ax27.xaxis.set_label_coords(0.5, -0.12)
	ax27.set_ylim(-85,85)
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')

	plt.subplot(G6[0:2,0:6])
	ax28.plot(dateflat[6][18:], datas3[6][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax28.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax28.grid(False)
        ax28.xaxis.set_minor_locator(months2018)
        ax28.xaxis.set_major_locator(years2018)
        ax28.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax28.spines['top'].set_visible(True)
	ax28.spines['right'].set_visible(True)
	ax28.spines['bottom'].set_visible(True)
	ax28.spines['left'].set_visible(True)
        ax28.get_xaxis().tick_bottom()
        ax28.get_yaxis().tick_left()
	ax28.axvline(x=volctimes[3],color='k',ls='dashed')
	ax28.set_ylim(-7.5,1.5)
	plt.yticks([-6, -3,0], [str(x) + "\%" for x in [-6,-3, 0]], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-6,-3,0]:    
              ax28.plot(dateflat[6][18:], [y] *len(dateflat[6][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax28.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G7[0:2,0:6])
	ax29.plot(dateflat[7][18:], datas3[7][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax29.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax29.grid(False)
        ax29.xaxis.set_minor_locator(months2018)
        ax29.xaxis.set_major_locator(years2018)
        ax29.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax29.spines['top'].set_visible(True)
	ax29.spines['right'].set_visible(True)
	ax29.spines['bottom'].set_visible(True)
	ax29.spines['left'].set_visible(True)
        ax29.get_xaxis().tick_bottom()
        ax29.get_yaxis().tick_left()
	ax29.axvline(x=volctimes[4],color='k',ls='dashed')
	ax29.set_ylim(-10,2)
        plt.yticks([-8,-4], [str(x) + "\%" for x in [-8,-4]], fontsize=10, fontweight='bold')
	plt.yticks([-8,-4, 0], ['-8\%', '-4\%', '0\%\  '], fontsize = 10, fontweight = 'bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-8,-4,0]:    
              ax29.plot(dateflat[7][18:], [y] *len(dateflat[7][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax29.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G8[0:2,0:6])
	ax30.plot(dateflat[8][18:], datas3[8][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax30.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax30.grid(False)
        ax30.xaxis.set_minor_locator(months2018)
        ax30.xaxis.set_major_locator(years2018)
        ax30.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax30.spines['top'].set_visible(True)
	ax30.spines['right'].set_visible(True)
	ax30.spines['bottom'].set_visible(True)
	ax30.spines['left'].set_visible(True)
        ax30.get_xaxis().tick_bottom()
        ax30.get_yaxis().tick_left()
	ax30.axvline(x=volctimes[5],color='k',ls='dashed')
	ax30.set_ylim(-25,5)
        plt.yticks([-20,-10, 0],['-20\%','-10\%','$\ $0\%'], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-20,-10,0]:    
              ax30.plot(dateflat[8][19:], [y] *len(dateflat[8][19:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax30.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')
	
	plt.subplot(G0[2:,6])
	ax13.plot(dataslat[0], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax13.grid(False)
        ax13.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax13.spines['top'].set_visible(True)
	ax13.spines['right'].set_visible(True)
	ax13.spines['bottom'].set_visible(True)
	ax13.spines['left'].set_visible(True)
        ax13.get_xaxis().tick_bottom()
        ax13.get_yaxis().tick_left()
	ax13.set_ylim(-85,85)
	ax13.set_xlim(-8.5,1.8)
	ax13.xaxis.set_label_coords(1,1.6)
        plt.xticks([-7, 0], [str(x) + "\%" for x in [-7,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-7,-3.5, 0]:    
              ax13.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax13.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G0[0:2,6])
	ax19.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax19.set_xlim(-1,1)
	ax19.set_ylim(-1,1)
	ax19.annotate(str(totalcol[0])[0:4] + '\%', xy = (0,0),horizontalalignment = 'center', verticalalignment = 'center', fontsize = 14, fontweight = 'heavy')
	ax19.xaxis.set_label_coords(1,1.525)

	plt.subplot(G1[2:,6])
	ax14.plot(dataslat[3], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax14.grid(False)
        ax14.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax14.spines['top'].set_visible(True)
	ax14.spines['right'].set_visible(True)
	ax14.spines['bottom'].set_visible(True)
	ax14.spines['left'].set_visible(True)
        ax14.get_xaxis().tick_bottom()
        ax14.get_yaxis().tick_left()
	ax14.set_ylim(-85,85)
	ax14.set_xlim(-11.5,2.5)
	ax14.xaxis.set_label_coords(1,1.6)
        plt.xticks([-10, 0], [str(x) + "\%" for x in [-10,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-10,-5, 0]:    
              ax14.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax14.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G1[0:2,6])
	ax20.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax20.set_xlim(-1,1)
	ax20.set_ylim(-1,1)
	ax20.annotate(str(totalcol[3])[0:4] + '\%', xy = (0.0,0), horizontalalignment = 'center', verticalalignment = 'center',fontsize = 14, fontweight = 'heavy')
	ax20.xaxis.set_label_coords(1,1.525)


	plt.subplot(G2[2:,6])
	ax15.plot(dataslat[6], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax15.grid(False)
        ax15.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax15.spines['top'].set_visible(True)
	ax15.spines['right'].set_visible(True)
	ax15.spines['bottom'].set_visible(True)
	ax15.spines['left'].set_visible(True)
        ax15.get_xaxis().tick_bottom()
        ax15.get_yaxis().tick_left()
	ax15.set_ylim(-85,85)
	ax15.set_xlim(-28,5)
	ax15.xaxis.set_label_coords(1,1.6)
        plt.xticks([-25, 0], [str(x) + "\%" for x in [-25,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-25,-12.5, 0]:    
              ax15.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax15.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2[0:2,6])
	ax21.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax21.set_xlim(-1,1)
	ax21.set_ylim(-1,1)
	ax21.annotate('-14\%', xy = (-0.70,-0.20), fontsize = 14, fontweight = 'heavy')
	ax21.xaxis.set_label_coords(1,1.525)


	plt.subplot(G3[2:,6])
	ax16.plot(dataslat[1], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax16.grid(False)
        ax16.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax16.spines['top'].set_visible(True)
	ax16.spines['right'].set_visible(True)
	ax16.spines['bottom'].set_visible(True)
	ax16.spines['left'].set_visible(True)
        ax16.get_xaxis().tick_bottom()
        ax16.get_yaxis().tick_left()
	ax16.set_ylim(-85,85)
	ax16.set_xlim(-8.5,1.8)
	ax16.xaxis.set_label_coords(1,1.6)
        plt.xticks([-7, 0], [str(x) + "\%" for x in [-7,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-7,-3.5, 0]:    
              ax16.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax16.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G3[0:2,6])
	ax22.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax22.set_xlim(-1,1)
	ax22.set_ylim(-1,1)
	ax22.annotate(str(totalcol[1])[0:4] + '\%', xy = (0,0),horizontalalignment = 'center', verticalalignment = 'center', fontsize = 14, fontweight = 'heavy')
	ax22.xaxis.set_label_coords(1,1.525)


	plt.subplot(G4[2:,6])
	ax17.plot(dataslat[4], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax17.grid(False)
        ax17.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax17.spines['top'].set_visible(True)
	ax17.spines['right'].set_visible(True)
	ax17.spines['bottom'].set_visible(True)
	ax17.spines['left'].set_visible(True)
        ax17.get_xaxis().tick_bottom()
        ax17.get_yaxis().tick_left()
	ax17.set_ylim(-85,85)
	ax17.set_xlim(-11.5,2.5)
	ax17.xaxis.set_label_coords(1,1.6)
        plt.xticks([-10, 0], [str(x) + "\%" for x in [-10,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-10,-5, 0]:    
              ax17.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax17.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G4[0:2,6])
	ax23.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax23.set_xlim(-1,1)
	ax23.set_ylim(-1,1)
	ax23.annotate(str(totalcol[4])[0:4] + '\%', xy = (0,0),horizontalalignment = 'center', verticalalignment = 'center', fontsize = 14, fontweight = 'heavy')
	ax23.xaxis.set_label_coords(1,1.525)


	plt.subplot(G5[2:,6])
	ax18.plot(dataslat[7], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax18.grid(False)
        ax18.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax18.spines['top'].set_visible(True)
	ax18.spines['right'].set_visible(True)
	ax18.spines['bottom'].set_visible(True)
	ax18.spines['left'].set_visible(True)
        ax18.get_xaxis().tick_bottom()
        ax18.get_yaxis().tick_left()
	ax18.set_ylim(-85,85)
	ax18.set_xlim(-28,5)
	ax18.xaxis.set_label_coords(1,1.6)
        plt.xticks([-25, 0], [str(x) + "\%" for x in [-25,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-25,-12.5, 0]:    
              ax18.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax18.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G5[0:2,6])
	ax24.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax24.set_xlim(-1,1)
	ax24.set_ylim(-1,1)
	ax24.annotate('-11\%', xy = (-0.7,-0.20), fontsize = 14, fontweight = 'heavy')
	ax24.xaxis.set_label_coords(1,1.525)


	plt.subplot(G6[2:,6])
	ax31.plot(dataslat[2], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax31.grid(False)
        ax31.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax31.spines['top'].set_visible(True)
	ax31.spines['right'].set_visible(True)
	ax31.spines['bottom'].set_visible(True)
	ax31.spines['left'].set_visible(True)
        ax31.get_xaxis().tick_bottom()
        ax31.get_yaxis().tick_left()
	ax31.set_ylim(-85,85)
	ax31.set_xlim(-8.5,1.8)
	ax31.xaxis.set_label_coords(1,1.6)
        plt.xticks([-7, 0], [str(x) + "\%" for x in [-7,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-7,-3.5, 0]:    
              ax31.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax31.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G6[0:2,6])
	ax34.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax34.set_xlim(-1,1)
	ax34.set_ylim(-1,1)
	ax34.annotate(str(totalcol[2])[0:4] + '\%', xy = (0,0),horizontalalignment = 'center', verticalalignment = 'center', fontsize = 14, fontweight = 'heavy')
	ax34.xaxis.set_label_coords(1,1.525)

	plt.subplot(G7[2:,6])
	ax32.plot(dataslat[5], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax32.grid(False)
        ax32.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax32.spines['top'].set_visible(True)
	ax32.spines['right'].set_visible(True)
	ax32.spines['bottom'].set_visible(True)
	ax32.spines['left'].set_visible(True)
        ax32.get_xaxis().tick_bottom()
        ax32.get_yaxis().tick_left()
	ax32.set_ylim(-85,85)
	ax32.set_xlim(-11.5,2.5)
	ax32.xaxis.set_label_coords(1,1.6)
        plt.xticks([-10, 0], [str(x) + "\%" for x in [-10,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-10,-5, 0]:    
              ax32.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax32.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G7[0:2,6])
	ax35.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax35.set_xlim(-1,1)
	ax35.set_ylim(-1,1)
	ax35.annotate(str(totalcol[5])[0:4] + '\%', xy = (0,0),horizontalalignment = 'center', verticalalignment = 'center', fontsize = 14, fontweight = 'heavy')
	ax35.xaxis.set_label_coords(1,1.525)

	
	plt.subplot(G8[2:,6])
	ax33.plot(dataslat[8], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax33.grid(False)
        ax33.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax33.spines['top'].set_visible(True)
	ax33.spines['right'].set_visible(True)
	ax33.spines['bottom'].set_visible(True)
	ax33.spines['left'].set_visible(True)
        ax33.get_xaxis().tick_bottom()
        ax33.get_yaxis().tick_left()
	ax33.set_ylim(-85,85)
	ax33.set_xlim(-28,5)
	ax33.xaxis.set_label_coords(1,1.6)
        plt.xticks([-25, 0], [str(x) + "\%" for x in [-25,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-25,-12.5, 0]:    
              ax33.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax33.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G8[0:2,6])
	ax36.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax36.set_xlim(-1,1)
	ax36.set_ylim(-1,1)
	ax36.annotate(str(totalcol[8])[0:4] + '\%', xy = (0,0), horizontalalignment = 'center', verticalalignment = 'center',fontsize = 14, fontweight = 'heavy')
	ax36.xaxis.set_label_coords(1,1.525)

	cbar_ax = fig.add_axes([0.02, 0.95, 0.97, 0.02])
	fmt = '%2.0f'
	tix =  levels
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt, orientation = 'horizontal')
	cbar_ax.tick_params(labelsize = 12)
	cbar.set_label('Percent change in column ozone', fontsize = 14, fontweight = 'bold', labelpad = -45)

def titfig(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global ax1,ax2,ax3,ax4, ax5, ax6,ax7,ax8,ax9, ax10, ax11, ax12,ax19,fig,cbar, plt, levels, datas0,datas1,datas2, dataslat, totalcol, volcinjectlats, Gs, G2017, G2050, G2060, G2070, G2100

	datas0 = []
	datas1 = []
	datas2 = []
	dateflat = []
	CS = []
	years = [2100]
	volcdays = [531] 
	volctimes = []
	dataslat=[]
	totalcol = []	


	datas0.append(datamodulator(var, dayt, 1, 0,1, 1990, num, flag))
	datas0.append(datamodulator(var, dayt, 4, 0,1, 1990, num, flag))
	datas0.append(datamodulator(var, dayt, 2, 0,1, 1990, num, flag))
	datas0.append(datamodulator(var, dayt, 3, 0,1, 1990, num, flag))
	volctimes.append(volclocator(531, 1990))
	volctimes.append(volclocator(531, 1990))
	volctimes.append(volclocator(531, 1990))
	volctimes.append(volclocator(531, 1990))
	datas1.append(datas0[0][2].mean(0))
	datas1.append(datas0[1][2].mean(0))
	datas1.append(datas0[2][2].mean(0))
	datas1.append(datas0[3][2].mean(0))
	dateflat.append(datas0[0][0][0])
	dateflat.append(datas0[1][0][0])
	dateflat.append(datas0[2][0][0])
	dateflat.append(datas0[3][0][0])
	
	for x in range(len(datas0)):
		latarray = []
		for y in range(len(datas0[0][0])):
			latarray.append(datas0[x][2][y][20:59].mean())
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray[13:16]))
	lats = datas0[0][1].mean(1)
	
	volclattropichigh = latitude_edges[12] - 15.9
	volclattropiclow = 15.9 - latitude_edges[10]
	#levels =  np.array([-25,-20,-17,-15,-13,-11,-9,-7,-5,-3,-1,1,3,5,7,9,11, 13])
	levels =  np.array([-80,-70,-60,-50,-40,-30,-25,-20, -15,-10,-8, -6,-4,-2,-1,1,2,])
	
	plt.figure
	Gs = gridspec.GridSpec(4,1, hspace = 0)
	G2017 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[0])
	G2050 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[1])
	G2060 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[2])
	G2070 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[3])
	ax1 = plt.subplot(G2017[1:3,0:9])
	ax2 = plt.subplot(G2050[1:3,0:9])
	ax3 = plt.subplot(G2060[1:3,0:9])
	ax4 = plt.subplot(G2070[1:3,0:9])
	ax6 = plt.subplot(G2017[0,0:9])
	ax7 = plt.subplot(G2050[0,0:9])
	ax8 = plt.subplot(G2060[0,0:9])
	ax9 = plt.subplot(G2070[0,0:9])
	ax11 = plt.subplot(G2017[1:3,9])
	ax12 = plt.subplot(G2050[1:3,9])
	ax13 = plt.subplot(G2060[1:3,9])
	ax14 = plt.subplot(G2070[1:3,9])
	ax16 = plt.subplot(G2017[0,9])
	ax17 = plt.subplot(G2050[0,9])
	ax18 = plt.subplot(G2060[0,9])
	ax19 = plt.subplot(G2070[0,9])

	
	fig = plt.gcf()
	fig.set_facecolor('white')
	plt.subplot(G2017[1:3,0:9])
	
	CS1 =plt.contourf(datas0[0][0],datas0[0][1],datas0[0][2],levels, cmap = cma, extend = "both")
	plt.subplot(G2050[1:3,0:9])
	CS2 = plt.contourf(datas0[1][0],datas0[1][1],datas0[1][2],levels, cmap = cma)
	plt.subplot(G2060[1:3,0:9])
	CS3 =plt.contourf(datas0[2][0],datas0[2][1],datas0[2][2],levels, cmap = cma, extend = "both")
	plt.subplot(G2070[1:3,0:9])
	CS4 = plt.contourf(datas0[3][0],datas0[3][1],datas0[3][2],levels, cmap = cma, extend = "both")
	

	stringy = []
	stringy = ['','75$^{\circ}$S','', '45$^{\circ}$S','', '15$^{\circ}$S','', '15$^{\circ}$N','', '45$^{\circ}$N','', '75$^{\circ}$N', '']
	labstring = ['a','b','c','d','e','f','g','h','i','j','k','l']
	
	plt.subplot(G2017[1:3,0:9])
	
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	labellocation = (DT.date(1991,1,25), -75)
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_xlim(DT.date(1991,1,1), DT.date(1996,7,1))
	ax1.xaxis.set_major_locator(years)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax1.xaxis.set_minor_locator(months)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax1.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax1.plot(datas0[0][0][0][0:70], [z] *len(datas0[0][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax1.plot(datas0[0][0][0],[0]*len(datas0[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax1.annotate(labstring[0],xy = labellocation, fontsize=16, fontweight='heavy')
	plt.xticks(rotation=15, fontsize=10, fontweight='heavy')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	for tick in ax1.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax1.set_ylim(-85,85)
	ax1.set_ylabel('Latitudinal column deviations', fontsize = 10, fontweight = 'heavy')	
	ax1.yaxis.set_label_coords(-0.005,0.74)

	
	plt.subplot(G2050[1:3,0:9])
	years2 = mdates.YearLocator()
	months2 = mdates.MonthLocator()
	minorLocator2 = MultipleLocator(2.5)
	labellocation = (DT.date(1991,1,25), -75)
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_xlim(DT.date(1991,1,1), DT.date(1996,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax2.plot(datas0[1][0][0], [z] *len(datas0[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax2.plot(datas0[1][0][0][0:70], [z] *len(datas0[1][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax2.plot(datas0[1][0][0],[0]*len(datas0[1][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax2.scatter(volctimes[1], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.xaxis.set_major_locator(years2)
	ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax2.xaxis.set_minor_locator(months2)
	ax2.annotate(labstring[1],xy = labellocation, fontsize=16, fontweight='heavy')
	plt.xticks(rotation=15, fontsize=10, fontweight='heavy')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	
	for tick in ax2.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax2.set_ylim(-85,85)
	plt.subplot(G2060[1:3,0:9])
	
	labellocation = (DT.date(1991,1,25), -75)
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_xlim(DT.date(1991,1,1), DT.date(1996,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax3.plot(datas0[2][0][0], [z] *len(datas0[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax3.plot(datas0[2][0][0][0:70], [z] *len(datas0[2][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax3.plot(datas0[2][0][0],[0]*len(datas0[2][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax3.scatter(volctimes[2], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	ax3.set_ylim(-85,85)
	for tick in ax3.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	years3 = mdates.YearLocator()
	months3 = mdates.MonthLocator()
	minorLocator3 = MultipleLocator(2.5)
	ax3.xaxis.set_major_locator(years3)
	ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax3.xaxis.set_minor_locator(months3)
	plt.xticks(rotation=15, fontsize=10, fontweight='heavy')
	ax3.annotate(labstring[2],xy = labellocation, fontsize=16, fontweight='heavy')
	ax3.set_ylim(-85,85)
	
	plt.subplot(G2070[1:3,0:9])
	
	years3a = mdates.YearLocator()
	months3a = mdates.MonthLocator()
	minorLocator3 = MultipleLocator(2.5)
	labellocation = (DT.date(1991,1,25), -75)
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_xlim(DT.date(1991,1,1), DT.date(1996,7,1))
	ax4.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax4.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax4.plot(datas0[3][0][0][0:70], [z] *len(datas0[3][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax4.plot(datas0[3][0][0],[0]*len(datas0[3][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax4.scatter(volctimes[3], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	ax4.xaxis.set_major_locator(years3a)
	ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax4.xaxis.set_minor_locator(months3a)
	plt.xticks(rotation=15, fontsize=10, fontweight='heavy')
	ax4.annotate(labstring[3],xy = labellocation, fontsize=16, fontweight='heavy')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	for tick in ax4.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax4.set_ylim(-85,85)


	ax4.set_xlabel('Model year', fontsize =10, fontweight = 'heavy', horizontalalignment='center')
	#ax5.xaxis.set_label_coords(0,-0.2)

	cbar_ax = fig.add_axes([0.03, 0.97, 0.95, 0.01])
	fmt = '%1.0f'
	tix =  levels
	cbar = fig.colorbar(CS2, cax = cbar_ax, ticks = tix, format =fmt, orientation = 'horizontal')
	cbar_ax.tick_params(labelsize = 10)
	cbar.set_label('Percent change in column ozone', fontsize=10, fontweight='heavy', labelpad = -40)


	plt.subplot(G2017[0,0:9])
	ax6.plot(dateflat[0][18:], datas1[0][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	years5 = mdates.YearLocator()
	months5 = mdates.MonthLocator()
	minorLocator5 = MultipleLocator(2.5)
	ax6.set_xlim(DT.date(1991,1,1), DT.date(1996,7,1))
	ax6.grid(False)
        ax6.xaxis.set_minor_locator(months5)
        ax6.xaxis.set_major_locator(years5)
        ax6.yaxis.set_minor_locator(minorLocator5)
        ax6.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax6.spines['top'].set_visible(True)
	ax6.spines['right'].set_visible(True)
	ax6.spines['bottom'].set_visible(True)
	ax6.spines['left'].set_visible(True)
        ax6.get_xaxis().tick_bottom()
        ax6.get_yaxis().tick_left()
	ax6.axvline(x=volctimes[0],color='k',ls='dashed')
	ax6.set_ylim(-11.5,2.5)
	ax6.set_xlabel('Temporal column ozone deviations', fontsize = 10, fontweight = 'heavy')	
	ax6.xaxis.set_label_coords(0.21,1.225)
	plt.yticks(range(-10,2,5), [str(x) + "\%" for x in range(-10,2,5)], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", labeltop='off',right="off", labelleft="on", labelright = "off")  
 	for y in range(-10,2,5):    
              ax6.plot(dateflat[0][18:], [y] *len(dateflat[0][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax6.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2050[0,0:9])
	years6 = mdates.YearLocator()
	months6 = mdates.MonthLocator()
	minorLocator6 = MultipleLocator(2.5)
	ax7.plot(dateflat[1][18:], datas1[1][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax7.set_xlim(DT.date(1991,1,1), DT.date(1996,7,1))
	ax7.grid(False)
        ax7.xaxis.set_minor_locator(months6)
        ax7.xaxis.set_major_locator(years6)
        ax7.yaxis.set_minor_locator(minorLocator6)
        ax7.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax7.spines['top'].set_visible(True)
	ax7.spines['right'].set_visible(True)
	ax7.spines['bottom'].set_visible(True)
	ax7.spines['left'].set_visible(True)
        ax7.get_xaxis().tick_bottom()
        ax7.get_yaxis().tick_left()
	ax7.axvline(x=volctimes[1],color='k',ls='dashed')
	ax7.set_ylim(-11.5,2.5)
        plt.yticks(range(-10,2,5), [str(x) + "\%" for x in range(-10,2,5)], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in range(-10,2,5):    
              ax7.plot(dateflat[1][18:], [y] *len(dateflat[1][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax7.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2060[0,0:9])
	years8 = mdates.YearLocator()
	months8 = mdates.MonthLocator()
	minorLocator8 = MultipleLocator(2.5)
	ax8.plot(dateflat[2][18:], datas1[2][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax8.set_xlim(DT.date(1991,1,1), DT.date(1996,7,1))
	ax8.grid(False)
        ax8.xaxis.set_minor_locator(months8)
        ax8.xaxis.set_major_locator(years8)
        ax8.yaxis.set_minor_locator(minorLocator8)
        ax8.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax8.spines['top'].set_visible(True)
	ax8.spines['right'].set_visible(True)
	ax8.spines['bottom'].set_visible(True)
	ax8.spines['left'].set_visible(True)
        ax8.get_xaxis().tick_bottom()
        ax8.get_yaxis().tick_left()
	ax8.axvline(x=volctimes[2],color='k',ls='dashed')
	ax8.set_ylim(-25,5)
        plt.yticks([-20,-10,0], [str(x) + "\%" for x in [-20,-10,0]], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in [-20,-10,0]:    
              ax8.plot(dateflat[2][18:], [y] *len(dateflat[2][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax8.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2070[0,0:9])
	years9 = mdates.YearLocator()
	months9 = mdates.MonthLocator()
	minorLocator9 = MultipleLocator(2.5)
	ax9.plot(dateflat[3][18:], datas1[3][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax9.set_xlim(DT.date(1991,1,1), DT.date(1996,7,1))
	ax9.grid(False)
        ax9.xaxis.set_minor_locator(months9)
        ax9.xaxis.set_major_locator(years9)
        ax9.yaxis.set_minor_locator(minorLocator9)
        ax9.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax9.spines['top'].set_visible(True)
	ax9.spines['right'].set_visible(True)
	ax9.spines['bottom'].set_visible(True)
	ax9.spines['left'].set_visible(True)
        ax9.get_xaxis().tick_bottom()
        ax9.get_yaxis().tick_left()
	ax9.axvline(x=volctimes[3],color='k',ls='dashed')
	ax9.set_ylim(-23.5,4.5)
        plt.yticks([-20,-10,0], [str(x) + "\%" for x in [-20,-10,0]], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in [-20,-10,0]:    
              ax9.plot(dateflat[3][18:], [y] *len(dateflat[3][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax9.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	
	
	plt.subplot(G2017[1:3,9])
	ax11.plot(dataslat[0], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax11.grid(False)
        ax11.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax11.spines['top'].set_visible(True)
	ax11.spines['right'].set_visible(True)
	ax11.spines['bottom'].set_visible(True)
	ax11.spines['left'].set_visible(True)
        ax11.get_xaxis().tick_bottom()
        ax11.get_yaxis().tick_left()
	ax11.set_ylim(-85,85)
	ax11.set_xlim(-9, 1.5)
	ax11.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-8,0], [str(x) + "\%" for x in [-8,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in range(-8,1,4):    
              ax11.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax11.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2017[0,9])
	ax16.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax16.set_xlim(-1,1)
	ax16.set_ylim(-1,1)
	ax16.annotate(str(totalcol[0])[0:4] + '\%', xy = (-0.7,-0.20), fontsize = 14, fontweight = 'heavy')
	ax16.set_xlabel('30\u00B0N-60\u00B0N - 3 year \n average', fontsize = 10, fontweight = 'heavy', horizontalalignment = 'right')
	ax16.xaxis.set_label_coords(1,1.525)

	plt.subplot(G2050[1:3,9])
	ax12.plot(dataslat[1], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax12.grid(False)
        ax12.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax12.spines['top'].set_visible(True)
	ax12.spines['right'].set_visible(True)
	ax12.spines['bottom'].set_visible(True)
	ax12.spines['left'].set_visible(True)
        ax12.get_xaxis().tick_bottom()
        ax12.get_yaxis().tick_left()
	ax12.set_ylim(-85,85)
	ax12.set_xlim(-9, 1.5)
	ax12.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-8,0], [str(x) + "\%" for x in [-8,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-8,-4,0]:    
              ax12.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax12.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2050[0,9])
	ax17.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax17.set_xlim(-1,1)
	ax17.set_ylim(-1,1)
	ax17.annotate(str(totalcol[1])[0:4] + '\%', xy = (-0.7,-0.20), fontsize = 14, fontweight = 'heavy')
	ax17.xaxis.set_label_coords(0.45,1.525)
	
	plt.subplot(G2060[1:3,9])
	ax13.plot(dataslat[2], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax13.grid(False)
        ax13.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax13.spines['top'].set_visible(True)
	ax13.spines['right'].set_visible(True)
	ax13.spines['bottom'].set_visible(True)
	ax13.spines['left'].set_visible(True)
        ax13.get_xaxis().tick_bottom()
        ax13.get_yaxis().tick_left()
	ax13.set_ylim(-85,85)
	ax13.set_xlim(-25, 1.5)
	ax13.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-20,0], [str(x) + "\%" for x in [-20,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-20,-10,0]:    
              ax13.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax13.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2060[0,9])
	ax18.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax18.set_xlim(-1,1)
	ax18.set_ylim(-1,1)
	ax18.annotate(str(totalcol[2])[0:5] + '\%', xy = (-0.7,-0.20), fontsize = 14, fontweight = 'heavy')
	ax18.xaxis.set_label_coords(0.45,1.525)
	
	plt.subplot(G2070[1:3,9])
	ax14.plot(dataslat[3], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax14.grid(False)
        ax14.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax14.spines['top'].set_visible(True)
	ax14.spines['right'].set_visible(True)
	ax14.spines['bottom'].set_visible(True)
	ax14.spines['left'].set_visible(True)
        ax14.get_xaxis().tick_bottom()
        ax14.get_yaxis().tick_left()
	ax14.set_ylim(-85,85)
	ax14.set_xlim(-25, 1.5)
	ax14.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-20,0], [str(x) + "\%" for x in [-20,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-20,-10,0]:    
              ax14.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax14.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2070[0,9])
	ax19.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax19.set_xlim(-1,1)
	ax19.set_ylim(-1,1)
	ax19.annotate(str(totalcol[3])[0:5] + '\%', xy = (-0.7,-0.20), fontsize = 14, fontweight = 'heavy')
	ax19.xaxis.set_label_coords(0.45,1.525)	
	ax1.set_xlabel('7 Tg SO$_2$', fontsize = 12)
	ax2.set_xlabel('14 Tg SO$_2$', fontsize = 12)
	ax3.set_xlabel('17 Tg SO$_2$', fontsize = 12)
	ax4.set_xlabel('21 Tg SO$_2$', fontsize = 12)

def senstudy(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global ax1,ax2,ax3,ax4, ax5, ax6,ax7,ax8,ax9, ax10,dataslat, totalcol,ax11, ax12,fig,cbar, plt, levels, datas0,datas1,datas2, volcinjectlats, Gs, G2017, G2050, G2060, G2070, G2100

	datas0 = []
	datas1 = []
	datas2 = []
	dateflat = []
	CS = []
	years = [2100]
	volcdays = [531] 
	volctimes = []	
	dataslat = []
	totalcol = []

	datas0.append(datamodulator(var, dayt, 0, 0,1, 2100, num, flag))
	datas0.append(datamodulator(var, dayt, 1, 0,1, 2100, num, flag))
	datas0.append(datamodulator(var, dayt, 2, 0,1, 2100, num, flag))
	datas0.append(datamodulator(var, dayt, 3, 0,1, 2100, num, flag))
	datas1.append(datamodulator(var, dayt, 4, 0,1, 2100, num, flag))
	datas1.append(datamodulator(var, dayt, 5, 0,1, 2100, num, flag))
	datas1.append(datamodulator(var, dayt, 6, 0,1, 2100, num, flag))
	datas1.append(datamodulator(var, dayt, 7, 0,1, 2100, num, flag))
	datas1.append(datamodulator(var, dayt, 8, 0,1, 2100, num, flag))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	datas2.append(datas0[0][2].mean(0))
	datas2.append(datas0[1][2].mean(0))
	datas2.append(datas0[2][2].mean(0))
	datas2.append(datas0[3][2].mean(0))
	datas2.append(datas1[0][2].mean(0))
	datas2.append(datas1[1][2].mean(0))
	datas2.append(datas1[2][2].mean(0))
	datas2.append(datas1[3][2].mean(0))
	datas2.append(datas1[4][2].mean(0))
	dateflat.append(datas0[0][0][0])
	dateflat.append(datas0[1][0][0])
	dateflat.append(datas0[2][0][0])
	dateflat.append(datas0[3][0][0])
	dateflat.append(datas1[0][0][0])
	dateflat.append(datas1[1][0][0])
	dateflat.append(datas1[2][0][0])
	dateflat.append(datas1[3][0][0])
	dateflat.append(datas1[4][0][0])
	
	for x in range(len(datas0)):
		latarray = []
		for y in range(len(datas0[0][0])):
			latarray.append(datas0[x][2][y][20:72].mean())
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))
	lats = datas0[0][1].mean(1)
	for x in range(len(datas1)):
		latarray = []
		for y in range(len(datas1[0][0])):
			latarray.append(np.nanmean(datas1[x][2][y][20:]))
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))

	volclattropichigh = latitude_edges[12] - 15.9
	volclattropiclow = 15.9 - latitude_edges[10]
	
	levels =  np.array([-13,-11,-9,-7,-5,-3,-1,1,3,5,7])
	plt.figure
	Gs = gridspec.GridSpec(3,2, hspace = 0.0, wspace =0.05)
	G26 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[0], hspace = 0)
	G45 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[1], hspace = 0)
	G60 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[2], hspace = 0)
	G85 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[3], hspace = 0)
	Gsal = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[4:6], hspace=0, wspace = 0)
	ax1 = plt.subplot(G26[1:3,0:9])
	ax2 = plt.subplot(G45[1:3,0:9])
	ax3 = plt.subplot(G60[1:3,0:9])
	ax4 = plt.subplot(G85[1:3,0:9])
	ax5 = plt.subplot(Gsal[1:3,0:5])
	ax23 = plt.subplot(Gsal[1:3,5:])
	ax6 = plt.subplot(G26[0,0:9])
	ax7 = plt.subplot(G45[0,0:9])
	ax8 = plt.subplot(G60[0,0:9])
	ax9 = plt.subplot(G85[0,0:9])
	ax10 = plt.subplot(Gsal[0,0:2])
	ax11 = plt.subplot(Gsal[0,2:4])
	ax12 = plt.subplot(Gsal[0,4:6])
	ax13 = plt.subplot(Gsal[0,6:8])
	ax14 = plt.subplot(Gsal[0,8:])
	ax15 = plt.subplot(G26[1:3,9])
	ax16 = plt.subplot(G45[1:3,9])
	ax17 = plt.subplot(G60[1:3,9])
	ax18 = plt.subplot(G85[1:3,9])
	ax19 = plt.subplot(G26[0,9])
	ax20 = plt.subplot(G45[0,9])
	ax21 = plt.subplot(G60[0,9])
	ax22 = plt.subplot(G85[0,9])
	fig = plt.gcf()
	fig.set_facecolor('white')
	
	plt.subplot(G26[1:3,0:9])
	CS1 =plt.contourf(datas0[0][0],datas0[0][1],datas0[0][2],levels, cmap = cma)
	
	plt.subplot(G45[1:3,0:9])
	CS2 = plt.contourf(datas0[1][0],datas0[1][1],datas0[1][2],levels, cmap = cma)
	
	plt.subplot(G60[1:3,0:9])
	CS3 =plt.contourf(datas0[2][0],datas0[2][1],datas0[2][2],levels, cmap = cma)
	
	plt.subplot(G85[1:3,0:9])
	CS4 = plt.contourf(datas0[3][0],datas0[3][1],datas0[3][2],levels, cmap = cma)
	
	plt.subplot(Gsal[0,0:2])
	CS5 = plt.contourf(datas1[0][0], datas1[0][1],datas1[0][2], levels, cmap = cma)
	
	plt.subplot(Gsal[0,2:4])
	CS6 = plt.contourf(datas1[1][0], datas1[1][1],datas1[1][2], levels, cmap = cma)
	
	plt.subplot(Gsal[0,4:6])
	CS7 = plt.contourf(datas1[2][0], datas1[2][1],datas1[2][2], levels, cmap = cma)
	
	plt.subplot(Gsal[0,6:8])
	CS8 = plt.contourf(datas1[3][0], datas1[3][1],datas1[3][2], levels, cmap = cma, exgtend = "both")
	
	plt.subplot(Gsal[0,8:])
	CS9 = plt.contourf(datas1[4][0], datas1[4][1],datas1[4][2], levels, cmap = cma, extend="both")
	stringy = []
	stringy = ['','75$^{\circ}$S','', '45$^{\circ}$S','', '15$^{\circ}$S','', '15$^{\circ}$N','', '45$^{\circ}$N','', '75$^{\circ}$N', '']
	labstring = ['a','b','c','d','e','f','g','h','i','j','k','l']
	stringgy = []
	stringgy = ['','','', '45$^{\circ}$S','', '','', '','', '45$^{\circ}$N','', '', '']
	plt.subplot(G26[1:3,0:9])
	
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax1.xaxis.set_major_locator(years)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax1.xaxis.set_minor_locator(months)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax1.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75,-45, -15, 15, 45]:    
	      ax1.plot(datas0[0][0][0][0:70], [z] *len(datas0[0][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax1.plot(datas0[0][0][0],[0]*len(datas0[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax1.plot(datas0[0][0][0][0:70], [75] *len(datas0[0][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax1.set_ylabel('Latitudinal column deviations\n RCP 2.6', fontsize=10, fontweight='bold')
	ax1.yaxis.set_label_coords(0, 0.7)
	ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax1.annotate(labstring[0],xy = labellocation, fontsize=16, fontweight='bold')
	plt.xticks(rotation=15, fontsize=10, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax1.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax1.set_ylim(-85,85)
	ax1.set_xlabel('Temporal column ozone deviations', fontsize = 10, fontweight = 'heavy', horizontalalignment = 'left')
	ax1.xaxis.set_label_coords(0,1.59)	
	
	plt.subplot(G45[1:3,0:9])
	years2 = mdates.YearLocator()
	months2 = mdates.MonthLocator()
	minorLocator2 = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax2.plot(datas0[1][0][0], [z] *len(datas0[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45]:    
	      ax2.plot(datas0[1][0][0][0:70], [z] *len(datas0[1][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax2.plot(datas0[1][0][0],[0]*len(datas0[1][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax2.plot(datas0[0][0][0][0:70], [75] *len(datas0[0][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax2.set_ylabel('RCP 4.5', fontsize=10, fontweight='bold')
	ax2.yaxis.set_label_coords(0, 0.7)
	ax2.scatter(volctimes[1], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.xaxis.set_major_locator(years2)
	ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax2.xaxis.set_minor_locator(months2)
	ax2.annotate(labstring[1],xy = labellocation, fontsize=16, fontweight='bold')
	plt.xticks(rotation=15, fontsize=10, fontweight='bold')
	
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax2.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax2.set_ylim(-85,85)
	
	
	plt.subplot(G60[1:3,0:9])
	labellocation = (DT.date(2101,1,25), -75)
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax3.plot(datas0[2][0][0], [z] *len(datas0[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45]:    
	      ax3.plot(datas0[2][0][0][0:70], [z] *len(datas0[2][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax3.plot(datas0[2][0][0],[0]*len(datas0[2][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax3.plot(datas0[0][0][0][0:70], [75] *len(datas0[0][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax3.set_ylabel('RCP 6.0', fontsize=10, fontweight='bold')
	ax3.yaxis.set_label_coords(0, 0.7)
	ax3.scatter(volctimes[2], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	ax3.set_ylim(-85,85)
	for tick in ax3.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	years3 = mdates.YearLocator()
	months3 = mdates.MonthLocator()
	minorLocator3 = MultipleLocator(2.5)
	ax3.xaxis.set_major_locator(years3)
	ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax3.xaxis.set_minor_locator(months3)
	plt.xticks(rotation=15, fontsize=10, fontweight='bold')
	ax3.annotate(labstring[2],xy = labellocation, fontsize=16, fontweight='bold')
	ax3.set_ylim(-85,85)
	
	plt.subplot(G85[1:3,0:9])
	years3a = mdates.YearLocator()
	months3a = mdates.MonthLocator()
	minorLocator3 = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax4.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax4.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45]:    
	      ax4.plot(datas0[3][0][0][0:70], [z] *len(datas0[3][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax4.plot(datas0[3][0][0],[0]*len(datas0[3][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax4.plot(datas0[0][0][0][0:70], [75] *len(datas0[0][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax4.set_ylabel('RCP 8.5', fontsize=10, fontweight='bold')
	ax4.yaxis.set_label_coords(0, 0.7)
	ax4.scatter(volctimes[3], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	ax4.xaxis.set_major_locator(years3a)
	ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax4.xaxis.set_minor_locator(months3a)
	plt.xticks(rotation=15, fontsize=10, fontweight='bold')
	ax4.annotate(labstring[3],xy = labellocation, fontsize=16, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax4.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax4.set_ylim(-85,85)

	plt.subplot(Gsal[0,0:2])
	
	yearssala = mdates.YearLocator()
	monthssala = mdates.MonthLocator()
	minorLocatorsala = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax10.axvline(x=volctimes[3],ymin = 0, ymax = 0.8,color='k',ls='dashed')
	ax10.set_xlim(DT.date(2101,1,1), DT.date(2105,1,1))
	ax10.tick_params(axis="both", which="both", bottom="off", top="off", labeltop="off", labelbottom="off", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-75, -45, -15, 15, 45]:    
	      ax10.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	ax10.plot(datas0[3][0][0][38:],[75]*len(datas0[3][0][0][38:]), "--", lw= 0.5, color = "black", alpha=0.3)	
	ax10.xaxis.set_major_locator(yearssala)
	ax10.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax10.xaxis.set_minor_locator(monthssala)
	plt.xticks(rotation=15, fontsize=10, fontweight='bold')
	ax10.annotate(labstring[4],xy = labellocation, fontsize=16, fontweight='bold')
	ax10.set_ylim(-85,85)
	ax10.annotate('+' + str(0.03) + '\% $\Delta$Column O3', xy = (DT.date(2101,2,1),40), fontsize = 10, fontweight = 'heavy')
	plt.subplot(Gsal[0,2:4])
	
	yearssala = mdates.YearLocator()
	monthssala = mdates.MonthLocator()
	minorLocatorsala = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax11.axvline(x=volctimes[3],ymin = 0, ymax = 0.8,color='k',ls='dashed')
	ax11.set_xlim(DT.date(2101,1,1), DT.date(2105,1,1))
	ax11.tick_params(axis="both", which="both", bottom="off", top="off", labeltop="off", labelbottom="off", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-75, -45, -15, 15, 45]:    
	      ax11.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	
	ax11.plot(datas0[3][0][0][21:],[75]*len(datas0[3][0][0][21:]), "--", lw= 0.5, color = "black", alpha=0.3)	
	ax11.xaxis.set_major_locator(yearssala)
	ax11.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax11.xaxis.set_minor_locator(monthssala)
	plt.xticks(rotation=15, fontsize=10, fontweight='bold')
	ax11.annotate(labstring[5],xy = labellocation, fontsize=16, fontweight='bold')
	ax11.set_ylim(-85,85)
	ax11.annotate(str(-0.3) + '\%', xy = (DT.date(2101,2,1),58), fontsize = 10, fontweight = 'heavy')
	plt.subplot(Gsal[0,4:6])
	
	yearssala = mdates.YearLocator()
	monthssala = mdates.MonthLocator()
	minorLocatorsala = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax12.axvline(x=volctimes[3],ymin = 0, ymax = 0.8,color='k',ls='dashed')
	ax12.set_xlim(DT.date(2101,1,1), DT.date(2105,1,1))
	ax12.tick_params(axis="both", which="both", bottom="off", top="off", labeltop="off", labelbottom="off", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-75, -45, -15, 15, 45]:    
	      ax12.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	
	ax12.plot(datas0[3][0][0][22:],[75]*len(datas0[3][0][0][22:]), "--", lw= 0.5, color = "black", alpha=0.3)	
	ax12.xaxis.set_major_locator(yearssala)
	ax12.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax12.xaxis.set_minor_locator(monthssala)
	plt.xticks(rotation=15, fontsize=10, fontweight='bold')
	ax12.annotate(labstring[6],xy = (DT.date(2101,1,25),-65), fontsize=16, fontweight='bold')
	ax12.set_ylim(-85,85)
	ax12.annotate(str(-0.2) + '\%', xy = (DT.date(2101,2,1),58), fontsize = 10, fontweight = 'heavy')
	plt.subplot(Gsal[0,6:8])
	
	yearssala = mdates.YearLocator()
	monthssala = mdates.MonthLocator()
	minorLocatorsala = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax13.axvline(x=volctimes[3],ymin = 0, ymax = 0.8,color='k',ls='dashed')
	ax13.set_xlim(DT.date(2101,1,1), DT.date(2105,1,1))
	ax13.tick_params(axis="both", which="both", bottom="off", top="off", labeltop="off", labelbottom="off", left="off", right="off",labelright = "off", labelleft="off")
	for z in [-75, -45, -15, 15, 45]:    
	      ax13.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	
	ax13.plot(datas0[3][0][0][22:],[75]*len(datas0[3][0][0][22:]), "--", lw= 0.5, color = "black", alpha=0.3)	
	ax13.xaxis.set_major_locator(yearssala)
	ax13.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax13.xaxis.set_minor_locator(monthssala)
	plt.xticks(rotation=15, fontsize=10, fontweight='bold')
	ax13.annotate(labstring[7],xy = labellocation, fontsize=16, fontweight='bold')
	ax13.set_ylim(-85,85)
	ax13.annotate(str(-0.1) + '\%', xy = (DT.date(2101,2,1),58), fontsize = 10, fontweight = 'heavy')
	plt.subplot(Gsal[0,8:])
	
	yearssala = mdates.YearLocator()
	monthssala = mdates.MonthLocator()
	minorLocatorsala = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax14.axvline(x=volctimes[3], ymin=0, ymax = 0.8,color='k',ls='dashed')
	ax14.set_xlim(DT.date(2101,1,1), DT.date(2105,1,1))
	ax14.tick_params(axis="both", which="both", bottom="off", top="off", labeltop="off", labelbottom="off", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-45, 45]:    
	      ax14.plot(datas0[3][0][0][0:60], [z] *len(datas0[3][0][0][0:60]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -15, 15]:    
	      ax14.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	
	ax14.plot(datas0[3][0][0][22:],[75]*len(datas0[3][0][0][22:]), "--", lw= 0.5, color = "black", alpha=0.3)	
	ax14.xaxis.set_major_locator(yearssala)
	ax14.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax14.xaxis.set_minor_locator(monthssala)
	plt.xticks(rotation=15, fontsize=10, fontweight='bold')
	ax14.annotate(labstring[8],xy = labellocation, fontsize=16, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,73,90], [stringgy[w] for w in range(len(stringgy))], fontsize=9)
	for tick in ax14.yaxis.get_major_ticks():
		tick.set_pad(-22)
		tick.label2.set_horizontalalignment('left')
	ax14.set_ylim(-85,85)

	ax14.annotate(str(-1.3) + '\%', xy = (DT.date(2101,2,1),58),alpha = 1, fontsize = 10, fontweight = 'heavy')
	cbar_ax = fig.add_axes([0.02, 0.97, 0.97, 0.01])
	fmt = '%1.0f'
	tix =  levels
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt, orientation = 'horizontal')
	cbar_ax.tick_params(labelsize = 10)
	cbar.set_label('Percent change in column ozone', fontsize=10, fontweight='bold', labelpad = -33)


	plt.subplot(G26[0,0:9])
	ax6.plot(dateflat[0][18:], datas2[0][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	years5 = mdates.YearLocator()
	months5 = mdates.MonthLocator()
	minorLocator5 = MultipleLocator(2.5)
	ax6.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax6.grid(False)
        ax6.xaxis.set_minor_locator(months5)
        ax6.xaxis.set_major_locator(years5)
        ax6.yaxis.set_minor_locator(minorLocator5)
        ax6.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax6.spines['top'].set_visible(True)
	ax6.spines['right'].set_visible(True)
	ax6.spines['bottom'].set_visible(True)
	ax6.spines['left'].set_visible(True)
        ax6.get_xaxis().tick_bottom()
        ax6.get_yaxis().tick_left()
	ax6.axvline(x=volctimes[0],color='k',ls='dashed')
	ax6.set_ylim(-2.5,0.5)
        plt.yticks([-2,-1,0], [str(x) + "\%" for x in [-2,-1,0]], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in [-2,-1,0]:    
              ax6.plot(dateflat[0][18:], [y] *len(dateflat[0][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax6.yaxis.get_major_ticks():
		tick.set_pad(-30)
		tick.label2.set_horizontalalignment('left')

	plt.subplot(G45[0,0:9])
	years6 = mdates.YearLocator()
	months6 = mdates.MonthLocator()
	minorLocator6 = MultipleLocator(2.5)
	ax7.plot(dateflat[1][18:], datas2[1][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax7.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax7.grid(False)
        ax7.xaxis.set_minor_locator(months6)
        ax7.xaxis.set_major_locator(years6)
        ax7.yaxis.set_minor_locator(minorLocator6)
        ax7.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax7.spines['top'].set_visible(True)
	ax7.spines['right'].set_visible(True)
	ax7.spines['bottom'].set_visible(True)
	ax7.spines['left'].set_visible(True)
        ax7.get_xaxis().tick_bottom()
        ax7.get_yaxis().tick_left()
	ax7.axvline(x=volctimes[1],color='k',ls='dashed')
	ax7.set_ylim(-2.5,0.5)
        plt.yticks(range(-2,1,1), [str(x) + "\%" for x in range(-2,1,1)], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in range(-2,1,1):    
              ax7.plot(dateflat[1][18:], [y] *len(dateflat[1][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax7.yaxis.get_major_ticks():
		tick.set_pad(-30)
		tick.label2.set_horizontalalignment('left')

	plt.subplot(G60[0,0:9])
	years8 = mdates.YearLocator()
	months8 = mdates.MonthLocator()
	minorLocator8 = MultipleLocator(2.5)
	ax8.plot(dateflat[2][18:], datas2[2][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax8.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax8.grid(False)
        ax8.xaxis.set_minor_locator(months8)
        ax8.xaxis.set_major_locator(years8)
        ax8.yaxis.set_minor_locator(minorLocator8)
        ax8.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax8.spines['top'].set_visible(True)
	ax8.spines['right'].set_visible(True)
	ax8.spines['bottom'].set_visible(True)
	ax8.spines['left'].set_visible(True)
        ax8.get_xaxis().tick_bottom()
        ax8.get_yaxis().tick_left()
	ax8.axvline(x=volctimes[0],color='k',ls='dashed')
	ax8.set_ylim(-1.5,1.5)
        plt.yticks(range(-1,2,1), [str(x) + "\%" for x in range(-1,2,1)], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in range(-1,2,1):    
              ax8.plot(dateflat[2][18:], [y] *len(dateflat[2][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax8.yaxis.get_major_ticks():
		tick.set_pad(-30)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G85[0,0:9])
	years9 = mdates.YearLocator()
	months9 = mdates.MonthLocator()
	minorLocator9 = MultipleLocator(2.5)
	ax9.plot(dateflat[3][18:], datas2[3][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax9.set_xlim(DT.date(2101,1,1), DT.date(2105,7,1))
	ax9.grid(False)
        ax9.xaxis.set_minor_locator(months9)
        ax9.xaxis.set_major_locator(years9)
        ax9.yaxis.set_minor_locator(minorLocator9)
        ax9.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax9.spines['top'].set_visible(True)
	ax9.spines['right'].set_visible(True)
	ax9.spines['bottom'].set_visible(True)
	ax9.spines['left'].set_visible(True)
        ax9.get_xaxis().tick_bottom()
        ax9.get_yaxis().tick_left()
	ax9.axvline(x=volctimes[3],color='k',ls='dashed')
	ax9.set_ylim(-1.5,1.5)
        plt.yticks([-1,0,1], [str(x) + "\%" for x in [-1,0,1]], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in [-1,0,1]:    
              ax9.plot(dateflat[3][18:], [y] *len(dateflat[3][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax9.yaxis.get_major_ticks():
		tick.set_pad(-30)
		tick.label2.set_horizontalalignment('left')

	plt.subplot(Gsal[1:3,0:5])
	years10 = mdates.YearLocator()
	labellocation = (DT.date(2101,3,15), -2.78)
	months10 = mdates.MonthLocator()
	minorLocator10 = MultipleLocator(2.5)
	ax5.plot(dateflat[4][18:], datas2[4][18:], 'b-', lw = 2, label = '0 ppmv CH4')
	ax5.plot(dateflat[5][18:], datas2[5][18:], 'g-', lw = 2, label = '1 ppmv CH4')
	ax5.plot(dateflat[6][18:], datas2[6][18:], 'k-', lw = 2, label = '2 ppmv CH4')
	ax5.plot(dateflat[7][18:], datas2[7][18:], 'orange', lw = 2, label = '3 ppmv CH4')
	ax5.plot(dateflat[8][18:], datas2[8][18:], 'r-', lw = 2, label = '4 ppmv CH4')
	ax5.set_xlim(DT.date(2101,3,1), DT.date(2105,1,1))
	ax5.grid(False)
        ax5.xaxis.set_minor_locator(months10)
        ax5.xaxis.set_major_locator(years10)
        ax5.yaxis.set_minor_locator(minorLocator10)
        ax5.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax5.spines['top'].set_visible(True)
	ax5.spines['right'].set_visible(True)
	ax5.spines['bottom'].set_visible(True)
	ax5.spines['left'].set_visible(True)
        ax5.get_xaxis().tick_bottom()
        ax5.get_yaxis().tick_left()
	ax5.axvline(x=volctimes[4],color='k',ls='dashed')
	ax5.set_ylim(-3.1,2.9)
	ax5.set_ylabel('VSL Br sensitivity\n  RCP 6.0', fontsize=10, fontweight='bold')
	ax5.yaxis.set_label_coords(0, 0.7)
        plt.yticks([-2,-1,0,1,2], [str(x) + "\%" for x in [-2,-1,0,1,2]], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="on", labelright = "off")  
	plt.xticks(rotation=15, fontsize=10, fontweight='bold')
 	for y in range(-2,3,1):    
              ax5.plot(dateflat[4][19:], [y] *len(dateflat[4][19:]), "--", lw=1, color="black", alpha=0.3)
       	ax5.plot(dateflat[4][19:], [0]*len(dateflat[4][19:]), "--", lw=2, color = "black", alpha = 0.3)
#	ax5.axvspan(dateflat[4][0], volctimes[4], alpha = 0.5, color = 'lightblue')
	for tick in ax5.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')       
	ax5.annotate(labstring[9],xy = labellocation, fontsize=16, fontweight='bold')
        handles, labels = ax5.get_legend_handles_labels()
        ax5.legend(handles, labels, bbox_to_anchor=(1,1.8),frameon = False, loc = 'upper center',ncol = 5, fancybox = False, fontsize=10, columnspacing = 10.5, handletextpad = 0.5) 
	ax5.set_xlabel('Model year', fontsize=10, fontweight='bold')	
	ax5.annotate('Column ozone deviation', xy = (DT.date(2101,7,25), 2.25), fontsize = 10, fontweight = 'heavy')

	plt.subplot(G26[1:3,9])
	ax15.plot(dataslat[0], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax15.grid(False)
        ax15.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax15.spines['top'].set_visible(True)
	ax15.spines['right'].set_visible(True)
	ax15.spines['bottom'].set_visible(True)
	ax15.spines['left'].set_visible(True)
        ax15.get_xaxis().tick_bottom()
        ax15.get_yaxis().tick_left()
	ax15.set_ylim(-85,85)
	ax15.set_xlim(-3.5, 0.5)
	ax15.xaxis.set_label_coords(1,-0.17)
        plt.xticks([-3,0], [str(x) + "\%" for x in [-3,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-3,-1.5,0]:    
              ax15.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax15.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G26[0,9])
	ax19.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax19.set_xlim(-1,1)
	ax19.set_ylim(-1,1)
	ax19.annotate( '-0.6\%', xy = (-0.75,-0.20), fontsize = 14, fontweight = 'heavy')
	ax19.xaxis.set_label_coords(1,1.525)
	ax19.set_xlabel('Global-temporal\n average', fontsize = 10, fontweight = 'heavy', horizontalalignment = 'right')
	ax19.xaxis.set_label_coords(1,1.37)	

	plt.subplot(G45[1:3,9])
	ax16.plot(dataslat[1], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax16.grid(False)
        ax16.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax16.spines['top'].set_visible(True)
	ax16.spines['right'].set_visible(True)
	ax16.spines['bottom'].set_visible(True)
	ax16.spines['left'].set_visible(True)
        ax16.get_xaxis().tick_bottom()
        ax16.get_yaxis().tick_left()
	ax16.set_ylim(-85,85)
	ax16.set_xlim(-2.5, 0.5)
	ax16.xaxis.set_label_coords(1,-0.17)
        plt.xticks([-2,0], [str(x) + "\%" for x in [-2,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-2,-1,0]:    
              ax16.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax16.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G45[0,9])
	ax20.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax20.set_xlim(-1,1)
	ax20.set_ylim(-1,1)
	ax20.annotate( '-0.5\%', xy = (-0.75,-0.20), fontsize = 14, fontweight = 'heavy')
	ax20.xaxis.set_label_coords(1,1.525)
	
	plt.subplot(G60[1:3,9])
	ax17.plot(dataslat[2], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax17.grid(False)
        ax17.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax17.spines['top'].set_visible(True)
	ax17.spines['right'].set_visible(True)
	ax17.spines['bottom'].set_visible(True)
	ax17.spines['left'].set_visible(True)
        ax17.get_xaxis().tick_bottom()
        ax17.get_yaxis().tick_left()
	ax17.set_ylim(-85,85)
	ax17.set_xlim(-2.25,0.5)
	ax17.xaxis.set_label_coords(1,-0.17)
        plt.xticks([-2, 0], [str(x) + "\%" for x in [-2,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-2,-1, 0]:    
              ax17.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax17.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G60[0,9])
	ax21.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax21.set_xlim(-1,1)
	ax21.set_ylim(-1,1)
	ax21.annotate( '-0.2\%', xy = (-0.75,-0.20), fontsize = 14, fontweight = 'heavy')
	ax21.xaxis.set_label_coords(1,1.525)
	
	plt.subplot(G85[1:3,9])
	ax18.plot(dataslat[3], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax18.grid(False)
        ax18.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax18.spines['top'].set_visible(True)
	ax18.spines['right'].set_visible(True)
	ax18.spines['bottom'].set_visible(True)
	ax18.spines['left'].set_visible(True)
        ax18.get_xaxis().tick_bottom()
        ax18.get_yaxis().tick_left()
	ax18.set_ylim(-85,85)
	ax18.set_xlim(-1.25, 1.25)
	ax18.xaxis.set_label_coords(1,-0.17)
        plt.xticks([-1,1], [str(x) + "\%" for x in [-1,1]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-1,0,1]:    
              ax18.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax18.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G85[0,9])
	ax22.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax22.set_xlim(-1,1)
	ax22.set_ylim(-1,1)
	ax22.annotate( '-0.2' + '\%', xy = (-0.75,-0.20), fontsize = 14, fontweight = 'heavy')
	ax22.xaxis.set_label_coords(1,1.525)

	plt.subplot(Gsal[1:3,5:])
	labellocation = (-3.4,-80)
	ax23.plot(dataslat[4], lats, 'b-', lw = 2, label = '0 ppmv CH4')
	ax23.plot(dataslat[5], lats, 'g-', lw = 2, label = '1 ppmv CH4')
	ax23.plot(dataslat[6], lats, 'k-', lw = 2, label = '2 ppmv CH4')
	ax23.plot(dataslat[7], lats, 'orange', lw = 2, label = '3 ppmv CH4')
	ax23.plot(dataslat[8], lats, 'r-', lw = 2, label = '4 ppmv CH4')
	ax23.grid(False)
        ax23.tick_params(axis = 'both', which = 'major', labelsize = 10, zorder = 10)
        ax23.spines['top'].set_visible(True)
	ax23.spines['right'].set_visible(True)
	ax23.spines['bottom'].set_visible(True)
	ax23.spines['left'].set_visible(True)
        ax23.get_xaxis().tick_bottom()
        ax23.get_yaxis().tick_left()
	ax23.set_ylim(-85,85)
	ax23.set_xlim(-3.5, 2)
	ax23.set_xlabel('Time-averaged column ozone deviation', fontsize = 10, fontweight = 'heavy')
        plt.xticks([-3,-2,-1,0,1], [str(x) + "\%" for x in [-3,-2,-1,0,1]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-3,-2,-1,0,1]:    
              ax23.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax23.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	ax23.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	
	ax23.annotate(labstring[10],xy = labellocation, fontsize=16, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold', zorder = 10)
	for tick in ax23.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax23.set_ylim(-85,85)
	for z in [-90,-60,-30,30,60,90]:    
	      ax23.plot(lats, [z] *len(lats), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45,75]:    
	      ax23.plot(lats, [z] *len(lats), "--", lw=0.5, color="black", alpha=0.3, zorder = 0)
	ax23.plot(lats,[0]*len(lats), "--", lw = 2, color = "black", alpha = 0.3)
       	ax23.axvspan(1.75, 3, alpha = 1, color = 'white', zorder = 1)

def brfig(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global ax1,ax2,ax3,ax4, ax5, ax6,ax7,ax8,ax9, ax10, ax11, ax12,ax19,fig,cbar, plt, levels, datas0,datas1,datas2, dataslat, totalcol, volcinjectlats, Gs, G2017, G2050, G2060, G2070, G2100

	datas0 = []
	datas1 = []
	datas2 = []
	dateflat = []
	CS = []
	years = [2100]
	volcdays = [531] 
	volctimes = []
	dataslat=[]
	totalcol = []	


	datas0.append(datamodulator(var, dayt, 0, 0,1, 2100, num, flag))
	datas0.append(datamodulator(var, dayt, 0, 1,13, 2100, num, flag))
	datas0.append(datamodulator(var, dayt, 0, 13,9, 2100, num, flag))
	datas0.append(datamodulator(var, dayt, 0, 1,11, 2100, num, flag))
	datas0.append(datamodulator(var, dayt, 0, 11,7, 2100, num, flag))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	volctimes.append(volclocator(531, 2100))
	datas1.append(datas0[0][2].mean(0))
	datas1.append(datas0[1][2].mean(0))
	datas1.append(datas0[2][2].mean(0))
	datas1.append(datas0[3][2].mean(0))
	datas1.append(datas0[4][2].mean(0))
	dateflat.append(datas0[0][0][0])
	dateflat.append(datas0[1][0][0])
	dateflat.append(datas0[2][0][0])
	dateflat.append(datas0[3][0][0])
	dateflat.append(datas0[4][0][0])
	
	for x in range(len(datas0)):
		latarray = []
		for y in range(len(datas0[0][0])):
			latarray.append(datas0[x][2][y][20:59].mean())
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray[13:16]))
	lats = datas0[0][1].mean(1)
	
	volclattropichigh = latitude_edges[12] - 15.9
	volclattropiclow = 15.9 - latitude_edges[10]
	#levels =  np.array([-25,-20,-17,-15,-13,-11,-9,-7,-5,-3,-1,1,3,5,7,9,11, 13])
	levels =  np.array([-80,-70,-60,-50,-40,-30,-25,-20, -15,-10,-8, -6,-4,-2,-1,1,2,])
	
	plt.figure
	Gs = gridspec.GridSpec(5,1, hspace = 0)
	G2017 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[0])
	G2050 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[1])
	G2060 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[2])
	G2070 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[3])
	G2100 = gridspec.GridSpecFromSubplotSpec(4,10,subplot_spec=Gs[4])
	ax1 = plt.subplot(G2017[1:3,0:9])
	ax2 = plt.subplot(G2050[1:3,0:9])
	ax3 = plt.subplot(G2060[1:3,0:9])
	ax4 = plt.subplot(G2070[1:3,0:9])
	ax5 = plt.subplot(G2100[1:3,0:9])
	ax6 = plt.subplot(G2017[0,0:9])
	ax7 = plt.subplot(G2050[0,0:9])
	ax8 = plt.subplot(G2060[0,0:9])
	ax9 = plt.subplot(G2070[0,0:9])
	ax10 = plt.subplot(G2100[0,0:9])
	ax11 = plt.subplot(G2017[1:3,9])
	ax12 = plt.subplot(G2050[1:3,9])
	ax13 = plt.subplot(G2060[1:3,9])
	ax14 = plt.subplot(G2070[1:3,9])
	ax15 = plt.subplot(G2100[1:3,9])
	ax16 = plt.subplot(G2017[0,9])
	ax17 = plt.subplot(G2050[0,9])
	ax18 = plt.subplot(G2060[0,9])
	ax19 = plt.subplot(G2070[0,9])
	ax20 = plt.subplot(G2100[0,9])
	
	fig = plt.gcf()
	fig.set_facecolor('white')
	plt.subplot(G2017[1:3,0:9])
	
	CS1 =plt.contourf(datas0[0][0],datas0[0][1],datas0[0][2],levels, cmap = cma, extend = "both")
	plt.subplot(G2050[1:3,0:9])
	CS2 = plt.contourf(datas0[1][0],datas0[1][1],datas0[1][2],levels, cmap = cma)
	plt.subplot(G2060[1:3,0:9])
	CS3 =plt.contourf(datas0[2][0],datas0[2][1],datas0[2][2],levels, cmap = cma, extend = "both")
	plt.subplot(G2070[1:3,0:9])
	CS4 = plt.contourf(datas0[3][0],datas0[3][1],datas0[3][2],levels, cmap = cma, extend = "both")
	
	plt.subplot(G2100[1:3,0:9])
	CS5 = plt.contourf(datas0[4][0],datas0[4][1],datas0[4][2],levels, cmap = cma, extend = "both")

	stringy = []
	stringy = ['','75$^{\circ}$S','', '45$^{\circ}$S','', '15$^{\circ}$S','', '15$^{\circ}$N','', '45$^{\circ}$N','', '75$^{\circ}$N', '']
	labstring = ['a','b','c','d','e','f','g','h','i','j','k','l']
	
	plt.subplot(G2017[1:3,0:9])
	
	years = mdates.YearLocator()
	months = mdates.MonthLocator()
	minorLocator = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_xlim(DT.date(2101,1,1), DT.date(2106,7,1))
	ax1.xaxis.set_major_locator(years)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax1.xaxis.set_minor_locator(months)
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax1.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax1.plot(datas0[0][0][0][0:83], [z] *len(datas0[0][0][0][0:83]), "--", lw=0.5, color="black", alpha=0.3)
	ax1.plot(datas0[0][0][0],[0]*len(datas0[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax1.annotate(labstring[0],xy = labellocation, fontsize=16, fontweight='heavy')
	plt.xticks(rotation=15, fontsize=10, fontweight='heavy')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	for tick in ax1.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax1.set_ylim(-85,85)
	ax1.set_ylabel('Latitudinal column deviations', fontsize = 10, fontweight = 'heavy')	
	ax1.yaxis.set_label_coords(-0.005,0.74)

	
	plt.subplot(G2050[1:3,0:9])
	years2 = mdates.YearLocator()
	months2 = mdates.MonthLocator()
	minorLocator2 = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_xlim(DT.date(2101,1,1), DT.date(2106,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax2.plot(datas0[1][0][0], [z] *len(datas0[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax2.plot(datas0[1][0][0][0:83], [z] *len(datas0[1][0][0][0:83]), "--", lw=0.5, color="black", alpha=0.3)
	ax2.plot(datas0[1][0][0],[0]*len(datas0[1][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax2.scatter(volctimes[1], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.xaxis.set_major_locator(years2)
	ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax2.xaxis.set_minor_locator(months2)
	ax2.annotate(labstring[1],xy = labellocation, fontsize=16, fontweight='heavy')
	plt.xticks(rotation=15, fontsize=10, fontweight='heavy')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	
	for tick in ax2.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax2.set_ylim(-85,85)
	plt.subplot(G2060[1:3,0:9])
	
	labellocation = (DT.date(2101,1,25), -75)
	ax3.axvline(x=volctimes[2],color='k',ls='dashed')
	ax3.set_xlim(DT.date(2101,1,1), DT.date(2106,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax3.plot(datas0[2][0][0], [z] *len(datas0[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax3.plot(datas0[2][0][0][0:83], [z] *len(datas0[2][0][0][0:83]), "--", lw=0.5, color="black", alpha=0.3)
	ax3.plot(datas0[2][0][0],[0]*len(datas0[2][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax3.scatter(volctimes[2], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[2],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	ax3.set_ylim(-85,85)
	for tick in ax3.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	years3 = mdates.YearLocator()
	months3 = mdates.MonthLocator()
	minorLocator3 = MultipleLocator(2.5)
	ax3.xaxis.set_major_locator(years3)
	ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax3.xaxis.set_minor_locator(months3)
	plt.xticks(rotation=15, fontsize=10, fontweight='heavy')
	ax3.annotate(labstring[2],xy = labellocation, fontsize=16, fontweight='heavy')
	ax3.set_ylim(-85,85)
	
	plt.subplot(G2070[1:3,0:9])
	
	years3a = mdates.YearLocator()
	months3a = mdates.MonthLocator()
	minorLocator3 = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_xlim(DT.date(2101,1,1), DT.date(2106,7,1))
	ax4.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax4.plot(datas0[3][0][0], [z] *len(datas0[3][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax4.plot(datas0[3][0][0][0:83], [z] *len(datas0[3][0][0][0:83]), "--", lw=0.5, color="black", alpha=0.3)
	ax4.plot(datas0[3][0][0],[0]*len(datas0[3][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax4.scatter(volctimes[3], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[3],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	ax4.xaxis.set_major_locator(years3a)
	ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax4.xaxis.set_minor_locator(months3a)
	plt.xticks(rotation=15, fontsize=10, fontweight='heavy')
	ax4.annotate(labstring[3],xy = labellocation, fontsize=16, fontweight='heavy')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	for tick in ax4.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax4.set_ylim(-85,85)


	ax4.set_xlabel('Model year', fontsize =10, fontweight = 'heavy', horizontalalignment='center')
	#ax5.xaxis.set_label_coords(0,-0.2)

	plt.subplot(G2100[1:3,0:9])
	
	years3a = mdates.YearLocator()
	months3a = mdates.MonthLocator()
	minorLocator3 = MultipleLocator(2.5)
	labellocation = (DT.date(2101,1,25), -75)
	ax5.axvline(x=volctimes[4],color='k',ls='dashed')
	ax5.set_xlim(DT.date(2101,1,1), DT.date(2106,7,1))
	ax5.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax5.plot(datas0[4][0][0], [z] *len(datas0[4][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax5.plot(datas0[4][0][0][0:83], [z] *len(datas0[4][0][0][0:83]), "--", lw=0.5, color="black", alpha=0.3)
	ax5.plot(datas0[4][0][0],[0]*len(datas0[4][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax5.scatter(volctimes[4], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[4],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	
	ax5.xaxis.set_major_locator(years3a)
	ax5.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax5.xaxis.set_minor_locator(months3a)
	plt.xticks(rotation=15, fontsize=10, fontweight='heavy')
	ax5.annotate(labstring[4],xy = labellocation, fontsize=16, fontweight='heavy')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='heavy')
	for tick in ax5.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	ax5.set_ylim(-85,85)


	ax5.set_xlabel('Model year', fontsize =10, fontweight = 'heavy', horizontalalignment='center')
	cbar_ax = fig.add_axes([0.03, 0.97, 0.95, 0.01])
	fmt = '%1.0f'
	tix =  levels
	cbar = fig.colorbar(CS2, cax = cbar_ax, ticks = tix, format =fmt, orientation = 'horizontal')
	cbar_ax.tick_params(labelsize = 10)
	cbar.set_label('Percent change in column ozone - RCP 2.6', fontsize=10, fontweight='heavy', labelpad = -40)


	plt.subplot(G2017[0,0:9])
	ax6.plot(dateflat[0][18:], datas1[0][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	years5 = mdates.YearLocator()
	months5 = mdates.MonthLocator()
	minorLocator5 = MultipleLocator(2.5)
	ax6.set_xlim(DT.date(2101,1,1), DT.date(2106,7,1))
	ax6.grid(False)
        ax6.xaxis.set_minor_locator(months5)
        ax6.xaxis.set_major_locator(years5)
        ax6.yaxis.set_minor_locator(minorLocator5)
        ax6.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax6.spines['top'].set_visible(True)
	ax6.spines['right'].set_visible(True)
	ax6.spines['bottom'].set_visible(True)
	ax6.spines['left'].set_visible(True)
        ax6.get_xaxis().tick_bottom()
        ax6.get_yaxis().tick_left()
	ax6.axvline(x=volctimes[0],color='k',ls='dashed')
	ax6.set_ylim(-8.5,2.5)
	ax6.set_xlabel('Temporal column ozone deviations', fontsize = 10, fontweight = 'heavy')	
	ax6.xaxis.set_label_coords(0.21,1.225)
	plt.yticks([-6,-3,0], [str(x) + "\%" for x in [-6,-3,0]], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", labeltop='off',right="off", labelleft="on", labelright = "off")  
 	for y in [-6,-3,0]:    
              ax6.plot(dateflat[0][18:], [y] *len(dateflat[0][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax6.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2050[0,0:9])
	years6 = mdates.YearLocator()
	months6 = mdates.MonthLocator()
	minorLocator6 = MultipleLocator(2.5)
	ax7.plot(dateflat[1][18:], datas1[1][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax7.set_xlim(DT.date(2101,1,1), DT.date(2106,7,1))
	ax7.grid(False)
        ax7.xaxis.set_minor_locator(months6)
        ax7.xaxis.set_major_locator(years6)
        ax7.yaxis.set_minor_locator(minorLocator6)
        ax7.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax7.spines['top'].set_visible(True)
	ax7.spines['right'].set_visible(True)
	ax7.spines['bottom'].set_visible(True)
	ax7.spines['left'].set_visible(True)
        ax7.get_xaxis().tick_bottom()
        ax7.get_yaxis().tick_left()
	ax7.axvline(x=volctimes[1],color='k',ls='dashed')
	ax7.set_ylim(-8.5,2.5)
        plt.yticks([-6,-3,0], [str(x) + "\%" for x in [-6,-3,0]], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in [-6,-3,0]:    
              ax7.plot(dateflat[1][18:], [y] *len(dateflat[1][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax7.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2060[0,0:9])
	years8 = mdates.YearLocator()
	months8 = mdates.MonthLocator()
	minorLocator8 = MultipleLocator(2.5)
	ax8.plot(dateflat[2][18:], datas1[2][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax8.set_xlim(DT.date(2101,1,1), DT.date(2106,7,1))
	ax8.grid(False)
        ax8.xaxis.set_minor_locator(months8)
        ax8.xaxis.set_major_locator(years8)
        ax8.yaxis.set_minor_locator(minorLocator8)
        ax8.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax8.spines['top'].set_visible(True)
	ax8.spines['right'].set_visible(True)
	ax8.spines['bottom'].set_visible(True)
	ax8.spines['left'].set_visible(True)
        ax8.get_xaxis().tick_bottom()
        ax8.get_yaxis().tick_left()
	ax8.axvline(x=volctimes[2],color='k',ls='dashed')
	ax8.set_ylim(-8.5,2.5)
        plt.yticks([-6,-3,0], [str(x) + "\%" for x in [-6,-3,0]], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in [-6,-3,0]:    
              ax8.plot(dateflat[2][18:], [y] *len(dateflat[2][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax8.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2070[0,0:9])
	years9 = mdates.YearLocator()
	months9 = mdates.MonthLocator()
	minorLocator9 = MultipleLocator(2.5)
	ax9.plot(dateflat[3][18:], datas1[3][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax9.set_xlim(DT.date(2101,1,1), DT.date(2106,7,1))
	ax9.grid(False)
        ax9.xaxis.set_minor_locator(months9)
        ax9.xaxis.set_major_locator(years9)
        ax9.yaxis.set_minor_locator(minorLocator9)
        ax9.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax9.spines['top'].set_visible(True)
	ax9.spines['right'].set_visible(True)
	ax9.spines['bottom'].set_visible(True)
	ax9.spines['left'].set_visible(True)
        ax9.get_xaxis().tick_bottom()
        ax9.get_yaxis().tick_left()
	ax9.axvline(x=volctimes[3],color='k',ls='dashed')
	ax9.set_ylim(-25,6)
        plt.yticks([-20,-10,0], [str(x) + "\%" for x in [-20,-10,0]], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in [-20,-10,0]:    
              ax9.plot(dateflat[3][18:], [y] *len(dateflat[3][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax9.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2100[0,0:9])
	years10 = mdates.YearLocator()
	months10 = mdates.MonthLocator()
	minorLocator10 = MultipleLocator(2.5)
	ax10.plot(dateflat[4][18:], datas1[4][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax10.set_xlim(DT.date(2101,1,1), DT.date(2106,7,1))
	ax10.grid(False)
        ax10.xaxis.set_minor_locator(months9)
        ax10.xaxis.set_major_locator(years9)
        ax10.yaxis.set_minor_locator(minorLocator9)
        ax10.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax10.spines['top'].set_visible(True)
	ax10.spines['right'].set_visible(True)
	ax10.spines['bottom'].set_visible(True)
	ax10.spines['left'].set_visible(True)
        ax10.get_xaxis().tick_bottom()
        ax10.get_yaxis().tick_left()
	ax10.axvline(x=volctimes[4],color='k',ls='dashed')
	ax10.set_ylim(-25,6)
        plt.yticks([-20,-10,0], [str(x) + "\%" for x in [-20,-10,0]], fontsize=10, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="on", labelright = "off")  
 	for y in [-20,-10,0]:    
              ax10.plot(dateflat[4][18:], [y] *len(dateflat[4][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax10.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2017[1:3,9])
	ax11.plot(dataslat[0], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax11.grid(False)
        ax11.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax11.spines['top'].set_visible(True)
	ax11.spines['right'].set_visible(True)
	ax11.spines['bottom'].set_visible(True)
	ax11.spines['left'].set_visible(True)
        ax11.get_xaxis().tick_bottom()
        ax11.get_yaxis().tick_left()
	ax11.set_ylim(-85,85)
	ax11.set_xlim(-10, 2)
	ax11.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-8,0], [str(x) + "\%" for x in [-8,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in range(-8,1,4):    
              ax11.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax11.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2017[0,9])
	ax16.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax16.set_xlim(-1,1)
	ax16.set_ylim(-1,1)
	ax16.annotate(str(totalcol[0])[0:4] + '\%', xy = (-0.7,-0.20), fontsize = 14, fontweight = 'heavy')
	ax16.set_xlabel('30\u00B0N-60\u00B0N - 3 year \n average', fontsize = 10, fontweight = 'heavy', horizontalalignment = 'right')
	ax16.xaxis.set_label_coords(1,1.525)

	plt.subplot(G2050[1:3,9])
	ax12.plot(dataslat[1], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax12.grid(False)
        ax12.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax12.spines['top'].set_visible(True)
	ax12.spines['right'].set_visible(True)
	ax12.spines['bottom'].set_visible(True)
	ax12.spines['left'].set_visible(True)
        ax12.get_xaxis().tick_bottom()
        ax12.get_yaxis().tick_left()
	ax12.set_ylim(-85,85)
	ax12.set_xlim(-10, 2)
	ax12.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-8,0], [str(x) + "\%" for x in [-8,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-8,-4,0]:    
              ax12.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax12.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2050[0,9])
	ax17.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax17.set_xlim(-1,1)
	ax17.set_ylim(-1,1)
	ax17.annotate(str(totalcol[1])[0:4] + '\%', xy = (-0.7,-0.20), fontsize = 14, fontweight = 'heavy')
	ax17.xaxis.set_label_coords(0.45,1.525)
	
	plt.subplot(G2060[1:3,9])
	ax13.plot(dataslat[2], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax13.grid(False)
        ax13.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax13.spines['top'].set_visible(True)
	ax13.spines['right'].set_visible(True)
	ax13.spines['bottom'].set_visible(True)
	ax13.spines['left'].set_visible(True)
        ax13.get_xaxis().tick_bottom()
        ax13.get_yaxis().tick_left()
	ax13.set_ylim(-85,85)
	ax13.set_xlim(-10, 2)
	ax13.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-8,0], [str(x) + "\%" for x in [-8,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-8,-4,0]:    
              ax13.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax13.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2060[0,9])
	ax18.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax18.set_xlim(-1,1)
	ax18.set_ylim(-1,1)
	ax18.annotate(str(totalcol[2])[0:4] + '\%', xy = (-0.7,-0.20), fontsize = 14, fontweight = 'heavy')
	ax18.xaxis.set_label_coords(0.45,1.525)
	
	plt.subplot(G2070[1:3,9])
	ax14.plot(dataslat[3], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax14.grid(False)
        ax14.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax14.spines['top'].set_visible(True)
	ax14.spines['right'].set_visible(True)
	ax14.spines['bottom'].set_visible(True)
	ax14.spines['left'].set_visible(True)
        ax14.get_xaxis().tick_bottom()
        ax14.get_yaxis().tick_left()
	ax14.set_ylim(-85,85)
	ax14.set_xlim(-25, 5)
	ax14.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-20,0], [str(x) + "\%" for x in [-20,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-20,-10,0]:    
              ax14.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax14.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2070[0,9])
	ax19.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax19.set_xlim(-1,1)
	ax19.set_ylim(-1,1)
	ax19.annotate(str(totalcol[3])[0:5] + '\%', xy = (-0.9,-0.20), fontsize = 14, fontweight = 'heavy')
	ax19.xaxis.set_label_coords(0.45,1.525)	

	plt.subplot(G2100[1:3,9])
	ax15.plot(dataslat[4], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax15.grid(False)
        ax15.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax15.spines['top'].set_visible(True)
	ax15.spines['right'].set_visible(True)
	ax15.spines['bottom'].set_visible(True)
	ax15.spines['left'].set_visible(True)
        ax15.get_xaxis().tick_bottom()
        ax15.get_yaxis().tick_left()
	ax15.set_ylim(-85,85)
	ax15.set_xlim(-25, 5)
	ax15.xaxis.set_label_coords(1,-0.2)
        plt.xticks([-20,0], [str(x) + "\%" for x in [-20,0]], fontsize=10,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-20,-10,0]:    
              ax15.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax15.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G2100[0,9])
	ax20.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax20.set_xlim(-1,1)
	ax20.set_ylim(-1,1)
	ax20.annotate(str(totalcol[4])[0:5] + '\%', xy = (-0.9,-0.20), fontsize = 14, fontweight = 'heavy')
	ax20.xaxis.set_label_coords(0.45,1.525)	
	ax1.set_xlabel('7 Tg SO$_2$', fontsize = 12)
	ax2.set_xlabel('7 Tg SO$_2$, 0.03 Tg HCl', fontsize = 12)	
	ax3.set_xlabel('7 Tg SO$_2$, 0.03 Tg HCl, 0.0007 Tg HBr', fontsize = 12)
	ax4.set_xlabel('7 Tg SO$_2$, 3 Tg HCl', fontsize = 12)
	ax5.set_xlabel('7 Tg SO$_2$, 3 Tg HCl, 0.007 Tg HBr', fontsize = 12)

def figureabridged4(var, dayt,idxa=0, idx=1, num=10, flag=0, flagg = 0, cma=  plt.cm.seismic_r):
	global Gs, ax1,ax2,ax3,ax4, ax5, ax6,ax7,ax8,ax9, ax10, ax11, ax12,fig,cbar, plt, levels, datas0,datas1,datas2, volcinjectlats



	datas0 = []
	datas1 = []
	datas2 = []
	datas3 = []
	dateflat = []
	CS = []
	years = [2017]
	volcdays = [531] 
	volctimes = []
	

	
	datas0.append(datamodulator(var, dayt, 4, 0,1, 2017, num, flag))
	datas0.append(datamodulator(var, dayt, 2, 0,1, 2017, num, flag))
	datas0.append(datamodulator(var, dayt, 0, 0,1, 2017, num, flag))
	
	datas1.append(datamodulator(var, dayt, 4, 0,2, 2017, num, flag))
	datas1.append(datamodulator(var, dayt, 2, 0,2, 2017, num, flag))
	datas1.append(datamodulator(var, dayt, 0, 0,2, 2017, num, flag))


	datas2.append(datamodulator(var, dayt, 4, 0,3, 2017, num, flag))
	datas2.append(datamodulator(var, dayt, 2, 0,3, 2017, num, flag))
	datas2.append(datamodulator(var, dayt, 0, 0,3, 2017, num, flag))
	
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	volctimes.append(volclocator(531, 2017))
	



	volclatarctichigh = latitude_edges[18] - 72
	volclatmidlathigh = latitude_edges[15] - 41
	volclattropichigh = latitude_edges[12] - 15.9
	volclatarcticlow = 72 - latitude_edges[16]
	volclatmidlatlow = 41 - latitude_edges[13]
	volclattropiclow = 15.9 - latitude_edges[10]


	latarray = []
	dataslat = []	
	totalcol = []

	
	datas3.append(datas0[0][2].mean(0))
	datas3.append(datas1[0][2].mean(0))
	datas3.append(datas2[0][2].mean(0))
	datas3.append(datas0[1][2].mean(0))
	datas3.append(datas1[1][2].mean(0))
	datas3.append(datas2[1][2].mean(0))
	datas3.append(datas0[2][2].mean(0))
	datas3.append(datas1[2][2].mean(0))
	datas3.append(datas2[2][2].mean(0))

	dateflat.append(datas0[0][0][0])
	dateflat.append(datas0[1][0][0])
	dateflat.append(datas0[2][0][0])
	dateflat.append(datas1[0][0][0])
	dateflat.append(datas1[1][0][0])
	dateflat.append(datas1[2][0][0])
	dateflat.append(datas2[0][0][0])
	dateflat.append(datas2[1][0][0])
	dateflat.append(datas2[2][0][0])

	for x in range(len(datas0)):
		latarray = []
		for y in range(len(datas0[0][0])):
			latarray.append(datas0[x][2][y][20:72].mean())
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))

	for x in range(len(datas1)):
		latarray = []
		for y in range(len(datas1[0][0])):
			latarray.append(datas1[x][2][y][20:72].mean())
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))
	for x in range(len(datas2)):
		latarray = []
		for y in range(len(datas2[0][0])):
			latarray.append(datas2[x][2][y][20:72].mean())
		dataslat.append(latarray)
		totalcol.append(np.mean(latarray))

	lats = datas0[0][1].mean(1)


	levels =  np.array([-35,-30,-25,-20, -15,-10,-8, -6,-4,-2,-1,0])
	
	plt.figure
	Gs = gridspec.GridSpec(3,3, hspace = 0.15, wspace = 0.05)
	G0 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[0,0], hspace =0, wspace = 0)
	G1 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[1,0],hspace = 0, wspace = 0)

	G3 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[0,1], hspace =0, wspace = 0)
	G4 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[1,1],hspace = 0, wspace = 0)

	G6 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[0,2], hspace =0, wspace = 0)
	G7 = gridspec.GridSpecFromSubplotSpec(7,7,subplot_spec=Gs[1,2],hspace = 0, wspace = 0)

	ax1 = plt.subplot(G0[2:,0:6])
	ax2= plt.subplot(G1[2:,0:6])
	
	ax4 = plt.subplot(G3[2:,0:6])
	ax5= plt.subplot(G4[2:,0:6])
	
	ax25 = plt.subplot(G6[2:,0:6])
	ax26= plt.subplot(G7[2:,0:6])

	ax10 = plt.subplot(G0[0:2,0:6])
	ax11 = plt.subplot(G1[0:2,0:6])

	ax7 = plt.subplot(G3[0:2,0:6])
	ax8 = plt.subplot(G4[0:2,0:6])
	
	ax28 = plt.subplot(G6[0:2,0:6])
	ax29 = plt.subplot(G7[0:2,0:6])
	
	ax13 = plt.subplot(G0[2:,6])
	ax14 = plt.subplot(G1[2:,6])

	ax16 = plt.subplot(G3[2:,6])
	ax17 = plt.subplot(G4[2:,6])

	ax31 = plt.subplot(G6[2:,6])
	ax32 = plt.subplot(G7[2:,6])
	
	ax19 = plt.subplot(G0[0:2,6])
	ax20 = plt.subplot(G1[0:2,6])

	ax22 = plt.subplot(G3[0:2,6])
	ax23 = plt.subplot(G4[0:2,6])

	ax34 = plt.subplot(G6[0:2,6])
	ax35 = plt.subplot(G7[0:2,6])
	
	fig = plt.gcf()
	fig.set_facecolor('white')
	
	plt.subplot(G0[2:,0:6])
	CS1 =plt.contourf(datas0[0][0],datas0[0][1],datas0[0][2],levels, cmap = cma)
	
	plt.subplot(G1[2:,0:6])
	CS2 = plt.contourf(datas1[0][0],datas1[0][1],datas1[0][2],levels, cmap = cma)
	

	plt.subplot(G3[2:,0:6])
	CS4 =plt.contourf(datas0[1][0],datas0[1][1],datas0[1][2],levels, cmap = cma)
	
	plt.subplot(G4[2:,0:6])
	CS5 = plt.contourf(datas1[1][0],datas1[1][1],datas1[1][2],levels, cmap = cma)
	
	
	plt.subplot(G6[2:,0:6])
	CS7 =plt.contourf(datas0[2][0],datas0[2][1],datas0[2][2],levels, cmap = cma)
	
	plt.subplot(G7[2:,0:6])
	CS8 =plt.contourf(datas1[2][0],datas1[2][1],datas1[2][2],levels, cmap = cma)
	
	

	label2018location = (DT.date(2018,1,25), -75)
	years2018 = mdates.YearLocator()
	months2018 = mdates.MonthLocator()
	minorLocator2018 = MultipleLocator(2.5)
	stringy = []
	stringy = ['','75$^{\circ}$S','', '45$^{\circ}$S','', '15$^{\circ}$S','', '15$^{\circ}$N','', '45$^{\circ}$N','', '75$^{\circ}$N', '']
	labstring = ['a', 'b', 'c','d','e','f','g','h','i','j','k','l']
	
	plt.subplot(G0[2:,0:6])

	
	ax1.axvline(x=volctimes[0],color='k',ls='dashed')
	ax1.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax1.plot(datas0[0][0][0], [z] *len(datas0[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax1.plot(datas0[2][0][0][0:70], [z] *len(datas0[2][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax1.plot(datas0[0][0][0],[0]*len(datas0[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax1.scatter(volctimes[0], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax1.xaxis.set_major_locator(years2018)
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax1.xaxis.set_minor_locator(months2018)
	ax1.annotate(labstring[0],xy = label2018location, fontsize = 18, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax1.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')
	ax1.set_ylim(-85,85)
	ax1.set_ylabel('Sulfur dioxide only', fontsize = 14, fontweight = 'bold')
	ax1.yaxis.set_label_coords(-0.02, 0.70)

	plt.subplot(G1[2:,0:6])
	
	ax2.axvline(x=volctimes[1],color='k',ls='dashed')
	ax2.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax2.plot(datas1[0][0][0], [z] *len(datas1[0][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax2.plot(datas1[0][0][0][0:70], [z] *len(datas1[0][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax2.plot(datas1[0][0][0],[0]*len(datas1[0][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax2.scatter(volctimes[1], 15.9,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[1],15.9, yerr=np.array([[volclattropiclow,volclattropichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax2.xaxis.set_major_locator(years2018)
	ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax2.xaxis.set_minor_locator(months2018)
	ax2.annotate(labstring[3],xy = label2018location, fontsize = 18, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,73,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	ax2.set_ylabel('Co-injected halogen', fontsize = 14, fontweight = 'bold')
	ax2.set_xlabel('Tropical eruption scenarios', fontsize = 14, fontweight='bold')
	ax2.yaxis.set_label_coords(-0.02, 0.70)
	for tick in ax2.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')	
	ax2.set_ylim(-85,85)


	plt.subplot(G0[0:2,0:6])
	ax10.plot(dateflat[0][18:], datas3[0][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax10.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax10.grid(False)
        ax10.xaxis.set_minor_locator(months2018)
        ax10.xaxis.set_major_locator(years2018)
        ax10.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax10.spines['top'].set_visible(True)
	ax10.spines['right'].set_visible(True)
	ax10.spines['bottom'].set_visible(True)
	ax10.spines['left'].set_visible(True)
        ax10.get_xaxis().tick_bottom()
        ax10.get_yaxis().tick_left()
	ax10.axvline(x=volctimes[0],color='k',ls='dashed')
	ax10.set_ylim(-10,2)
        plt.yticks([-8, -4,0], [str(x) + "\%" for x in [-8,-4, 0]], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-8,-4,0]:    
              ax10.plot(dateflat[0][18:], [y] *len(dateflat[0][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax10.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G1[0:2,0:6])
	ax11.plot(dateflat[1][18:], datas3[1][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax11.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax11.grid(False)
        ax11.xaxis.set_minor_locator(months2018)
        ax11.xaxis.set_major_locator(years2018)
        ax11.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax11.spines['top'].set_visible(True)
	ax11.spines['right'].set_visible(True)
	ax11.spines['bottom'].set_visible(True)
	ax11.spines['left'].set_visible(True)
        ax11.get_xaxis().tick_bottom()
        ax11.get_yaxis().tick_left()
	ax11.axvline(x=volctimes[1],color='k',ls='dashed')
	ax11.set_ylim(-10,2)

        plt.yticks([-8,-4,0], [str(x) + "\%" for x in [-8,-4,0]], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-8,-4,0]:    
              ax11.plot(dateflat[1][18:], [y] *len(dateflat[1][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax11.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')


	plt.subplot(G3[2:,0:6])

	
	ax4.axvline(x=volctimes[3],color='k',ls='dashed')
	ax4.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax4.plot(datas0[1][0][0], [z] *len(datas0[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax4.plot(datas0[1][0][0][0:70], [z] *len(datas0[1][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax4.plot(datas0[1][0][0],[0]*len(datas0[1][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax4.scatter(volctimes[0], 41,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],41, yerr=np.array([[volclatmidlatlow,volclatmidlathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax4.xaxis.set_major_locator(years2018)
	ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax4.xaxis.set_minor_locator(months2018)
	ax4.annotate(labstring[1],xy = label2018location, fontsize = 18, fontweight = 'bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax4.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')
	ax4.set_ylim(-85,85)

	plt.subplot(G4[2:,0:6])
	
	ax5.axvline(x=volctimes[4],color='k',ls='dashed')
	ax5.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax5.plot(datas1[1][0][0], [z] *len(datas1[1][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax5.plot(datas1[1][0][0][0:70], [z] *len(datas1[1][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax5.plot(datas1[1][0][0],[0]*len(datas1[1][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax5.scatter(volctimes[4], 41,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[4],41, yerr=np.array([[volclatmidlatlow,volclatmidlathigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax5.xaxis.set_major_locator(years2018)
	ax5.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax5.xaxis.set_minor_locator(months2018)
	ax5.annotate(labstring[4],xy = label2018location, fontsize = 18, fontweight = 'bold')
	ax5.set_xlabel('Mid-latitude eruption scenarios', fontsize = 14, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax5.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')	
	ax5.set_ylim(-85,85)
	
	plt.subplot(G3[0:2,0:6])
	ax7.plot(dateflat[3][18:], datas3[3][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax7.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax7.grid(False)
        ax7.xaxis.set_minor_locator(months2018)
        ax7.xaxis.set_major_locator(years2018)
        ax7.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax7.spines['top'].set_visible(True)
	ax7.spines['right'].set_visible(True)
	ax7.spines['bottom'].set_visible(True)
	ax7.spines['left'].set_visible(True)
        ax7.get_xaxis().tick_bottom()
        ax7.get_yaxis().tick_left()
	ax7.axvline(x=volctimes[3],color='k',ls='dashed')
	ax7.set_ylim(-10,2)
	plt.yticks([-8, -4,0], [str(x) + "\%" for x in [-8,-4, 0]], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-8,-4,0]:    
              ax7.plot(dateflat[3][18:], [y] *len(dateflat[3][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax7.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G4[0:2,0:6])
	ax8.plot(dateflat[4][18:], datas3[4][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax8.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax8.grid(False)
        ax8.xaxis.set_minor_locator(months2018)
        ax8.xaxis.set_major_locator(years2018)
        ax8.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax8.spines['top'].set_visible(True)
	ax8.spines['right'].set_visible(True)
	ax8.spines['bottom'].set_visible(True)
	ax8.spines['left'].set_visible(True)
        ax8.get_xaxis().tick_bottom()
        ax8.get_yaxis().tick_left()
	ax8.axvline(x=volctimes[4],color='k',ls='dashed')
	ax8.set_ylim(-10,2)
        plt.yticks([-8,-4], [str(x) + "\%" for x in [-8,-4]], fontsize=10, fontweight='bold')
	plt.yticks([-8,-4, 0], ['-8\%', '-4\%', '0\%\  '], fontsize = 10, fontweight = 'bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-8,-4,0]:    
              ax8.plot(dateflat[4][18:], [y] *len(dateflat[4][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax8.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')


	plt.subplot(G6[2:,0:6])

	
	ax25.axvline(x=volctimes[6],color='k',ls='dashed')
	ax25.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax25.plot(datas0[2][0][0], [z] *len(datas0[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax25.plot(datas0[2][0][0][0:70], [z] *len(datas0[2][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax25.plot(datas0[2][0][0],[0]*len(datas0[2][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax25.scatter(volctimes[0], 72,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[0],72, yerr=np.array([[volclatarcticlow,volclatarctichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax25.xaxis.set_major_locator(years2018)
	ax25.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax25.xaxis.set_minor_locator(months2018)
	ax25.annotate(labstring[2],xy = label2018location, fontsize = 18, fontweight = 'bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax25.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')
	ax25.yaxis.set_label_coords(-0.02, 0.70)
	ax25.set_ylim(-85,85)

	plt.subplot(G7[2:,0:6])
	
	ax26.axvline(x=volctimes[4],color='k',ls='dashed')
	ax26.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	plt.tick_params(axis="both", which="both", bottom="on", top="off", labeltop="off", labelbottom="on", left="off", right="off",labelright = "on", labelleft="off")
	for z in [-90,-60,-30,30,60,90]:    
	      ax26.plot(datas1[2][0][0], [z] *len(datas1[2][0][0]), "--", lw=0.5, color="black", alpha=0.3)
	for z in [-75, -45, -15, 15, 45, 75]:    
	      ax26.plot(datas1[2][0][0][0:70], [z] *len(datas1[2][0][0][0:70]), "--", lw=0.5, color="black", alpha=0.3)
	ax26.plot(datas1[2][0][0],[0]*len(datas1[2][0][0]), "--", lw = 2, color = "black", alpha = 0.3)
	ax26.scatter(volctimes[4], 72,  s = 100,color = 'k', marker= '^')
	plt.errorbar(volctimes[4],72, yerr=np.array([[volclatarcticlow,volclatarctichigh]]).T, marker = '^', color = 'k', capsize = 3, linewidth = 2)
	ax26.xaxis.set_major_locator(years2018)
	ax26.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax26.xaxis.set_minor_locator(months2018)
	ax26.annotate(labstring[5],xy = label2018location, fontsize = 18, fontweight = 'bold')
	ax26.set_xlabel('High-latitude eruption scenarios', fontsize = 14, fontweight='bold')
	plt.yticks([-90,-73,-60, -45,-30,-15,0,15,30,45,60,71,90], [stringy[w] for w in range(len(stringy))], fontsize=10, fontweight='bold')
	for tick in ax26.yaxis.get_major_ticks():
		tick.set_pad(-25)
		tick.label2.set_horizontalalignment('left')
	plt.xticks(rotation = 0, fontsize = 12, fontweight = 'bold')	
	ax26.yaxis.set_label_coords(-0.02, 0.70)
	ax26.set_ylim(-85,85)
	

	plt.subplot(G6[0:2,0:6])
	ax28.plot(dateflat[6][18:], datas3[6][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax28.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax28.grid(False)
        ax28.xaxis.set_minor_locator(months2018)
        ax28.xaxis.set_major_locator(years2018)
        ax28.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax28.spines['top'].set_visible(True)
	ax28.spines['right'].set_visible(True)
	ax28.spines['bottom'].set_visible(True)
	ax28.spines['left'].set_visible(True)
        ax28.get_xaxis().tick_bottom()
        ax28.get_yaxis().tick_left()
	ax28.axvline(x=volctimes[3],color='k',ls='dashed')
	ax28.set_ylim(-10,2)
	plt.yticks([-8, -4,0], [str(x) + "\%" for x in [-8,-4, 0]], fontsize=10, fontweight='bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-8,-4,0]:    
              ax28.plot(dateflat[6][18:], [y] *len(dateflat[6][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax28.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')

	plt.subplot(G7[0:2,0:6])
	ax29.plot(dateflat[7][18:], datas3[7][18:], 'k-', lw = 2, label = 'Tropical sulfate')
	ax29.set_xlim(DT.date(2017,11,1), DT.date(2022,7,1))
	ax29.grid(False)
        ax29.xaxis.set_minor_locator(months2018)
        ax29.xaxis.set_major_locator(years2018)
        ax29.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax29.spines['top'].set_visible(True)
	ax29.spines['right'].set_visible(True)
	ax29.spines['bottom'].set_visible(True)
	ax29.spines['left'].set_visible(True)
        ax29.get_xaxis().tick_bottom()
        ax29.get_yaxis().tick_left()
	ax29.axvline(x=volctimes[4],color='k',ls='dashed')
	ax29.set_ylim(-10,2)
        plt.yticks([-8,-4], [str(x) + "\%" for x in [-8,-4]], fontsize=10, fontweight='bold')
	plt.yticks([-8,-4, 0], ['-8\%', '-4\%', '0\%\  '], fontsize = 10, fontweight = 'bold')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="off", left="off", right="off", labelleft="off", labelright = "on")  
 	for y in [-8,-4,0]:    
              ax29.plot(dateflat[7][18:], [y] *len(dateflat[7][18:]), "--", lw=1, color="black", alpha=0.3)
	for tick in ax29.yaxis.get_major_ticks():
		tick.set_pad(-235)
		tick.label2.set_horizontalalignment('center')

	
	plt.subplot(G0[2:,6])
	ax13.plot(dataslat[0], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax13.grid(False)
        ax13.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax13.spines['top'].set_visible(True)
	ax13.spines['right'].set_visible(True)
	ax13.spines['bottom'].set_visible(True)
	ax13.spines['left'].set_visible(True)
        ax13.get_xaxis().tick_bottom()
        ax13.get_yaxis().tick_left()
	ax13.set_ylim(-85,85)
	ax13.set_xlim(-11.5,2.5)
	ax13.xaxis.set_label_coords(1,1.6)
        plt.xticks([-10, 0], [str(x) + "\%" for x in [-10,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-10,-5, 0]:    
              ax13.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax13.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G0[0:2,6])
	ax19.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax19.set_xlim(-1,1)
	ax19.set_ylim(-1,1)
	ax19.annotate(str(totalcol[0])[0:4] + '\%', xy = (0,0),horizontalalignment = 'center', verticalalignment = 'center', fontsize = 14, fontweight = 'heavy')
	ax19.xaxis.set_label_coords(1,1.525)

	plt.subplot(G1[2:,6])
	ax14.plot(dataslat[3], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax14.grid(False)
        ax14.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax14.spines['top'].set_visible(True)
	ax14.spines['right'].set_visible(True)
	ax14.spines['bottom'].set_visible(True)
	ax14.spines['left'].set_visible(True)
        ax14.get_xaxis().tick_bottom()
        ax14.get_yaxis().tick_left()
	ax14.set_ylim(-85,85)
	ax14.set_xlim(-11.5,2.5)
	ax14.xaxis.set_label_coords(1,1.6)
        plt.xticks([-10, 0], [str(x) + "\%" for x in [-10,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-10,-5, 0]:    
              ax14.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax14.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G1[0:2,6])
	ax20.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax20.set_xlim(-1,1)
	ax20.set_ylim(-1,1)
	ax20.annotate(str(totalcol[3])[0:4] + '\%', xy = (0.0,0), horizontalalignment = 'center', verticalalignment = 'center',fontsize = 14, fontweight = 'heavy')
	ax20.xaxis.set_label_coords(1,1.525)




	plt.subplot(G3[2:,6])
	ax16.plot(dataslat[1], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax16.grid(False)
        ax16.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax16.spines['top'].set_visible(True)
	ax16.spines['right'].set_visible(True)
	ax16.spines['bottom'].set_visible(True)
	ax16.spines['left'].set_visible(True)
        ax16.get_xaxis().tick_bottom()
        ax16.get_yaxis().tick_left()
	ax16.set_ylim(-85,85)
	ax16.set_xlim(-11.5,2.5)
	ax16.xaxis.set_label_coords(1,1.6)
        plt.xticks([-10, 0], [str(x) + "\%" for x in [-10,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-10,-5, 0]:    
              ax16.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax16.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G3[0:2,6])
	ax22.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax22.set_xlim(-1,1)
	ax22.set_ylim(-1,1)
	ax22.annotate(str(totalcol[1])[0:4] + '\%', xy = (0,0),horizontalalignment = 'center', verticalalignment = 'center', fontsize = 14, fontweight = 'heavy')
	ax22.xaxis.set_label_coords(1,1.525)


	plt.subplot(G4[2:,6])
	ax17.plot(dataslat[4], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax17.grid(False)
        ax17.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax17.spines['top'].set_visible(True)
	ax17.spines['right'].set_visible(True)
	ax17.spines['bottom'].set_visible(True)
	ax17.spines['left'].set_visible(True)
        ax17.get_xaxis().tick_bottom()
        ax17.get_yaxis().tick_left()
	ax17.set_ylim(-85,85)
	ax17.set_xlim(-11.5,2.5)
	ax17.xaxis.set_label_coords(1,1.6)
        plt.xticks([-10, 0], [str(x) + "\%" for x in [-10,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-10,-5, 0]:    
              ax17.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax17.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G4[0:2,6])
	ax23.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax23.set_xlim(-1,1)
	ax23.set_ylim(-1,1)
	ax23.annotate(str(totalcol[4])[0:4] + '\%', xy = (0,0),horizontalalignment = 'center', verticalalignment = 'center', fontsize = 14, fontweight = 'heavy')
	ax23.xaxis.set_label_coords(1,1.525)




	plt.subplot(G6[2:,6])
	ax31.plot(dataslat[2], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax31.grid(False)
        ax31.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax31.spines['top'].set_visible(True)
	ax31.spines['right'].set_visible(True)
	ax31.spines['bottom'].set_visible(True)
	ax31.spines['left'].set_visible(True)
        ax31.get_xaxis().tick_bottom()
        ax31.get_yaxis().tick_left()
	ax31.set_ylim(-85,85)
	ax31.set_xlim(-11.5,2.5)
	ax31.xaxis.set_label_coords(1,1.6)
        plt.xticks([-10,0], [str(x) + "\%" for x in [-10,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-10,-5, 0]:    
              ax31.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax31.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G6[0:2,6])
	ax34.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax34.set_xlim(-1,1)
	ax34.set_ylim(-1,1)
	ax34.annotate(str(totalcol[2])[0:4] + '\%', xy = (0,0),horizontalalignment = 'center', verticalalignment = 'center', fontsize = 14, fontweight = 'heavy')
	ax34.xaxis.set_label_coords(1,1.525)

	plt.subplot(G7[2:,6])
	ax32.plot(dataslat[5], lats, 'k-', lw = 2, label = 'Tropical sulfate')
	ax32.grid(False)
        ax32.tick_params(axis = 'both', which = 'major', labelsize = 10)
        ax32.spines['top'].set_visible(True)
	ax32.spines['right'].set_visible(True)
	ax32.spines['bottom'].set_visible(True)
	ax32.spines['left'].set_visible(True)
        ax32.get_xaxis().tick_bottom()
        ax32.get_yaxis().tick_left()
	ax32.set_ylim(-85,85)
	ax32.set_xlim(-11.5,2.5)
	ax32.xaxis.set_label_coords(1,1.6)
        plt.xticks([-10, 0], [str(x) + "\%" for x in [-10,0]], fontsize=12,rotation = 15, fontweight='heavy')
        plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off", labelleft="off", labelright = "off")  
 	for y in [-10,-5, 0]:    
              ax32.plot([y]*len(lats), lats, "--", lw=1, color="black", alpha=0.3)
	for tick in ax32.xaxis.get_major_ticks():
		tick.set_pad(3)
		tick.label2.set_horizontalalignment('left')
	
	plt.subplot(G7[0:2,6])
	ax35.grid(False)
	plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left = "off", right = "off", labelleft = "off", labelright = "off")
	ax35.set_xlim(-1,1)
	ax35.set_ylim(-1,1)
	ax35.annotate(str(totalcol[5])[0:4] + '\%', xy = (0,0),horizontalalignment = 'center', verticalalignment = 'center', fontsize = 14, fontweight = 'heavy')
	ax35.xaxis.set_label_coords(1,1.525)

	cbar_ax = fig.add_axes([0.02, 0.95, 0.97, 0.02])
	fmt = '%2.0f'
	tix =  levels
	cbar = fig.colorbar(CS1, cax = cbar_ax, ticks = tix, format =fmt, orientation = 'horizontal')
	cbar_ax.tick_params(labelsize = 12)
	cbar.set_label('Percent change in column ozone', fontsize = 14, fontweight = 'bold', labelpad = -43)

