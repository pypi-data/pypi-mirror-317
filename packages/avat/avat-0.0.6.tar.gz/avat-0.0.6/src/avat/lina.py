import requests
import json
from icecream import ic
from .api_request import ApiRequest
import concurrent.futures
import time

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

def get_avatar(avatar_id, auth_token):

    avatar_url = 'http://0.0.0.0:8888/get_avatar?avatar_id=' + avatar_id
    avatar_headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + auth_token,
    }
    avatar = ApiRequest(avatar_url, avatar_headers, json_flag=False).get()
    return avatar

def create_avatar(auth_token, avatar_bio, first_message):

    avatar_url = 'http://0.0.0.0:8888/create_avatar?avatar_bio=' + avatar_bio + "&first_message=" + first_message
    avatar_headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + auth_token,
    }
    avatar_id = ApiRequest(avatar_url, avatar_headers, json_flag=False).get()
    return avatar_id.json()

def get_eval_data(msg_to_eval, chat_session_id, custom_eval_questions=[], standard_eval_tags=[]):

    data = {
            "chat_session_id": chat_session_id,
            "custom_eval_questions": custom_eval_questions,
            "standard_eval_tags": standard_eval_tags,
            "msg_to_eval": msg_to_eval
        }    
    return data

def user_login(user_email, user_password):

    login_url = 'http://0.0.0.0:8888/auth/jwt/login/'
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


def parse_agent_reply(customer_agent_response):

    if "agent_reply" in customer_agent_response.json():
        return customer_agent_response.json()["agent_reply"]
    else:
        # TODO frontline specific 
        return customer_agent_response.json()[-1]["content"]["text"]


def run_chat_evals(custom_eval_questions, 
                   standard_eval_tags, 
                   customer_agent_endpoints, 
                   auth_token, 
                   n_max_turns=2, 
                   n_runs=2, 
                   avatar_id="671e876cb93db3a0c724b1d5", 
                   avatar_first_message="", 
                   customer_agent_avatar_mes_key = "avatar_msg", 
                   json_flag=True,
                   eval_every_message=False):

    
    customer_agent_url, customer_agent_headers, agent_data = customer_agent_endpoints
    
    evals_run_url = 'http://0.0.0.0:8888/create_eval_run/'
    evals_run_update_url = 'http://0.0.0.0:8888/update_eval_run/'

    ev_run_data = {"n_runs":str(n_runs), "tot_eval_scores": {}, "aggregate_score": "0"}
    evals_run = ApiRequest(evals_run_url, customer_agent_headers, ev_run_data).post().json()

    run_id = evals_run["eval_run_id"]        

    tot_eval_scores = {}    

    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        avatar_run = [executor.submit(_run_chat_evals, customer_agent_url, customer_agent_headers, agent_data, auth_token, customer_agent_avatar_mes_key, avatar_first_message, n_max_turns, eval_every_message, run_id, custom_eval_questions, standard_eval_tags, avatar_id, json_flag) for run_n in range(0, n_runs)]
        
        for future in concurrent.futures.as_completed(avatar_run):
            correct_count, tot, eval_scores = future.result()
            
            for ev,score in eval_scores.items():
                if ev in tot_eval_scores:
                    tot_eval_scores[ev] += score
                else:
                    tot_eval_scores[ev] = score
    
    accuracy_scores, aggregate_score = get_tot_eval_scores(tot_eval_scores, n_runs)
    evals_run_response = ApiRequest(evals_run_update_url, customer_agent_headers, {"run_id": run_id, "eval_chat_ids": [], "tot_eval_scores": accuracy_scores, "aggregate_score": aggregate_score}).post()

