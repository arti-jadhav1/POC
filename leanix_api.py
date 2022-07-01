import json
import requests


api_token = 'xx' #Please contact Arti or Kojo for the token or generate a new one
auth_url = 'https://manulife.leanix.net/services/mtm/v1/oauth2/token'
request_url = 'https://manulife.leanix.net/services/pathfinder/v1/graphql' # same thing as with the auth_url

response = requests.post(auth_url, auth=('apitoken', api_token),
                         data={'grant_type': 'client_credentials'})
response.raise_for_status() 
access_token = response.json()['access_token']
auth_header = 'Bearer ' + access_token
header = {'Authorization': auth_header}

# General function to call GraphQL given a query
def call(query):
  data = {"query" : query}
  json_data = json.dumps(data)
  response = requests.post(url=request_url, headers=header, data=json_data)
  response.raise_for_status()
  return response.json()

# Read all existing Application - IT Component relations
def getFactsheetData():
    query="""{
        allFactSheets (factSheetType: Application) {
        totalCount
        edges {
        node {
            id
            name
            description
            ... on Application {
            externalId {
                externalId
            }
            containsCDI
                relApplicationToUserGroup {
                edges {
                    node {
                    id
                    factSheet {
                    id
                    }
                    description
                    
                    
                    }
                }
                }
            }
        
        }
        }
    }
    }"""

    response = call(query)
    return response

apps = getFactsheetData()

#Checking details of the fetched data
print(type(apps))
print(apps['data']['allFactSheets']['edges'])
print(len(apps['data']['allFactSheets']['edges']))
