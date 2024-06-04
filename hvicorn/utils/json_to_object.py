from hvicorn.models.server import ChatPackage, EmotePackage, InfoPackage, InvitePackage, OnlineAddPackage, OnlineRemovePackage, OnlineSetPackage, UpdateUserPackage, WarnPackage, WhisperPackage, UpdateMessagePackage
from typing import Union

def json_to_object(data: dict) -> Union[ChatPackage, EmotePackage, InfoPackage, InvitePackage, OnlineAddPackage, OnlineRemovePackage, OnlineSetPackage, UpdateUserPackage, WarnPackage, WhisperPackage, UpdateMessagePackage]:
    if not data.get("cmd"):
        raise ValueError("No `cmd` provided")
    command=data.get("cmd")
    if command == "chat":
        return ChatPackage(**data)
    elif command == "emote":
        data["content"] = data["text"].split(" ",1)[1]
        return EmotePackage(**data)
    elif command == "info":
        if not data.get("type"):
            return InfoPackage(**data)
        elif data.get("type") == "whisper":
            data["nick"] = data["from"]
            data["userid_to"] = data["to"]
            del data["from"]
            del data["to"]
            data["content"] = data["text"].split(": ",1)[1]
            return WhisperPackage(**data)
        elif data.get("type") == "invite":
            data["from_nick"] = data["from"]
            data["to_userid"] = data["to"]
            del data["from"]
            del data["to"]
            return InvitePackage(**data)
    elif command == "onlineSet":
        return OnlineSetPackage(**data)
    elif command == "onlineAdd":
        return OnlineAddPackage(**data)
    elif command == "onlineRemove":
        return OnlineRemovePackage(**data)
    elif command == "updateUser":
        return UpdateUserPackage(**data)
    elif command == "updateMessage":
        return UpdateMessagePackage(**data)
    elif command == "warn":
        return WarnPackage(**data)
    else:
        raise ValueError("Unknown package type")