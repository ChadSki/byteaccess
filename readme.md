# ByteAccess

A Python module which provides a common interface for reading or writing data to files or to the memory of another process.

## Usage

Open a file or process, accessing them the same way

    from byteaccess import FileByteAccessContext,
                           WinMemByteAccessContext

    if location == 'file':
        context = FileByteAccessContext('file.txt')
    elif location == 'mem'
        context = MemByteAccessContext('process')  #=> looks for 'process.exe' on Windows
     
    foo = context.ByteAccess(offset, size)
    foo.write_bytes(0, b'somedata')
    foo.read_bytes(4, 4)  #=> b'data'

## License

bytearray is free software released under the BSD 2-clause license.
