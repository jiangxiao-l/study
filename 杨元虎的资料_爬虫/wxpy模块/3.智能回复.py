


import wxpy,requests,json
weichat = wxpy.Bot()

def get_message(msg):
    url = "http://www.tuling123.com/openapi/api"
    api_key = "9df516a74fc443769b233b01e8536a42"
    payload = {
        "key": api_key,
        "info": msg,
    }
    res = requests.post(url,data=json.dumps(payload))
    dicts = json.loads(res.content)
    return dicts["text"]



@weichat.register()
def receiver(msg):
    weichat.file_helper.send("%s: %s" % (msg.sender.name,msg.text))
    return get_message(msg.text)

wxpy.embed()


