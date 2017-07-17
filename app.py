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
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "askForLeave":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    name = parameters.get("name")
    if name is none :
        
        return ({'speech':"can you provide me with your name please ? "})
    start = parameters.get("start_date")
    if start is none : 
        return ({'speech': name + " , you have only 14 days left , from which date ? "})
    end = parameters.get("end_date")
    
    if end is none :
        return ({'speech':"and for the end date ? "})    
    
    employee = {}
    employee["name"]="amira dorgham"
    employee["days"]=14
    

    
    speech =  " okey " + name + " , "can you please confirm your leave ?"
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
