from diff_match_patch import diff_match_patch
import sys, os

if len(sys.argv) == 1 or sys.argv[1][0] not in 'DP':
    print('args are')
    print('arg1: D for diff or P for patch')
elif sys.argv[1] == 'D':
    if len(sys.argv) != 5:
        print('arg2: file 1 to compare')
        print('arg3: file 2 to compare')
        print('arg4: diff output')
    elif not os.path.exists(sys.argv[4]):
        f1 = open(sys.argv[2], 'r').read()
        f2 = open(sys.argv[3], 'r').read()
        dmp = diff_match_patch()
        patches = dmp.patch_make(f1, f2)
        diff = dmp.patch_toText(patches)
        fout = open(sys.argv[4], 'w')
        fout.write(diff)
        fout.close()
    else:
        print(f'Error {sys.argv[4]} exists')
elif sys.argv[1] == 'P':
    if len(sys.argv) < 5:
        print('arg2: file to patch')
        print('arg3: patch')
        print('arg4: file output')
        print('arg5: -f to force write')
    elif not os.path.exists(sys.argv[4]) or (len(sys.argv) == 6 and sys.argv[5] == '-f'):
        f1 = open(sys.argv[2], 'r').read()
        f2 = open(sys.argv[3], 'r').read()

        dmp = diff_match_patch()
        patches = dmp.patch_fromText(f2)
        new_text, status = dmp.patch_apply(patches, f1)
        print(f'Status = {status}')
        if False in status:
            print('Patch failed')
        else:
            patches = dmp.patch_make(f1, f2)
            fout = open(sys.argv[4], 'w')
            fout.write(new_text)
            fout.close()
    else:
        print(f'Error {sys.argv[4]} exists')
else:
    print('Error arg')
