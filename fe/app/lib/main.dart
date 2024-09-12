import 'package:flutter/material.dart';

import 'paint.dart';
import 'result.dart';
import 'select.dart';
import 'talk.dart';
import 'welcome.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      initialRoute: '/welcome',
      routes: {
        '/welcome': (context) => WelcomePage(),
        '/select': (context) => SelectPage(),
        '/paint': (context) => ClockPaint(),
        '/result': (context) => ResultPage(),
        '/talk': (context) => TalkPage(),
      },
    );
  }
}