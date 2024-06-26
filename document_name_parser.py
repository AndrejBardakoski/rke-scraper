import cyrtranslit


def document_name_parser(document_name):
    document_name = cyrtranslit.to_latin(document_name, 'mk')
    document_name = (document_name.strip().lower()
                     .replace(' ', '_')
                     .replace('ḱ', 'kj')
                     .replace('č', 'c')
                     .replace('š', 's')
                     .replace('ž', 'z')
                     .replace('ć', 'c')
                     .replace('đ', 'dj'))

    return document_name
