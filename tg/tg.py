#!/usr/bin/python3

import json
import os
import requests
from typing import List
StringsArray = List[str]

class Tg:

    def __init__(self, token: str, log_callback = None):
        self.__api_url_template = 'https://api.telegram.org/bot<token>/<method_name>'.replace('<token>', token)
        self.__log_callback = log_callback

    def __log(self, obj):
        if self.__log_callback is not None:
            self.__log_callback(obj)

    def __get_url(self, method: str):
        return self.__api_url_template \
                   .replace('<method_name>', method)

    def set_token(self, token):
        self.__token = token
        return self

    def get_token(self):
        return self.__token

    def get_me(self):
        return requests.post(self.__get_url('getMe'))

    def get_updates(self, last_update_id = None):
        url = self.__get_url('getUpdates')
        if last_update_id is not None:
            url = url + '?offset=' + str(last_update_id)

        # log_callback("get updates urlURL: %s" % url)

        rsp = requests.get(url)
        return { 'content' : rsp.content, 'json' : rsp.json() }

    def send_message(
        self,
        chat_id,
        text: str,
        parse_mode: str = None,
        reply_to_message_id = None
    ):
        if parse_mode is None:
            parse_mode = 'HTML'
        data = {
            'chat_id' : chat_id,
            'text' : text,
            'parse_mode' : parse_mode,
        }
        if reply_to_message_id is not None:
            data['reply_to_message_id'] = reply_to_message_id

        self.__log('send_message debug data')
        self.__log(data)

        return requests.post(self.__get_url('sendMessage'), data = data)

    def get_sticker_set(self, name: str):
        return requests.get(self.__get_url('getStickerSet') + '?name=' + name)

    def create_new_sticker_set(
        self,
        user_id,
        name: str,
        title: str,
        png_sticker,
        emojis: str
    ):
        params = {
            'user_id' : user_id,
            'name' : name,
            'title' : title,
            'png_sticker' : png_sticker,
            'emojis' : emojis,
        }

        self.__log('create_new_sticker_set debug params')
        self.__log(params)

        return requests.post(
            self.__get_url('createNewStickerSet'),
            data = params
        )

    def upload_sticker_file(self, user_id, png_sticker_file):
        return requests.post(
            self.__get_url('uploadStickerFile'),
            data = {
                'user_id' : user_id,
            },
            files = {
                'png_sticker' : png_sticker_file,
            }
        )

    def add_sticker_to_set(
        self,
        user_id,
        set_name: str,
        sticker: str,
        emojis: str):

        self.__log('add_sticker_to_set set_name: ' + set_name)
        return requests.post(
            self.__get_url('addStickerToSet'),
            data = {
                'user_id' : user_id,
                'name' : set_name,
                'png_sticker' : sticker,
                'emojis' : emojis,
            }
        )

    def delete_sticker_from_set(self, sticker: str):
        self.__log('delete sticker: ' + sticker)
        return requests.post(
            self.__get_url('deleteStickerFromSet'),
            data = {
                'sticker': sticker,
            }
        )

    def send_sticker(self, chat_id, sticker_id: str):
        self.__log('send sticker ' + str(sticker_id) + ' to chat ' + str(chat_id))

        return requests.post(
            self.__get_url('sendSticker'),
            data = {
                'chat_id' : chat_id,
                'sticker' : sticker_id
            }
        )

    def send_poll(self, chat_id, question: str, options: StringsArray):
        data = {
            'chat_id' : chat_id,
            'question' : question,
            'options' : json.dumps(options),
        }

        self.__log('send poll data: %s' % str(data))

        return requests.post(
            self.__get_url('sendPoll'),
            data = data
        )
