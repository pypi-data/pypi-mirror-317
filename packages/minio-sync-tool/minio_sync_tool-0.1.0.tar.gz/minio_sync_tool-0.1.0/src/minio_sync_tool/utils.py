import hashlib
import logging


def calculate_multipart_etag(file_path, part_size):
    """
    Calculate the multipart ETag for a given file.
    
    :param file_path: Path to the file
    :param part_size: Size of each part in bytes
    :return: Multipart ETag as a string
    """
    md5s = []
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(part_size):
                md5s.append(hashlib.md5(chunk).digest())
        
        # Concatenate MD5s and compute the final hash
        concatenated_md5s = b''.join(md5s)
        final_etag = hashlib.md5(concatenated_md5s).hexdigest()
        
        return f"{final_etag}-{len(md5s)}"
    except FileNotFoundError:
        logging.error("File not found")
        return None
    except Exception as e:
        logging.error(f"Error: {e}")
        return None
