def generate_video_stream(video_path):
    """
    Generator function to stream video in chunks
    """
    chunk_size = 8192
    with open(video_path, 'rb') as video_file:
        while True:
            chunk = video_file.read(chunk_size)
            if not chunk:
                break
            yield chunk