from pandas import DataFrame,Series
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.lines as mlines
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
import math, warnings
from datetime import datetime

warnings.filterwarnings("ignore")

#commands to set basemap settings
#sudo apt-get install libgeos-3.5.0
#sudo apt-get install libgeos-dev
#sudo pip install https://github.com/matplotlib/basemap/archive/master.zip

#Function to convert names according to data in structured files
#input: string with state name as per in shapefile
#output: string with state name as per in excel sheet
def convertStateName(st):
	if 'Jammu' in st:
		st='Jammu & Kashmir'
	elif 'Orissa' in st:
		st='Odisha'
	elif 'Delhi' in st:
		st="Delhi"
	elif "ANDAMAN" in st:
		st='A. & N. Islands'
	elif "DADRA" in st:
		st='D. & N. Haveli'
	elif "DAMAN" in st:
		st='Daman & Diu'
	elif "Pondicherry" in st:
		st='Puducherry'
	elif "LAKSHADWEEP" in st:
		st="Lakshadweep"
	elif "CHANDIGARH" in st:
		st="Chandigarh"
	return st


labels=None
colors = ['red','blue','green','yellow']
num_colors=8
cm = plt.get_cmap('YlOrBr')
scheme = [cm(i*270/num_colors) for i in range(1,num_colors+1)]


#Function to generate the dataframe with the data of each state for particular year
#input: structured file with data, particular year
#output: dataframe with the respective data
def getChoroplethFrame(file,year):
	frame=pd.read_csv(file,usecols=["State/Union Territory",year])
	frame.columns=["States",year]
	#frame['States']=frame['States'].str.rstrip()
	frame.set_index('States',inplace=True)
	frame=frame.dropna()
	return frame

#Function to generate the central locations of each Indian state
#also generates land utilization data for given file and year
#input: structured file with data, particular year
#output: location and land utilization dataframes
def getSymbolFrame(file,year):
	loc=pd.read_csv("shapefile/locations.csv")
	loc.columns=["States","lat","lng"]
	loc.set_index('States',inplace=True)
	loc=loc.dropna()

	landvar=pd.read_csv(file)
	landvar=landvar[landvar['Year']==year]
	global labels
	labels=landvar.columns.tolist()[1:]
	landvar.columns=["States","Year","A","B","C","D"]
	landvar.set_index('States',inplace=True)
	landvar=landvar.dropna()

	return loc,landvar


#Function to display the Indian geographical map using the shapefile provided
#input: frame and subplot reference
def generateBasemapChoropleth(frame,ax):
	# create the map
	map = Basemap(resolution = 'l',llcrnrlon=67,llcrnrlat=7,urcrnrlon=98, urcrnrlat=38)
	# load the shapefile, use the name 'states'
	map.readshapefile('shapefile/INDIA', name='states',color='#444444')

	for state, shape in zip(map.states_info, map.states):
		st = convertStateName(state['ST_NAME'])
		if st not in frame.index:
			color = '#DDDDDD'
		else:
			color = scheme[frame.ix[st]['bin'].astype('int')]

		patches = [Polygon(np.array(shape), True)]
		pc = PatchCollection(patches)
		pc.set_facecolor(color)
		ax.add_collection(pc)

	map.drawmeridians([67, 78.9629, 98], labels=[1,0,0,1])
	map.drawparallels([7,20.5937,38],labels=[1,0,0,1])


#Function to display two choropleth maps on the Indian geographical map 
#for a two randomly selected years using given file data
#input: structured file containing the required data
def choroplethMapComparison(file):
	years=["2009-10","2010-11","2011-12","2012-13","2013-14","2014-15"]
	yindex=np.random.randint(0,len(years))
	
	year1=years[yindex]
	year2=years[(yindex+3)%len(years)]
	frame1=getChoroplethFrame("cleaned data/"+file,year1)
	frame2=getChoroplethFrame("cleaned data/"+file,year2)
	values = [frame1[year1].max(),frame2[year2].max()]
	bins = np.linspace(0, max(values), num_colors)
	

	fig = plt.figure(figsize=(22, 12))
	texts=file.split('_')
	fig.suptitle("Statewise "+texts[0].title()+" "+texts[1].title()+" Comparison", fontsize=20, y=.95)
	
	frame1['bin'] = np.digitize(frame1[year1], bins) - 1
	frame1.sort_values('bin', ascending=False).head(10)
	ax1 = fig.add_subplot(121, axisbg='w', frame_on=False)
	generateBasemapChoropleth(frame1,ax1)
	ax1.set_title("Statewise "+texts[0].title()+" "+texts[1].title()+" in Year "+year1, fontsize=15)

	frame2['bin'] = np.digitize(frame2[year2], bins) - 1
	frame2.sort_values('bin', ascending=False).head(10)
	ax2 = fig.add_subplot(122, axisbg='w', frame_on=False)
	generateBasemapChoropleth(frame2,ax2)
	ax2.set_title("Statewise "+texts[0].title()+" "+texts[1].title()+" in Year "+year2, fontsize=15)


	# Draw color legend.
	ax_legend = fig.add_axes([0.3, 0.10, 0.4, 0.02], zorder=3)
	cmap = mpl.colors.ListedColormap(scheme)
	cb = mpl.colorbar.ColorbarBase(ax_legend, cmap=cmap, ticks=bins, boundaries=bins, orientation='horizontal')
	cb.ax.set_xticklabels([str(round(i, 1)) for i in bins])

	# get current axes instance
	ax = plt.gca()
	plt.savefig("images/choroplethmap"+datetime.now().strftime("%d%b-%H:%M:%S")+".png")
	plt.show()


