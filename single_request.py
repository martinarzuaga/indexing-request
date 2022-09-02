from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
 
url = 'https://www.tero.us/'
 
JSON_KEY_FILE = "credentials.json"
 
SCOPES = [ "https://www.googleapis.com/auth/indexing" ]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
 
 
# Authorize credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
http = credentials.authorize(httplib2.Http())
 
# Build the request body
print(url)
content = {}
content['url'] = url
content['type'] = "URL_UPDATED"
json_content = json.dumps(content)
 
 
response, content = http.request(ENDPOINT, method="POST", body=json_content)
result = json.loads(content.decode())
print(result)