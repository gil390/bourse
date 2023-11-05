import sys, os
from diff_match_patch import diff_match_patch

def diff_to_patch(filea, fileb, patchfile):
    with open(filea, 'r') as fobj:
        obja = fobj.read()
    with open(fileb, 'r') as fobj:
        objb = fobj.read()
    dmp = diff_match_patch()
    patches= dmp.patch_make(obja, objb)

    with open(patchfile, 'w') as fobj:
        fobj.write(dmp.patch_toText(patches))

def apply_diff(fileSrc, fileDst):
    dmp = diff_match_patch()

    with open(fileSrc, 'r') as fSrc:
        diff = fSrc.read()
        patches = dmp.patch_fromText(diff)

        new_text = None
        with open(fileDst, 'r') as fDst:
            text = fDst.read()
            new_text, state = dmp.patch_apply(patches, text)
            print(f'state = {state}')
            fDst.close()

        if new_text:
            with open(fileDst, 'w') as fDst:
                fDst.write(new_text)

if __name__ == '__main__':
    if len(sys.argv) == 4:
        print(f'-- create diff to {sys.argv[3]}')
        if os.path.exists(sys.argv[3]):
            print(f'ERROR: {sys.argv[3]} exists')
        else:
            diff_to_patch(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        print(f'-- apply patch to {sys.argv[2]}')
        apply_diff(sys.argv[1], sys.argv[2])
