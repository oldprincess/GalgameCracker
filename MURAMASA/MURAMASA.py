import struct
import os
from typing import BinaryIO
import zlib

FILE_PATH_ENCODING = "gbk"
DIR_TYPE = 1
FILE_TYPE = 2
UINT8_MASK = 0xFF
UINT32_MASK = 0xFFFFFFFF

# use in un obfuscate
REORDER_TABLE = [
    0x48, 0xE8, 0xD3, 0x11, 0x1D, 0x58, 0xEA, 0xE5, 0x23, 0xBD, 0x41, 0xC0, 0x86, 0x6A, 0x0A, 0xB3,
    0xE9, 0x26, 0xAE, 0x90, 0xBF, 0x92, 0x02, 0x55, 0x06, 0x61, 0xAF, 0xF1, 0x76, 0xF0, 0x96, 0x91,
    0x34, 0x40, 0x30, 0xA6, 0x15, 0x1E, 0x89, 0x09, 0x7E, 0x2E, 0x63, 0x8B, 0xA1, 0x43, 0x9E, 0x51,
    0xB5, 0xFA, 0xB2, 0x93, 0xE7, 0xD1, 0xBA, 0x33, 0xE2, 0x9F, 0xF6, 0x56, 0xCC, 0x67, 0x71, 0xBC,
    0xED, 0x08, 0xDC, 0xE0, 0xC6, 0xD6, 0xFC, 0x21, 0x99, 0x0E, 0x5F, 0xF2, 0xB4, 0xDB, 0x84, 0xD7,
    0xA7, 0x2A, 0x82, 0x3F, 0xEC, 0x6D, 0xA8, 0x62, 0x5E, 0x8A, 0x28, 0x00, 0xE4, 0x36, 0xFD, 0x8C,
    0x65, 0xA9, 0x39, 0xB7, 0x25, 0x7B, 0x7F, 0xA5, 0x10, 0x2C, 0x54, 0x3B, 0x74, 0xC9, 0x4A, 0x53,
    0xCE, 0xFE, 0xE1, 0x2B, 0xD9, 0x3D, 0xDF, 0x22, 0x3E, 0xD2, 0xB6, 0x8D, 0x8E, 0x72, 0xC4, 0x0D,
    0x52, 0x88, 0x85, 0xB0, 0x7C, 0xD0, 0x6C, 0x31, 0xB8, 0x13, 0x46, 0xAB, 0xF3, 0x81, 0x5C, 0x01,
    0xCB, 0xC2, 0xF5, 0xFB, 0x20, 0xA4, 0x47, 0xD5, 0xB9, 0x4C, 0x3A, 0x77, 0x3C, 0x44, 0x2D, 0x19,
    0x14, 0x5A, 0x45, 0x0B, 0xD8, 0xDD, 0xF7, 0x07, 0xCF, 0xDA, 0x0F, 0x32, 0x38, 0x37, 0x9C, 0x75,
    0x24, 0x57, 0x05, 0xCD, 0xBB, 0xF4, 0xCA, 0x69, 0x03, 0xA3, 0xBE, 0x49, 0xEE, 0x17, 0x1F, 0x59,
    0x7A, 0x78, 0x1C, 0xC8, 0xC7, 0x7D, 0x66, 0x5B, 0x35, 0x04, 0x9A, 0x64, 0xAA, 0x9D, 0x4D, 0x83,
    0x42, 0xC3, 0xDE, 0x1A, 0x50, 0x6F, 0xFF, 0x6E, 0x0C, 0x2F, 0xAD, 0x94, 0xA2, 0x97, 0x9B, 0xC5,
    0x70, 0x79, 0xC1, 0xEF, 0x98, 0xA0, 0xF9, 0xEB, 0x80, 0xF8, 0x73, 0x27, 0x18, 0x6B, 0x29, 0xAC,
    0x4B, 0x16, 0x68, 0x12, 0xE3, 0x95, 0x4E, 0xD4, 0x8F, 0x87, 0xE6, 0x5D, 0x1B, 0xB1, 0x4F, 0x60,
]

