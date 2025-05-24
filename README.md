# Smart Glasses BLE Pipeline

This project simulates a BLE data flow from a Flutter iOS app to a Flask backend that calls LLaMA4 to generate dynamic ciphers.

## 📦 Components

- `smart_glasses_app/`: Flutter iOS app that sends BLE payloads (mocked in simulator)
- `smart_glasses_backend/`: Flask API that receives BLE data and sends it to a LLaMA4 model
- `flutter.puml`: PlantUML diagram for system architecture

## 🚀 Quickstart

### Backend Setup (Flask + LLaMA)

```bash
cd smart_glasses_backend
python3 -m venv venv
source venv/bin/activate
pip install flask requests
python app.py
