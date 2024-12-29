from safetensors import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

from bad_code.lstm_cb import tokenizer, model


class BERTBOT:
    def predict(self, user_input):
        inputs = tokenizer(user_input, return_tensors="pt", padding=True, truncation=True)
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=-1)

        # Map the predicted label to a tag
        predicted_tag = id_to_tag[prediction.item()]

        # Return the response based on the predicted tag
        tag_responses = dict(zip(greetings_data['tag'], greetings_data['response']))
        return tag_responses.get(predicted_tag, "Sorry, I didn't understand that.")


        # Test the chatbot
        user_input = "Good morning!"
        print(get_response(user_input))  # Expected output: "Good morning! How can I assist?"

        user_input = "How are you?"
        print(get_response(user_input))  # Expected output: "I'm doing well! How about you?"

    def train(self):
        import torch

        # Define the dataset with patterns (greetings), tags, and responses
        greetings_data = {
            "input": [
                "Good morning!", "Hi, there!", "Hello!", "Good evening!", "How are you?",
                "Hey!", "Greetings!", "What's up?", "Good day!", "Salutations!"
            ],
            "tag": [
                "morning_greeting", "casual_greeting", "casual_greeting", "evening_greeting", "casual_greeting",
                "casual_greeting", "casual_greeting", "casual_greeting", "morning_greeting", "casual_greeting"
            ],
            "response": [
                "Good morning! How can I assist?", "Hey! What's up?", "Hi! How can I help you?",
                "Good evening! How are you?", "I'm doing well! How about you?", "Hey! How can I assist?",
                "Greetings! How may I help?", "What's going on?", "Good day! How can I help?",
                "Salutations! How can I be of service?"
            ]
        }

        # Convert to Dataset object
        dataset = Dataset.from_dict(greetings_data)

        # Tokenizer
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        # Tokenize the data_gen
        def tokenize_function(examples):
            return tokenizer(examples['input'], padding="max_length", truncation=True)

        tokenized_datasets = dataset.map(tokenize_function, batched=True)

        # Encode the tags into numerical labels
        tag_to_id = {tag: idx for idx, tag in enumerate(set(greetings_data['tag']))}
        id_to_tag = {idx: tag for tag, idx in tag_to_id.items()}
        dataset = dataset.add_column("labels", [tag_to_id[tag] for tag in greetings_data['tag']])

        # Define BERT model for sequence classification
        model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(tag_to_id))

        # Training arguments
        training_args = TrainingArguments(
            output_dir='./results',
            num_train_epochs=3,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
        )

        # Trainer for fine-tuning
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_datasets,
        )

        # Train the model
        trainer.train()