# use in obfuscate
ORDER_TABLE = [
    0x5b, 0x8f, 0x16, 0xb8, 0xc9, 0xb2, 0x18, 0xa7, 0x41, 0x27, 0x0e, 0xa3, 0xd8, 0x7f, 0x49, 0xaa,
    0x68, 0x03, 0xf3, 0x89, 0xa0, 0x24, 0xf1, 0xbd, 0xec, 0x9f, 0xd3, 0xfc, 0xc2, 0x04, 0x25, 0xbe,
    0x94, 0x47, 0x77, 0x08, 0xb0, 0x64, 0x11, 0xeb, 0x5a, 0xee, 0x51, 0x73, 0x69, 0x9e, 0x29, 0xd9,
    0x22, 0x87, 0xab, 0x37, 0x20, 0xc8, 0x5d, 0xad, 0xac, 0x62, 0x9a, 0x6b, 0x9c, 0x75, 0x78, 0x53,
    0x21, 0x0a, 0xd0, 0x2d, 0x9d, 0xa2, 0x8a, 0x96, 0x00, 0xbb, 0x6e, 0xf0, 0x99, 0xce, 0xf6, 0xfe,
    0xd4, 0x2f, 0x80, 0x6f, 0x6a, 0x17, 0x3b, 0xb1, 0x05, 0xbf, 0xa1, 0xc7, 0x8e, 0xfb, 0x58, 0x4a,
    0xff, 0x19, 0x57, 0x2a, 0xcb, 0x60, 0xc6, 0x3d, 0xf2, 0xb7, 0x0d, 0xed, 0x86, 0x55, 0xd7, 0xd5,
    0xe0, 0x3e, 0x7d, 0xea, 0x6c, 0xaf, 0x1c, 0x9b, 0xc1, 0xe1, 0xc0, 0x65, 0x84, 0xc5, 0x28, 0x66,
    0xe8, 0x8d, 0x52, 0xcf, 0x4e, 0x82, 0x0c, 0xf9, 0x81, 0x26, 0x59, 0x2b, 0x5f, 0x7b, 0x7c, 0xf8,
    0x13, 0x1f, 0x15, 0x33, 0xdb, 0xf5, 0x1e, 0xdd, 0xe4, 0x48, 0xca, 0xde, 0xae, 0xcd, 0x2e, 0x39,
    0xe5, 0x2c, 0xdc, 0xb9, 0x95, 0x67, 0x23, 0x50, 0x56, 0x61, 0xcc, 0x8b, 0xef, 0xda, 0x12, 0x1a,
    0x83, 0xfd, 0x32, 0x0f, 0x4c, 0x30, 0x7a, 0x63, 0x88, 0x98, 0x36, 0xb4, 0x3f, 0x09, 0xba, 0x14,
    0x0b, 0xe2, 0x91, 0xd1, 0x7e, 0xdf, 0x44, 0xc4, 0xc3, 0x6d, 0xb6, 0x90, 0x3c, 0xb3, 0x70, 0xa8,
    0x85, 0x35, 0x79, 0x02, 0xf7, 0x97, 0x45, 0x4f, 0xa4, 0x74, 0xa9, 0x4d, 0x42, 0xa5, 0xd2, 0x76,
    0x43, 0x72, 0x38, 0xf4, 0x5c, 0x07, 0xfa, 0x34, 0x01, 0x10, 0x06, 0xe7, 0x54, 0x40, 0xbc, 0xe3,
    0x1d, 0x1b, 0x4b, 0x8c, 0xb5, 0x92, 0x3a, 0xa6, 0xe9, 0xe6, 0x31, 0x93, 0x46, 0x5e, 0x71, 0xd6,
]


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ==================================================================
# ========================== Common Utils ==========================
# ==================================================================
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class BinaryReader:
    def __init__(self, fp: BinaryIO):
        self._fp = fp

    def read(self, n: int):
        buf = self._fp.read(n)
        assert len(buf) == n, "Reading Data Fail"
        return buf

    def seek(self, offset, whence):
        self._fp.seek(offset, whence)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ==================================================================
