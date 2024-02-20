import re


def cyrillic_check(text: str):
    if re.search(r'\d', text):
        return None
    else:
        return re.findall('[А-ЯЁ][а-яё]', text)
