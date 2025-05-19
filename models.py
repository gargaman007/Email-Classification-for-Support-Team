import pickle

import torch
import torch.nn as nn
from sentence_transformers import SentenceTransformer
from transformers import (AutoModelForTokenClassification, AutoTokenizer,
                          TokenClassificationPipeline)


class MLPClassifier(nn.Module):
    def __init__(self, input_dim, num_classes):
        super(MLPClassifier, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
    
    def forward(self, x):
        return self.model(x)

class ModelManager:
    def __init__(self):
        self.ner_model = None
        self.ner_tokenizer = None
        self.ner_pipeline = None
        self.classification_model = None
        self.label_encoder = None
        self.pca_model = None
        self.mlp_model = None

    def load_models(self):
        # Load NER model
        ner_model_name = "Davlan/bert-base-multilingual-cased-ner-hrl"
        self.ner_tokenizer = AutoTokenizer.from_pretrained("./model")
        self.ner_model = AutoModelForTokenClassification.from_pretrained("./model")
        self.ner_pipeline = TokenClassificationPipeline(
            model=self.ner_model.to('cpu'),
            tokenizer=self.ner_tokenizer,
            device=-1,
            aggregation_strategy="simple"
        )

        # Load classification models
        self.classification_model = SentenceTransformer('./sbert_model')
        
        with open("label_encoder.pkl", "rb") as f:
            self.label_encoder = pickle.load(f)
        
        with open("pca.pkl", "rb") as f:
            self.pca_model = pickle.load(f)
        
        model_state_dict = torch.load("mlp_model.pth", map_location=torch.device('cpu'))
        num_classes = len(self.label_encoder.classes_)
        input_dim = self.pca_model.n_components_
        
        self.mlp_model = MLPClassifier(input_dim, num_classes)
        self.mlp_model.load_state_dict(model_state_dict)
        self.mlp_model.eval()

    def predict(self, text):
        # Get embeddings and reduce dimensions
        email_embedding = self.classification_model.encode([text])
        email_reduced = self.pca_model.transform(email_embedding)
        email_tensor = torch.tensor(email_reduced, dtype=torch.float32)

        # Make prediction
        with torch.no_grad():
            output = self.mlp_model(email_tensor)
            predicted_class_index = torch.argmax(output, dim=1).item()
            predicted_category = self.label_encoder.inverse_transform([predicted_class_index])[0]

        return predicted_category 