# ======================== NPA Structure Def =======================
# ==================================================================
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class NpaHeader:
    FMT = "<3sIII2sIIIIII"
    SIZE = 3 + 4 + 4 + 4 + 2 + 4 + 4 + 4 + 4 + 4 + 4
    SIG = b'NPA'

    def __init__(self, signature_3s: bytes, unknown1_I: int, seed1_I: int, seed2_I: int, unknown2_2s: bytes,
                 entryCount_I: int, dirCount_I: int, fileCount_I: int,  # excluding directories
                 unknown4_I: int, unknown5_I: int, tocLength_I: int):
        assert signature_3s == NpaHeader.SIG, "invalid Signature"
        assert entryCount_I == dirCount_I + fileCount_I

        self.signature_3s = signature_3s
        self.unknown1_I = unknown1_I
        self.seed1_I = seed1_I
        self.seed2_I = seed2_I
        self.unknown2_2s = unknown2_2s
        self.entryCount_I = entryCount_I
        self.dirCount_I = dirCount_I
        self.fileCount_I = fileCount_I
        self.unknown4_I = unknown4_I
        self.unknown5_I = unknown5_I
        self.tocLength_I = tocLength_I

    @staticmethod
    def unpack(data: bytes):
        assert len(data) == NpaHeader.SIZE
        return NpaHeader(*struct.unpack(NpaHeader.FMT, data))

    def pack(self):
        return struct.pack(NpaHeader.FMT, self.signature_3s, self.unknown1_I, self.seed1_I, self.seed2_I,
                           self.unknown2_2s, self.entryCount_I, self.dirCount_I, self.fileCount_I, self.unknown4_I,
                           self.unknown5_I, self.tocLength_I)


class NpaEntry1:
    FMT = "<I"
    SIZE = 4

    def __init__(self, filePathLength_I: int):
        self.filePathLength_I = filePathLength_I

    @staticmethod
    def unpack(data: bytes):
        assert len(data) == NpaEntry1.SIZE
        return NpaEntry1(*struct.unpack(NpaEntry1.FMT, data))

    def pack(self):
        return struct.pack(NpaEntry1.FMT, self.filePathLength_I)


class NpaEntry2:
    FMT = "<BIIII"
    SIZE = 1 + 4 + 4 + 4 + 4

    def __init__(self, type_B: int, fileBatch_I: int, offset_I: int, length_I: int, originalLength_I: int):
        assert type_B in (DIR_TYPE, FILE_TYPE)
        assert not (type_B == DIR_TYPE and fileBatch_I != 0)

        self.type_B = type_B
        self.fileBatch_I = fileBatch_I
        self.offset_I = offset_I
        self.length_I = length_I
        self.originalLength_I = originalLength_I

    @staticmethod
    def unpack(data: bytes):
        assert len(data) == NpaEntry2.SIZE
        return NpaEntry2(*struct.unpack(NpaEntry2.FMT, data))

    def pack(self):
        return struct.pack(NpaEntry2.FMT, self.type_B, self.fileBatch_I, self.offset_I,
                           self.length_I, self.originalLength_I)


