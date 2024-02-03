from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

# from aiogram.utils.callback_data import CallbackData
# from icecream import ic


class UserReplyMarkup:
    MESSAGES = {
        "choose_option_to_continue": {
            "get_recipe": {
                "text": "Отримати рецепт після святкування у Гастролофт",
                "callback_data": "get_recipe",
            },
            "send_booking_req": {
                "text": "Відправити запит на бронювання події",
                "callback_data": "change_form",
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
                "web_app": WebAppInfo(url="https://www.google.com"),
            },
            "view_latest_studio_news": {
                "text": "Переглянути останні новини студії",
                "callback_data": "view_latest_studio_news",
            },
        },
        "when_event_happened": {
            "event_happedned_day": {
                "text": "Вдень",
                "callback_data": "when_event_happened:д",
            },
            "event_happedned_evening": {
                "text": "Ввечері",
                "callback_data": "when_event_happened:в",
            },
        },
        "change_form": {
            "name": {
                "text": "Змінити ім'я",
                "callback_data": "change_form:name",
            },
            "phone": {
                "text": "Змінити телефон",
                "callback_data": "change_form:phone",
            },
            "action": {
                "text": "Змінити подію",
                "callback_data": "change_form:action",
            },
            "num_of_people": {
                "text": "Змінити кількість людей",
                "callback_data": "change_form:num_of_people",
            },
            "desired_date": {
                "text": "Змінити бажану дату",
                "callback_data": "change_form:desired_date",
            },
        },
        "should_we_send_form": {
            "text": "Надіслати запит",
            "callback_data": "should_we_send_form",
        },
        "admin_menu": {"mail_to_all_users": "Розсилка всім користувачам"},
    }

    def __init__(self):
        self.text = UserReplyMarkup.MESSAGES

    async def get_marcup(self, key: str, row_width=1) -> InlineKeyboardMarkup:
        reply_marcup = InlineKeyboardMarkup(row_width=row_width)
        for el in self.text.get(key):
            reply_marcup.add(InlineKeyboardButton(**self.text[key].get(el)))
        return reply_marcup
