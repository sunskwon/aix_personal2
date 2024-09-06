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
      backgroundColor: Colors.white,
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
    double score = 0;
    String _instruction = '';
    double circularity = result['circularity'];
    double hour_angle = result['hour_angle'];
    double minute_angle = result['minute_angle'];

    score += circularity;

    if (result['bool_location']) {
      score += 1;
    }

    if (result['numbers'].length > 10) {
      score += 1;
    } else if (result['numbers'].length > 7) {
      score += 0.5;
    }

    if (hour_angle >= 315 && hour_angle <= 345) {
      score += 1;
    } else if (hour_angle > 300 && hour_angle < 360) {
      score += 0.5;
    }

    if (minute_angle >= 45 && minute_angle <= 75) {
      score += 1;
    } else if (minute_angle > 30 && minute_angle < 90) {
      score += 0.5;
    }

    if (score >= 4) {
      _instruction = '좋은 결과입니다.\n하지만 안전에 유의해서 운전 하세요.';
    } else if (score >= 3) {
      _instruction = '아슬아슬하지만 나쁘지 않습니다.\n 주의해서 운전하세요.';
    } else if (score >= 2) {
      _instruction = '피곤하거나 힘든 상황에서는\n운전을 삼가주시기 바랍니다.';
    } else {
      _instruction = '대중교통을 이용하셔서\n가까운 병원에 방문해보기를 권장합니다';
    }

    score *= 20;

    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        Text.rich(
          TextSpan(
            children: [
              TextSpan(
                text: '점수: ',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              TextSpan(
                text: '${score.toInt().toString()}점',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: score >= 80
                      ? Colors.green
                      : score >= 40
                          ? Colors.yellow
                          : Colors.red,
                ),
              )
            ],
          ),
        ),
        SizedBox(
          height: 10,
        ),
        Text(
          _instruction,
          textAlign: TextAlign.center,
        ),
        SizedBox(
          height: 20,
        ),
        Text('테두리: ${result['circularity'].toInt() * 20 ?? 0}점'),
        Text('12의 위치: ${result['bool_location'] ? 20 : 0}점'),
        Text(
            '입력된 숫자: ${result['numbers'].length > 10 ? 20 : result['numbers'].length > 7 ? 10 : 0}점'),
        Text('[${result['numbers'].join(', ') ?? '없음'}]'),
        Text(
            '시침의 방향: ${result['hour_angle'] >= 315 && result['hour_angle'] <= 345 ? 20 : result['hour_angle'] > 300 && result['hour_angle'] < 360 ? 10 : 0}점'),
        Text(
            '분침의 방향: ${result['minute_angle'] >= 45 && result['minute_angle'] <= 75 ? 20 : result['minute_angle'] > 30 && result['minute_angle'] < 90 ? 10 : 0}점'),
      ],
    );
  }
}