class NpsiHeader:
    FMT = "<4sIHIIII"
    SIZE = 4 + 4 + 2 + 4 + 4 + 4 + 4
    SIG = b'NPSI'

    def __init__(self, signature_4s: bytes, unknown1_I: int, unknown2_H: int,
                 width_I: int, width2_I: int, height_I: int, height2_I: int):
        assert signature_4s == NpsiHeader.SIG, "invalid sig"

        self.signature_4s = signature_4s
        self.unknown1_I = unknown1_I
        self.unknown2_H = unknown2_H
        self.width_I = width_I
        self.width2_I = width2_I
        self.height_I = height_I
        self.height2_I = height2_I

    @staticmethod
    def unpack(data: bytes):
        assert len(data) == NpsiHeader.SIZE
        return NpsiHeader(*struct.unpack(NpsiHeader.FMT, data))

    def pack(self):
        return struct.pack(NpsiHeader.FMT, self.signature_4s, self.unknown1_I, self.unknown2_H,
                           self.width_I, self.width2_I, self.height_I, self.height2_I)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ==================================================================
# ======================== NPA Unpacking  ==========================
# ==================================================================
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def un_obfuscate(buf: bytes, len_I: int, key_I: int) -> bytes:
    # buf'[i] = REORDER_TABLE[ buf[i] ] - key_I - i
    return bytes([(REORDER_TABLE[buf[i]] - key_I - i) & UINT8_MASK for i in range(len_I)])


def obfuscate(buf: bytes, len_I: int, key_I: int) -> bytes:
    # buf'[i] = ORDER_TABLE[ buf[i] + key_I + i ]
    return bytes([ORDER_TABLE[(buf[i] + key_I + i) & UINT8_MASK] for i in range(len_I)])


def generate_file_key(buf: bytes, len_I: int, dataLength_I: int, seed1_I: int, seed2_I: int) -> int:
    """

    :param buf:             buffer, use to gen key
    :param len_I:           length of buf           (uint32_t, 4 bytes length)
    :param dataLength_I:    file original length    (uint32_t, 4 bytes length)
    :param seed1_I:         seed1                   (uint32_t, 4 bytes length)
    :param seed2_I:         seed2                   (uint32_t, 4 bytes length)
    :return:                key                     (uint32_t, 4 bytes length)
    """
    # key: uint32_t = ( (0x87654321 - sum(buf)) * len + seed1 * seed2 ) * dataLength
    return (((0x87654321 - sum(buf)) * len_I + seed1_I * seed2_I) * dataLength_I) & UINT32_MASK


def un_obfuscate_file_path(buf: bytes, len_I: int, index_I: int, seed1_I: int, seed2_I: int) -> bytes:
    ret = []
    for i in range(len_I):
        key = i * 0xFC
        mutator = seed1_I * seed2_I

        key -= (mutator >> 24) & UINT8_MASK
        key -= (mutator >> 16) & UINT8_MASK
        key -= (mutator >> 8) & UINT8_MASK

        key -= seed1_I * seed2_I

        key -= (index_I >> 24) & UINT8_MASK
        key -= (index_I >> 16) & UINT8_MASK
        key -= (index_I >> 8) & UINT8_MASK
        key -= index_I & UINT8_MASK

        ret.append((buf[i] + key) & UINT8_MASK)
    return bytes(ret)


def obfuscate_file_path(raw_path: bytes, len_I: int, index_I: int, seed1_I: int, seed2_I: int) -> bytes:
    ret = []
    for i in range(len_I):
        key = i * 0xFC
        mutator = seed1_I * seed2_I

        key -= (mutator >> 24) & UINT8_MASK
        key -= (mutator >> 16) & UINT8_MASK
        key -= (mutator >> 8) & UINT8_MASK

        key -= seed1_I * seed2_I

        key -= (index_I >> 24) & UINT8_MASK
        key -= (index_I >> 16) & UINT8_MASK
        key -= (index_I >> 8) & UINT8_MASK
        key -= index_I & UINT8_MASK

        ret.append((raw_path[i] - key) & UINT8_MASK)
    return bytes(ret)


