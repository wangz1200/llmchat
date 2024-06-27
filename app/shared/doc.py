from .base import *


__all__ = (
    "load_from_file",
    "Doc",
    "Text",
    "Word",
    "Excel",
    "PDF",
)


def load_from_file(
        file_path: str | Path,
):
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileExistsError("文件不存在。")
    ext = file_path.suffix
    match ext.lower():
        case "txt", ".txt", "json", ".json":
            cls = Text
        case ".json":
            cls = Text
        case _:
            raise Exception(f"不支持的文件格式{ext}")
    loader = cls(file_path)
    return loader


class Doc(object):

    def __init__(self):
        super().__init__()
        self.content = None

    def split(
            self,
            chunk_size: int = 1000,
            overlap_size: int = 300,
    ):
        length = len(self.content)
        chunks = []
        if length < chunk_size:
            chunks.append(self.content)
        else:
            start = 0
            while start + chunk_size <= length:
                end = start + chunk_size
                if end > length:
                    end = length
                chunk = self.content[start:end]
                chunks.append(chunk)
                start = (
                    end - overlap_size
                    if start + chunk_size + overlap_size <= length
                    else start + chunk_size
                )
        return chunks


class Text(Doc):

    def __init__(
            self,
            file_path: str | Path,
    ):
        super().__init__()
        self.file_path = Path(file_path)
        with self.file_path.open(
                mode="r", encoding="utf-8"
        ) as f:
            self.content = f.read()


class Word(Doc):

    def __init__(self):
        super().__init__()


class Excel(object):

    def __init__(self):
        super().__init__()


class PDF(Doc):

    def __init__(self):
        super().__init__()
