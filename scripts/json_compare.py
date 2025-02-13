#! /usr/bin/env python3
from gzip import open as gopen
from json import load as jload
from sys import argv, stderr
from tqdm import tqdm

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
    if len(argv) != 3:
        print("USAGE: %s <json1> <json2>" % argv[0], file=stderr); exit(1)
    json_files = [open_file(fn, 'rt') for fn in argv[1:]]
    rar1, rar2 = [(jload(f), f.close())[0] for f in json_files]
    rar1_fns, rar2_fns = [set(r.keys()) for r in [rar1, rar2]]
    print("- File 1 (%d files): %s" % (len(rar1), argv[1]))
    print("- File 2 (%d files): %s" % (len(rar2), argv[2]))
    in_rar1_not_rar2 = {k for k in rar1 if k not in rar2}
    print("- In File 1, not File 2: %d files" % len(in_rar1_not_rar2))
    print('\n'.join('  - %s' % fn.encode('ascii', errors='ignore').decode() for fn in sorted(in_rar1_not_rar2)))
    in_rar2_not_rar1 = {k for k in rar2 if k not in rar1}
    print("- In File 2, not File 1: %d files" % len(in_rar2_not_rar1))
    print('\n'.join('  - %s' % fn.encode('ascii', errors='ignore').decode() for fn in sorted(in_rar2_not_rar1)))
    in_both = {k for k in rar1 if k in rar2}
    in_both_unchanged = {k for k in in_both if rar1[k].strip() == rar2[k].strip()}
    in_both_changed = in_both - in_both_unchanged
    print("- In Both, Unchanged: %d files" % len(in_both_unchanged))
    print('\n'.join('  - %s' % fn.encode('ascii', errors='ignore').decode() for fn in sorted(in_both_unchanged)))
    print("- In Both, Changed: %d files" % len(in_both_changed))
    print('\n'.join('  - %s' % fn.encode('ascii', errors='ignore').decode() for fn in sorted(in_both_changed)))