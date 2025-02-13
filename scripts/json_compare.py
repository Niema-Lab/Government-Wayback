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

# pairwise alignment of two strings
def align(s, t, match=2, mismatch=-4, gap=-4, gap_char='-'):
    S = [[None for j in range(len(t)+1)] for i in range(len(s)+1)]
    B = [[None for j in range(len(t)+1)] for i in range(len(s)+1)] # 0 = match/mismatch, 1 = use s (gap in t), 2 = use t (gap in s)
    S[0][0] = 0
    for i in range(1, len(s)+1):
        S[i][0] = S[i-1][0] + gap
        B[i][0] = 1
    for j in range(1, len(t)+1):
        S[0][j] = S[0][j-1] + gap
        B[0][j] = 2
    for i in range(1, len(s)+1):
        for j in range(1, len(t)+1):
            S[i][j], B[i][j] = max([
                (S[i-1][j-1] + {True:match,False:mismatch}[s[i-1] == t[j-1]], 0),
                (S[i-1][j] + gap, 1),
                (S[i][j-1] + gap, 2),
            ])
    i, j = len(s), len(t); s_tmp, t_tmp = list(), list()
    while i > 0 and j > 0:
        if B[i][j] == 0:
            s_tmp.append(s[i-1]); i -= 1
            t_tmp.append(t[j-1]); j -= 1
        elif B[i][j] == 1:
            s_tmp.append(s[i-1]); i -= 1
            t_tmp.append(gap_char)
        elif B[i][j] == 2:
            s_tmp.append(gap_char)
            t_tmp.append(t[j-1]); j -= 1
        else:
            assert False, "INVALID BACKTRACK (%d, %d): %s" % (i, j, B[i][j])
    return ''.join(s_tmp[::-1]), ''.join(t_tmp[::-1])

# main program
if __name__ == "__main__":
    if len(argv) != 4:
        print("USAGE: %s <json1> <json2> <out_txt>" % argv[0], file=stderr); exit(1)
    json_files = [open_file(fn, 'rt') for fn in argv[1:3]]
    rar1, rar2 = [(jload(f), f.close())[0] for f in json_files]
    rar1_fns, rar2_fns = [set(r.keys()) for r in [rar1, rar2]]
    for fn in rar1_fns:
        rar1[fn] = rar1[fn].encode('ascii', errors='ignore').decode(errors='ignore')
    for fn in rar2_fns:
        rar2[fn] = rar2[fn].encode('ascii', errors='ignore').decode(errors='ignore')
    with open_file(argv[3], 'wt') as out_f:
        print("- File 1 (%d files): %s" % (len(rar1), argv[1]), file=out_f)
        print("- File 2 (%d files): %s" % (len(rar2), argv[2]), file=out_f)
        in_rar1_not_rar2 = {k for k in rar1 if k not in rar2}
        print("- In File 1, not File 2: %d files" % len(in_rar1_not_rar2), file=out_f)
        print('\n'.join('  - %s' % fn for fn in sorted(in_rar1_not_rar2)), file=out_f)
        in_rar2_not_rar1 = {k for k in rar2 if k not in rar1}
        print("- In File 2, not File 1: %d files" % len(in_rar2_not_rar1), file=out_f)
        print('\n'.join('  - %s' % fn for fn in sorted(in_rar2_not_rar1)), file=out_f)
        in_both = {k for k in rar1 if k in rar2}
        in_both_unchanged = {k for k in in_both if rar1[k].strip() == rar2[k].strip()}
        in_both_changed = in_both - in_both_unchanged
        print("- In Both, Unchanged: %d files" % len(in_both_unchanged), file=out_f)
        print('\n'.join('  - %s' % fn for fn in sorted(in_both_unchanged)), file=out_f)
        print("- In Both, Changed: %d files" % len(in_both_changed), file=out_f)
        for fn in tqdm(sorted(in_both_changed)):
            print('  - %s' % fn, file=out_f)
            print('    - File 1: %s\n    - File 2: %s' % align(rar1[fn], rar2[fn]), file=out_f)
            out_f.flush()