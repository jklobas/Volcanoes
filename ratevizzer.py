from __future__ import division
import numpy as np
import matplotlib.gridspec as gspec
import matplotlib.pyplot as plt
import outplqparser as opp
from scipy.interpolate import interp1d
def levelinit():
	global level
	level = np.array( [  9.20044434e+02,   7.78800781e+02,   6.59240662e+02,
        	 5.58035156e+02,   4.72366547e+02,   3.99849640e+02,
        	 3.38465424e+02,   2.86504791e+02,   2.42521072e+02,
         	2.05289642e+02,   1.73773941e+02,   1.47096466e+02,
         	1.24514450e+02,   1.05399208e+02,   8.92185135e+01,
         	7.55218353e+01,   6.39278488e+01,   5.41137619e+01,
         	4.58063087e+01,   3.87741966e+01,   3.28216553e+01,
         	2.77829304e+01,   2.35177402e+01,   1.99073410e+01,
         	1.68511982e+01,   1.42642336e+01,   1.20744152e+01,
         	1.02207689e+01,   8.65169525e+00,   7.32350302e+00,
         	6.19920969e+00,   5.24751854e+00,   4.44192934e+00,
         	3.76001072e+00,   3.18278074e+00,   2.69416618e+00,
         	2.28056169e+00,   1.93045413e+00,   1.63409448e+00,
         	1.38323057e+00,   1.17087960e+00,   9.91128385e-01,
         	8.38971794e-01,   7.10174382e-01,   6.01149738e-01,
         	5.08862078e-01,   4.30742532e-01,   3.64615738e-01,
         	3.08640331e-01,   2.61258304e-01,   2.21150517e-01], dtype = float)

def ratemaker(file1,file2):
	levelinit()
	out1 = opp.parser(str(file1))
	out2 = opp.parser(str(file2))
	return out1, out2

def dateextractor(file1, file2, date):
	global o31, o32, prod1, prod2, loss1, loss2, brx1, brx2, clx1, clx2, brxclx1, brxclx2, hox1, hox2, nox1,nox2, ox1, ox2
	o31, prod1, loss1, brx1, brxclx1, clx1, nox1, hox1, ox1 = opp.rxnrates(file1, int(date))
	o32, prod2, loss2, brx2, brxclx2, clx2, nox2, hox2, ox2 = opp.rxnrates(file2, int(date))
	
def latextractor(lat):
	global cclx1, cclx2, nnox1, nnox2, oo31, oo32, oo3num1, oo3num2, bbrx1, bbrx2, bbrxclx1, bbrxclx2, hhox1, hhox2, lloss1, lloss2, pprod1, pprod2, oox1, oox2
	levelinit()
	cclx1 = np.zeros(51,dtype = float)
	cclx2 = np.zeros(51,dtype = float)
	bbrx1 = np.zeros(51,dtype = float)
	bbrx2 = np.zeros(51,dtype = float)
	bbrxclx1 = np.zeros(51,dtype = float)
	bbrxclx2 = np.zeros(51,dtype = float)
	nnox1 = np.zeros(51,dtype = float)
	nnox2 = np.zeros(51,dtype = float)
	hhox1 = np.zeros(51,dtype = float)
	hhox2 = np.zeros(51,dtype = float)
	oox1 = np.zeros(51,dtype = float)
	oox2 = np.zeros(51,dtype = float)
	oo31 = np.zeros(51,dtype = float)
	oo32  = np.zeros(51,dtype = float)
	oo3num1 = np.zeros(51,dtype = float)
	oo3num2 = np.zeros(51, dtype = float)
	pprod1 = np.zeros(51,dtype = float)
	pprod2 = np.zeros(51,dtype = float)
	lloss1 = np.zeros(51,dtype = float)
	lloss2 = np.zeros(51,dtype = float)
	
	for x in range(51):
		cclx1[x] = clx1[x][lat][1]
		cclx2[x] = clx2[x][lat][1]
		nnox1[x] = nox1[x][lat][1]
		nnox2[x] = nox2[x][lat][1]
		oo3num1[x] = o31[x][lat][0]
		oo3num2[x] = o32[x][lat][0]
		oo31[x] = o31[x][lat][1]
		oo32[x] = o32[x][lat][1]
		bbrx1[x] = brx1[x][lat][1]
		bbrx2[x] = brx2[x][lat][1]
		bbrxclx1[x] = brxclx1[x][lat][1]
		bbrxclx2[x] = brxclx2[x][lat][1]
		hhox1[x] = hox1[x][lat][1]
		hhox2[x] = hox2[x][lat][1]
		lloss1[x] = loss1[x][lat][0]
		lloss2[x] = loss2[x][lat][0]
		pprod1[x] = prod1[x][lat][0]
		pprod2[x] = prod2[x][lat][0]
		oox1[x] = ox1[x][lat][1]
		oox2[x] = ox2[x][lat][1]
	interperator()

