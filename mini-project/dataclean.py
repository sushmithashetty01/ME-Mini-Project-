import pandas as pd 
import numpy as np
import re
from pandas import DataFrame

#class to clean agriculture data in given excel sheets
class AgricultureData:

	def __init__(self):
		pass

	#Function to clean agriculture land utilization data for all india 
	def generateLandIndia(self):
		frame=pd.read_excel('data/agriculture_land.xlsx',skiprows=8,skipfooter=7,parse_cols='A:D,G,K,N:Q,T')
		labels=['Year','Geographical Area','Reporting area','Forest','Not available for cultivation','Uncultivated land excluding fallow land','Fallow lands','Net area sown','Total cropped area','Area sown more than once','Cropping intensity']
		frame.columns=labels
		frame['Year']=frame['Year'].str.strip().str[:7]
		frame.replace('-',np.nan,inplace=True)
		frame.to_csv('cleaned data/agriculture_land_india.csv',index=False,header=labels)

	#Function to clean agriculture area data for all india 
	def generateAreaIndia(self):
		frame=pd.read_excel('data/agriculture_area.xlsx',skiprows=10,skipfooter=6,parse_cols="A:O")
		labels=['Year','Rice','Wheat','Jowar','Bajra','Maize','Ragi','Small Millets','Barley','Total Cereals','Tur','Gram','Other Pulses','Total Pulses','Total Foodgrains']
		frame.replace('-',np.nan,inplace=True)
		frame.columns=labels
		frame['Year']=frame['Year'].str.strip().str[:7]
		frame.to_csv('cleaned data/agriculture_area_india.csv',index=False,header=labels)

	#Function to clean agriculture production data for all india 
	def generateProductionIndia(self):
		frame=pd.read_excel('data/agriculture_production.xlsx',skiprows=12,skipfooter=12,parse_cols="A:O")
		labels=['Year','Rice','Wheat','Jowar','Bajra','Maize','Ragi','Small Millets','Barley','Total Cereals','Tur','Gram','Other Pulses','Total Pulses','Total Foodgrains']
		frame.columns=labels
		frame['Year']=frame['Year'].str.strip().str[:7]
		frame.replace('-',np.nan,inplace=True)
		frame.to_csv('cleaned data/agriculture_production_india.csv',index=False,header=labels)

	#Function to clean agriculture yield data for all india 
	def generateYieldIndia(self):
		frame=pd.read_excel('data/agriculture_yield.xlsx',skiprows=12,skipfooter=5,parse_cols="A:O")
		labels=['Year','Rice','Wheat','Jowar','Bajra','Maize','Ragi','Small Millets','Barley','Total Cereals','Tur','Gram','Other Pulses','Total Pulses','Total Foodgrains']
		frame.columns=labels
		frame['Year']=frame['Year'].str.strip().str[:7]
		frame.replace('-',np.nan,inplace=True)
		frame.to_csv('cleaned data/agriculture_yield_india.csv',index=False,header=labels)


	#Function to clean agriculture yield data for indian states
	def generateYieldStatewise(self):
		frame1=pd.read_excel('data/agriculture_yield.xlsx',sheetname='Statewise ',skiprows=9,skipfooter=14,parse_cols="A,BO:BS")
		frame2=pd.read_excel('data/agriculture_yield.xlsx',sheetname='Statewise ',skiprows=39,skipfooter=6,parse_cols="A,BO:BS")
		labels=['State/Union Territory','2009-10','2010-11','2011-12','2012-13','2013-14']
		frame1.columns=labels
		frame2.columns=labels
		frame=pd.concat([frame1,frame2])
		frame['State/Union Territory']=frame['State/Union Territory'].str.strip()
		frame.replace('-',np.nan,inplace=True)
		frame.to_csv('cleaned data/agriculture_yield_statewise.csv',index=False)

	#Function to clean agriculture land utilization data for indian states
	def generateLandStatewise(self):
		states=[]
		data=[]
		for i in range(0,25):
			states.append(pd.read_excel('data/agriculture_land.xlsx',sheetname='Statewise',skiprows=9+i*12,skipfooter=421-i*12,parse_cols="A").columns)
		for i in range(0,11):
			states.append(pd.read_excel('data/agriculture_land.xlsx',sheetname='Statewise',skiprows=299+i*12,skipfooter=133-i*12,parse_cols="A").columns)
		for i in range(0,24):
			data.append(pd.read_excel('data/agriculture_land.xlsx',sheetname='Statewise',skiprows=20+i*12,skipfooter=410-i*12,parse_cols="I:J,P:Q").columns)
		data.append(pd.read_excel('data/agriculture_land.xlsx',sheetname='Statewise',skiprows=298,skipfooter=131,parse_cols="I:J,P:Q").columns)
		for i in range(0,11):
			data.append(pd.read_excel('data/agriculture_land.xlsx',sheetname='Statewise',skiprows=310+i*12,skipfooter=120-i*12,parse_cols="I:J,P:Q").columns)
		
		frame=pd.concat([DataFrame(states),DataFrame(data)],axis=1)
		frame.columns=['State/Union Territory','Land under misc. crops & groves','Culturable waste land','Fallow lands','Net area sown']
		frame['State/Union Territory']=frame['State/Union Territory'].map(lambda x:re.sub(r'[*]','',x)).str.title().str.strip()

		frame.set_value(8,'State/Union Territory','Himachal Pradesh')
		frame.set_value(29,'State/Union Territory','A. & N. Islands')
		frame.set_value(31,'State/Union Territory','D. & N. Haveli')
		frame.replace(['Unnamed.*'],[np.nan],regex=True,inplace=True)
		frame.replace('-',np.nan,inplace=True)
		frame.to_csv('cleaned data/agriculture_land_statewise.csv',index=False)


	#Function to clean agriculture land utilization data for indian states excluding Telengana
	def generateLandStatewiseAll(self):
		
		with open('cleaned data/agriculture_land_statewise.csv', 'w') as f:
			DataFrame(columns=['A','B','C','D','E']).to_csv(f)
		for i in range(0,24):
			state=pd.read_excel('data/agriculture_land.xlsx',sheetname='Statewise',skiprows=9+i*12,skipfooter=421-i*12,parse_cols="A").columns
			data=pd.read_excel('data/agriculture_land.xlsx',sheetname='Statewise',skiprows=9+i*12,skipfooter=410-i*12,parse_cols="A,I:J,P:Q")
			totalframe=pd.concat([DataFrame([state.values]*11),DataFrame(data)],axis=1)
			with open('cleaned data/agriculture_land_statewise.csv', 'a') as f:
				totalframe.to_csv(f, header=None,index=None)

		for i in range(0,11):
			state=pd.read_excel('data/agriculture_land.xlsx',sheetname='Statewise',skiprows=299+i*12,skipfooter=133-i*12,parse_cols="A").columns
			data=pd.read_excel('data/agriculture_land.xlsx',sheetname='Statewise',skiprows=299+i*12,skipfooter=120-i*12,parse_cols="A,I:J,P:Q")
			totalframe=pd.concat([DataFrame([state.values]*11),DataFrame(data)],axis=1)
			with open('cleaned data/agriculture_land_statewise.csv', 'a') as f:
				totalframe.to_csv(f, header=None,index=None)

		frame=pd.read_csv("cleaned data/agriculture_land_statewise.csv")
		frame.columns=['State/Union Territory','Year','Land under misc. crops & groves','Culturable waste land','Fallow lands','Net area sown']
		frame['Year']=frame['Year'].str.strip().str[:7]
		frame['State/Union Territory']=frame['State/Union Territory'].map(lambda x:re.sub(r'[*]','',x)).str.title().str.strip()
		for i in range(11):
			frame.set_value(88+i,'State/Union Territory','Himachal Pradesh')
			frame.set_value(308+i,'State/Union Territory','A. & N. Islands')
			frame.set_value(330+i,'State/Union Territory','D. & N. Haveli')
		frame.replace('-',np.nan,inplace=True)
		frame.to_csv('cleaned data/agriculture_land_statewise.csv',index=False)


	#Function to clean agriculture cost estimate data for all india
	def generateCostIndia(self):
		labels=['State']
		labels.extend(pd.read_excel('data/agriculture_cost.xlsx',skiprows=7,skipfooter=66,parse_cols="A,H:M").columns.str.strip().str[:7].values[1:].tolist())
		
		frame=DataFrame()
		for i in range(0,10):
			frame1=pd.read_excel('data/agriculture_cost.xlsx',skiprows=9+i*6,skipfooter=58-i*6,parse_cols="A,H:M")
			frame1.columns=labels
			frame2=DataFrame(pd.read_excel('data/agriculture_cost.xlsx',skiprows=9+i*6,skipfooter=63-i*6,parse_cols="A").columns)
			frame2=pd.concat([frame2]*5,ignore_index=True)
			frame2.columns=['Crop']
			frame1=pd.concat([frame2,frame1],axis=1)
			frame=pd.concat([frame,frame1])
		frame.replace('-',np.nan,inplace=True)
		frame['State']=frame['State'].str.strip()
		frame['Crop']=frame['Crop'].str.strip()
		frame.to_csv('cleaned data/agriculture_cultivation_cost_india.csv',index=False)
		
		frame=DataFrame()
		for i in range(0,10):
			frame1=pd.read_excel('data/agriculture_cost.xlsx',skiprows=9+i*6,skipfooter=58-i*6,parse_cols="A,N:S")
			frame1.columns=labels
			frame2=DataFrame(pd.read_excel('data/agriculture_cost.xlsx',skiprows=9+i*6,skipfooter=63-i*6,parse_cols="A").columns)
			frame2=pd.concat([frame2]*5,ignore_index=True)
			frame2.columns=['Crop']
			frame1=pd.concat([frame2,frame1],axis=1)
			frame=pd.concat([frame,frame1])
		frame.replace('-',np.nan,inplace=True)
		frame['State']=frame['State'].str.strip()
		frame['Crop']=frame['Crop'].str.strip()
		frame.to_csv('cleaned data/agriculture_production_cost_india.csv',index=False)
		


