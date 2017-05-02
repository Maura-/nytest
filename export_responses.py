import requests
import zipfile
try: import simplejson as json
except ImportError: import json

#Setting user Parameters
apiToken = "YOUR_API_TOKEN"
surveyId = "YOUR_SURVEY_ID"
fileFormat = "csv"
dataCenter = 'ca1'

#optional
#lastname = "R_3KZSvhK8MZHRCsk" 

#Setting static parameters
requestCheckProgress = 0
baseUrl = "https://{0}.qualtrics.com/API/v3/responseexports/".format(dataCenter)
headers = {
    "content-type": "application/json",
    "x-api-token": apiToken,

    }

#Creating Data Export
downloadRequestUrl = baseUrl
downloadRequestPayload = '{"format":"' + fileFormat + '","surveyId":"' + surveyId + '"}'
downloadRequestResponse = requests.request("POST", downloadRequestUrl, data=downloadRequestPayload, headers=headers)
progressId = downloadRequestResponse.json()["result"]["id"]
print downloadRequestResponse.text


#Checking on Data Export Progress and waiting until export is ready
while requestCheckProgress < 100:
  requestCheckUrl = baseUrl + progressId
  requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
  requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
  print "Download is " + str(requestCheckProgress) + " complete"


#Downloading and unzipping file
requestDownloadUrl = baseUrl + progressId + '/file'
requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)
with open("RequestFile.zip", "w") as f:
    for chunk in requestDownload.iter_content(chunk_size=1024):
      f.write(chunk)
zipfile.ZipFile("RequestFile.zip").extractall("MyQualtricsDownload")