#Function to generate symbol map on the Indian geographical map
#input: subplot reference, file containing data, particular year
#pie charts are placed on each Indian state
def generateBasemapSymbol(ax,file,year):

	loc,landvar=getSymbolFrame("cleaned data/"+file,year)
	map = Basemap(resolution='i',projection='merc',llcrnrlon=67,llcrnrlat=7,urcrnrlon=98, urcrnrlat=38)
	map.readshapefile('shapefile/INDIA', name='states',color='#444444')

	for state in map.states_info:
		st = convertStateName(state['ST_NAME'])
		if st in landvar.index:
			a,b,c,d=float(landvar.ix[st]['A']),float(landvar.ix[st]['B']),float(landvar.ix[st]['C']),float(landvar.ix[st]['D'])
			size=a+b+c+d
			r1 = a/size
			r2 = b/size
			r3 = c/size
			r4 = d/size
			X,Y=map((loc.ix[st]['lng']),(loc.ix[st]['lat']))
			draw_pie(ax,[r1, r2, r3, r4], X, Y,size/8)
	ax.set_title('Land Utilization for year '+year+" ('1000 Hectares)", fontsize=15)
	p=[]
	for i in range(len(colors)):
		p.append(mlines.Line2D([],[],color=colors[i],label=labels[i+1],marker="s",markersize=7.0))
	ax.legend(handles=p,loc="upper right")


#Function to draw pie chart on each Indian state on the map
#input: subplot reference, ratios to be plotted, locations X,Y on the Indian geographical map, size of the pie chart
def draw_pie(ax,ratios,X,Y,size):
	xy = []
	start = 0.
	for ratio in ratios:
		x = [0] + np.cos(np.linspace(2*math.pi*start,2*math.pi*(start+ratio), 30)).tolist()
		y = [0] + np.sin(np.linspace(2*math.pi*start,2*math.pi*(start+ratio), 30)).tolist()
		xy.append(zip(x,y))
		start += ratio

	for i, xyi in enumerate(xy):
		ax.scatter([X],[Y] , marker=(xyi,0), s=size, facecolor=colors[i])


#Function to display two symbol maps on the Indian geographical map 
#for a two randomly selected years using given file data
#input: structured file containing the required data
def symbolMapComparison(file):

	years=["2003-04","2004-05","2005-06","2007-08","2008-09","2009-10","2010-11","2011-12","2012-13","2013-14"]
	yindex=np.random.randint(0,len(years))
	year1=years[yindex]
	year2=years[(yindex+5)%len(years)]

	fig=plt.figure(figsize=(22,12))
	fig.suptitle('Land Utilization Comparison', fontsize=20, y=.95)	
	
	ax1=plt.subplot(121)
	generateBasemapSymbol(ax1,file,year1)
	
	ax2=plt.subplot(122)
	generateBasemapSymbol(ax2,file,year2)

	plt.savefig("images/symbolmap"+datetime.now().strftime("%d%b-%H:%M:%S")+".png")
	plt.show()


