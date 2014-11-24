# ByteAccess

A Python module which provides a common interface for reading or writing data to files or to the memory of another process.

## Usage

Open a file or process, accessing their internal data the same way.

    import byteaccess

    if location == 'file':
        data_context = byteaccess.FileContext('filename.txt')
    elif location == 'mem'
        data_context = byteaccess.MemContext('processname')

    foo = data_context.ByteAccess(offset, size)

    foo.write_bytes(0, b'somedata')    # write data to offsets within the ByteAccess

    foo.read_bytes(2, 6)  #=> b'medata'  # read any length of data from any offset

For more examples, read the tests at /byteaccess/test/test_byteaccess.py

## License

ByteAccess is free software released under the BSD 2-clause license.
