import sys, os
from diff_match_patch import diff_match_patch

if len(sys.argv) == 3:
    fileSrc = sys.argv[1]
    fileDst = sys.argv[2]
    dmp = diff_match_patch()

    with open(fileSrc, 'r') as fSrc:
        diff = fSrc.read()
        patches = dmp.patch_fromText(diff)

        new_text = None
        with open(fileDst, 'r') as fDst:
            text = fDst.read()
            new_text, _ = dmp.patch_apply(patches, text)
            fDst.close()

        if new_text:
            print(f'Patch to {fileDst}')
            print(new_text)
            with open(fileDst, 'w') as fDst:
                fDst.write(new_text)