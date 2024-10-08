import 'package:dio/dio.dart';
import 'package:flutter/material.dart';

class TalkPage extends StatefulWidget {
  const TalkPage({super.key});

  @override
  State<TalkPage> createState() => _TalkPageState();
}

class _TalkPageState extends State<TalkPage> {
  final Dio _dio = Dio();
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  List<Map<String, String>> _talks = [];
  String _inputText = '';
  bool _isLoading = false;

  Future<void> _fetchData() async {
    if (_inputText.isEmpty) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      // String url = 'http://10.0.2.2:8000/questiontest?query=$_inputText';
      String url = 'http://10.0.2.2:8000/question?query=$_inputText';
      final response = await _dio.get(
        url,
        options: Options(
          contentType: 'application/json',
        ),
      );

      if (response.statusCode == 200) {
        // Map<String, String> answer = {'bot': response.data['result']};
        Map<String, String> answer = {'bot': response.data['answer']};
        setState(() {
          _talks.add(answer);
          _scrollToBottom();
        });
      } else {
        throw Exception('Failed to load data');
      }
    } catch (e) {
      print('Error fetching data: $e');
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _onSubmit() {
    setState(() {
      _inputText = _controller.text;
      if (_inputText.isNotEmpty) {
        Map<String, String> input = {'user': _inputText};
        _talks.add(input);
        _fetchData();
      }
      _controller.clear(); // 텍스트 필드를 비움
    });
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.jumpTo(_scrollController.position.maxScrollExtent);
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
      ),
      body: Stack(
        children: [
          Column(
            children: [
              Expanded(
                child: ListView.builder(
                  controller: _scrollController,
                  padding: EdgeInsets.all(16.0),
                  itemCount: _talks.length,
                  itemBuilder: (context, index) {
                    final talk = _talks[index];
                    final key = talk.keys.first;

                    return ListTile(
                      title: Align(
                        alignment: key == 'user'
                            ? Alignment.centerRight
                            : Alignment.centerLeft,
                        child: Container(
                          padding: EdgeInsets.all(8.0),
                          decoration: BoxDecoration(
                            border: Border.all(
                              color: key == 'user' ? Colors.green : Colors.orange,
                              width: 2.0,
                              style: BorderStyle.solid,
                            ),
                            // color: key == 'user' ? Colors.green : Colors.orange,
                            borderRadius: BorderRadius.circular(10.0),
                          ),
                          child: Text(
                            talk.values.first,
                            style: TextStyle(fontSize: 16),
                          ),
                        ),
                      ),
                    );
                  },
                ),
              ),
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: _controller,
                        keyboardType: TextInputType.text,
                        decoration: InputDecoration(
                          labelText: '메세지를 입력하세요',
                          border: OutlineInputBorder(),
                        ),
                      ),
                    ),
                    SizedBox(width: 8),
                    ElevatedButton(
                      style: ButtonStyle(
                        backgroundColor:
                            MaterialStateProperty.all(Colors.blueAccent),
                        padding: MaterialStateProperty.all(
                            EdgeInsets.symmetric(horizontal: 16.0)),
                      ),
                      onPressed: _onSubmit,
                      child: Text(
                        '전송',
                        style: TextStyle(fontSize: 16, color: Colors.white),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          if (_isLoading)
            Container(
              color: Colors.black54,
              child: Center(
                child: CircularProgressIndicator(),
              ),
            )
        ],
      ),
    );
  }
}
