


## Snippet Converter
* お遊びで作ったコードをスニペット形式に変換してくれるプログラムです。


### `snippet_converter.py`:
* ファイルのパスを受け取り、スニペットの`body`形式に変換します。
* 変換後のスニペットはクリップボードにコピーされます。

### 使用方法
1. `snippet_converter.py`を実行します。
```bash
python snippet_converter.py
```
2. ファイル名を入力します。
```Plain Text
Welcome to the Snippet Converter!
スニペットのbodyを作成します。
Please enter the file name to convert:
> File name: hogehoge.py
```


1. スニペットのプレビューが表示され、変換されたスニペットがクリップボードにコピーされます。

```Plain Text
✅ Snippet converted and copied to clipboard successfully!

Preview of the snippet:
[
"# //////////////////////////////////////////////////",
"",
"\"\"\"debug print\"\"\"",
"def dprint(*args, end: str = \"\\n\") -> None:",
"    import sys",
"    \"\"\"",
"    標準エラー出力する debug print.",
"    引数はprint()と同等.",
"    AtcoderののJudgeでは標準エラー出力はスルーされる.",
"    \"\"\"",
"    print(*args, end=end, file=sys.stderr)",
"",
"# //////////////////////////////////////////////////"
]

You can now paste the snippet in your VSCode user snippets file.
スニペットの変換に成功しました！
変換された"[body]"はクリップボードにコピーされました。
スニペットを VSCode のユーザースニペットファイルに貼り付けることができます。
```

### 使用するライブラリ
* `pyperclip` - クリップボード操作のためのライブラリ
* `os` - ファイルシステム操作のための標準ライブラリ
* `re` - 正規表現操作のための標準ライブラリ

* インストール方法
    * 依存関係をインストールするには、以下のコマンドを実行してください：

```bash
pip install pyperclip
```
