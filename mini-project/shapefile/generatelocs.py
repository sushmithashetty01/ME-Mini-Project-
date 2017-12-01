import pandas as pd 
import urllib2,json
from pandas import DataFrame


frame=pd.read_csv("st.csv")
location=[]
for st in frame['State/Union Territory']:
	url_response = urllib2.urlopen("http://maps.googleapis.com/maps/api/geocode/json?address="+st.replace(' ','%2F'))
	data=json.loads(url_response.read())
	location.append(data['results'][0]['geometry']['location'])
frame=pd.concat([frame,DataFrame(location)],axis=1)
frame.columns=['State/Union Territory','lat','lng']
frame.to_csv("st.csv",index=False)