def interperator():
	global cclx1, cclx2, nnox1, nnox2, oo31, oo32, oo3num1, oo3num2, bbrx1, bbrx2, bbrxclx1, bbrxclx2, hhox1, hhox2, lloss1, lloss2, pprod1, pprod2, oox1, oox2, level
	levelnew = np.linspace(level[0],level[-1], 10000, endpoint = True)
	cclx1 = interp1d(level, cclx1, kind = 5)
	cclx2 = interp1d(level, cclx2, kind = 5)
	nnox1 = interp1d(level, nnox1, kind = 5)
	nnox2 = interp1d(level, nnox2, kind = 5)
	oo3num1 = interp1d(level, oo3num1, kind = 5)
	oo3num2 = interp1d(level, oo3num2, kind = 5)
	oo31 = interp1d(level, oo31, kind = 5)
	oo32 = interp1d(level, oo32, kind = 5)
	bbrx1 = interp1d(level, bbrx1, kind = 5)
	bbrx2 = interp1d(level, bbrx2, kind = 5)
	bbrxclx1 = interp1d(level, bbrxclx1, kind = 5)
	bbrxclx2 = interp1d(level, bbrxclx2, kind = 5)
	hhox1 = interp1d(level, hhox1, kind = 5)
	hhox2 = interp1d(level, hhox2, kind = 5)
	lloss1 = interp1d(level, lloss1, kind = 5)
	lloss2 = interp1d(level, lloss2, kind = 5)
	pprod1 = interp1d(level, pprod1, kind = 5)
	pprod2 = interp1d(level, pprod2, kind = 5)
	oox1 = interp1d(level, oox1, kind = 5)
	oox2 = interp1d(level, oox2, kind = 5)
		
	cclx1 = cclx1(levelnew)
	cclx2 = cclx2(levelnew)
	bbrx1 = bbrx1(levelnew)
	bbrx2 = bbrx2(levelnew)
	nnox1 = nnox1(levelnew)
	nnox2 = nnox2(levelnew)
	hhox1 = hhox1(levelnew)
	hhox2 = hhox2(levelnew)
	oox1 = oox1(levelnew)
	oox2 = oox2(levelnew)
	oo31 = oo31(levelnew)
	oo32 = oo32(levelnew)
	oo3num1 = oo3num1(levelnew)
	oo3num2 = oo3num2(levelnew)
	bbrxclx1 = bbrxclx1(levelnew)
	bbrxclx2 = bbrxclx2(levelnew)
	lloss1 = lloss1(levelnew)
	lloss2 = lloss2(levelnew)
	pprod1 = pprod1(levelnew)
	pprod2 = pprod2(levelnew)
	level = levelnew
	adderator()
		
def plotinit():
	global fig, ax1, ax2, gs
	#define plot
	plt.ion()
	gs = gspec.GridSpec(1,2, wspace = 0.1)
	ax1 = plt.subplot(gs[0,0])
	ax2 = plt.subplot(gs[0,1])
	fig = plt.gcf()
	fig.set_facecolor('white')
	fig.subplots_adjust(bottom = 0.04, left = 0.055, right = 0.98, top = 0.98)
	fig.set_size_inches(6,10.66)

	ax1.set_ylim(1000,1)
	ax1.set_yscale('log')
	ax1.set_xlim(0,1)
	ax1.grid(which = 'both')
	ax2.set_ylim(1000,1)
	ax2.set_yscale('log')
	ax2.set_xlim(0,1)
	ax2.grid(which = 'both')
	ax1.set_xlabel('fractional role of chemical family in ozone loss rate', fontsize = 20)
	ax1.set_ylabel('pressure (hPa)', fontsize = 20)
	ax1.xaxis.set_label_coords(1.05, -0.018)
	ax2.yaxis.set_tick_params(labelleft= "off")

def plotnoratinit():
	global fig, ax1, ax2, gs
	#define plot
	plt.ion()
	gs = gspec.GridSpec(1,2, wspace = 0.1)
	ax1 = plt.subplot(gs[0,0])
	ax2 = plt.subplot(gs[0,1])
	fig = plt.gcf()
	fig.set_facecolor('white')
	fig.subplots_adjust(bottom = 0.04, left = 0.055, right = 0.98, top = 0.98)
	fig.set_size_inches(6,10.66)

	ax1.set_ylim(1000,1)
	ax1.set_yscale('log')
	ax1.grid(which = 'both')
	ax2.set_ylim(1000,1)
	ax2.set_yscale('log')
	ax2.grid(which = 'both')
	ax1.set_ylabel('pressure (hPa)', fontsize = 20)
	ax1.xaxis.set_label_coords(1.05, -0.018)
	ax2.yaxis.set_tick_params(labelleft= "off")

