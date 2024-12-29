import numpy as np
import random
import json

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# from nltk_utils import bag_of_words, tokenize, stem
# from model import NeuralNet
from RFML.engines.supervised.NLP.labeled_classification.conversational_intelligence.models.FNN.model import NeuralNet
from RFML.engines.supervised.NLP.labeled_classification.conversational_intelligence.models.FNN.nltk_utils import \
    bag_of_words, tokenize, stem


class FNNBOTTrainer:
    @staticmethod
    def Train(intents, model: str, vector_db_path: str):
        import os
        import numpy as np
        import torch
        import torch.nn as nn
        from torch.utils.data import Dataset, DataLoader
        from sklearn.model_selection import train_test_split

        vector_data_path = os.path.join(vector_db_path, f"{model}.pth")

        all_words = []
        tags = []
        xy = []
        for intent in intents['intents']:
            tag = intent['tag']
            tags.append(tag)
            for pattern in intent['patterns']:
                w = tokenize(pattern)
                all_words.extend(w)
                xy.append((w, tag))

        ignore_words = ['?', '.', '!', ',', ';', ':']
        all_words = [stem(w.lower()) for w in all_words if w not in ignore_words]
        all_words = sorted(set(all_words))
        tags = sorted(set(tags))

        print(len(xy), "patterns")
        print(len(tags), "tags:", tags)
        print(len(all_words), "unique stemmed words:", all_words)

        X = []
        y = []
        for (pattern_sentence, tag) in xy:
            bag = bag_of_words(pattern_sentence, all_words)
            X.append(bag)
            y.append(tags.index(tag))

        X = np.array(X)
        y = np.array(y)

        # Split data_gen into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        class ChatDataset(Dataset):
            def __init__(self, data, labels):
                self.data = data
                self.labels = labels

            def __getitem__(self, index):
                return self.data[index], self.labels[index]

            def __len__(self):
                return len(self.data)

        train_dataset = ChatDataset(X_train, y_train)
        val_dataset = ChatDataset(X_val, y_val)
        train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, num_workers=0)
        val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, num_workers=0)

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        model = NeuralNet(len(X[0]), 16, len(tags)).to(device)

        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=100, gamma=0.9)

        best_loss = float('inf')
        for epoch in range(1000):
            model.train()
            for words, labels in train_loader:
                words, labels = words.to(device), labels.to(dtype=torch.long).to(device)
                optimizer.zero_grad()
                outputs = model(words)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
            scheduler.step()

            model.eval()
            val_loss = 0
            with torch.no_grad():
                for words, labels in val_loader:
                    words, labels = words.to(device), labels.to(dtype=torch.long).to(device)
                    outputs = model(words)
                    loss = criterion(outputs, labels)
                    val_loss += loss.item()

            val_loss /= len(val_loader)
            if (epoch + 1) % 100 == 0:
                print(f'Epoch [{epoch + 1}/1000], Loss: {loss.item():.4f}, Val Loss: {val_loss:.4f}')

            # Save the best model
            if val_loss < best_loss:
                best_loss = val_loss
                torch.save(model.state_dict(), vector_data_path)

        data = {
            "model_state": model.state_dict(),
            "input_size": len(X[0]),
            "hidden_size": 16,
            "output_size": len(tags),
            "all_words": all_words,
            "tags": tags
        }
        torch.save(data, vector_data_path)

        print(f'Training complete. Best validation loss: {best_loss:.4f}')
        return True, f"Model training was successful! (Best Val Loss: {best_loss:.4f})"

    @staticmethod
    def Train1111(intents, model: str, vector_db_path: str):
        # with open('intents.json', 'r') as f:
        #     intents = json.load(f)
        vector_data_path = rf"{vector_db_path}\{model}.pth"

        all_words = []
        tags = []
        xy = []
        # loop through each sentence in our intents patterns
        for intent in intents['intents']:
            tag = intent['tag']
            # add to tag list
            tags.append(tag)
            for pattern in intent['patterns']:
                # tokenize each word in the sentence
                w = tokenize(pattern)
                # add to our words list
                all_words.extend(w)
                # add to xy pair
                xy.append((w, tag))

        # stem and lower each word
        ignore_words = ['?', '.', '!']
        all_words = [stem(w) for w in all_words if w not in ignore_words]
        # remove duplicates and sort
        all_words = sorted(set(all_words))
        tags = sorted(set(tags))

        print(len(xy), "patterns")
        print(len(tags), "tags:", tags)
        print(len(all_words), "unique stemmed words:", all_words)

        # create training data_gen
        X_train = []
        y_train = []
        for (pattern_sentence, tag) in xy:
            # X: bag of words for each pattern_sentence
            bag = bag_of_words(pattern_sentence, all_words)
            X_train.append(bag)
            # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
            label = tags.index(tag)
            y_train.append(label)

        X_train = np.array(X_train)
        y_train = np.array(y_train)

        # Hyper-parameters
        num_epochs = 1000
        batch_size = 8
        learning_rate = 0.001
        input_size = len(X_train[0])
        hidden_size = 8
        output_size = len(tags)
        print(input_size, output_size)

        class ChatDataset(Dataset):

            def __init__(self):
                self.n_samples = len(X_train)
                self.x_data = X_train
                self.y_data = y_train

            # support indexing such that dataset[i] can be used to get i-th sample
            def __getitem__(self, index):
                return self.x_data[index], self.y_data[index]

            # we can call len(dataset) to return the size
            def __len__(self):
                return self.n_samples

        dataset = ChatDataset()
        train_loader = DataLoader(dataset=dataset,
                                  batch_size=batch_size,
                                  shuffle=True,
                                  num_workers=0)

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        model = NeuralNet(input_size, hidden_size, output_size).to(device)

        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        # Train the model
        for epoch in range(num_epochs):
            for (words, labels) in train_loader:
                words = words.to(device)
                labels = labels.to(dtype=torch.long).to(device)

                # Forward pass
                outputs = model(words)
                # if y would be one-hot, we must apply
                # labels = torch.max(labels, 1)[1]
                loss = criterion(outputs, labels)

                # Backward and optimize
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if (epoch + 1) % 100 == 0:
                print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

        print(f'final loss: {loss.item():.4f}')

        data = {
            "model_state": model.state_dict(),
            "input_size": input_size,
            "hidden_size": hidden_size,
            "output_size": output_size,
            "all_words": all_words,
            "tags": tags
        }

        FILE = vector_data_path  # "data_gen.pth"
        torch.save(data, FILE)

        print(f'Training complete. file saved to {FILE}')
        return True, f"Model training was successful! (Epoch: {num_epochs}, Loss: {loss.item()})"  # Success
