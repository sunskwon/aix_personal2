import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';

class ResultPage extends StatefulWidget {
  const ResultPage({super.key});

  @override
  State<ResultPage> createState() => _ResultPageState();
}

class _ResultPageState extends State<ResultPage> {
  final Dio _dio = Dio();
  final String _uploadUrl = 'http://10.0.2.2:8000/uploadfile';
  Map<String, dynamic>? _result;

  @override
  void initState() {
    super.initState();
    _uploadImages();
  }

  Future<void> _uploadImages() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final filePaths = [
        '${directory.path}/step1.png',
        '${directory.path}/step2.png',
        '${directory.path}/step3.png',
        '${directory.path}/step4.png',
      ];

      final formData = FormData();

      for (int i = 0; i < filePaths.length; i++) {
        if (File(filePaths[i]).existsSync()) {
          formData.files.add(
            MapEntry(
                'files',
                await MultipartFile.fromFile(filePaths[i],
                    filename: 'step${i + 1}.png')),
          );
        }
      }

      final response = await _dio.post(
        _uploadUrl,
        data: formData,
        options: Options(
          contentType: 'multipart/form-data',
        ),
      );

      if (response.statusCode == 200) {
        setState(() {
          _result = response.data;
        });
        print('Upload successful: ${response.data}');
      } else {
        setState(() {
          _result = {'result': 'Something is wrong...'};
        });
        print('Upload failed with status code: ${response.statusCode}');
      }
    } catch (e) {
      setState(() {
        _result = {'result': 'An error has occured'};
      });
      print('Upload error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Upload Images'),
      ),
      body: Center(
        child: _result == null
            ? CircularProgressIndicator()
            : ResultDisplay(result: _result!),
      ),
    );
  }
}

class ResultDisplay extends StatelessWidget {
  final Map<String, dynamic> result;

  const ResultDisplay({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        Text('Circularity: ${result['circularity'] ?? '0'}'),
        Text('Numbers: ${result['number'].join(', ') ?? '0'}'),
        Text('Hour Angle: ${result['hour_angle'] ?? '0'}'),
        Text('Minute Angle: ${result['minute_angle'] ?? '0'}'),
      ],
    );
  }
}
