import os
import google.cloud.dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
import requests
import json
from flask import Flask, request,jsonify

#dialogflow 인증
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] ='private_key.json'
#private key=서비스 계정 발급키
#https://cloud.google.com/iam/docs/creating-managing-service-account-keys?hl=ko 참고
DIALOGFLOW_PROJECT_ID ='tastyfood-ohel'
DIALOGFLOW_LANGUAGE_CODE ='ko'

SESSION_ID ='me'
session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID,SESSION_ID)

#dialogflow에서 텍스트 반환
def get_answer(test_query):
    our_input =dialogflow.types.TextInput(text=test_query, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query = dialogflow.types.QueryInput(text=our_input)
    response = session_client.detect_intent(session=session,query_input=query)
    return response.query_result.fulfillment_text;

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/test', methods=['POST'])
def test():
    #카카오 json 규격
    req = request.get_json()
    input_text=req['userRequest']['utterance']
    res={
        "version":"2.0",
           "template":{
               "outputs":[
                   {
                       "simpleText":{
                           "text":get_answer(input_text)
                    }
                }
            ]
           }
       }
    return jsonify(res)

#메인 함수
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)