def plotfill(ax, var1, var2, facec, edgec, sign =1):
	global fig, ax1, ax2, gs
	if sign == 1:
		ax.fill_betweenx(level, np.divide(var1, lloss1), np.divide(var2,lloss2), where = np.divide( var1, lloss1) > np.divide(var2,lloss2), facecolor = facec, edgecolor = edgec, alpha = 0.4)
	if sign == -1:
		ax.fill_betweenx(level, np.divide(var1, lloss1), np.divide(var2,lloss2), where = np.divide(var1, lloss1) < np.divide(var2,lloss2), facecolor = facec, edgecolor = edgec, alpha = 0.4)

def plotpercentfill(ax, var1, var2, facec, edgec, sign =1):
	global fig, ax1, ax2, gs 
	if sign == 1:
		ax.fill_betweenx(level, np.divide(var1, np.sum(lloss1)), np.divide(var2,np.sum(lloss2)), where = np.divide( var1, np.sum(lloss1)) > np.divide(var2,np.sum(lloss2)), facecolor = facec, edgecolor = edgec, alpha = 0.4)
	if sign == -1:
		ax.fill_betweenx(level, np.divide(var1, np.sum(lloss1)), np.divide(var2,np.sum(lloss2)), where = np.divide(var1,np.sum(lloss1)) < np.divide(var2,np.sum(lloss2)), facecolor = facec, edgecolor = edgec, alpha = 0.4)

def plotlinedraw(ax, var1, var2, sign =1, levelhigh = 1000, levellow = 1):
	global fig, ax1, ax2, gs
	if sign == 1:
		ax.plot( np.divide(var1[(np.divide(var1,lloss1) > np.divide(var2,lloss2)) & (level > levellow) & (level < levelhigh)],lloss1[(np.divide(var1,lloss1) > np.divide(var2,lloss2)) & (level >levellow) & ( level < levelhigh)]), level[(np.divide(var1,lloss1) > np.divide(var2, lloss2)) & (level > levellow) & (level < levelhigh)], linestyle = 'dashed', linewidth = 2, color = 'k')
	if sign == -1:
		ax.plot( np.divide(var1[(np.divide(var1,lloss1) < np.divide(var2,lloss2)) & (level > levellow) & (level < levelhigh)],lloss1[(np.divide(var1,lloss1) < np.divide(var2,lloss2)) & (level >levellow) & ( level < levelhigh)]), level[(np.divide(var1,lloss1) < np.divide(var2, lloss2)) & (level > levellow) & (level < levelhigh)], linestyle = 'dashed', linewidth = 2, color = 'k')


def plotpercentlinedraw(ax, var1, var2, sign =1, levelhigh = 1000, levellow = 1):
	global fig, ax1, ax2, gs
	if sign == 1:
		ax.plot( np.divide(var1[(np.divide(var1,np.sum(lloss1)) > np.divide(var2,np.sum(lloss2))) & (level > levellow) & (level < levelhigh)],np.sum(lloss1)), level[(np.divide(var1,np.sum(lloss1)) > np.divide(var2, np.sum(lloss2))) & (level > levellow) & (level < levelhigh)], linestyle = 'dashed', linewidth = 2, color = 'k')
	if sign == -1:
		ax.plot( np.divide(var1[(np.divide(var1,np.sum(lloss1)) < np.divide(var2,np.sum(lloss2))) & (level > levellow) & (level < levelhigh)],np.sum(lloss1)), level[(np.divide(var1,np.sum(lloss1)) < np.divide(var2, np.sum(lloss2))) & (level > levellow) & (level < levelhigh)], linestyle = 'dashed', linewidth = 2, color = 'k')


def plotnoratfill(ax, var1, var2, facec, edgec, sign =1):
	global fig, ax1, ax2, gs
	if sign == 1:
		ax.fill_betweenx(level, var1, var2, where = var1 > var2, facecolor = facec, edgecolor = edgec, alpha = 0.4)
	if sign == -1:
		ax.fill_betweenx(level, var1, var2, where = var1 < var2, facecolor = facec, edgecolor = edgec, alpha = 0.4)


def plotratlinedraw(ax, var1, var2, clr,  sign =1, levelhigh = 1000, levellow = 1):
	global fig, ax1, ax2, gs
	if sign == 1:
		ax.plot(var1[(var1 > var2) & (level > levellow) & (level < levelhigh)], level[(var1 > var2) & (level > levellow) & (level < levelhigh)], linestyle = 'dashed', linewidth = 2, color = clr)
	if sign == -1:
		ax.plot( var1[(var1 < var2) & (level > levellow) & (level < levelhigh)], level[(var1< var2) & (level > levellow) & (level < levelhigh)], linestyle = 'dashed', linewidth = 2, color = clr)

def adderator():
	global halo1, halo2, bromo1, bromo2
	halo1 = np.add(np.add(cclx1,bbrx1),bbrxclx1)
	halo2 = np.add(np.add(cclx2, bbrx2), bbrxclx2)
	bromo1 = np.add(bbrx1,bbrxclx1)
        bromo2 = np.add(bbrx2, bbrxclx2)
