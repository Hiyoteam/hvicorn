from hvicorn.utils.json_to_object import json_to_object
from traceback import print_exc
from rich import print as prettyprint
import json, websocket
ws=websocket.create_connection("wss://hack.chat/chat-ws")
ws.send(json.dumps({"cmd":"join","channel":"lounge","nick":"hvicorn_testing"}))
while 1:
    data=json.loads(ws.recv())
    try:
        prettyprint(json_to_object(data))
    except:
        print_exc()
        prettyprint(data)
