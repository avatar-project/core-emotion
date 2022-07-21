from pyrsistent import thaw
import torch
from transformers import BertTokenizer, BertForSequenceClassification


class BertToxic():
    device = torch.device(
        "cuda:0" if torch.cuda.is_available() else "cpu")
    max_len = 512
    tokenizer = BertTokenizer.from_pretrained('app/models/rubert-toxic-detection')
    model = BertForSequenceClassification.from_pretrained('app/models/rubert-toxic-detection')

    def eval_model():
        BertToxic.model.to(BertToxic.device)
        BertToxic.model.eval()


class BertPredict():

    def predict(self, text: str, model_name: str = 'toxic') -> int:

        if model_name == 'toxic':
            CUR_MODEL = BertToxic
        else:
            raise ValueError('model_name must be toxic')

        CUR_MODEL.eval_model()

        encoding = CUR_MODEL.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=CUR_MODEL.max_len,
            return_token_type_ids=False,
            truncation=True,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
        )

        out = {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten()
        }

        input_ids = out["input_ids"].to(CUR_MODEL.device)
        attention_mask = out["attention_mask"].to(CUR_MODEL.device)

        outputs = CUR_MODEL.model(
            input_ids=input_ids.unsqueeze(0),
            attention_mask=attention_mask.unsqueeze(0)
        )

        prediction = torch.argmax(outputs.logits, dim=1).cpu().numpy()[0]

        return True if prediction else False
