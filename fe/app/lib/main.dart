import 'package:flutter/material.dart';

import 'paint.dart';
import 'result.dart';
import 'welcome.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      initialRoute: '/paint',
      routes: {
        '/welcome': (context) => WelcomePage(),
        '/paint': (context) => ClockPaint(),
        '/result': (context) => ResultPage(),
      },
    );
  }
}