import hashlib

def translate(text):
    hex_list = []
    mirror_text = text[::-1]
    for char in text:
        ascii_value = ord(char)

        hex_char = hex(ascii_value)[2:].upper()
        hex_list.append(hex_char)
    hex_end = ''.join(hex_list)

    hash1 = hashlib.md5(hex_end[::-1].encode()).hexdigest()
    hash2 = hashlib.sha1(hash1[::-1].encode()).hexdigest()
    hash3 = hashlib.sha256(hash2[::-1].encode()).hexdigest()
    hash4 = hashlib.sha1(hash3[::-1].encode()).hexdigest()
    hash5 = hashlib.sha256(hash4[::-1].encode()).hexdigest()
    hash6 = hashlib.md5(hash5[::-1].encode()).hexdigest()
    hash7 = hashlib.sha256(hash6[::-1].encode()).hexdigest()

    return hash7
