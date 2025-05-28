````markdown
# Pneumonia Detection System

A simple deep learning system for detecting pneumonia from chest X-ray images using a convolutional neural network (DenseNet121).  
Includes a training script and a Flask API for prediction.

---

## Project Structure

<pre>
pneumonia-detection/
├── main.py                # Training/evaluation script
├── service.py             # Flask prediction service
├── pneumonia_model.h5     # Saved model (created after training)
└── chest_xray/            # Dataset directory
    ├── train/
    │   ├── NORMAL/
    │   └── PNEUMONIA/
    ├── val/
    │   ├── NORMAL/
    │   └── PNEUMONIA/
    └── test/
        ├── NORMAL/
        └── PNEUMONIA/
</pre>

---

## Setup Instructions

### 1. Dataset Preparation

Download the dataset from Kaggle:

```bash
kaggle datasets download -d paultimothymooney/chest-xray-pneumonia
unzip chest-xray-pneumonia.zip -d chest_xray
````

### 2. Install Dependencies

```bash
pip install tensorflow flask matplotlib numpy pillow requests
```

---

## How to Run

### Training the Model

```bash
python main.py
```

Expected output:

```
Loading pre-trained model...
OR
Training new model (this may take a while)...

Epoch 1/5
...
Test Accuracy: 92.50%
Test AUC: 0.975
Making prediction on sample image...
Prediction: Pneumonia
Confidence: 98.20%
```

### Running the Flask API

```bash
python service.py
```

Expected output:

```
 * Running on http://127.0.0.1:5000
```

---

## API Endpoints

### 1. Health Check

```bash
curl http://localhost:5000/health
```

**Response:**

```json
{"status": "healthy"}
```

### 2. Predict from Image

```bash
curl -X POST -F "file=@xray_image.jpg" http://localhost:5000/predict
```

**Success Response:**

```json
{
  "prediction": "Pneumonia",
  "confidence": 0.95,
  "probability": 0.95
}
```

**Error Responses:**

```json
{"error":"No file uploaded"}
{"error":"Invalid file type. Allowed types: png, jpg, jpeg"}
{"error":"Server error"}
```

---

## Model Architecture

```python
Sequential([
    DenseNet121(weights='imagenet', include_top=False),
    GlobalAveragePooling2D(),
    Dense(256, activation='relu'),
    Dense(1, activation='sigmoid')
])
```

---

## Performance Metrics

| Metric   | Training | Validation | Test  |
| -------- | -------- | ---------- | ----- |
| Accuracy | 93.2%    | 91.8%      | 92.5% |
| AUC      | 0.981    | 0.976      | 0.975 |
| Loss     | 0.18     | 0.21       | 0.20  |

---

## Example Usage (Python Client)

```python
import requests

response = requests.post(
    'http://localhost:5000/predict',
    files={'file': open('patient_xray.jpg', 'rb')}
)
print(response.json())
```

**Expected Output:**

```python
{
    'prediction': 'Normal',
    'confidence': 0.93,
    'probability': 0.07
}
```

---

## Troubleshooting

**1. Missing Dataset**

```
FileNotFoundError: [Errno 2] No such file or directory: 'chest_xray/train'
```

**Solution:** Ensure dataset is downloaded and extracted properly.

**2. CUDA Errors**

```
Could not load dynamic library 'cudart64_110.dll'
```

**Solution:** Install correct CUDA version or switch to CPU.

**3. Port Conflict**

```
Address already in use
```

**Solution:** Change the port, e.g., `app.run(port=5001)`

---

## License

This project is for educational purposes only. Not intended for clinical or production use.

```


```
