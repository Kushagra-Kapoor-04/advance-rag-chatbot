import hashlib


def hash_files(file_paths):
    hasher = hashlib.md5()
    for path in sorted(file_paths):
        with open(path, "rb") as f:
            hasher.update(f.read())
    return hasher.hexdigest()