def unpack(in_filePath: str, out_dirPath: str) -> None:
    assert os.path.exists(out_dirPath), "output path '{0}' doesn't exist".format(out_dirPath)
    with open(in_filePath, "rb") as _fp_in:
        fp_in = BinaryReader(_fp_in)  # wrap BinaryReader
        # read NPA Header and Entry
        hdr = NpaHeader.unpack(fp_in.read(NpaHeader.SIZE))
        toc_buf = fp_in.read(hdr.tocLength_I)
        data_base = NpaHeader.SIZE + hdr.tocLength_I
        # unpack files
        for i in range(hdr.entryCount_I):
            # unpack entry1: file name
            entry1 = NpaEntry1.unpack(toc_buf[:NpaEntry1.SIZE])
            toc_buf = toc_buf[NpaEntry1.SIZE:]
            # get filePath
            file_path = toc_buf[:entry1.filePathLength_I]
            toc_buf = toc_buf[entry1.filePathLength_I:]
            # unpack entry2: file data
            entry2 = NpaEntry2.unpack(toc_buf[:NpaEntry2.SIZE])
            toc_buf = toc_buf[NpaEntry2.SIZE:]
            # un obfuscate file name
            file_path = un_obfuscate_file_path(file_path, entry1.filePathLength_I, i, hdr.seed1_I, hdr.seed2_I)
            # write file data
            if entry2.length_I:
                # read file data
                fp_in.seek(data_base + entry2.offset_I, 0)
                buf = fp_in.read(entry2.length_I)
                # un obfuscate file data
                un_obfuscate_len = 0x1000 + entry1.filePathLength_I
                if un_obfuscate_len > len(buf):
                    un_obfuscate_len = len(buf)
                key = generate_file_key(file_path, entry1.filePathLength_I, entry2.originalLength_I,
                                        hdr.seed1_I, hdr.seed2_I)
                buf = un_obfuscate(buf[:un_obfuscate_len], un_obfuscate_len, key) + buf[un_obfuscate_len:]
                # un compress file data
                if entry2.length_I != entry2.originalLength_I:
                    obj = zlib.decompressobj()
                    buf = obj.decompress(buf) + obj.flush()
                    assert len(buf) == entry2.originalLength_I, "Decompress Fail"
                # write file data
                out_file_path = os.path.join(out_dirPath, file_path.decode(FILE_PATH_ENCODING))
                if len(buf) >= 4 and buf[:4] == b"NPSI":
                    raise RuntimeError("TODO")
                else:
                    with open(out_file_path, "wb") as fp_out:
                        fp_out.write(buf)
                print("[write]", out_file_path)
            else:
                # create dir
                dir_path = os.path.join(out_dirPath, file_path.decode(FILE_PATH_ENCODING))
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)  # create file path dir
                    print("[write]", dir_path)
    print("[log] unpack '{}' finish!".format(in_filePath))


