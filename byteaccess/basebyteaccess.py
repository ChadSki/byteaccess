# Copyright (c) 2013, Chad Zawistowski
# All rights reserved.
#
# This software is free and open source, released under the 2-clause BSD
# license as detailed in the LICENSE file.

import abc


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
