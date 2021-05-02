import os
import logging as log
import subprocess
from datetime import time


def main():
    filename = 'debuglog.txt'
    filename = os.path.join(os.path.dirname(__file__), filename)
    # the root logger needs a level equal to the lowest handler
    log.getLogger().setLevel(log.DEBUG)
    formatter = log.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = log.FileHandler(filename, delay=True)
    file_handler.setLevel(log.DEBUG)
    file_handler.setFormatter(formatter)
    log.getLogger().addHandler(file_handler)

    stream_handler = log.StreamHandler(sys.stdout)
    stream_handler.setLevel(log.INFO)
    stream_handler.setFormatter(formatter)
    log.getLogger().addHandler(stream_handler)

    log.debug('Logging initialized')


def convert(filepath):
    subprocess.run(f'ebook-convert.exe {filepath} {filepath.replace("awz", "epub")}')
    filename = filepath.split("\\")[-1]
    log.info(f'Converted {filename} to EPUB')

def scan(directory, q):
    log.debug(f'scanning {directory}')
    stat_info = os.stat(directory)
    last_checked = stat_info.st_mtime

    while True:
        time.sleep(5)
        stat_info = os.stat(directory)
        _last_modified = stat_info.st_mtime

        if last_checked < _last_modified:
            files = os.listdir(directory)
            for file in files:
                if file.endswith('.azw'):
                    file_stats = os.stat(os.path.join(directory, file))
                    if file_stats.st_ctime > last_checked:
                        convert(os.path.join(directory, file))


if __name__ == '__main__':
    main()