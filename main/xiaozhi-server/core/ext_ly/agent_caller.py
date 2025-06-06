
import requests
import json


def new_session(base_url: str, api_key: str, agent_id: str) -> str:
    try:
        url = f"{base_url}/api/v1/agents/{agent_id}/sessions"
        payload = {}
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            session_id = response.json()['data']['id']
            return session_id
        else:
            return None
    except Exception as e:
        print(f"new_session Error: {e}")
        return None


def ask_agent(base_url: str, api_key: str, agent_id: str, question: str, session_id: str) -> str:
    try:
        url = f"{base_url}/api/v1/agents/{agent_id}/completions"
        payload = json.dumps({
            "question": question,
            "stream": False,
            "session_id": session_id
        })
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            res = response.json()
            if res['code']!=0:
                print(f"ask_agent Error: {response.text}")
                return None
            answer = res['data']['answer']
            return answer
    except Exception as e:
        print(f"ask_agent Error: {e}")
        return None


def delete_session(base_url: str, api_key: str, agent_id: str, session_id: str) -> bool:
    try:
        url = f"{base_url}/api/v1/agents/{agent_id}/sessions"
        payload = json.dumps({
            "ids": [
                session_id
            ]
        })
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.request(
            "DELETE", url, headers=headers, data=payload)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(f"delete_session Error: {e}")
        return False
