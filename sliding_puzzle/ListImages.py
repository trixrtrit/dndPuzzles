import os


def list_images(directory):
    supported_formats = (".png", ".jpg", ".jpeg", ".gif", ".bmp")
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(supported_formats)]