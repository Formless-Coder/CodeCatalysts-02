import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load trained model
MODEL_PATH = '../../models/category_model'  # Relative to utils/
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.eval()

import joblib
label_map = joblib.load('../../models/label_map.pkl')
inv_label_map = {v: k for k, v in label_map.items()}

def categorize(text):
    encoding = tokenizer(text, truncation=True, padding='max_length', max_length=128, return_tensors='pt')
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
    pred = torch.argmax(outputs.logits, dim=1).item()
    return inv_label_map.get(pred, 'Unknown')