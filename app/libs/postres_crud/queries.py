from typing import List


async def get_all_advices() -> List[dict]:
    """
        TODO: create sql query to get advices
        select * from advice
    """

    return [dict(advice_id="6938d943-68d2-437d-92ef-2475cab01f11",
                 emotion="fear",
                 text="По твоим сообщениям, мне кажется, что ты немного напуган. Поделись с <Name> своими эмоциями. Можешь начать так: «Я сейчас чувствую...»",
                 is_deprecated=False,
                 is_sender=True),
            dict(advice_id="19c59cdc-67b5-49b5-b5fb-dc1c37eecc3b",
                 emotion="fear",
                 text="Кажется, <Name> испуган. Попробуй поддержать его/ее",
                 is_deprecated=False,
                 is_sender=False),
            dict(advice_id="94254ae6-0748-431c-92ea-1df00f442443",
                 emotion="anger",
                 text="Попробуй продолжить диалог так: «Я сейчас злюсь, потому что...».",
                 is_deprecated=False,
                 is_sender=True),
            dict(advice_id="d3efd1b7-9527-4ad1-80e9-c5085b4f1cbe",
                 emotion="anger",
                 text="Я определил, что <Name> нервничает. Попробуй уточнить причины его состояния.",
                 is_deprecated=False,
                 is_sender=False)
            ]


async def get_user_emotion_a_message(chat_id, user_id, from_at, to_at) -> List[dict]:
    """
        TODO: Все сообщения пользователя в чате за промежуток времени от from_at до to_ad с эмоциями и советами если они есть.

        select ma.user_id, ms.chat_id, ms.created_at, ma.advice_id, ad.*  from message_advice ma
        join messages ms on ma.message_id = ms.message_id
        join advice ad on ad.advice_id = ma.advice_id
        where ma.chat_id = '43313ac2-e18f-47b6-aa0b-73015465ded8'
        and ma.user_id = '7374700d-494d-480f-b99b-9ed76be14322'
        and ms.created_at between '2022-09-19 18:20:46.596121' and '2022-09-19 18:21:45.789603'
    """
    # Возврат тут примерный, сам запрос будет возвращать больше
    return [
        dict(
            emotion='joy',
            advice_id="6938d943-68d2-437d-92ef-2475cab01f11",
        ),
        dict(
            emotion='fear',
            advice_id=None,
        ),
        dict(
            emotion='anger',
            advice_id=None,
        ),
        dict(
            emotion='anger',
            advice_id=None,
        ),
        dict(
            emotion='anger',
            advice_id=None,
        ),
        dict(
            emotion='neutral',
            advice_id=None,
        ),
        dict(
            emotion='neutral',
            advice_id=None,
        ),
        dict(
            emotion='neutral',
            advice_id=None,
        ),
        dict(
            emotion='neutral',
            advice_id=None,
        )
    ]


async def get_last_user_advice_with_emotion(user_id, emotion: str, is_sender: bool):
    """
        TODO: Получить последний совет пользователя, с выбранной эмоцией (без привязки к чату), может вернуться None

        select ma.user_id, ma.advice_id, ad.*  from message_advice ma
        join messages ms on ma.message_id = ms.message_id
        join advice ad on ad.advice_id = ma.advice_id
        where ma.user_id = '7374700d-494d-480f-b99b-9ed76be14322'
        and ad.emotion = 'fear'
        and ad.is_sender = True
        order by ms.created_at desc
        limit 1
    """

    return None


async def get_chat_users(message_id):
    """
    TODO: Получить id и имя пользователей в личном чате

    select ms.* , u.username, u.firstname, u.lastname from message ms
    join users u on ms.user_id = u.user_id
    where ms.message_id = 1
    """
    # Примерный формат возврата
    return [
        dict(
            user_id="7374700d-494d-480f-b99b-9ed76be14322",
            username='Avatar',
            firstname='Тимур',
            lastname='Самигулин'
        ),
        dict(
            user_id="43313ac2-e18f-47b6-aa0b-73015465ded8",
            username='Alex',
            firstname='Александр',
            lastname='Леонов'
        )
    ]


async def get_user_all_emotion_messages(user_id, from_at, to_at) -> List[dict]:
    """
        TODO: Все сообщения пользователя за промежуток времени от from_at до to_ad с эмоциями из всех чатов.

        select ma.user_id, ms.chat_id, ms.created_at, ma.emotion, ma.advice_id  from message_advice ma
        where ma.user_id = '7374700d-494d-480f-b99b-9ed76be14322'
        and ms.created_at between '2022-09-19 18:20:46.596121' and '2022-09-19 18:21:45.789603'
    """
    # Возврат тут примерный, сам запрос будет возвращать больше
    return [
        dict(
            emotion='joy',
            advice_id="6938d943-68d2-437d-92ef-2475cab01f11",
        ),
        dict(
            emotion='fear',
            advice_id=None,
        ),
        dict(
            emotion='anger',
            advice_id=None,
        ),
        dict(
            emotion='anger',
            advice_id=None,
        ),
        dict(
            emotion='anger',
            advice_id=None,
        ),
        dict(
            emotion='neutral',
            advice_id=None,
        ),
        dict(
            emotion='neutral',
            advice_id=None,
        ),
        dict(
            emotion='neutral',
            advice_id=None,
        ),
        dict(
            emotion='neutral',
            advice_id=None,
        )
    ]
