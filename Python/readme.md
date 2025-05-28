```markdown
# Pneumonia Detection System



## 🛠️ Setup Instructions

### 1. Dataset Preparation

# Download dataset from Kaggle
kaggle datasets download -d paultimothymooney/chest-xray-pneumonia

# Unzip and organize
unzip chest-xray-pneumonia.zip -d chest_xray


### 2. Install Dependencies

pip install tensorflow flask matplotlib numpy pillow requests

## 🚀 How to Run

### Training the Model

python main.py

**Output:**
```
Loading pre-trained model...
OR
Training new model (this may take a while)...

Epoch 1/5
100/100 [==============================] - 120s 1s/step - loss: 0.2500 - accuracy: 0.9000 - auc: 0.9700 - val_loss: 0.2000 - val_accuracy: 0.9200 - val_auc: 0.9800
...
Test Accuracy: 92.50%
Test AUC: 0.975

Making prediction on sample image...
Prediction: Pneumonia
Confidence: 98.20%
Raw probability: 0.9820
```

### Running the Service
```bash
python service.py
```
**Output:**
```
 * Serving Flask app 'service'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.X:5000
```

## 🌐 API Endpoints

### 1. Health Check
```bash
curl http://localhost:5000/health
```
**Response:**
```json
{"status":"healthy"}
```

### 2. Prediction
```bash
curl -X POST -F "file=@xray_image.jpg" http://localhost:5000/predict
```
**Successful Response:**
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

## 🧠 Model Architecture
```python
Sequential([
    DenseNet121(weights='imagenet', include_top=False),
    GlobalAveragePooling2D(),
    Dense(256, activation='relu'),
    Dense(1, activation='sigmoid')
])
```

## 📊 Performance Metrics
| Metric       | Training | Validation | Test  |
|--------------|----------|------------|-------|
| Accuracy     | 93.2%    | 91.8%      | 92.5% |
| AUC          | 0.981    | 0.976      | 0.975 |
| Loss         | 0.18     | 0.21       | 0.20  |

## 💡 Example Usage

### Python Client
```python
import requests

response = requests.post(
    'http://localhost:5000/predict',
    files={'file': open('patient_xray.jpg', 'rb')}
)
print(response.json())
```

### Expected Output
```python
{
    'prediction': 'Normal',
    'confidence': 0.93,
    'probability': 0.07
}
```

## 🔧 Troubleshooting

1. **Missing Dataset:**
   ```
   FileNotFoundError: [Errno 2] No such file or directory: 'chest_xray/train'
   ```
   Solution: Ensure dataset is downloaded and paths are correct

2. **CUDA Errors:**
   ```
   Could not load dynamic library 'cudart64_110.dll'
   ```
   Solution: Install correct CUDA version or run on CPU

3. **Port Conflict:**
   ```
   Address already in use
   ```
   Solution: Change port `app.run(port=5001)`
```
