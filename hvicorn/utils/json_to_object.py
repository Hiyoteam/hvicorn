from hvicorn.models.server import (
    ChatPackage,
    EmotePackage,
    InfoPackage,
    InvitePackage,
    OnlineAddPackage,
    OnlineRemovePackage,
    OnlineSetPackage,
    UpdateUserPackage,
    WarnPackage,
    WhisperPackage,
    UpdateMessagePackage,
    ChangeNickPackage,
    CaptchaPackage,
    LockroomPackage,
    WhisperSentPackage,
    UncatchedPackage,
)
from typing import Union
import string


def verifyNick(nick: str) -> bool:
    if len(nick) > 24:
        return False
    for char in nick:
        if char not in string.ascii_letters + string.digits + "_":
            return False
    return True


def json_to_object(
    data: dict,
) -> Union[
    ChatPackage,
    EmotePackage,
    InfoPackage,
    InvitePackage,
    OnlineAddPackage,
    OnlineRemovePackage,
    OnlineSetPackage,
    UpdateUserPackage,
    WarnPackage,
    WhisperPackage,
    UpdateMessagePackage,
    ChangeNickPackage,
    CaptchaPackage,
    LockroomPackage,
    WhisperSentPackage,
    UncatchedPackage,
]:
    if not data.get("cmd"):
        raise ValueError("No `cmd` provided")
    command = data.get("cmd")
    if command == "chat":
        return ChatPackage(**data)
    elif command == "emote":
        data["content"] = data["text"].split(" ", 1)[1]
        return EmotePackage(**data)
    elif command == "info":
        if not data.get("type"):
            if (
                data.get("text", "").count(" ") == 3
                and data.get("text", "").split(" ", 1)[1].startswith("is now")
                and verifyNick(data.get("text", "").split()[0])
                and verifyNick(data.get("text", "").split()[3])
            ):
                data["old_nick"] = data.get("text", "").split(" ")[0]
                data["new_nick"] = data.get("text", "").split(" ")[3]
                return ChangeNickPackage(**data)
            elif (
                data.get("text", "")
                == "You have been denied access to that channel and have been moved somewhere else. Retry later or wait for a mod to move you."
            ):
                return LockroomPackage(time=data["time"])
            return InfoPackage(**data)
        elif data.get("type") == "whisper":
            if data.get("text", "").startswith("You whispered to"):
                data["userid_from"] = data["from"]
                data["userid_to"] = data["to"]
                del data["from"]
                del data["to"]
                data["content"] = data["text"].split(": ", 1)[1]
                return WhisperSentPackage(**data)
            else:
                data["nick"] = data["from"]
                data["userid_to"] = data["to"]
                del data["from"]
                del data["to"]
                data["content"] = data["text"].split(": ", 1)[1]
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
    elif command == "captcha":
        return CaptchaPackage(**data)
    elif command == "warn":
        return WarnPackage(**data)
    else:
        return UncatchedPackage(rawjson=data)
