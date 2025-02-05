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
    assert len(argv) == 4, "USAGE: %s <input_url_txt> <output_url_md/txt> <YYYYMMDD>"
    assert isfile(argv[1]), "Input file not found: %s" % argv[1]
    assert not (isfile(argv[2]) or isdir(argv[2])), "Output exists: %s" % argv[2]
    assert (len(argv[3]) == 8) and (sum(1 for c in argv[3] if '0' <= c <= '9') == 8), "Date must be YYYYMMDD: %s" % argv[3]
    f_in = open_file(argv[1], 'rt'); f_out = open_file(argv[2], 'wt')
    md_out = argv[2].strip().lower().replace('.gz','').endswith('.md')
    for l in f_in:
        url = clean(l)
        skip = False
        for c in SKIP:
            if c in url:
                skip = True
        if skip:
            continue
        elif md_out:
            f_out.write('* `%s` - [Before 2025-01-27](https://web.archive.org/web/%s000000/%s) - [Latest](https://web.archive.org/web/%s)\n' % (url, argv[3], url, url))
        else:
            f_out.write('%s\n' % url)
    f_in.close(); f_out.close()
