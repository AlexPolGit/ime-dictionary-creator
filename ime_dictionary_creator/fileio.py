from pathlib import Path

def read_utf16le_txt(file_path: Path) -> str:
    """UTF-16 LEのテキストファイルの内容を読み込む。

    Params:
        file_path: 読み込みたいファイルのパス。
    """
    with open(file_path, "r", encoding="utf-16-le") as f:
        return f.read()[1:]


def save_utf16le_txt(file_path: Path, content: str) -> None:
    """テキストをUTF-16 LEのテキストファイルに保存する。

    Params:
        file_path: 保存したいファイルのパス。
        content: 保存したいファイル内容。
    """
    with open(file_path, "w", encoding="utf-16-le") as f:
        f.write(u'\ufeff')
        f.write(content)
