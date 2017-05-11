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

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

 

def makeWebhookResult(req):
    
    #if req.get("result").get("action") != "forecastdata":
       # return {}
    result = req.get("result")
    parameters = result.get("parameters")
    date=parameters.get("date")
    lob=parameters.get("LOBType")
    data={"forecast":[{"LOB": "Cloud Dedicated", "STLF": 26.0, "AREA": "Western Europe", "year": 2016.0, "Arima": 27.0, "mon": "April", "V": 10.0, "Forecast_Indicator": "Actual"}, 
                    {"LOB": "Cloud Dedicated", "STLF": 28.0, "AREA": "Western Europe", "year": 2016.0, "Arima": 29.0, "mon": "May", "V": 11.0, "Forecast_Indicator": "Actual"}, 
                    {"LOB": "Cloud Dedicated", "STLF": 30.0, "AREA": "Western Europe", "year": 2016.0, "Arima": 31.0, "mon": "June", "V": 12.0, "Forecast_Indicator": "Actual"}, 
                    {"LOB": "Cloud Dedicated", "STLF": 32.0, "AREA": "Western Europe", "year": 2016.0, "Arima": 33.0, "mon": "July", "V": 13.0, "Forecast_Indicator": "Actual"}, 
                    {"LOB": "Cloud Dedicated", "STLF": 34.0, "AREA": "Western Europe", "year": 2016.0, "Arima": 35.0, "mon": "August", "V": 14.0, "Forecast_Indicator": "Actual"}, 
                    {"LOB": "Cloud Dedicated", "STLF": 36.0, "AREA": "Western Europe", "year": 2016.0, "Arima": 37.0, "mon": "September", "V": 15.0, "Forecast_Indicator": "Actual"}]}
    res=1000.0
    for num in data["forecast"]:
        if str.lower(num["LOB"])==str.lower(lob) and str.lower(num["mon"])==str.lower(date):
            res=num["Arima"]
    # print(json.dumps(item, indent=4))
    
    if req.get("result").get("action") == "forecastdata":
            speech = "The forecast of " + parameters.get("LOBType") + " for the month " + parameters.get("date") +" is "+ str(res)
                     
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "api_ai_forecast"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
