from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.preprocessing import LabelEncoder

# Load your dataset
ds = load_dataset('csv', data_files='e-commerce.csv')
print(ds)  # Print the dataset structure

# Split the dataset into train and test sets
ds = ds["train"].train_test_split(test_size=0.2)  # 80% train, 20% test

# Convert string labels to numerical values
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(ds['train']['label'])
ds['train'] = ds['train'].remove_columns(['label']).add_column('labels', labels)  # Remove old label column
test_labels = label_encoder.transform(ds['test']['label'])
ds['test'] = ds['test'].remove_columns(['label']).add_column('labels', test_labels)  # Remove old label column

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

# Apply tokenization to the dataset
tokenized_datasets = ds.map(tokenize_function, batched=True)

# Get number of unique labels
num_labels = len(label_encoder.classes_)

# Load the model
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=num_labels)

# Set training arguments
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",  # Updated from evaluation_strategy to eval_strategy
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Create a Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

# Train the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained("backend/models/my_model")
tokenizer.save_pretrained("backend/models/my_model")
# Save the label encoder
import pickle
with open("backend/models/my_model/label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)
