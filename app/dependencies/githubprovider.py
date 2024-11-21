import requests
from ..utils.config import Settings
from ..utils.models import GitToken, GitUser
from fastapi import HTTPException, status

settings = Settings()

#********* fetching access token for user's github profile information

def get_gitToken(code:str):
    client_id = settings.CLIENT_ID
    client_secret = settings.CLIENT_SECRET
    token_queries = {"client_id":client_id, "client_secret":client_secret, "code":code}
    token_url = f"https://github.com/login/oauth/access_token"
    header={"Content-Type":"application/json"}
    response = requests.post(token_url, params=token_queries, headers=header)

    if response.status_code == 200:
        token = response.text.split("=")[1].split("&")[0]
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Unknown error')
    
    return token


#****** Some users have no public emails so this fetches their private emails in case so

def get_email(token:str)->str:
    email_url = "https://api.github.com/user/emails"
    request_header = {"Authorization":f"Bearer {token}"}
    response = requests.get(email_url, headers=request_header)

    if response.status_code == 200:
        emails = response.json()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Unknown error')

    primary_email = list(filter(lambda a:a["primary"] == True, list(emails)))[0]["email"]

    return primary_email

    
#******** User's info fetching

def get_user(code:str):
    token = get_gitToken(code)
    user_url = "https://api.github.com/user"
    request_header = {"Authorization":f"Bearer {token}"}

    response = requests.get(user_url, headers=request_header)

    if(response.status_code == 200):
        user_data:GitUser = response.json()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail='Unknown error while fetching user')

    userdata_copy = dict(user_data)

    if userdata_copy["email"] == None:
        email = get_email(token)
        userdata_copy.update({"email":email})
    
    return userdata_copy  