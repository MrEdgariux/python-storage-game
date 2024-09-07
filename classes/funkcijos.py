
def bytes_to_human_readable(bytes):
    sizes = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    i = 0
    while bytes >= 1024:
        bytes /= 1024
        i += 1
    return f"{bytes:.2f} {sizes[i]}"