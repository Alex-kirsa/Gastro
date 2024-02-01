from user.text import UserText
from user.reply_marcups import UserReplyMarkup


class UserManager:
    def __init__(self, user_id, call=None, state=None):
        self.text = UserText()
        self.reply_markup = UserReplyMarkup()
