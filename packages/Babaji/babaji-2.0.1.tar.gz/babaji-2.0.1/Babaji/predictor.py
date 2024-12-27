import pickle
import requests
from io import BytesIO

class HeightPredictor:
    def __init__(self):
        """
        Initializes the predictor by loading the scaler and model from GitHub URLs.
        """
        # GitHub raw URLs for scaler and model
        self.scaler_url = 'https://raw.githubusercontent.com/PyBabaji/Babaji_Weight_height/main/Scalar.pkl'
        self.model_url = 'https://raw.githubusercontent.com/PyBabaji/Babaji_Weight_height/main/Regrassor.pkl'

        # Load the scaler from GitHub
        self.scaler = self.load_model_from_url(self.scaler_url)

        # Load the model from GitHub
        self.model = self.load_model_from_url(self.model_url)

    def load_model_from_url(self, url):
        """
        Loads a model from a given GitHub raw URL.
        """
        print(f"Loading model from {url}...")
        response = requests.get(url)
        
        if response.status_code == 200:
            model = pickle.load(BytesIO(response.content))
            return model
        else:
            raise Exception(f"Failed to download the model from {url}. Status code: {response.status_code}")

    def predict(self, weight):
        """
        Predicts the height for the given weight using the loaded model.
        """
        # Scale the input weight
        scaled_weight = self.scaler.transform([[weight]])[0][0]

        # Predict the height using the model
        predicted_height = self.model.predict([[scaled_weight]])[0]

        return predicted_height


class DiabeticPredictor:
    def __init__(self):
        """
        Initializes the diabetic predictor by loading the model from GitHub URL.
        """
        # GitHub raw URL for the model
        self.model_url = 'https://raw.githubusercontent.com/Nachiket858/ML_Projects/main/2.Diabetes_Prediction/Models/svc_classifire.pkl'

        # Load the model from GitHub
        self.model = self.load_model_from_url(self.model_url)

    def load_model_from_url(self, url):
        """
        Loads a model from a given GitHub raw URL.
        """
        print(f"Loading model from {url}...")
        response = requests.get(url)
        
        if response.status_code == 200:
            model = pickle.load(BytesIO(response.content))
            return model
        else:
            raise Exception(f"Failed to download the model from {url}. Status code: {response.status_code}")

    def predict(self, input_data):
        """
        Predicts the likelihood of diabetes based on the given input data.
        """
        # Ensure input_data is in the right format (e.g., a list of features)
        prediction = self.model.predict([input_data])[0]
        return prediction
