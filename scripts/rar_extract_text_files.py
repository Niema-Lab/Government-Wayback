#! /usr/bin/env python3
# Add the WinRAR install directory to your PATH (or make sure `unrar` is in your PATH)
from bs4 import BeautifulSoup
from gzip import open as gopen
from json import dump as jdump
from rarfile import RarFile
from sys import argv, stderr
from tqdm import tqdm
EXTS = {'html', 'txt'}

# main program
if __name__ == "__main__":
    if len(argv) != 2:
        print("USAGE: %s <rar_file>" % argv[0], file=stderr); exit(1)
    print("Loading files from: %s" % argv[1])
    text_files = dict()
    with RarFile(argv[1], mode='r', crc_check=False) as rar_file:
        fns_raw = rar_file.namelist()
        for fn_raw in tqdm(fns_raw):
            fn = fn_raw.encode('ascii', errors='ignore').decode(errors='ignore').strip()
            if fn.split('.')[-1].strip() in EXTS:
                text_files[fn] = ' '.join(BeautifulSoup(rar_file.read(fn_raw).decode(errors='ignore'), features='html.parser').get_text().strip().split())
    with gopen(argv[1] + '.text_files.json.gz', mode='wt') as json_file:
        jdump(text_files, json_file)