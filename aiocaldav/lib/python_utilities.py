def to_wire(text):
    if text and isinstance(text, str):
        text = bytes(text, 'utf-8')
    return text


def to_local(text):
    if text and not isinstance(text, str):
        text = text.decode('utf-8')
    return text
