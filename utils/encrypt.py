import md5

def encodeMD5(str):
    return md5.new(str).hexdigest()

