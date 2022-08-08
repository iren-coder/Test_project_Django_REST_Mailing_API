import json
import time

import requests
from django.db.models import Q

from app.celery import app
from app.settings import PROBE_SERVER_URL, TOKEN
from mailing.models import Client, Mailing, Message

# Start mailing
@app.task
def start_maillist(maillist_id):
    maillist = Mailing.objects.get(id=maillist_id)
    op_code = maillist.operator_code
    tag = maillist.tag
    clients = Client.objects.filter(
        Q(operator_code__exact=op_code) & Q(tag__exact=tag)
    )
    for client in clients:
        message = Message(
            status="Pending",
            maillist=maillist,
            client=client
        )
        message.save()
        msg_id = message.id
        phone = message.client.phone_number
        text = maillist.text
        send_message.delay(msg_id, phone, text)

# Send message
@app.task
def send_message(msg_id, phone, text):
    url = "{}/send/{}".format(PROBE_SERVER_URL, msg_id)
    data = {
        "id": msg_id,
        "phone": phone,
        "text": text
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(TOKEN),
        "Content-Type": "application/json"
    }
    
    counter = 0
    while counter < 3:
        response = requests.post(
            url=url,
            data=json.dumps(data),
            headers=headers
        )
        if response.status_code == 200:
            message = Message.objects.get(id=msg_id)
            message.status = "Success"
            message.save()
            return True
        else:
            counter += 1
            time.sleep(300)
    message = Message.objects.get(id=msg_id)
    message.status = "Failed"
    message.save()
    return True