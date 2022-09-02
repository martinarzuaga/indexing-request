from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest
import httplib2
import json
import pandas as pd

urls = open('./urls.txt', 'r')

requests = {}

action = 'URL_UPDATED'

for url in urls:
    new_request = {url.rstrip('\n'): action}
    requests.update(new_request)

JSON_KEY_FILE = "credentials.json"

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

# Authorize credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    JSON_KEY_FILE, scopes=SCOPES)
http = credentials.authorize(httplib2.Http())

# Build service
service = build('indexing', 'v3', credentials=credentials)

results = []

def insert_event(request_id, response, exception):
    if exception is not None:
        print(exception)
    else:
        # print(response)
        results.append(response)


batch = service.new_batch_http_request(callback=insert_event)

for url, api_type in requests.items():
    batch.add(service.urlNotifications().publish(
        body={"url": url, "type": api_type}))
    

batch.execute()

urlsNotifications = {}

index = 0
while index <= len(results):
    res = results[0]['urlNotificationMetadata']['latestUpdate']
    urlsNotifications[index] = res
    index += 1


df = pd.DataFrame.from_dict({(i,j): urlsNotifications[i][j]
                                for i in urlsNotifications.keys()
                                for j in urlsNotifications[i].keys()},
                            orient='index')


df.to_csv('results.csv', index=False)