#class to clean horticulture data in given excel sheets
class HorticultureData:

	def __init__(self):
		pass

	#Function to clean horticulture area data for all india
	def generateAreaIndia(self):
		frame=pd.read_excel('data/horticulture.xlsx',skiprows=8,skipfooter=8,parse_cols="A,B,D,F,L,N,R")
		labels=['Year','Fruits','Vegetables','Flowers','Plantation Crops','Spices','Total Area']
		frame.columns=labels
		frame['Year']=frame['Year'].str.strip().str[:7]
		frame.replace('-',np.nan,inplace=True)
		frame.to_csv('cleaned data/horticulture_area_india.csv',index=False)


	#Function to clean horticulture production data for all india
	def generateProductionIndia(self):
		frame=pd.read_excel('data/horticulture.xlsx',skiprows=8,skipfooter=8,parse_cols="A,C,E,G,M,O,P,Q,S")
		labels=['Year','Fruits','Vegetables','Flowers','Plantation Crops','Spices','Mushroom','Honey','Total Production']
		frame.columns=labels
		frame['Year']=frame['Year'].str.strip().str[:7]
		frame.replace('-',np.nan,inplace=True)
		frame.to_csv('cleaned data/horticulture_production_india.csv',index=False)


	#Function to clean horticulture area data for indian states
	def generateAreaStatewise(self):
		frame1=pd.read_excel('data/horticulture.xlsx',sheetname='T 9.2 state-wise',skiprows=10,skipfooter=24,parse_cols="A,CT,CV,CX,CZ,DB,DD")
		frame2=pd.read_excel('data/horticulture.xlsx',sheetname='T 9.2 state-wise',skiprows=40,skipfooter=16,parse_cols="A,CT,CV,CX,CZ,DB,DD")
		labels=pd.read_excel('data/horticulture.xlsx',sheetname='T 9.2 state-wise',skiprows=7,skipfooter=56,parse_cols="A,CT,CV,CX,CZ,DB,DD").columns
		labels.values[-1]=labels.values[-1].split()[0]
		frame1.columns=labels.str.strip()
		frame2.columns=labels.str.strip()
		frame2.set_value(3,'State/Union Territory','Daman & Diu')
		frame=pd.concat([frame1,frame2])
		frame['State/Union Territory']=frame['State/Union Territory'].str.strip()
		frame.replace('-',np.nan,inplace=True)
		frame.to_csv('cleaned data/horticulture_area_statewise.csv',index=False)


	#Function to clean horticulture production data for indian states
	def generateProductionStatewise(self):
		frame1=pd.read_excel('data/horticulture.xlsx',sheetname='T 9.2 state-wise',skiprows=10,skipfooter=24,parse_cols="A,CU,CW,CY,DA,DC,DE")
		frame2=pd.read_excel('data/horticulture.xlsx',sheetname='T 9.2 state-wise',skiprows=40,skipfooter=16,parse_cols="A,CU,CW,CY,DA,DC,DE")
		labels=pd.read_excel('data/horticulture.xlsx',sheetname='T 9.2 state-wise',skiprows=7,skipfooter=56,parse_cols="A,CT,CV,CX,CZ,DB,DD").columns
		labels.values[-1]=labels.values[-1].split()[0]
		frame1.columns=labels.str.strip()
		frame2.columns=labels.str.strip()
		frame2.set_value(3,'State/Union Territory','Daman & Diu')
		frame=pd.concat([frame1,frame2])
		frame['State/Union Territory']=frame['State/Union Territory'].str.strip()
		frame.replace('-',np.nan,inplace=True)
		frame.to_csv('cleaned data/horticulture_production_statewise.csv',index=False)


