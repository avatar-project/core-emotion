import torch
from transformers import BertTokenizer, BertForSequenceClassification


class EmotionModels:
    """Статика, для того, чтобы модель загрузилась всего один раз
    """
    tokenizer = BertTokenizer.from_pretrained('app/models/emotion-detection')
    model = BertForSequenceClassification.from_pretrained(
        'app/models/emotion-detection', problem_type="multi_label_classification")


class Emotion:
    """Классификация эмоций по тексту
    """

    def predict(self, text: str):
        """Метод для определения эмоций из текста

        Args:
            text (str): _description_

        Returns:
            tuple: (emotion id, emotion title)
        """
        inputs = EmotionModels.tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            logits = EmotionModels.model(**inputs).logits

        predicted_class_id = logits.argmax().item()

        return (predicted_class_id, float(torch.softmax(logits, -1).cpu().numpy()[0][predicted_class_id]))
