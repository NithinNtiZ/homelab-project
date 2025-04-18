
import requests
import json
import boto3
region = 'ap-east-1'
# Create a Boto3 client for IAM
iam = boto3.client('iam', region_name=region)

def get_user(username):
    res = iam.get_user(UserName=username)
    # for User in res['User']:
    print( res['User']['CreateDate'])

def list_users():
    res = iam.list_users()
    # for User in res['User']:
    for user in res['Users']:
        print(user['UserName'])

# Define the JSON data you want to send
json_data = {
    "name" : "nbabu",
    "Instance_ID" : "i-56454894614864",
    "Instance_name" : "supportlab-prod-westsu-ec2-1",
    "Region" : "us-west-1"
}
# Define the URL of the API endpoint
url = "http://localhost:8000/mail-expire"

# Make a POST request with the JSON data in the body
response = requests.post(url, json=json_data)

# Print the response
print(response.json())



# get_user('nbabu')
# list_users()