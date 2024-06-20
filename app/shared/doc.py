__all__ = (
    "Doc",
    "Text",
    "Word",
    "Excel",
    "PDF",
)


class Doc(object):

    def __init__(self):
        super().__init__()

    def split(
            self,
            text: str,
            length: int = 1000,
            overrided: int = 300,
    ):
        pass


class Text(Doc):

    def __init__(self):
        super().__init__()


class Word(Doc):

    def __init__(self):
        super().__init__()


class Excel(object):

    def __init__(self):
        super().__init__()


class PDF(Doc):

    def __init__(self):
        super().__init__()
