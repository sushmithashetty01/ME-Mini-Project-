import dataclean as dc

#Function to call methods of dataclean.py to clean data into excel sheets
#cleans files of agriculture and horticulture data
#output: structured data files generated within 'cleaned data' folder
def cleanData():
	agr=dc.AgricultureData()
	agr.generateAreaIndia()
	agr.generateLandIndia()
	agr.generateProductionIndia()
	agr.generateYieldIndia()
	agr.generateYieldStatewise()
	agr.generateCostIndia()
	agr.generateLandStatewiseAll()

	hor=dc.HorticultureData()
	hor.generateAreaIndia()
	hor.generateProductionIndia()
	hor.generateProductionStatewise()
	hor.generateAreaStatewise()
