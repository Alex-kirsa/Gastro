# from states import *

# from aiogram import types
# from icecream import ic


class UserText:
    def __init__(self):
        self._stock = {
            "start_message": (
                "<i>Привіт, це Бот Кулінарної Студії Гастролофт\n"
                "Я допоможу тобі:\n"
                "• отримати рецепти після твоєї події\n"
                "• відправити запит на бронювання події\n"
                "• отримувати нові рецепти та знання з кулінарії від Команди Шеф-Кухарів Гастролофт\n"
                "• бути в курсі останніх подій у Кулінарній студії\n"
                "• переглянути цікаві статті від авторів і Шеф-кухарів\n"
                "• у разі питань - швидко зв’яжу з нашим адміністратором студії\n"
                "прийму ваш щирий та чесний відгук про ваш захід і нашу студію, щоб в наступний раз ми були якомога ближче до “10 з 10”</i>\n"
            ),
            "choose_option_to_continue": "<i>Для того щоб продовжити виберіть із меню наступну дію:</i>",
            "enter_date": "<i>Введіть дату формату дд/мм/рррр</i>",
            "when_event_happened": "<i>Коли відбулася ця подія: вдень чи ввечері?</i>",
            "food_was_then": "<i>Замовлення того дня:</i>\n{food}",
            "send_form": "<i>Відправте мені дані по наступному шаблонові</i>",
            "change_form": (
                "Ім'я: <b>{name}</b>\n"
                "Телефон: <b>{phone}</b>\n"
                "Подія(Корпоратив,Весілля,День Народження/Інші варіанти): <b>{action}</b>\n"
                # "Кількість людей: <b>{num_of_people}</b>\n"
                # "Бажана дата: <b>{desired_date}</b>\n"
            ),
            "change_form_state": {
                "name": "<i>Введіть ім'я:</i>",
                "phone": "<i>Введіть телефон:</i>",
                "action": "<i>Введіть назву події:</i>",
                # "num_of_people": "<i>Введіть кількість людей:</i>",
                # "desired_date": "<i>Введіть бажану дату (формат дд.мм.рррр):</i>",
            },
            "should_we_send_form": "<i>Натисніть кнопку нижче, щоб відправити запит.</i>",
            "form_sent": "<i>Запит успішно надіслано. /help</i>",
            "send_me_comment": "<i>Напишіть мені ваш коментар по наших подіям.</i>",
            "message_sent": "<i>Ваш коментар розміщено. /help</i>",
            "no_mailing": "<i>Ще не було жодної новини.</i>",
            "admin_menu": "Адмінове меню.",
            "admin_send_post": "<i>Надішліть пост, який я маю надіслати.</i>",
            "admin_post_sent": "<i>Оголошення надіслано <b>{cou}</b> користувачам.</i>",
            "new_comment": "<i>Новий коментар від @{username}.</i>\n{text}",
            "no_food": "<i>На цей день не було замовлень.</i>",
            "last_studio_new": "<i>Остання новина студії:</i>",
            "you_must_fill_blanks": "Ви маєте заповнити всі пусті бланки.",
            "new_booking": "<i>Нове бронювання від @{username}</i>:\n{text}",
            "reminder": ".",
            "manager_contact": "<i>Наш менеджер: @{username}</i>",
            "wait_food": "<i>Очікуйте, шукаю інформацію.</i>",
        }

    async def get_text(self, key: str | None = None, **kwargs):
        return self._stock.get(key).format(**kwargs)
