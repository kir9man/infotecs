URLS = [
    (),
    ('127.31.255.255', ),
    ('localhost', '5413'),
]

URLS_IDS = [f"({','.join(map(str, param))})" for param in URLS]
