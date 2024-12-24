from hashlib import md5

def compute_file_hash(file,buffer_size=65536):
    hash=md5()
    with open(file,"rb") as f:
        while True:
            data=f.read(buffer_size)
            if not data:
                break
            hash.update(data)
    return hash.hexdigest()

def merge_fingerprints(hashes):
    return md5("#".join(sorted(hashes)).encode()).hexdigest()