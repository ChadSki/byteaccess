# Copyright (c) 2013, Chad Zawistowski
# All rights reserved.
#
# This software is free and open source, released under the 2-clause BSD
# license as detailed in the LICENSE file.

from ctypes import (byref, c_ulong, c_ulonglong, c_char, windll, sizeof, Structure)
import platform


def find_process(name):
    """Return the first running process found with the specified name, or None."""
    CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
    Process32First = windll.kernel32.Process32First
    Process32Next = windll.kernel32.Process32Next
    CloseHandle = windll.kernel32.CloseHandle

    class ProcessEntry32(Structure):
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

    # get a snapshot of running processes
    TH32CS_SNAPPROCESS = 0x00000002
    hTH32Snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)

    try:  # iterate over processes
        process_entry = ProcessEntry32()
        process_entry.dwSize = sizeof(ProcessEntry32)

        if Process32First(hTH32Snapshot, byref(process_entry)) is False:
            raise Exception("Failed iterating processes while looking for '{0}'"
                            .format(name))

        while True:
            if process_entry.szExeFile == name:
                return process_entry

            if Process32Next(hTH32Snapshot, byref(process_entry)) is False:
                break

        raise Exception("'{0}' is not running".format(name))

    finally:  # ensure we close the snapshot
        CloseHandle(hTH32Snapshot)
