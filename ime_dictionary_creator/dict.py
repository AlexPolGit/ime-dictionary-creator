from typing import Optional, List
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pathlib import Path
from pydantic import BaseModel, field_validator

from ime_dictionary_creator.constants import PartOfSpeech, VALID_READING_CHARACTERS


class DictionaryComment(BaseModel):
    """抽象型のIME辞書内のコメント。"""

    content: str
    """コメントの内容(テキスト)。"""


class DictionaryEntry(BaseModel):
    """抽象型のIME辞書内の一行(言葉)。"""

    reading: str
    """言葉の読み。"""
    word: str
    """言葉そのもの。"""
    pos: PartOfSpeech
    """言葉の品詞。"""
    comment: Optional[str]
    """（任意）言葉のコメント。"""

    class Config:
        validate_assignment = True

    @field_validator("reading")
    def must_be_valid_reading(cls, reading: str):
        """言葉の読みの構成は正当な文字からなっているかどうかを確認する。"""
        for char in reading:
            if char not in VALID_READING_CHARACTERS:
                raise TypeError(f"不当な文字が読み（{reading}）に含まれています：「{char}」。ひらがな、英数字、記号のみが使用可能です。")
        return reading


DictionaryItemType = TypeVar("DictionaryItemType", bound=(DictionaryEntry | DictionaryComment))
"""辞書内に存在可能なアイテム(内容)のジェネリックタイプ。"""


class Dictionary(BaseModel, ABC, Generic[DictionaryItemType]):
    """抽象型のIME辞書。"""

    name: str
    """この辞書の名前。ファイル保存時にファイル名として使用されます。"""
    save_path: Path = Path()
    """ファイル保存時に使用されるファイルパス。"""
    entries: List[DictionaryItemType] = []
    """この辞書の全ての行とコメント。"""

    @abstractmethod
    def add_entry(self, reading: str, word: str, pos: PartOfSpeech | str = PartOfSpeech.名詞, comment: Optional[str] = None) -> DictionaryItemType:
        """新規の行(言葉)をこの辞書に追加する。

        Params:
            reading: 新規言葉の読み。
            word: 新規言葉そのもの。
            pos: 新規言葉の品詞。
            comment: （任意）新規言葉のコメント。

        Returns:
            entry: 追加された新規言葉。
        """
        pass

    @abstractmethod
    def add_comment(self, content: str) -> DictionaryItemType:
        """新規のコメントをこの辞書に追加する。

        Params:
            content: 新規コメントの内容(テキスト)。
        """
        pass

    @abstractmethod
    def save_to_file(self) -> None:
        """この辞書をファイルに保存する。"""
        pass

    def get_entries(self) -> List[DictionaryItemType]:
        """この辞書の行とコメントを全て取り出す。

        Returns:
            entry: この辞書の全部の行とコメント。
        """
        return self.entries
