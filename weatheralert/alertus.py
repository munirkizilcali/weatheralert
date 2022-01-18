import requests
import json

from base64 import b64encode


url = "https://demo.alertustech.com/alertusmw/services/rest/activation/preset/"


# launches a Alertus preset alert with a given preset id, basic auth and a custom message
def activate_alert(alert_message: str):
    res = requests.post(
        url,
        headers={"Content-Type": "application/json", "Authorization": authorization()},
        data=json.dumps(
            {
                "sender": "Dev Candidate - Samuel",
                "presetId": 2207,
                "text": alert_message,
            }
        ),
    )

    id = int(res.content.decode("utf-8"))

    return id


# basic authorization using username:password with encode and decode
def authorization() -> str:
    auth_token = b64encode(("devcandidate:gooWmJQe").encode()).decode("ascii")
    return f"Basic {auth_token}"
