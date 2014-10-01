# Copyright (c) 2013, Chad Zawistowski
# All rights reserved.
#
# This software is free and open source, released under the 2-clause BSD
# license as detailed in the LICENSE file.
"""
Common interface for reading and writing binary data to files and processes.

Within a ByteAccess, offsets are relative. This means that ByteAccesses which
wrap the same data always appear and behave identically, regardless of where
that data actually is. This is useful when operations need to be performed on
identical data from different locations.

Example usage:

    from byteaccess import FileByteAccessContext,
                           MemByteAccessContext

    if location == 'file':
        context = FileByteAccessContext('file.txt')
    elif location == 'mem'
        context = MemByteAccessContext('process.exe')
     
    foo = context.ByteAccess(offset, size)
    foo.write_bytes(0, b'somedata')
    foo.read_bytes(4, 4)  #=> b'data'
"""

__version__ = '0.3.0'

import abc
import platform


class BaseByteAccess(metaclass=abc.ABCMeta):

    """Abstract base class implements common ByteAccess functionality."""

    def __init__(self, offset, size):
        """Provide access to a region of bytes.

        offset -- Absolute offset within the source medium.
        size -- Number of bytes to grant access to.
        """
        self.offset = offset
        self.size = size

    def read_bytes(self, offset, size):
        """Read a number of bytes from the source.

        offset -- Relative offset within the ByteAccess.
        size -- Number of bytes to read.
        """
        if offset + size > self.size:
            raise ValueError("Cannot read past end of ByteAccess. " +
                             "offset:{0} size:{1} self.size:{2}"
                             .format(offset, size, self.size))

        return self._read_bytes(offset, size)

    def read_all_bytes(self):
        """Read all data this ByteAccess encapsulates."""
        return self.read_bytes(0, self.size)

    def write_bytes(self, offset, to_write):
        """Write a bytestring to the source.

        offset -- Relative offset within the ByteAccess
        to_write -- The bytestring to write. If too large to write
                    at the specified offset, throws ValueError.
        """
        if offset + len(to_write) > self.size:
            raise ValueError("Cannot write past end of ByteAccess. " +
                             "offset:{0} size:{1} self.size:{2}"
                             .format(offset, len(to_write), self.size))

        self._write_bytes(offset, to_write)

    # This abstract class is defined such that subclasses only need to
    # implement the following two methods:

    @abc.abstractmethod
    def _read_bytes(self, offset, size):
        pass

    @abc.abstractmethod
    def _write_bytes(self, offset, to_write):
        pass


class FileByteAccessContext(object):

    """Context for creating ByteAccesses which read and write to a specific file."""

    def __init__(self, filepath):
        import mmap

        self.file_handle = open(filepath, 'r+b')
        self.mmap_f = mmap.mmap(self.file_handle.fileno(), 0)

        class FileByteAccess(BaseByteAccess):

            """Read/write bytes to a file on disk."""

            def _read_bytes(slf, offset, size):
                begin = slf.offset + offset
                end = begin + size
                return self.mmap_f[begin:end]

            def _write_bytes(slf, offset, to_write):
                begin = slf.offset + offset
                end = begin + len(to_write)
                self.mmap_f[begin:end] = to_write

        self.ByteAccess = FileByteAccess

    def close(self):
        """Close the file and invalidate all child ByteAccesses."""
        self.mmap_f.close()
        self.file_handle.close()



class WinMemByteAccessContext(object):

    """Context for creating ByteAccesses which read and write to a specific process."""

    def __init__(self, process_name):
        from .windowsinterop import find_process
        from ctypes import (byref, c_ulong, c_char_p, create_string_buffer, windll)
        k32 = windll.kernel32

        PROCESS_ALL_ACCESS = 0x1F0FFF
        process_entry = find_process((process_name + '.exe').encode('ascii'))
        self.process = k32.OpenProcess(PROCESS_ALL_ACCESS, False,
                                       process_entry.th32ProcessID)

        class WinMemByteAccess(BaseByteAccess):

            """Read/write bytes to a specific process's memory."""

            def _read_bytes(slf, offset, size):
                address = slf.offset + offset
                buf = create_string_buffer(size)
                bytesRead = c_ulong(0)
                if k32.ReadProcessMemory(self.process, address,
                                         buf, size, byref(bytesRead)):
                    return bytes(buf)
                else:
                    raise RuntimeError("Failed to read memory")

            def _write_bytes(slf, offset, to_write):
                address = slf.offset + offset
                buf = c_char_p(to_write)
                size = len(to_write)
                bytesWritten = c_ulong(0)
                if k32.WriteProcessMemory(self.process, address,
                                          buf, size, byref(bytesWritten)):
                    return
                else:
                    raise RuntimeError("Failed to write memory")

        self.ByteAccess = WinMemByteAccess

    def close(self):
        """Close the process and invalidate all child ByteAccesses."""
        from ctypes import windll
        windll.kernel32.CloseHandle(self.process)


p = platform.system()
if p == 'Windows':
    MemByteAccessContext = WinMemByteAccessContext
elif p == 'Darwin':
    # MemByteAccessContext = MacMemByteAccessContext
    raise NotImplementedError("Mac support not yet available")
else:
    raise NotImplementedError("Unsupported platform.")
