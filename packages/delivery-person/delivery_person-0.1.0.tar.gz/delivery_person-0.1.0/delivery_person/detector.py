# delivery_person/detector.py

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os

class DeliveryPersonDetector:
    def __init__(self, model_path, threshold=0.985, device=None):
        """
        Initializes the DeliveryPersonDetector.

        Args:
            model_path (str): Path to the fine-tuned ResNet-50 model weights (.pth file).
            threshold (float, optional): Confidence threshold for classifying as 'Delivery Person'. Defaults to 0.985.
            device (str, optional): Device to run the model on ('cpu' or 'cuda'). If None, automatically detects.
        """
        self.model_path = model_path
        self.threshold = threshold
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model()
        self.transform = self._get_transform()

    def _load_model(self):
        """Loads the ResNet-50 model with the fine-tuned weights."""
        try:
            model = models.resnet50(pretrained=False)
            num_ftrs = model.fc.in_features
            model.fc = nn.Linear(num_ftrs, 2)  # 2 classes: Delivery Person and Non-Delivery Person

            # Load the state_dict
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found at '{self.model_path}'. Please provide a valid path.")

            state_dict = torch.load(self.model_path, map_location=self.device)
            model.load_state_dict(state_dict)
            model.to(self.device)
            model.eval()
            print("Delivery person detection model loaded successfully.")
            return model
        except Exception as e:
            print(f"Error loading delivery person model: {e}")
            raise e

    def _get_transform(self):
        """Defines the image transformations."""
        return transforms.Compose([
            transforms.Resize((224, 224)),  # Resize to the input size expected by ResNet
            transforms.ToTensor(),  # Convert image to a PyTorch tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406],  # Normalize using ImageNet stats
                                 std=[0.229, 0.224, 0.225]),
        ])

    def predict_image(self, image_path):
        """
        Predicts whether the image contains a delivery person.

        Args:
            image_path (str): Path to the image file.

        Returns:
            tuple: (predicted_label (str), predicted_prob (float))
        """
        try:
            # Load and transform the image
            image = Image.open(image_path).convert('RGB')
            input_tensor = self.transform(image).unsqueeze(0)  # Add batch dimension
            input_tensor = input_tensor.to(self.device)

            # Make the prediction
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                delivery_prob = probabilities[0][0].item()  # Assuming class 0 is 'Delivery Person'
                non_delivery_prob = probabilities[0][1].item()

                print(f"Delivery Person Probability: {delivery_prob * 100:.2f}%")
                print(f"Non-Delivery Person Probability: {non_delivery_prob * 100:.2f}%")

                # Determine the predicted label
                if delivery_prob > non_delivery_prob:
                    predicted_label = 'Delivery Person'
                    predicted_prob = delivery_prob * 100  # Convert to percentage
                    if predicted_prob >= self.threshold * 100:
                        print("Prediction is confident as Delivery Person.")
                    else:
                        print("Prediction is below threshold. Classifying as Non-Delivery Person.")
                        predicted_label = 'Non-Delivery Person'
                        predicted_prob = non_delivery_prob * 100
                else:
                    predicted_label = 'Non-Delivery Person'
                    predicted_prob = non_delivery_prob * 100
                    print("Prediction is confident as Non-Delivery Person.")

                return predicted_label, predicted_prob

        except FileNotFoundError:
            print(f"Image file '{image_path}' not found.")
            return 'Non-Delivery Person', 0.0
        except Exception as e:
            print(f"Error during prediction: {e}")
            return 'Non-Delivery Person', 0.0
