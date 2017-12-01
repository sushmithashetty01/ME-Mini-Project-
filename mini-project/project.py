import clean
import timeseries
import maps

#Function to display menu for area, production and yield time series plot
#call the plotAPY() function with user selected crop
def menuAPY():
	attributes=['Rice','Wheat','Gram','Total Pulses','Total Foodgrains']
	while True:
		print "\nArea, Production and Yield\n1.Rice\n2.Wheat\n3.Gram\n4.Total Pulses\n5.Total Foodgrains\nChoose option:",
		try:
			value=int(input())
		except:
			print "Wrong choice!"
			continue
		if 1<=value<=5:
			timeseries.plotAPY(attributes[value-1])
			return
		print "Wrong choice!"

#Function to display menu for comaprison plots for horiculture area and production, and agriculture land utilization
#calls choroplethMapComparison() function to display horiculture comparisons
#calls symbolMapComparison() function to display land utilization comparisons
def menuCompare():
	values=["area","production"]
	while True:
		print "\nComparisons\n1.Horticulture Area Statewise\n2.Horticulture Production Statewise\n3.Land Utilization Statewise\nChoose option:",
		try:
			value=int(input())
		except:
			print "Wrong choice!"
			continue
		if value==1 or value==2:
			maps.choroplethMapComparison("horticulture_"+values[value-1]+"_statewise.csv")
			return
		elif value==3:
			maps.symbolMapComparison("agriculture_land_statewise.csv")
			return
		print "Wrong choice!"


#Function to display main menu of the project
#calls cleanData() to clean the given files into structured files
#depending on user input, respective functions are invoked.
def menu():
	print "\nAnalysis and Visualization of Indian Agriculture Crop Statistics\n"
	print "\nData cleaning..."
	clean.cleanData()
	print "Cleaning Done!"
	print "\nAnalysis and Visualization..."
	while True:
		print "\t1.Area, Production and Yield\n\t2.Land Utilization and Yield\n\t3.Horiculture Area and Production\n\t4.Comparisons\nEnter e/E to exit\nChoose option:",
		value=raw_input()
		try:
			value=int(value)
		except:
			if value.strip().lower()=='e':
				return
		if value==1:
			menuAPY()
		elif value==2:
			maps.symbolMapYield("agriculture_land_statewise.csv")
		elif value==3:
			maps.choroplethMapAreaProd()
		elif value==4:
			menuCompare()
		print "\nAny other visualization?"
		

if __name__=="__main__":
	menu()



