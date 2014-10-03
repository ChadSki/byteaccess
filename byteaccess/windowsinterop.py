# Copyright (c) 2013, Chad Zawistowski
# All rights reserved.
#
# This software is free and open source, released under the 2-clause BSD
# license as detailed in the LICENSE file.

from ctypes import (byref, c_ulong, c_ulonglong, c_char, windll, sizeof, Structure)
import platform
k32 = windll.kernel32


class ProcessEntry32(Structure):

    """Holds process-related info.

    See http://www.pinvoke.net/default.aspx/kernel32/PROCESSENTRY32.html
    """

    _fields_ = [("dwSize", c_ulong),
                ("cntUsage", c_ulong),
                ("th32ProcessID", c_ulong),
                ("th32DefaultHeapID",
                    c_ulonglong if platform.architecture()[0] == '64bit'
                    else c_ulong),
                ("th32ModuleID", c_ulong),
                ("cntThreads", c_ulong),
                ("th32ParentProcessID", c_ulong),
                ("pcPriClassBase", c_ulong),
                ("dwFlags", c_ulong),
                ("szExeFile", c_char * 260)]


def find_process(name):
    """Return the first running process found with the specified name.

    Raises a RuntimeError if the process cannot be found, or if searching fails.
    """
    # get a snapshot of running processes
    TH32CS_SNAPPROCESS = 0x00000002
    hTH32Snapshot = k32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    try:
        # iterate over processes
        process_entry = ProcessEntry32()
        process_entry.dwSize = sizeof(ProcessEntry32)

        if 0 == k32.Process32First(hTH32Snapshot, byref(process_entry)):
            raise RuntimeError("Failed iterating processes while looking for '{0}'"
                               .format(name))
        while True:
            if process_entry.szExeFile == name:
                return process_entry

            if 0 == k32.Process32Next(hTH32Snapshot, byref(process_entry)):
                break

        raise RuntimeError("'{0}' is not running".format(name))

    finally:  # ensure we close the snapshot
        k32.CloseHandle(hTH32Snapshot)
