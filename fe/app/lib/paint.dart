import 'dart:io';
import 'dart:typed_data';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';

class ClockPaint extends StatefulWidget {
  const ClockPaint({super.key});

  @override
  State<ClockPaint> createState() => _PaintState();
}

class _PaintState extends State<ClockPaint> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(''),
      ),
      body: Center(
        child: DrawingScreen(),
      ),
    );
  }
}

class DrawingScreen extends StatefulWidget {
  const DrawingScreen({super.key});

  @override
  State<DrawingScreen> createState() => _DrawingScreenState();
}

class _DrawingScreenState extends State<DrawingScreen> {
  final GlobalKey _repaintBoundaryKey = GlobalKey();
  List<Offset?> points = [];
  int _step = 1;

  String get _instruction {
    switch (_step) {
      case 1:
        return '1단계: 시계 테두리를 그려주세요';
      case 2:
        return '2단계: 시계 숫자를 그려주세요';
      case 3:
        return '3단계: 시침을 그려주세요';
      case 4:
        return '4단계: 분침을 그려주세요';
      default:
        return '';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        Text(
          _instruction,
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        Container(
          width: 400,
          height: 400,
          decoration: BoxDecoration(
            border: Border.all(
              color: Colors.black,
              width: 2.0,
            ),
          ),
          child: Stack(
            children: [
              RepaintBoundary(
                key: _repaintBoundaryKey,
                child: CustomPaint(
                  painter: DrawingPainter(points),
                  child: Container(),
                ),
              ),
              Positioned.fill(
                child: GestureDetector(
                  onPanUpdate: (details) {
                    RenderBox renderBox = _repaintBoundaryKey.currentContext!
                        .findRenderObject() as RenderBox;
                    setState(() {
                      points
                          .add(renderBox.globalToLocal(details.globalPosition));
                    });
                  },
                  onPanEnd: (details) {
                    points.add(null);
                  },
                ),
              ),
            ],
          ),
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            if (_step == 4)
              IconButton(
                icon: Icon(Icons.save),
                onPressed: () async {
                  await _saveToFile();
                  Navigator.of(context).pushNamed('/result');
                },
              ),
            if (_step < 4)
              IconButton(
                icon: Icon(Icons.navigate_next),
                onPressed: () async {
                  await _saveToFile();
                  setState(() {
                    if (_step < 4) _step++;
                  });
                },
              ),
            IconButton(
              icon: Icon(Icons.clear),
              onPressed: () {
                setState(() {
                  if (_step != 1) _step = 1;
                });
                points.clear();
              },
            ),
          ],
        ),
      ],
    );
  }

  Future<void> _saveToFile() async {
    final RenderRepaintBoundary boundary = _repaintBoundaryKey.currentContext!
        .findRenderObject() as RenderRepaintBoundary;
    final ui.Image originalImage = await boundary.toImage();

    final width = originalImage.width.toDouble();
    final height = originalImage.height.toDouble();

    final recorder = ui.PictureRecorder();
    final canvas =
        Canvas(recorder, Rect.fromPoints(Offset(0, 0), Offset(400, 400)));

    final paint = Paint();
    canvas.drawImageRect(
      originalImage,
      Rect.fromLTWH(0, 0, width, height),
      Rect.fromLTWH(0, 0, 400, 400),
      paint,
    );

    final picture = recorder.endRecording();
    final resizedImage = await picture.toImage(400, 400);

    final ByteData? byteData =
        await resizedImage.toByteData(format: ui.ImageByteFormat.png);
    final Uint8List imageBytes = byteData!.buffer.asUint8List();

    final directory = await getApplicationDocumentsDirectory();
    final imagePath = '${directory.path}/step$_step.png';
    final file = File(imagePath);

    await file.writeAsBytes(imageBytes);
    print('Image saved to $imagePath');

    if (await Permission.storage.request().isGranted) {
      print('Permission granted');
    } else {
      print('Permission denied');
    }
  }
}

class DrawingPainter extends CustomPainter {
  final List<Offset?> points;

  DrawingPainter(this.points);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.black
      ..strokeCap = StrokeCap.round
      ..strokeWidth = 5.0;

    final backgroundPaint = Paint()
    ..color = Colors.white
    ..style = PaintingStyle.fill;
    canvas.drawRect(Rect.fromLTWH(0, 0, size.width, size.height), backgroundPaint);

    for (int i = 0; i < points.length - 1; i++) {
      if (points[i] != null && points[i + 1] != null) {
        canvas.drawLine(points[i]!, points[i + 1]!, paint);
      } else if (points[i] != null && points[i + 1] == null) {
        canvas.drawPoints(ui.PointMode.points, [points[i]!], paint);
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true;
  }
}
