import torch
from transformers import BertTokenizer, BertForSequenceClassification


class EmotionModels:
    tokenizer = BertTokenizer.from_pretrained('app/models/emotion-detection')
    model = BertForSequenceClassification.from_pretrained(
        'app/models/emotion-detection', problem_type="multi_label_classification")


class Emotion:
    # def __init__(self):
    #     self.tokenizer = BertTokenizer.from_pretrained('app/models/emotion-detection')
    #     self.model = BertForSequenceClassification.from_pretrained(
    #         'app/models/emotion-detection', problem_type="multi_label_classification")

    def predict(self, text):
        inputs = EmotionModels.tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            logits = EmotionModels.model(**inputs).logits

        predicted_class_id = logits.argmax().item()
        print('Emotion class')
        print(EmotionModels.model.config.id2label)
        print(EmotionModels.model.config.label2id)
        print('Emotion class')

        return (predicted_class_id, EmotionModels.model.config.id2label[predicted_class_id])


# def get_emotion_object():
#     emotion = Emotion()
#     return emotion
