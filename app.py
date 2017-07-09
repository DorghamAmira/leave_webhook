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
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    result ={}
    if req.get("result").get("action") != "askForLeave":
        return {}
    
    
    
    afl_query = makeAflQuery(req)
    #if afl_query is None:
     #   return {}
    #conn = mysql.connector.connect(host="localhost", user="root", password="root", database="mydata")
    #cursor = conn.cursor()    
    #try:
    # Execute the SQL command
    #cursor.execute(afl_query)
    # Fetch all the rows in a list of lists.
    #results = cursor.fetchall()
    #for row in results:
     #   name = row[0]
      #  days = row[1]
        
        # Now print fetched result
       # print "name=%s,days=%d" % \
        #      (name, days)
    #except:
     # print "Error: unable to fecth data"
    
        
    
    #result["name"] = results[0][0] 
    #result["days"] = results[0][1]
    print(afl_query)
    
    res = makeWebhookResult(afl_query)
    print(res)
    return res


def makeAflQuery(req):
    data = {}
    data["emlpoyee"]=[]
    employee = {}
    employee["name"]="amira dorgham"
    employee["days"]=14
    data["emlpoyee"].append(employee)
    print(data)
    result = req.get("result")
    parameters = result.get("parameters")
    name = parameters.get("name")
    if name is None:
        return None
    
    for item in data["emlpoyee"]:
        if item["name"]==name:
           res = item 
    return item
   


def makeWebhookResult(data):
    print(data)
    print(json.dumps(data))
    name = data.get("name")
    if name is None:
        return {}

    days = data.get("days")
    if days is None:
        return {}

    speech = "well " + name + " ,you only have " + days + " left, can you provide me with the begin and end date please?"
             

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "amira-leave-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
