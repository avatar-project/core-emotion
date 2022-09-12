# Руководство по установке

Клонировать репозиторий

    https://gitlab.actcognitive.org/avatar/core-emotion.git

Скачать модель для детекции эмоций и токсичности по [ссылке](https://drive.google.com/drive/folders/1jGZDYIR1e6bvxtltvpQoQw67hcjuWUxX?usp=sharing) и добавить в папку app/models

В файле app/libs/main.py находятся функции для получения эмоций и советов для сообщений

<b>Функция /psycho_text_analyze</b>

Получает на вход сообщение по схеме MessageBase:

    class MessageBase(BaseModel):
        chat_id: UUID4
        message_id: UUID4
        created_at: datetime
        content: str = ''

А на выход MessageWithEmotions:

    class MessageWithEmotions(BaseModel):
        message_id: UUID4
        emotion: EmotionType
        advice: Advice
