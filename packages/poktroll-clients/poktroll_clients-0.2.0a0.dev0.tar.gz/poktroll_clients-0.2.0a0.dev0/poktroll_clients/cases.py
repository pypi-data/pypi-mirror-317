def camel_to_snake_case(s: str) -> str:
    chars = []
    for i, c in enumerate(s):
        if c.isupper() and i > 0:
            chars.append('_')
        chars.append(c.lower())
    return ''.join(chars)