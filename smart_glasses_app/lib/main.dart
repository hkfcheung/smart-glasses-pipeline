import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Glasses BLE (Mock)',
      home: const BLEMockPage(),
    );
  }
}

class BLEMockPage extends StatefulWidget {
  const BLEMockPage({super.key});

  @override
  State<BLEMockPage> createState() => _BLEMockPageState();
}

class _BLEMockPageState extends State<BLEMockPage> {
  Future<void> sendBLEData() async {
    final uri = Uri.parse("http://10.0.0.32:5000/ingest");  // Replace with your actual backend IP if needed

    final payload = {
      "modality": "multi",
      "audio": {
        "raw_text": "Turn off the kitchen light",
        "language": "en-US"
      },
      "vision": {
        "objects": ["person", "light switch", "kitchen"],
        "snapshot_id": "frame_00123"
      },
      "device_id": "ESP32-CAM-01",
      "timestamp": DateTime.now().toUtc().toIso8601String()
    };

    try {
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(payload),
      );
      print("Server response: ${response.body}");

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Data sent!')),
      );
    } catch (e) {
      print("Failed to send BLE data: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to send data')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Simulated BLE Payload")),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            sendBLEData(); // ✅ fixed: no arguments
          },
          child: const Text("Send Simulated BLE Payload"),
        ),
      ),
    );
  }
}
