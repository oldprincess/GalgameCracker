import os
import MURAMASA

in_filePath = "npa/cg2.npa"
out_dirPath = "out_cg2"

if not os.path.exists(out_dirPath):
    os.mkdir(out_dirPath)
MURAMASA.unpack(in_filePath, out_dirPath)


in_dirPath = "out_cg2"
out_filePath = "out_npa/cg2.npa"
if not os.path.exists(os.path.dirname(out_filePath)):
    os.mkdir(os.path.dirname(out_filePath))
MURAMASA.pack(in_dirPath, out_filePath)