import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.nn import CrossEntropyLoss
import joblib
import pytesseract
from PIL import Image
from tqdm import tqdm  # For progress bars

# Paths (adjust if needed)
DATA_DIR = 'data/'
MODELS_DIR = 'models/'
os.makedirs(MODELS_DIR, exist_ok=True)

# 1. OCR Evaluation (on image datasets; compute accuracy)
def evaluate_ocr():
    # Example: Load SROIE images/ground truth (assume 'sroie-datasetv2/' unzipped with images and .txt annotations)
    ocr_dir = os.path.join(DATA_DIR, 'sroie-datasetv2')
    if not os.path.exists(ocr_dir):
        print("Download and unzip SROIE to data/sroie-datasetv2/")
        return
    # Sample evaluation (expand to all datasets)
    accuracies = []
    for img_file in os.listdir(ocr_dir):
        if img_file.endswith('.jpg'):
            img_path = os.path.join(ocr_dir, img_file)
            gt_path = img_path.replace('.jpg', '.txt')  # Assume GT exists
            if os.path.exists(gt_path):
                extracted = pytesseract.image_to_string(Image.open(img_path))
                with open(gt_path, 'r') as f:
                    gt = f.read()
                acc = len(set(extracted.split()) & set(gt.split())) / len(set(gt.split())) if gt else 0
                accuracies.append(acc)
    print(f"Average OCR Accuracy on SROIE: {np.mean(accuracies):.2f}")
    # Repeat for other OCR datasets (e.g., expenses-receipt-ocr)

# 2. Train Categorization Model (PyTorch BERT on combined CSVs)
def train_categorization():
    # Load and combine datasets (assume CSVs with 'text'/'description' and 'category')
    cat_files = [
        'personal-expense-classification-dataset/transactions.csv',
        'expense-tracker/data.csv',  # Adjust filenames
        'my-expenses-data/expenses.csv',
        'personal-expense-data/expenses.csv',
        'expenses-2024/expenses.csv'
    ]
    dfs = []
    for file in cat_files:
        path = os.path.join(DATA_DIR, file)
        if os.path.exists(path):
            df = pd.read_csv(path)
            df = df[['description', 'category']]  # Standardize columns
            df.columns = ['text', 'category']
            dfs.append(df)
    if not dfs:
        print("No categorization data found; skipping.")
        return
    combined = pd.concat(dfs, ignore_index=True).dropna()
    labels = combined['category'].unique()
    label_map = {label: idx for idx, label in enumerate(labels)}
    combined['label'] = combined['category'].map(label_map)

    # Dataset class
    class ExpenseDataset(Dataset):
        def __init__(self, texts, labels):
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
            self.texts = texts
            self.labels = labels

        def __len__(self):
            return len(self.texts)

        def __getitem__(self, idx):
            encoding = self.tokenizer(self.texts[idx], truncation=True, padding='max_length', max_length=128, return_tensors='pt')
            return {
                'input_ids': encoding['input_ids'].flatten(),
                'attention_mask': encoding['attention_mask'].flatten(),
                'labels': torch.tensor(self.labels[idx])
            }

    # Split
    train_texts, val_texts, train_labels, val_labels = train_test_split(combined['text'], combined['label'], test_size=0.2)
    train_ds = ExpenseDataset(train_texts.tolist(), train_labels.tolist())
    val_ds = ExpenseDataset(val_texts.tolist(), val_labels.tolist())
    train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=16)

    # Model
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(labels))
    optimizer = AdamW(model.parameters(), lr=2e-5)
    loss_fn = CrossEntropyLoss()

    # Train
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    for epoch in range(3):  # Few epochs for hackathon
        model.train()
        for batch in tqdm(train_loader):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            outputs = model(input_ids, attention_mask=attention_mask)
            loss = loss_fn(outputs.logits, labels)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
    # Save
    model.save_pretrained(os.path.join(MODELS_DIR, 'category_model'))
    with open(os.path.join(MODELS_DIR, 'label_map.pkl'), 'wb') as f:
        joblib.dump(label_map, f)
    print("Categorization model trained and saved.")

# 3. Train Anomaly Model (IsolationForest on combined fraud data)
def train_anomaly():
    # Load and combine (assume CSVs with numerical features like 'amount', 'time', etc.; unsupervised)
    anomaly_files = [
        'bank-transaction-dataset-for-fraud-detection/transactions.csv',
        'financial-anomaly-data/data.csv',
        'creditcardfraud/creditcard.csv'  # Adjust
    ]
    dfs = []
    for file in anomaly_files:
        path = os.path.join(DATA_DIR, file)
        if os.path.exists(path):
            df = pd.read_csv(path)
            # Select numerical features (e.g., 'amount')
            num_cols = df.select_dtypes(include=np.number).columns
            dfs.append(df[num_cols])
    if not dfs:
        print("No anomaly data found; skipping.")
        return
    combined = pd.concat(dfs, ignore_index=True).fillna(0)

    # Train IsolationForest
    model = IsolationForest(contamination=0.01, random_state=42)  # Assume 1% anomalies
    model.fit(combined)
    joblib.dump(model, os.path.join(MODELS_DIR, 'anomaly_model.pkl'))
    print("Anomaly model trained and saved.")

if __name__ == "__main__":
    evaluate_ocr()  # Test OCR on datasets
    train_categorization()
    train_anomaly()