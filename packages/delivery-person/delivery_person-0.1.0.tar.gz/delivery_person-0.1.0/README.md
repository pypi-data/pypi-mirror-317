# Delivery Person Detection

A Python package to detect whether an image contains a delivery person using a fine-tuned ResNet-50 model.

## Installation

You can install the package using `pip`:

```bash
pip install delivery-person
```
Note: Ensure that the delivery-person package is available on PyPI. If not, you can install it from the local directory as shown below.

# Installing from Local Directory
Clone the repository or download the package files.
Navigate to the package directory.
Run:

```bash
pip install .

```

# Usage
```bash
from delivery_person import DeliveryPersonDetector

# Initialize the detector
detector = DeliveryPersonDetector(
    model_path='path/to/fine_tuned_resnet50_1.pth',
    threshold=0.985,  # Optional: Set your desired threshold (default is 0.985)
    device='cuda'  # Optional: 'cpu' or 'cuda' (default is auto-detected)
)

# Predict on an image
image_path = 'path/to/image.jpg'
predicted_label, predicted_prob = detector.predict_image(image_path)

print(f"Predicted Label: {predicted_label}")
print(f"Confidence: {predicted_prob:.2f}%")
```
