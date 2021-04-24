import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import  VkBotLongPoll, VkBotEventType
from vk_api import VkUpload
import os

vk_session = vk_api.VkApi(token=os.environ["vk_token"])
longpoll = VkBotLongPoll(vk_session, os.environ["vk_group_id"])
Upload = VkUpload(vk_session)


def send_msg(peer_id, text):
    print(f"[method: send_msg, peer_id: {peer_id}, text: {text}]")
    vk_session.method("messages.send", {"peer_id": peer_id, "message": text, "random_id": get_random_id()})


def send_photo(peer_id, text):
    print(f"[method: send_photo, peer_id: {peer_id}, text: {text}]")
    try:
        c = Upload.photo_messages(photos="group.png")[0]
        d = 'photo{}_{}'.format(c['owner_id'], c['id'])
        vk_session.method('messages.send', {'peer_id': peer_id, 'message': text, 'attachment': d, 'random_id': get_random_id()})
        return True
    except:
        return False