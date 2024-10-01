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
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
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
  bool isDrawing = true;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          Container(
            width: 400,
            padding: EdgeInsets.all(10.0),
            child: Text.rich(
              TextSpan(
                text: '11시 10분',
                style: TextStyle(fontSize: 36, fontWeight: FontWeight.bold),
                children: [
                  TextSpan(
                    text: '을 가리키는\n',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  TextSpan(
                    text: '시계',
                    style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: Colors.blueAccent),
                  ),
                  TextSpan(
                    text: '를 그려주세요',
                    style: TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          ),
          SizedBox(
            height: 10,
          ),
          Container(
            width: 400,
            height: 500,
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
                        points.add(
                            renderBox.globalToLocal(details.globalPosition));
                      });
                    },
                    onPanEnd: (details) {
                      points.add(null);
                    },
                  ),
                ),
                // Positioned(
                //   bottom: 10,
                //   right: 80,
                //   child: FloatingActionButton(
                //     child: Icon(isDrawing ? Icons.draw : Icons.check),
                //     backgroundColor: Colors.black,
                //     shape: RoundedRectangleBorder(
                //       borderRadius: BorderRadius.circular(40),
                //     ),
                //     onPressed: () {
                //       setState(() {
                //         isDrawing = !isDrawing;
                //       });
                //     },
                //   ),
                // ),
                // Positioned(
                //   bottom: 10,
                //   right: 10,
                //   child: FloatingActionButton(
                //     child: Icon(Icons.phonelink_erase),
                //     backgroundColor: Colors.black,
                //     shape: RoundedRectangleBorder(
                //       borderRadius: BorderRadius.circular(40),
                //     ),
                //     onPressed: () {
                //       setState(() {
                //         if (isDrawing) {
                //           points.clear();
                //         } else {
                //           if (points.isNotEmpty) {
                //             points.removeLast();
                //           }
                //         }
                //       });
                //     },
                //   ),
                // ),
              ],
            ),
          ),
          SizedBox(
            height: 20,
          ),
          Container(
            width: 400,
            padding: EdgeInsets.all(10.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  style: ButtonStyle(
                    backgroundColor:
                        MaterialStateProperty.all(Colors.blueAccent),
                    padding: MaterialStateProperty.all(EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 5,
                    )),
                  ),
                  onPressed: () async {
                    await _saveToFile();
                    Navigator.of(context).pushReplacementNamed('/result');
                  },
                  child: Text(
                    '결과 확인',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                ),
                SizedBox(
                  width: 20,
                ),
                ElevatedButton(
                  style: ButtonStyle(
                    backgroundColor: MaterialStateProperty.all(Colors.white),
                    padding: MaterialStateProperty.all(
                      EdgeInsets.symmetric(
                        horizontal: 10,
                        vertical: 5,
                      ),
                    ),
                    side: MaterialStateProperty.all(
                      BorderSide(
                        color: Colors.blueAccent,
                        width: 2.0,
                      ),
                    ),
                  ),
                  onPressed: () {
                    points.clear();
                    setState(() {

                    });
                  },
                  child: Text(
                    '초기화',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.blueAccent,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
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
      Rect.fromLTWH(0, 0, 400, 500),
      paint,
    );

    final picture = recorder.endRecording();
    final resizedImage = await picture.toImage(400, 400);

    final ByteData? byteData =
        await resizedImage.toByteData(format: ui.ImageByteFormat.png);
    final Uint8List imageBytes = byteData!.buffer.asUint8List();

    final directory = await getApplicationDocumentsDirectory();
    final imagePath = '${directory.path}/clock.png';
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
      ..strokeWidth = 3.0;

    final backgroundPaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.fill;
    canvas.drawRect(
        Rect.fromLTWH(0, 0, size.width, size.height), backgroundPaint);

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
