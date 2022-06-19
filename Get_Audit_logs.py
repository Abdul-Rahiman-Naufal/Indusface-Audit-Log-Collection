import requests
import json
from pathlib import Path
import time
from datetime import date, datetime,timedelta

Log_Folder='C:\Indusface'

URL="https://tas.indusface.com/wafportal/rest/siem/v1/getActivity"
API_Key=""


now = datetime.now()

endDate=datetime.now().strftime('%Y-%m-%dT%H:%MZ')
startDate=(datetime.now() - timedelta(hours=0, minutes=5)).strftime('%Y-%m-%dT%H:%MZ')

with open (Log_Folder+"\Indusface.ini", "r") as file:
    API_Key = str(file.read().rstrip())

headers = {'content-type': 'application/json', "Authorization": "Bearer "+str(API_Key)}


with open(Log_Folder+"\websites.txt") as ws:
  websites = ws.read().split('\n')

for website in websites:
    data = { "startDate":startDate,"endDate":endDate,"offSet":0,"maxResult":10000,"websiteName":website}

    response=requests.post(URL, data=json.dumps(data), headers=headers).json()

    try:
        logMessage=""

        if('Successfully got the Action Details for a website.' in response['messages']):
            for row in response['result']['actions']:           
                logMessage=logMessage+str(row)+"\n"
        
        today = str(date.today())
        hour=now.strftime("%H")

        # file = Path(Log_Folder+'\indusface-'+today+'-'+hour+'.log')
        file = Path(Log_Folder+'\indusface-audit-'+today+'.log')
        
        file.touch(exist_ok=True)

        with open(file, "a") as text_file:
            text_file.write(logMessage)
    except Exception as e:    
        file = Path(Log_Folder+'\Error-audit.log')
        file.touch(exist_ok=True)
        with open(file, "a") as text_file:
            current_time = now.strftime("%H:%M:%S")
            text_file.write(current_time+'   '+str(e)+'\n')
            text_file.write(current_time+'   '+str(response['errorMessages'])+'\n')

            