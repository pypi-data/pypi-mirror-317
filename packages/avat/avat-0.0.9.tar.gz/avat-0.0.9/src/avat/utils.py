from .api_request import ApiRequest
from icecream import ic

base_url = "http://0.0.0.0:8888/"
evals_url = base_url + 'run_msg_eval/'
evals_run_update_url = base_url + 'update_eval_run/'
avatar_url = base_url + 'chat/'

def visualise_chat(chat_url, chat_headers):

    chat_response = ApiRequest(chat_url, chat_headers, json_flag=False).get()

    for i, msg in enumerate(chat_response.json()['previous_conversation']):
        if i % 2 == 0:
            print("Avatar: ", msg)
        else:
            print("Biz Agent: ", msg)


def get_av_headers(auth_token):
    avatar_headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + auth_token,
        'Content-Type': 'application/json'
    }
    return avatar_headers

def get_eval_headers(auth_token):
    eval_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + auth_token,
    }
    return eval_headers

def get_chat_headers(auth_token):
    chat_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + auth_token,
    }
    return chat_headers


def get_avatar_data(avatar_id = "671e876cb93db3a0c724b1d5", new_chat=True, chat_session_id="", customer_agent_msg="", customer_agent_external_id="", avatar_instructions=""):
    data = {
        "avatar_id": avatar_id,
        "avatar_instructions": avatar_instructions,
        "chat_session_id": chat_session_id,
        "customer_agent_external_id": customer_agent_external_id,
        "customer_agent_msg": customer_agent_msg,
        "new_chat": new_chat
    }
    return data

def get_eval_data(msg_to_eval, chat_session_id, custom_eval_questions=[], standard_eval_tags=[]):
    data = {
            "chat_session_id": chat_session_id,
            "custom_eval_questions": custom_eval_questions,
            "standard_eval_tags": standard_eval_tags,
            "msg_to_eval": msg_to_eval
        }    
    return data


def user_login(user_email, user_password):

    login_url = base_url + 'auth/jwt/login/'
    login_headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    login_data = {
        'grant_type': 'password',
        'username': user_email,
        'password': user_password,
        'scope': '',
        #'client_id': 'string',
        #'client_secret': 'string'
    }

    login_response = ApiRequest(login_url, login_headers, login_data, json_flag=False).post()
    
    if "access_token" in login_response.json():
        auth_token = login_response.json()["access_token"]
    else:
        auth_token = ""
        ic(login_response.json())

    return auth_token

def user_signup(user_email, user_password):

    signup_url = base_url + 'auth/register/'
    signup_headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    signup_data = {
        "email": user_email,
        "password": user_password,
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,   
    }

    signup_response = ApiRequest(signup_url, signup_headers, signup_data, json_flag=True).post()
    return signup_response.json()