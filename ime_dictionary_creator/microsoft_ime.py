from typing import Optional, List
from pathlib import Path

from ime_dictionary_creator.fileio import save_utf16le_txt, read_utf16le_txt
from ime_dictionary_creator.constants import PartOfSpeech
from ime_dictionary_creator.dict import DictionaryComment, DictionaryEntry, Dictionary


class MicrosoftImeDictionaryComment(DictionaryComment):
    """Microsoft IME辞書内のコメント。"""

    @classmethod
    def from_txt(cls, text: str) -> "MicrosoftImeDictionaryComment":
        """Microsoft IME辞書内のコメントをテキストから作成する。"""
        return MicrosoftImeDictionaryComment(content=text[1:] if text.startswith("!") else text)

    def __str__(self) -> str:
        return f"!{self.content}"


class MicrosoftImeDictionaryEntry(DictionaryEntry):
    """Microsoft IME辞書内の一行(単語)。"""

    @classmethod
    def from_txt(cls, text: str) -> "MicrosoftImeDictionaryEntry":
        """Microsoft IME辞書内の行(単語)をテキストから作成する。"""
        fields: List[Optional[str]] = [f for f in text.split("\t")]

        if len(fields) < 3 or len(fields) > 4 or fields[0] is None or fields[1] is None or fields[2] is None:
            raise ValueError(f"テキスト内で不当な行が見つかりました：「{text}」")
        if len(fields) == 3:
            fields.append(None)

        return MicrosoftImeDictionaryEntry(
            reading=fields[0],
            word=fields[1],
            pos=PartOfSpeech(fields[2]),
            comment=fields[3]
        )

    def __str__(self) -> str:
        return f"{self.reading}\t{self.word}\t{self.pos}{f"\t{self.comment}" if self.comment else ""}"


MicrosoftImeDictionaryItem = MicrosoftImeDictionaryEntry | MicrosoftImeDictionaryComment
"""Microsoft IME辞書内に存在可能なアイテム(内容)。"""

class MicrosoftImeDictionary(Dictionary[MicrosoftImeDictionaryItem]):
    """Microsoft IME辞書。"""

    @classmethod
    def from_file(cls, path: Path, name: Optional[str] = None) -> "MicrosoftImeDictionary":
        """Microsoft IME辞書をファイルから作成する。"""
        dict = MicrosoftImeDictionary(name=name or path.name, save_path=path.parent)

        text = read_utf16le_txt(path)
        for l in text.splitlines():
            line = l.strip()
            if line == "" or line == u'\ufeff':
                continue
            if line.startswith("!"):
                dict.entries.append(MicrosoftImeDictionaryComment.from_txt(line))
            else:
                dict.entries.append(MicrosoftImeDictionaryEntry.from_txt(line))

        return dict

    def add_entry(self, reading: str, word: str, pos: PartOfSpeech | str = PartOfSpeech.名詞, comment: Optional[str] = None):
        """新規の行(単語)をこのMicrosoft IME辞書に追加する。

        Params:
            reading: 新規単語の読み。
            word: 新規単語そのもの。
            pos: 新規単語の品詞。
            comment: （任意）新規単語のコメント。

        Returns:
            entry: 追加された新規単語。
        """
        new_entry = MicrosoftImeDictionaryEntry(
            reading=reading,
            word=word,
            pos=PartOfSpeech(pos),
            comment=comment
        )
        self.entries.append(new_entry)
        return new_entry

    def add_comment(self, content: str):
        """新規のコメントをこのMicrosoft IME辞書に追加する。

        Params:
            content: 新規コメントの内容(テキスト)。
        """
        new_comment = MicrosoftImeDictionaryComment(content=content)
        self.entries.append(new_comment)
        return new_comment

    def save_to_file(self) -> None:
        """このMicrosoft IME辞書をファイルに保存する。"""
        save_utf16le_txt(self.save_path / f"{self.name}.txt", str(self))

    def __str__(self) -> str:
        str_rep = ""
        for entry in self.entries:
            str_rep = str_rep + str(entry) + "\n"
        return str_rep
