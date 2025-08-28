# # chatbot/logic.py
# import os
# import pandas as pd
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

# class Chatbot:
#     def __init__(self, dataset_path=None):
#         """
#         Initialize the chatbot with sentence embeddings.
#         """
#         if dataset_path is None:
#             # Default path: same folder as logic.py
#             dataset_path = os.path.join(os.path.dirname(__file__), "chatbot_data.csv")

#         # Load dataset safely
#         if not os.path.isfile(dataset_path):
#             print(f"Warning: dataset not found at {dataset_path}. Using empty dataset.")
#             data = pd.DataFrame(columns=['question', 'answer'])
#         else:
#             try:
#                 data = pd.read_csv(dataset_path)
#                 # Ensure required columns exist
#                 if 'question' not in data.columns or 'answer' not in data.columns:
#                     raise ValueError("CSV must contain 'question' and 'answer' columns")
#             except Exception as e:
#                 print(f"Error loading dataset: {e}")
#                 data = pd.DataFrame(columns=['question', 'answer'])

#         # Convert to lists
#         self.questions = data['question'].astype(str).tolist()
#         self.answers = data['answer'].astype(str).tolist()

#         # Load pre-trained Sentence Transformer model
#         self.model = SentenceTransformer('all-MiniLM-L6-v2')

#         # Compute embeddings for all questions
#         if self.questions:
#             self.question_embeddings = self.model.encode(self.questions, convert_to_tensor=True)
#         else:
#             print("No questions found in dataset; chatbot will not respond correctly.")
#             self.question_embeddings = None

#     def get_response(self, user_input):
#         """
#         Get the most similar response for the user's input.
#         """
#         if not self.questions or self.question_embeddings is None:
#             return "Sorry, I have no data to answer yet."

#         if not user_input.strip():
#             return "Please say something so I can respond."

#         # Encode user input
#         user_embedding = self.model.encode([user_input], convert_to_tensor=True)

#         # Compute cosine similarity
#         similarity = cosine_similarity(user_embedding.cpu(), self.question_embeddings.cpu())
#         best_match_idx = similarity.argmax()
#         return self.answers[best_match_idx]

# # Initialize chatbot globally
# chatbot = Chatbot()






# chatbot/logic.py
import os
import pandas as pd
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier

def preprocess(text):
    """Lowercase and remove punctuation."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

class Chatbot:
    def __init__(self, dataset_path=None, k_neighbors=3):
        if dataset_path is None:
            dataset_path = os.path.join(os.path.dirname(__file__), "chatbot_data.csv")

        if not os.path.isfile(dataset_path):
            print(f"Warning: dataset not found at {dataset_path}. Using empty dataset.")
            data = pd.DataFrame(columns=['question', 'answer'])
        else:
            try:
                data = pd.read_csv(dataset_path)
                if 'question' not in data.columns or 'answer' not in data.columns:
                    raise ValueError("CSV must contain 'question' and 'answer' columns")
            except Exception as e:
                print(f"Error loading dataset: {e}")
                data = pd.DataFrame(columns=['question', 'answer'])

        # Map question -> list of possible answers
        self.qa_map = {}
        for _, row in data.iterrows():
            q = preprocess(str(row['question']))
            a = str(row['answer']).strip()
            if q in self.qa_map:
                self.qa_map[q].append(a)
            else:
                self.qa_map[q] = [a]

        self.questions = list(self.qa_map.keys())
        self.vectorizer = TfidfVectorizer()
        if self.questions:
            X = self.vectorizer.fit_transform(self.questions)
            y = list(range(len(self.questions)))  # label each question
            self.knn = KNeighborsClassifier(n_neighbors=k_neighbors)
            self.knn.fit(X, y)
        else:
            print("No questions found in dataset; chatbot will not respond correctly.")
            self.knn = None

    def get_response(self, user_input):
        if not self.questions or self.knn is None:
            return "Sorry, I have no data to answer yet."

        if not user_input.strip():
            return "Please say something so I can respond."

        user_input_processed = preprocess(user_input)
        user_vec = self.vectorizer.transform([user_input_processed])
        idx = self.knn.predict(user_vec)[0]  # get closest question index
        matched_question = self.questions[idx]
        possible_answers = self.qa_map.get(matched_question, ["Sorry, I have no answer."])
        return random.choice(possible_answers)

# Initialize chatbot globally
chatbot = Chatbot()
