from datetime import datetime

from typing import List

class Update:

    def __init__(self, input: dict):
        self.input = input
        self.message = input.get('message', dict())
        self.edited_message = input.get('edited_message', dict())
        self.author = self.message.get('from', {})
        self.chat = self.message.get('chat', {})
        self.sticker = self.message.get('sticker', {})

    def get(self):
        return self.input

    def get_id(self):
        return self.input.get('update_id')

    def get_date(self):
        return self.message.get('date', self.edited_message.get('date'))

    def get_message(self):
        return self.message

    def get_message_id(self):
        return self.message.get('message_id', None)

    def get_text(self):
        return self.message.get('text', '')

    def get_text_lower(self):
        return self.get_text().lower()

    def get_chat(self):
        return self.chat

    def get_chat_id(self):
        return self.chat.get('id')

    def get_chat_title(self):
        return self.chat.get('title')

    def get_author(self):
        return self.author

    def get_author_id(self):
        return self.author.get('id', '')

    def get_author_username(self):
        return self.author.get('username', '')

    def get_author_first_name(self):
        return self.author.get('first_name', '')

    def get_author_last_name(self):
        return self.author.get('last_name', '')

    def get_author_string(self) -> str:
        return '|'.join([
            self.get_author_username(),
            self.get_author_first_name(),
            self.get_author_last_name(),
        ])

    def is_sticker(self):
        return bool(self.sticker)

    def get_sticker(self):
        return self.sticker

    def get_sticker_file_id(self):
        if isinstance(self.sticker, dict):
            return self.sticker.get('file_id', None)
        return None

    def get_sticker_setname(self):
        if isinstance(self.sticker, dict):
            return self.sticker.get('set_name', None)
        return None

    def is_private(self):
        return self.chat.get('type') == 'private'

    def get_date_diff(self, date: datetime = None) -> int:
        if date is None:
            date = datetime.now()

        upd_date = datetime.fromtimestamp(self.get_date())
        diff = date - upd_date
        return diff.seconds

    def text_contains(self, values: List[str]):
        return len(list(filter(lambda v: v.lower() in self.get_text_lower(), values))) > 0

    def get_mentions(self) -> List[str]:
        text = self.get_text()
        entities = self.message.get('entities', [])
        return list(
            map(
                lambda entity: text[entity.get('offset'):entity.get('length') + entity.get('offset')].replace('@', ''),
                entities
            )
        )