def pack(in_dirPath: str, out_filePath: str, seed1_I: int = 0, seed2_I: int = 0, compress: bool = True):
    class NpaEntry:
        def __init__(self, _raw_file_path: str, _entry1: NpaEntry1, _file_path: bytes, _entry2: NpaEntry2):
            self.raw_file_path = _raw_file_path
            self.entry1 = _entry1
            self.file_path = _file_path
            self.entry2 = _entry2

    out_tmp_file_path = out_filePath + '.tmp'
    assert not os.path.exists(out_tmp_file_path), \
        "File exists: need to create '{0}' as a tmp file".format(out_tmp_file_path)
    # glob all files and dirs
    entry_lst = []
    file_count = 0
    offset = 0
    index = 0
    batch = 1
    # check first file batch num
    for root, dirs, files in os.walk(in_dirPath):
        if len(dirs) == 0:
            batch = 0
    with open(out_tmp_file_path, "wb") as out_fileTmpFp:
        for root, dirs, files in os.walk(in_dirPath):
            # add dir into Entry
            for _dir in dirs:
                # absolute raw path
                raw_dir_path = os.path.relpath(os.path.join(root, _dir), in_dirPath)
                # obfuscate path data
                dir_path = raw_dir_path.encode(FILE_PATH_ENCODING)
                dir_path = obfuscate_file_path(dir_path, len(dir_path), index, seed1_I, seed2_I)
                dir_path_length = len(dir_path)
                # add to entry
                entry_lst.append(NpaEntry(
                    _raw_file_path=raw_dir_path,
                    _entry1=NpaEntry1(dir_path_length),
                    _file_path=dir_path,
                    _entry2=NpaEntry2(type_B=DIR_TYPE, fileBatch_I=0, offset_I=0, length_I=0, originalLength_I=0)
                ))
                index += 1
                print("[pack]", raw_dir_path)
            # add file into Entry
            new_batch = batch
            for file in files:
                new_batch = batch + 1
                # absolute raw path
                raw_file_path = os.path.relpath(os.path.join(root, file), in_dirPath)
                # obfuscate path data
                file_original_length = os.path.getsize(os.path.join(root, file))
                file_path = raw_file_path.encode(FILE_PATH_ENCODING)
                file_path = obfuscate_file_path(file_path, len(file_path), index, seed1_I, seed2_I)
                file_path_length = len(file_path)
                # write to tmp file
                with open(os.path.join(in_dirPath, raw_file_path), "rb") as in_fileFp:
                    # read file
                    buf = in_fileFp.read()
                    # compress file
                    if compress:
                        obj = zlib.compressobj()
                        buf = obj.compress(buf) + obj.flush()
                    # obfuscate file
                    obfuscate_len = 0x1000 + file_path_length
                    if obfuscate_len > len(buf):
                        obfuscate_len = len(buf)
                    key = generate_file_key(raw_file_path.encode(FILE_PATH_ENCODING),
                                            file_path_length, file_original_length, seed1_I, seed2_I)
                    buf = obfuscate(buf[:obfuscate_len], obfuscate_len, key) + buf[obfuscate_len:]
                    file_length = len(buf)
                    # write file
                    out_fileTmpFp.write(buf)
                # add to entry
                entry_lst.append(NpaEntry(
                    _raw_file_path=raw_file_path,
                    _entry1=NpaEntry1(len(file_path)),
                    _file_path=file_path,
                    _entry2=NpaEntry2(type_B=FILE_TYPE, fileBatch_I=batch, offset_I=offset,
                                      length_I=file_length, originalLength_I=file_original_length)
                ))
                offset += file_length
                file_count += 1
                index += 1
                print("[pack]", raw_file_path)
            batch = new_batch
    entry_count = len(entry_lst)
    hdr = NpaHeader(NpaHeader.SIG, unknown1_I=1, seed1_I=seed1_I, seed2_I=seed2_I, unknown2_2s=b'\x01\x01',
                    entryCount_I=entry_count, dirCount_I=entry_count - file_count, fileCount_I=file_count,
                    unknown4_I=0, unknown5_I=0,
                    tocLength_I=sum([NpaEntry1.SIZE + len(item.file_path) + NpaEntry2.SIZE for item in entry_lst]))
    # pack
    with open(out_filePath, "wb") as out_fileFp:
        # write NpaHeader
        out_fileFp.write(hdr.pack())
        # write Entry
        for i in range(len(entry_lst)):
            out_fileFp.write(entry_lst[i].entry1.pack())
            out_fileFp.write(entry_lst[i].file_path)
            out_fileFp.write(entry_lst[i].entry2.pack())
        # write files(copy from tmp)
        with open(out_tmp_file_path, "rb") as in_fileTmpFp:
            buf = in_fileTmpFp.read(1024 * 1024)
            while len(buf) > 0:
                out_fileFp.write(buf)
                buf = in_fileTmpFp.read(1024 * 1024)
    os.remove(out_tmp_file_path)
    print("[log] pack '{}' finish!".format(in_dirPath))
