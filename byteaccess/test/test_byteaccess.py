import os
import sys
sys.path.insert(0, os.path.abspath('..\..'))

import byteaccess


def test_filebyteaccess():
    context = byteaccess.FileByteAccessContext('./testfile.bin')
    foo = context.ByteAccess(0, 21)
    assert foo.read_bytes(0, 4) == b'asdf'
    assert foo.read_bytes(4, 10) == b'0123456789'

    foo.write_bytes(0, b'test')
    assert foo.read_bytes(0, 4) == b'test'

    bar = context.ByteAccess(0, 4)
    assert bar.read_all_bytes() == foo.read_bytes(0, 4)

    bar.write_bytes(0, b'asdf')
    assert foo.read_bytes(0, 4) == b'asdf'

def test_membyteaccess():
    context = byteaccess.MemByteAccessContext('halo')
    foo = context.ByteAccess(0x6A8154, 4)
    assert foo.read_all_bytes() == b'daeh'
    foo.write_bytes(0, b'toof')
    assert foo.read_all_bytes() == b'toof'
    foo.write_bytes(0, b'daeh')
    assert foo.read_all_bytes() == b'daeh'


if __name__ == '__main__':
    test_filebyteaccess()
    test_membyteaccess()
    print("Tests successful!")
