
#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

	
	
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
				

	if req.get("result").get("action") == "yahooWeatherForecast":
		#result 		= req.get("result")
		#parameters 	= result.get("parameters")
		#city 		= parameters.get("geo-city") 
		
		city 		= 'Rome' 
		
		baseurl = "https://query.yahooapis.com/v1/public/yql?"
		yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text= '"+ city+"')"
		yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
		result1 = urlopen(yql_url).read()
    		data = json.loads(result1)
		
		query = data.get('query')
    		result2 = query.get('results')
    		channel = result2.get('channel')
    		item = channel.get('item')
    		date=item["forecast"][0].get("date")
		location = channel.get('location')
    		units = channel.get('units')
    		condition = item.get('condition')
		day	=item["forecast"][0].get("day")
		atm	= channel.get('atmosphere')
		umidita = atm.get('humidity')
		
		celsius=int(condition.get('temp'))
		Gc=int((celsius-32)/1.8)
       		
		speech1 =day+", "+date+"\n\nToday in " + location.get('city') + ": " + condition.get('text') + ".\nThe temperature is " + str(Gc)+ " C with a humidity of "+umidita+"%"
		res = makeWebhookResult(speech1)
		return res
		
	
def makeWebhookResult(speech):
    print("Response:")
    print(speech)
	
    return {
        "speech": speech,
        "displayText": speech,
        # "data":[],
        # "contextOut": [],
        "source": "prueba"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')




