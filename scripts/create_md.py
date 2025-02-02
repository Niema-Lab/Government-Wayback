#! /usr/bin/env python3
from gzip import open as gopen
from os.path import isdir, isfile
from sys import argv

# bad characters to replace
REPLACE = [
    ('﹖', '?'),
    ('﹕', ':'),
    ('ꤷ', '/'),
]

# characters to skip URLs
SKIP = ['?']

# clean a string
def clean(s):
    s = s.strip()
    for k, v in REPLACE:
        s = s.replace(k,v)
    return s

# open a file
def open_file(fn, mode='rt'):
    if fn == 'stdin':
        from sys import stdin as f
    elif fn == 'stdout':
        from sys import stdout as f
    elif fn == 'stderr':
        from sys import stderr as f
    elif fn.strip().lower().endswith('.gz'):
        f = gopen(fn, mode=mode)
    else:
        f = open(fn, mode=mode)
    return f

# main program
if __name__ == "__main__":
    assert len(argv) == 3, "USAGE: %s <input_url_txt> <output_url_md>"
    assert isfile(argv[1]), "Input file not found: %s" % argv[1]
    assert not (isfile(argv[2]) or isdir(argv[2])), "Output exists: %s" % argv[2]
    f_in = open_file(argv[1], 'rt'); f_out = open_file(argv[2], 'wt')
    for l in f_in:
        url = clean(l)
        if url.endswith('.html'):
            skip = False
            for c in SKIP:
                if c in url:
                    skip = True
            if skip:
                continue
            f_out.write('* [%s](%s)\n' % (url, url))
    f_in.close(); f_out.close()
