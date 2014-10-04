# ByteAccess

A Python module which provides a common interface for reading or writing data to files or to the memory of another process.

## Usage

Open a file or process, accessing their internal data the same way.

    import byteaccess

    if location == 'file':
        data_context = byteaccess.FileContext('file.txt')
    elif location == 'mem'
        data_context = byteaccess.WinMemContext('process.exe')

    foo = data_context.ByteAccess(offset, size)
    foo.write_bytes(0, b'somedata')
    foo.read_bytes(4, 4)  #=> b'data'

For more examples, read the tests at /byteaccess/test/test_byteaccess.py

## License

ByteAccess is free software released under the BSD 2-clause license.
