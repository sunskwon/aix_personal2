import 'dart:typed_data';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';

class ExamplePage extends StatelessWidget {
  const ExamplePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
      ),
      body: Center(
        child: ImageScreen(),
      ),
    );
  }
}

class ImageScreen extends StatefulWidget {
  const ImageScreen({super.key});

  @override
  State<ImageScreen> createState() => _ImageScreenState();
}

class _ImageScreenState extends State<ImageScreen> {
  String? imagePath;
  String? errorMessage;
  Map<String, dynamic>? _result;

  @override
  void initState() {
    super.initState();
    fetchImage();
  }

  Future<void> fetchImage() async {
    try {
      final response = await Dio().post(
        'http://10.0.2.2:8000/downloadtest/0-2',
        options: Options(responseType: ResponseType.bytes),
      );

      if (response.statusCode == 200) {
        final bytes = response.data as Uint8List;
        final filePath = await saveImageToFile(bytes);
        setState(() {
          imagePath = filePath;
        });
        await uploadImage(filePath);
      } else {
        setState(() {
          errorMessage = 'Error: ${response.data}';
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Error: $e';
      });
    }
  }

  Future<String> saveImageToFile(Uint8List bytes) async {
    final directory = await getTemporaryDirectory();
    final filePath = '${directory.path}/downloaded_image.png';
    final file = File(filePath);

    await file.writeAsBytes(bytes);
    return filePath;
  }

  Future<void> uploadImage(String filePath) async {
    final formData = FormData();
    if (File(filePath).existsSync()) {
      formData.files.add(
        MapEntry(
            'file',
            await MultipartFile.fromFile(filePath,
                filename: 'downloaded_image.png')),
      );
    }
    try {
      final response = await Dio().post(
        'http://10.0.2.2:8000/uploadfile',
        data: formData,
        options: Options(
          contentType: 'multipart/form-data',
        ),
      );

      if (response.statusCode == 200) {
        print(response.data);
        setState(() {
          _result = response.data;
        });
      } else {
        setState(() {
          errorMessage = 'Error: ${response.data}';
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Error: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: _result != null
            ? Column(
                children: [
                  Image.file(File(imagePath!)),
                  ResultDisplay(result: _result!),
                ],
              )
            : errorMessage != null
                ? Text(errorMessage!)
                : CircularProgressIndicator(),
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

    double shape_score = result['circularity'];
    double hour_angle = result['hour_angle'];
    double minute_angle = result['minute_angle'];

    double position_score = result['bool_location'] ? 1 : 0;
    double number_score = result['numbers'].length > 10
        ? 1
        : result['numbers'].length > 7
            ? 0.5
            : 0;
    double hour_score = hour_angle >= 315 && hour_angle <= 345
        ? 1
        : hour_angle > 300 && hour_angle < 360
            ? 0.5
            : 0;
    double minute_score = minute_angle >= 45 && minute_angle <= 75
        ? 1
        : minute_angle > 30 && minute_angle < 90
            ? 0.5
            : 0;

    score =
        shape_score + position_score + number_score + hour_score + minute_score;

    if (score >= 4) {
      _instruction = '좋은 결과입니다.\n하지만 안전에 주의해서 운전 하세요.';
    } else if (score >= 3) {
      _instruction = '아슬아슬하지만 나쁘지 않습니다.\n안전에 주의해서 운전하세요.';
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
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
        SizedBox(
          height: 20,
        ),
        Container(
          padding: EdgeInsets.all(10.0),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(10),
            border: Border.all(
              color: score >= 80
                  ? Colors.green
                  : score >= 40
                      ? Colors.yellow
                      : Colors.red,
              width: 2.0,
            ),
          ),
          child: Column(
            children: [
              Text(
                '세부 내용',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(
                height: 10,
              ),
              shape_score == 1.0
                  ? SizedBox()
                  : Text(
                      '시계 테두리가 원형이 되도록 신경써주세요',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w400,
                      ),
                    ),
              SizedBox(
                height: 5,
              ),
              position_score == 1
                  ? SizedBox()
                  : Text(
                      '숫자들이 제자리에 있는지 신경써주세요',
                      style: TextStyle(
                        fontSize: 14,
                      ),
                    ),
              SizedBox(
                height: 5,
              ),
              number_score == 1
                  ? SizedBox()
                  : Text(
                      '1부터 12까지 숫자들을 모두 작성했는지 신경써주세요',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w400,
                      ),
                    ),
              // Text(
              //   '${result['numbers'].length > 0 ? '(' + result['numbers'].join(', ') + ')' : ''}',
              //   style: TextStyle(
              //     fontSize: 10,
              //   ),
              // ),
              SizedBox(
                height: 5,
              ),
              hour_score == 1.0 && minute_score == 1.0
                  ? SizedBox()
                  : hour_angle == minute_angle
                      ? Text(
                          '시침과 분침이 11시 10분을 가리키는지 신경써주세요',
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w400,
                          ),
                        )
                      : Text(
                          '시침, 분침의 방향에 신경써주세요',
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w400,
                          ),
                        ),
            ],
          ),
        ),
        SizedBox(
          height: 10,
        ),
      ],
    );
  }
}
