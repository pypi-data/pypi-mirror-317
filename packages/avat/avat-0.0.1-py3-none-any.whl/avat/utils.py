from .api_request import ApiRequest

def visualise_chat(chat_url, chat_headers):

    chat_response = ApiRequest(chat_url, chat_headers, json_flag=False).get()

    for i, msg in enumerate(chat_response.json()['previous_conversation']):
        if i % 2 == 0:
            print("Avatar: ", msg)
        else:
            print("Biz Agent: ", msg)