#Function to display bar chart of yield of top 10 land utilising states
#input: the subplot reference, structured file name containing land utilization data, particular year
def plotYieldBar(ax,file,year):

	loc,landvar=getSymbolFrame(file,year)
	landvar['Ratio']=landvar['D']/(landvar['A']+landvar['B']+landvar['C']+landvar['D'])
	topstates=landvar.sort_values(["Ratio"],ascending=[0]).head(10).index

	yieldvar=pd.read_csv("cleaned data/agriculture_yield_statewise.csv",usecols=['State/Union Territory',year])
	yieldvar=yieldvar.dropna()
	yieldvar=yieldvar[yieldvar['State/Union Territory'].isin(topstates)]
	yieldvar[year].plot(kind='bar',color='orange',ax=ax,width=0.6,alpha=0.7,label='Yield')
	ax.set_ylabel('Yield (kg/hectare)',color='orange',size=15)
	ax.tick_params(axis='y',colors='orange',labelsize=13)
	ax.set_ylim(0,max(yieldvar[year])+min(yieldvar[year])/2)
	ax.set_xticklabels(topstates,rotation=30)
	ax.set_title('Yield of Top 10 Land Utilizing States',fontsize=15)


#Function to display symbol map of the agriculture land utilization data for a randomly selected year
#it is shown on the Indian geographical map
#also displays bar chart of the yield of top 10 land utilizing states 
#input: structured file name of land utilising data
def symbolMapYield(file):

	years=["2009-10","2010-11","2011-12","2012-13","2013-14"]
	yindex=np.random.randint(len(years))

	fig=plt.figure(figsize=(22,12))
	fig.suptitle('Land Utilization and Yield Statewise', fontsize=20, y=.95)

	ax1=plt.subplot(121)
	generateBasemapSymbol(ax1,file,years[yindex])
	
	ax2=plt.subplot(122)
	plotYieldBar(ax2,"cleaned data/"+file,years[yindex])

	plt.subplots_adjust(left=None,bottom=0.15,right=None,top=0.8,wspace=None,hspace=None)

	plt.savefig("images/symbolmap"+datetime.now().strftime("%d%b-%H:%M:%S")+".png")
	plt.show()
	

#Function to display two choropleth maps
#one for algriculture area and other for production data for a randomly selected year
def choroplethMapAreaProd():
	years=["2009-10","2010-11","2011-12","2012-13","2013-14","2014-15"]
	yindex=np.random.randint(0,len(years))
	
	year=years[yindex]
	frame1=getChoroplethFrame("cleaned data/horticulture_area_statewise.csv",year)
	values = frame1[year]
	bins = np.linspace(0, max(values), num_colors)
	

	fig = plt.figure(figsize=(22, 12))
	fig.suptitle("Horticulture Area and Production Statewise", fontsize=20, y=.95)
	
	frame1['bin'] = np.digitize(frame1[year], bins) - 1
	frame1.sort_values('bin', ascending=False).head(10)
	ax1 = fig.add_subplot(122, axisbg='w', frame_on=False)
	generateBasemapChoropleth(frame1,ax1)
	ax1.set_title("Area in Year "+year+" ('1000 Hectares)", fontsize=15)

	prodvar=pd.read_csv("cleaned data/horticulture_production_statewise.csv",usecols=['State/Union Territory',year])
	prodvar=prodvar.dropna()
	topstates=prodvar.sort_values([year],ascending=[0]).head(6).values.tolist()
	otherstates=sum(prodvar.sort_values([year],ascending=[0]).tail(30)[year])
	topstates.append(['Others',otherstates])
	topstates=DataFrame(topstates)
	topstates.columns=['States',year]
	ax2 = fig.add_subplot(121, axisbg='w', frame_on=False)

	colors = ['#F8A757','#FF9966','#FF6633','#FF6600','#FF3300','#CC3300','#D98E4D']
	topstates[year].plot(kind='pie',ax=ax2,colors=colors,autopct='%1.2f%%',startangle=120,explode=None,labels=topstates['States'],radius=0.75)
	ax2.set_title("Production in Year "+year+" ('1000 Tonnes)", fontsize=15)
	ax2.set_ylabel('')
	# Draw color legend.
	ax_legend = fig.add_axes([0.58, 0.10, 0.3, 0.02], zorder=3)
	cmap = mpl.colors.ListedColormap(scheme)
	cb = mpl.colorbar.ColorbarBase(ax_legend, cmap=cmap, ticks=bins, boundaries=bins, orientation='horizontal')
	cb.ax.set_xticklabels([str(round(i, 1)) for i in bins])

	plt.subplots_adjust(left=None,bottom=0.15,right=None,top=0.75,wspace=0.3,hspace=None)
	# get current axes instance
	ax = plt.gca()
	plt.savefig("images/choroplethmap"+datetime.now().strftime("%d%b-%H:%M:%S")+".png")
	plt.show()
