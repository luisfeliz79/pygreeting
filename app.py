# app.py
# python -m venv flask
# .\flask\Scripts\Activate.ps1
# pip install flask flasgger flask-swagger-ui

# access http://127.0.0.1:5000/apidocs

from flask import Flask, request, jsonify
from flasgger import Swagger
import shared_memory


# https://github.com/flasgger/flasgger

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Greetings API',
    'description': 'An API that greets you and tells you its hostname',
    'uiversion': 3,
    'version': '1.0.0'
}

swagger = Swagger(app)


#######################################################
#  API Functions
########################################################

@app.post("/greeting")
def post_greeting():
    """Sets the greeting phrase
    ---
    consumes:
    - application/json
    parameters:
      - name: body
        in: body    
        schema:
          properties:
            phrase:
              type: string
              description: A phrase that I will greet you with
    responses:
      201:
        description: phrase
    """
    if request.is_json:
        payLoad = request.get_json()
        print ("got this far")
        phraseValue = payLoad["phrase"]
        shared_memory.greeting_phrase =  phraseValue
        answer = [
            {"phrase":phraseValue}           
        ]
        return answer, 201

    return {"error": "Request must be JSON"}, 415

@app.get("/greeting")
def get_greeting():
    """Ask for a greeting
    ---
    responses:
      200:
        description: greeting
    """
    greetingValue = shared_memory.greeting_phrase + " " + shared_memory.hostname + "\n"
    answer = greetingValue
    return answer, 201

if __name__ == '__main__':
   app.run(debug = False) 

# Note, if you use localhost, connections will be much slower
# it has to do with IPV6 being preferred
# this is why, we are using 127.0.0.1, to force IPV4   
   