# TODO refactor
def _run_chat_evals(customer_agent_url, customer_agent_headers, agent_data, auth_token, customer_agent_avatar_mes_key, avatar_first_message, n_max_turns, eval_every_message, run_id, custom_eval_questions, standard_eval_tags, avatar_id, json_flag, sleep_time=2):

    correct_count = 0
    tot = 0

    evals_url = 'http://0.0.0.0:8888/run_msg_eval/'
    evals_run_update_url = 'http://0.0.0.0:8888/update_eval_run/'

    avatar_url = 'http://0.0.0.0:8888/chat/'
    avatar_headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer ' + auth_token,
        'Content-Type': 'application/json'
    }
    
    chat_headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + auth_token,
    }

    agent_data[customer_agent_avatar_mes_key] = avatar_first_message
    agent_data["is_new_chat"] = True
    customer_agent_response = ApiRequest(customer_agent_url, customer_agent_headers, agent_data, json_flag=json_flag).post()
    customer_agent_response = parse_agent_reply(customer_agent_response)
    
    avatar_data = get_avatar_data(new_chat=True,customer_agent_msg=customer_agent_response, avatar_id=avatar_id)
    avatar_response = ApiRequest(avatar_url, avatar_headers, avatar_data).post()
    avatar_reply = avatar_response.json()["avatar_reply"]

    # TODO ugly, generalise
    chat_session_id = avatar_response.json()["chat_session_id"]
    agent_data["chat_session_id"] = chat_session_id # TODO to support the dummy agent
    agent_data[customer_agent_avatar_mes_key] = avatar_reply
    
    if eval_every_message:
        evals_response = ApiRequest(evals_url, customer_agent_headers, get_eval_data(customer_agent_response, chat_session_id, custom_eval_questions, standard_eval_tags)).post()
        compute_score(evals_response)

    for i in range(0, n_max_turns):

        time.sleep(sleep_time)
        
        agent_data["is_new_chat"] = False
        agent_data["chat_session_id"] = chat_session_id
        customer_agent_response = ApiRequest(customer_agent_url, customer_agent_headers, agent_data, json_flag=json_flag).post()
        customer_agent_response = parse_agent_reply(customer_agent_response)

        avatar_data = get_avatar_data(new_chat=False, chat_session_id=chat_session_id,customer_agent_msg=customer_agent_response, avatar_id =avatar_id)
        avatar_response = ApiRequest(avatar_url, avatar_headers, avatar_data).post()
        avatar_reply = avatar_response.json()["avatar_reply"]
        is_last_avatar_message = avatar_response.json()["is_last_message"]
        #ic(is_last_avatar_message)

        agent_data[customer_agent_avatar_mes_key] = avatar_reply 

        if eval_every_message:
            evals_response = ApiRequest(evals_url, customer_agent_headers, get_eval_data(customer_agent_response, chat_session_id, custom_eval_questions, standard_eval_tags)).post()
            compute_score(evals_response)

        if is_last_avatar_message:
            break


    # Get whole chat
    chat_url = 'http://0.0.0.0:8888/get_chat/' + "?chat_session_id=" + chat_session_id
    chat_response = ApiRequest(chat_url, chat_headers).get()
    ic(chat_response.json())
    whole_chat = str(chat_response.json()['previous_conversation'])
    

    # Eval whole chat
    evals_response = ApiRequest(evals_url, customer_agent_headers, get_eval_data(whole_chat, chat_session_id, custom_eval_questions, standard_eval_tags)).post()
    # TODO Verbose to have to pass empty values. Fix.
    evals_run_response = ApiRequest(evals_run_update_url, customer_agent_headers, {"run_id": run_id, "eval_chat_ids": [chat_session_id,], "tot_eval_scores": {}, "aggregate_score": "0"}).post()

    accuracy_count, tot_count, eval_scores = compute_score(evals_response, verbose=False)

    correct_count += accuracy_count
    tot += tot_count

    return correct_count, tot, eval_scores

    
            
def get_tot_eval_scores(tot_eval_scores, n_runs, verbose=True):

    accuracy_scores = {}
    aggregate_score = 0

    if verbose: print("Eval Results for " + str(n_runs) + " runs:")
    for ev,score in tot_eval_scores.items():
        acc = round(score / n_runs, 3)
        s_acc = str(acc)
        accuracy_scores[ev] = s_acc
        if verbose: print(ev + ": " + s_acc)
        aggregate_score += acc

    aggregate_score = str(round(aggregate_score / len(tot_eval_scores), 3))

    return accuracy_scores, aggregate_score





def compute_score(evals_response, verbose=False):

    evals_response = evals_response.json()["evals"]

    accuracy_count = 0
    tot_count = 0

    if len(evals_response) == 0:
        return ""
    
    log = "########################### \nMessage to evaluate: \n"
    log += evals_response[0]["msg_to_eval"] + "\n"
    log += "########################### \nEvaluation: \n"

    eval_scores = {}

    for eval in evals_response:

        tot_count += 1
        result = eval["eval_result"]

        score = 0
        if "pass" in result.lower():
            score = 1
            
        accuracy_count += score

        if "eval_question" in eval:
            log += result + ": " + str(eval["eval_question"]) + "\n"
            eval_scores[eval["eval_question"]] = score

        elif "eval_tag" in eval:
            log += result + ": " + str(eval["eval_tag"]) + "\n"
            eval_scores[eval["eval_tag"]] = score

    log += "########################## \nAccuracy: \n"
    log += str(accuracy_count) + "/" + str(tot_count) + "\n"

    if verbose:
        print(log)
    return accuracy_count, tot_count, eval_scores


