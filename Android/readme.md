```markdown
# Pneumonia Detection Android App

An Android application that detects pneumonia from chest X-ray images by communicating with a local Python prediction service.

## 📱 App Features
- Select X-ray images from device gallery
- Upload images to local prediction API
- Display diagnosis results with confidence percentage
- Clean Material Design 3 UI

## 🚀 Quick Start Guide

### 1. Prerequisites
- Android Studio (latest version)
- Python service running locally
- Android device/emulator (API level 24+)

### 2. Start the Python Service
```bash
# In your Python project directory
python service.py
```
*Service will run at:* `http://10.0.2.2:5000` (for emulator)  
*or* `http://<your-local-ip>:5000` (for physical device)

### 3. Configure Android Project

1. **Open in Android Studio:**
    - Select "Open an Existing Project"
    - Navigate to the project directory

2. **Update API URL (if needed):**
   In `RetrofitInstance.kt`:
   ```kotlin
   private const val BASE_URL = "http://10.0.2.2:5000/" // For emulator
   // OR for physical device testing:
   // private const val BASE_URL = "http://192.168.1.X:5000/" 
   ```

### 4. Build and Run
1. Connect your Android device or start an emulator
2. Click "Run" in Android Studio (▶️ button)
3. Select your target device

## 🌐 Network Configuration

### For Emulator:
- Use `http://10.0.2.2:5000` (special alias for localhost)
- No additional configuration needed

### For Physical Device:
1. Find your computer's local IP:
    - Windows: `ipconfig` (look for IPv4)
    - Mac/Linux: `ifconfig` or `ip a`

2. Update `RetrofitInstance.kt`:
   ```kotlin
   private const val BASE_URL = "http://192.168.1.X:5000/"
   ```

3. Ensure both devices are on the same network

## 🛠️ Troubleshooting

### Common Issues:
1. **Connection Failed:**
    - Verify Python service is running
    - Check Android's network permission:
      ```xml
      <uses-permission android:name="android.permission.INTERNET"/>
      ```

2. **Cleartext Traffic Blocked:**
   Add to `AndroidManifest.xml`:
   ```xml
   <application
       android:usesCleartextTraffic="true"
       ...>
   ```
   Or create `network_security_config.xml` (recommended):
   ```xml
   <network-security-config>
       <domain-config cleartextTrafficPermitted="true">
           <domain includeSubdomains="true">10.0.2.2</domain>
           <!-- Add your local IP if using physical device -->
       </domain-config>
   </network-security-config>
   ```

3. **CORS Errors:**
   In your Python service (`service.py`), add:
   ```python
   from flask_cors import CORS
   app = Flask(__name__)
   CORS(app)
   ```

## 🧑‍💻 Development Notes

### Key Components:
- **Retrofit**: For API communication
- **ActivityResultContracts**: Image selection
- **Material 3 Components**: Modern UI
- **ViewModel**: Lifecycle-aware data handling

### Testing with Sample Images:
Sample X-rays can be found in the Python project's `chest_xray/test/` directory.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```


