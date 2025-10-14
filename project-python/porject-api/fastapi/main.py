from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import boto3,sys
app = FastAPI()

# uvicorn main:app --reload

region = 'ap-east-1'
# Create a Boto3 client for IAM
iam = boto3.client('iam', region_name=region)

new_date_str = "01-04-2024"

class Item(BaseModel):
    name : str
    Instance_ID : str 
    Instance_name : str
    Region : str

def send_mail(aws_id, instances_id, new_date_str,instance_name, region):
    ses = boto3.client('ses', region_name="us-west-1")
    data = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instance Lease Expiration Notification</title>
</head>
<body>
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; text-align: center;">
        <h1>Instance Lease Expiration Notification</h1>
        <p>The Instance <span style="background-color: yellow;">{instance_name}</span> (<span style="background-color: yellow;">{instances_id}</span>) you created in {region} will expire on <strong><span style="background-color: yellow;">{new_date_str}</span></strong>.</p>
        <p>If you want to extend the lease duration, please issue a ticket at <a href="https://infoblox.atlassian.net/jira/software/c/projects/SUPLAB/boards/177?atlOrigin=eyJpIjoiN2EwNTVlMjI3NDBlNGNkYmJlNzg3ODVmYjMzZDhkMzAiLCJwIjoiaiJ9">supportlab Jira</a>.</p>
        <p>Ensure that the 'Environment' tag is set to 'Production' for SSOPS production machines.</p>
        <p>For more best practice please refere <a href="https://infoblox.sharepoint.com/:w:/r/sites/CustomerSupport/Shared%20Documents/Support%20Lab/Help%20Docs/Cloud%20Deployment%20Best%20Practice/Best%20Practice%20AWS.docx?d=w5d6ecced23fe49fe9678a9ca9bdbfa3a&csf=1&web=1&e=dr3aN0">Best Practice Guide AWS</a></p>
        <p>Thank you.</p>
        <p>Supprot Lab Admin</p>
        <p>supportlabadmin@infoblox.com</p>
    </div>
</body>
</html>
    """
    to_addr = aws_id+"@infoblox.com"
    try:
        res = ses.send_email(
            Source="supportlabadmin@infoblox.com",
            Destination={
                'ToAddresses': [to_addr]
            },
            Message={
                'Subject': {
                    'Data': "AWS Instance Lease Notification"
                },
                'Body': {
                    'Html': {
                        'Data': data
                    }
                }
            }
        )
    except Exception as err:
        return err
    print(res)
    return res


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/getusers/{username}")
def get_user(username : str):
    res = iam.get_user(UserName=username)
    #  res['User']['CreateDate']
    return res

@app.get("/listuser")
def list_user():
    user_name = []
    res = iam.list_users()
    for user in res['Users']:
         user_name.append(user['UserName'])
    return user_name

@app.post("/mail-expire")
async def json_endpoint(data: Item):
    name = data.name
    instance_id = data.Instance_ID
    instance_name = data.Instance_name
    region = data.Region
    # name = data['name']
    # instance_id = data['Instance_ID']
    # instance_name = data['Instance_name']
    # region = data['Region']
    Message = f"email : {name}, ID : {instance_id}, Name : {instance_name}, Region : {region}"
    res = send_mail(name, instance_id, new_date_str,instance_name, region)
    print (res)
    return Message