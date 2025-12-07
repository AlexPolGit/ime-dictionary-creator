# IME辞書作成道具 (IME Dictionary Creator)

## 概要
IME辞書をプログラム的に作成するための様々な道具。

## 使用方法

### 一般的な使い方
どんな辞書もいくつかの一般的なプロトコルを持っています。

- コンストラクタの用例：
```py
# これは辞書の一番簡単な初期化。「name」というフィールドは必須。
dictionary = Dictionary(name="使用例の辞書")

# 任意の保存パスを設定したい場合は「save_path」を使用してください。デフォルトは実行されているプログラムと同じパス。pathlibのPathを使ってください。
dictionary2 = Dictionary(name="使用例の辞書その2", save_path=Path("jisho/custom"))
```

- `add_entry()`：新規の行(単語)を辞書に追加する。用例：
```py
# 新規の辞書を作成する。
dictionary = Dictionary(name="使用例の辞書")

# 一番簡単な単語の追加方法。
dictionary.add_entry("ことば", "言葉")

# 品詞を含む単語の追加方法。デフォルトは「名詞」。
dictionary.add_entry("さとう", "佐藤さん", pos="人名")

# コメントを含む単語の追加方法。デフォルトはコメントなし。
dictionary.add_entry("をたく", "ヲタク", comment="より一般的な書き方")
```

- `add_comment()`：新規のコメントを辞書に追加する。コメントは登録時に追加されません。用例：
```py
# 新規の辞書を作成する。
dictionary = Dictionary(name="使用例の辞書")

# コメントを辞書に追加する。
dictionary.add_comment("これはコメント！")
```

- `save_to_file()`：辞書の内容をファイルに保存する。用例：
```py
# 新規の辞書を作成して適当な内容を追加する。
dictionary = Dictionary(name="使用例の辞書")
dictionary.add_entry("ことば", "言葉")
dictionary.add_comment("これはコメント！")

# ファイルに保存する。
# ファイル名は「使用例の辞書」になってファイル拡張子は辞書の種類によります。
dictionary.save_to_file()
```

- `get_entries()`：辞書の行とコメントを全て取り出す。用例：
```py
# 新規の辞書を作成して適当な内容を追加する。
dictionary = Dictionary(name="使用例の辞書")
dictionary.add_entry("ことば", "言葉")
dictionary.add_comment("これはコメント！")

# 行とコメントを取り出して内容をプリントする。
entries = dictionary.get_entries()
print(len(entries)) # 2
print(entries[0].word) # 言葉
print(entries[0].reading) # ことば
print(entries[1].content) # これはコメント！
```

- `from_file()`：既存の辞書ファイルから辞書を作成する。用例：
```py
# 既存のファイルお開いて内容を読み込む。
# 名前(とファイル名)を編集したい場合は「name」という任意のフィールドを使ってください。
dictionary = Dictionary.from_file(Path("使用例の辞書.txt"))

# 新しい単語を追加する。
dictionary.add_entry("はんたーはんたー", "HUNTER×HUNTER")

# 既存と新規の内容を保存する。
dictionary.save_to_file()
```

### Microsoft IMEテキスト辞書 (Microsoft IME Text Dictionary)
Microsoft IMEなどに登録(インポート)できるテキスト辞書を作成する方法：

1. `MicrosoftImeDictionary`を名前を付けてインスタンス化する：
```py
dictionary = MicrosoftImeDictionary(name="MicrosoftIME辞書")
```

2. 内容を追加する：
```py
dictionary = Dictionary(name="MicrosoftIME辞書")
dictionary.add_entry("ことば", "言葉")
dictionary.add_entry("さとう", "佐藤さん", pos="人名", comment="私の友人")
dictionary.add_comment("これはコメント")
```

3. ファイルに保存する：
```py
dictionary.save_to_file()
```
出力されるファイル名は「MicrosoftIME辞書.txt」。その内容は下記通り：
```txt
ことば	言葉	名詞
さとう	佐藤さん	人名    私の友人
!これはコメント
```

4. Microsoft IMEに登録(インポート)する：
    1. Windowsのシステム設定に移動する。
    2. `時刻と言語 > 言語と地域 > Microsoft IME > 学習と辞書`に移動する。
    3. `ユーザー辞書ツールを開く`をクリックする。
    4. `ツール(T) > テキスト ファイルからの登録(T)`をクリックする。
    5. 先ほど作成されたファイル(MicrosoftIME辞書.txt)を開く。

こうすると以下の単語テーブルは表示されます。コメントは登録されません。

|   読み   |   語句  | 品詞 | 登録種別 | ユーザー コメント
|:--------:|:------:|:-----:|:------:|:-------------:|
|  ことば  |   言葉  | 名詞 |         |               |
|  さとう  | 佐藤さん | 人名 |         |    私の友人 　|
