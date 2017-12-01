from pandas import DataFrame
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines
from datetime import datetime


#Function to generate DataFrame for agriculture area, production and yield for a specified crop
#input: crop name taken from user input
#output: frame consisting of area, production and yield values of that crop for all years
def generateFrame(attribute):

	areavar=pd.read_csv('cleaned data/agriculture_area_india.csv',usecols=['Year',attribute])
	areavar.columns=['Year','Area']
	yieldvar=pd.read_csv('cleaned data/agriculture_yield_india.csv',usecols=[attribute])
	yieldvar.columns=['Yield']
	prodvar=pd.read_csv('cleaned data/agriculture_production_india.csv',usecols=[attribute])
	prodvar.columns=['Production']
	frame=pd.concat([areavar,prodvar,yieldvar],axis=1)
	return frame

#Function to hide the axes of subplot
#input: subplot reference
def make_patch_spines_invisible(ax):
	ax.set_frame_on(True)
	ax.patch.set_visible(False)
	for sp in ax.spines.values():
		sp.set_visible(False)

#Function to show time series plot of agriculture area, production and yield for a specified crop
#input: crop name taken from user input
#output: double bar chart with area and production against years, line plot of yield against years
def plotAPY(attribute):

	frame=generateFrame(attribute)
	years=frame['Year']
	num=np.arange(len(years))

	fig = plt.figure(figsize=(15,10)) # Create matplotlib figure
	ax1 = fig.add_subplot(111) # Create matplotlib axes
	ax2 = ax1.twinx() # Create another axes that shares the same x-axis as ax.
	ax3 = ax1.twinx()

	width = 0.4

	frame['Area'].plot(kind='bar',color='seagreen',ax=ax1,width=width,position=1,alpha=0.5,label='Area')
	frame['Production'].plot(kind='bar',color='olive',ax=ax2,width=width,position=0,alpha=0.5,label='Production')
	frame['Yield'].plot(kind='line',ax=ax3,color='orange',lw=3.0,label='Yield')

	ax1.set_ylabel('Area (thousand hectares)',color='seagreen',size=16)
	ax1.tick_params(axis='y',colors='seagreen',labelsize=13)
	ax1.set_ylim(0,max(frame['Area'])+min(frame['Area'])/2)

	ax1.set_xlabel('Years',size=13)
	ax1.set_xticklabels(years,rotation=35)

	ax2.set_ylim(0,max(frame['Production'])+min(frame['Production'])/2)
	ax2.set_ylabel('Production (thousand tonnes)',color='olive',size=16)
	ax2.tick_params(axis='y',colors='olive',labelsize=13)

	
	ax3.spines["right"].set_position(("axes",1.08))
	make_patch_spines_invisible(ax3)
	ax3.spines["right"].set_visible(True)
	ax3.spines["right"].set_color("orange")
	ax3.tick_params(axis='y',colors='orange',labelsize=13)
	ax3.set_ylabel('Yield (kg/hectare)',color='orange',size=16)
	ax3.set_ylim(0,max(frame['Yield'])+min(frame['Yield'])/2)
	
	for x,y in zip(num,frame['Yield']):
		ax3.annotate("{0:.3f}".format(y),xy=(x,y),xytext=(x,y+0.05),bbox=dict(boxstyle='round,pad=0.2', fc='orange', alpha=0.5))

	p1= mlines.Line2D([],[],color='seagreen',label='Area',lw=4.0)
	p2= mlines.Line2D([],[],color='olive',label='Production',lw=4.0)
	p3= mlines.Line2D([],[],color='orange',label='Yield',lw=4.0)
	plt.legend(handles=[p1,p2,p3],loc="upper left")

	plt.title("Area, Production and Yield for "+attribute,{'fontsize':22})
	
	plt.xlim(-1,14)
	plt.tight_layout()
	plt.savefig("images/timeseries"+datetime.now().strftime("%d%b-%H:%M:%S")+".png")
	plt.show()
