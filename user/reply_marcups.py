from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from icecream import ic


class UserReplyMarkup:
    MESSAGES = {
        "choose_option_to_continue": {
            "get_recipe": {
                "text": "Отримати рецепт після святкування у Гастролофт",
                "callback_data": "get_recipe",
            },
            "send_booking_req": {
                "text": "Відправити запит на бронювання події",
                "callback_data": "send_booking_req",
            },
            "leave_review": {
                "text": "Залишити відгук",
                "callback_data": "leave_review",
            },
            "contact_manager": {
                "text": "Зв’язатись з менеджером",
                "callback_data": "contact_manager",
            },
            "view_articles": {
                "text": "Переглянути статті",
                "callback_data": "view_articles",
            },
            "view_latest_studio_news": {
                "text": "Переглянути останні новини студії",
                "callback_data": "view_latest_studio_news",
            },
        },
    }

    def __init__(self):
        self.text = UserReplyMarkup.MESSAGES

    async def get_marcup(self, key: str, row_width=1) -> InlineKeyboardMarkup:
        reply_marcup = InlineKeyboardMarkup(row_width=row_width)
        for el in self.text.get(key):
            reply_marcup.add(InlineKeyboardButton(**self.text[key].get(el)))
        return reply_marcup
