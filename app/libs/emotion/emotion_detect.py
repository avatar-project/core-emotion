import torch
from transformers import BertTokenizer, BertForSequenceClassification

class Emotion():
    def __init__(self) -> None:
        self.tokenizer = BertTokenizer.from_pretrained('app/models/emotion-detection')
        self.model = BertForSequenceClassification.from_pretrained('app/models/emotion-detection', problem_type="multi_label_classification")
        
    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            logits = self.model(**inputs).logits

        predicted_class_id = logits.argmax().item()

        return (predicted_class_id, self.model.config.id2label[predicted_class_id])
