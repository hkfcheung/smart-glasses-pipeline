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
  Future<void> sendBLEData(String value) async {
    final uri = Uri.parse("http://10.0.0.32:5000/ingest"); // Replace with your Mac's IP

    try {
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'ble_payload': value}),
      );
      print("Server response: ${response.body}");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Sent: $value")),
      );
    } catch (e) {
      print("Failed to send BLE data: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Failed to send data")),
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
            sendBLEData("simulated-payload-from-simulator");
          },
          child: const Text("Send Simulated BLE Payload"),
        ),
      ),
    );
  }
}
