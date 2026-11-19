"""Windows-only Job Object primitive for a suspended process.

Internal, experimental: no reference CLI depends on this module yet.
"""
import ctypes
import os
import math
from ctypes import wintypes


class _BasicLimits(ctypes.Structure):
    _fields_ = [('PerProcessUserTimeLimit', ctypes.c_longlong),
                ('PerJobUserTimeLimit', ctypes.c_longlong),
                ('LimitFlags', wintypes.DWORD),
                ('MinimumWorkingSetSize', ctypes.c_size_t),
                ('MaximumWorkingSetSize', ctypes.c_size_t),
                ('ActiveProcessLimit', wintypes.DWORD),
                ('Affinity', ctypes.c_size_t),
                ('PriorityClass', wintypes.DWORD),
                ('SchedulingClass', wintypes.DWORD)]


class _IoCounters(ctypes.Structure):
    _fields_ = [(name, ctypes.c_ulonglong) for name in (
        'ReadOperationCount', 'WriteOperationCount', 'OtherOperationCount',
        'ReadTransferCount', 'WriteTransferCount', 'OtherTransferCount')]


class _ExtendedLimits(ctypes.Structure):
    _fields_ = [('BasicLimitInformation', _BasicLimits), ('IoInfo', _IoCounters),
                ('ProcessMemoryLimit', ctypes.c_size_t), ('JobMemoryLimit', ctypes.c_size_t),
                ('PeakProcessMemoryUsed', ctypes.c_size_t), ('PeakJobMemoryUsed', ctypes.c_size_t)]


class _StartupInfo(ctypes.Structure):
    _fields_ = [('cb', wintypes.DWORD), ('lpReserved', wintypes.LPWSTR),
                ('lpDesktop', wintypes.LPWSTR), ('lpTitle', wintypes.LPWSTR),
                ('dwX', wintypes.DWORD), ('dwY', wintypes.DWORD),
                ('dwXSize', wintypes.DWORD), ('dwYSize', wintypes.DWORD),
                ('dwXCountChars', wintypes.DWORD), ('dwYCountChars', wintypes.DWORD),
                ('dwFillAttribute', wintypes.DWORD), ('dwFlags', wintypes.DWORD),
                ('wShowWindow', wintypes.WORD), ('cbReserved2', wintypes.WORD),
                ('lpReserved2', ctypes.c_void_p), ('hStdInput', wintypes.HANDLE),
                ('hStdOutput', wintypes.HANDLE), ('hStdError', wintypes.HANDLE)]


class _StartupInfoEx(ctypes.Structure):
    _fields_ = [('StartupInfo', _StartupInfo), ('lpAttributeList', ctypes.c_void_p)]


class _ProcessInformation(ctypes.Structure):
    _fields_ = [('hProcess', wintypes.HANDLE), ('hThread', wintypes.HANDLE),
                ('dwProcessId', wintypes.DWORD), ('dwThreadId', wintypes.DWORD)]


class _Pipe:
    """Own one CRT descriptor, looping until all input bytes are written."""
    def __init__(self, fd):
        self._fd = fd

    @property
    def closed(self):
        return self._fd is None

    def fileno(self):
        if self._fd is None:
            raise ValueError('pipe closed')
        return self._fd

    def write(self, data):
        view = memoryview(data)
        done = 0
        while done < len(view):
            written = os.write(self.fileno(), view[done:])
            if written <= 0:
                raise OSError('short pipe write')
            done += written
        return done

    def read(self, size=-1):
        if size >= 0:
            return os.read(self.fileno(), size)
        chunks = []
        while True:
            chunk = os.read(self.fileno(), 65536)
            if not chunk:
                return b''.join(chunks)
            chunks.append(chunk)

    def close(self):
        if self._fd is not None:
            fd, self._fd = self._fd, None
            os.close(fd)


class _OwnedProcess:
    def __init__(self, kernel, handle, pid):
        self._kernel, self._handle, self.pid = kernel, handle, pid
        self._kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        self._kernel.WaitForSingleObject.restype = wintypes.DWORD
        self._kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        self._kernel.GetExitCodeProcess.restype = wintypes.BOOL

    def wait(self, timeout):
        try:
            if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
                raise ValueError('timeout')
            timeout = float(timeout)
            if not math.isfinite(timeout) or not 0 <= timeout <= 86400:
                raise ValueError('timeout')
        except (ValueError, OverflowError):
            raise ValueError('invalid timeout') from None
        result = self._kernel.WaitForSingleObject(self._handle, int(timeout * 1000))
        if result == 258:
            raise TimeoutError('child did not exit')
        if result != 0:
            raise ctypes.WinError(ctypes.get_last_error())
        code = wintypes.DWORD()
        if not self._kernel.GetExitCodeProcess(self._handle, ctypes.byref(code)):
            raise ctypes.WinError(ctypes.get_last_error())
        return code.value

    def close(self):
        if self._handle:
            if not self._kernel.CloseHandle(self._handle):
                raise ctypes.WinError(ctypes.get_last_error())
            self._handle = None


class Job:
    """Job with kill-on-close, active process cap and job commit-memory cap."""
    def __init__(self, *, memory_bytes, active_processes):
        if os.name != 'nt':
            raise OSError('Windows Job Object unavailable')
        if (type(memory_bytes) is not int or not 1 <= memory_bytes <= 1024 * 1024 * 1024 or
                type(active_processes) is not int or not 1 <= active_processes <= 8):
            raise ValueError('invalid job limits')
        self._kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        self._kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        self._kernel.CreateJobObjectW.restype = wintypes.HANDLE
        self._kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        self._kernel.SetInformationJobObject.restype = wintypes.BOOL
        self._kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        self._kernel.AssignProcessToJobObject.restype = wintypes.BOOL
        self._kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        self._kernel.CloseHandle.restype = wintypes.BOOL
        self._handle = self._kernel.CreateJobObjectW(None, None)
        if not self._handle:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            limits = _ExtendedLimits()
            limits.BasicLimitInformation.LimitFlags = 0x2000 | 0x0200 | 0x0008
            limits.BasicLimitInformation.ActiveProcessLimit = active_processes
            limits.JobMemoryLimit = memory_bytes
            if not self._kernel.SetInformationJobObject(self._handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
                raise ctypes.WinError(ctypes.get_last_error())
        except BaseException:
            self.close()
            raise

    def spawn(self, argv, *, pipes=False):
        """Create inside this job using JOB_LIST, then resume the primary thread.

        Only three explicitly listed stdio handles can be inherited. The executable
        must be a locally anchored, single-link file. No filesystem sandbox is implied.
        """
        import msvcrt
        import ntpath
        import re
        import subprocess
        from ..effect_library import _native_windows as native
        if (not self._handle or not isinstance(argv, list) or not argv or
                any(not isinstance(a, str) or '\x00' in a for a in argv)):
            raise ValueError('invalid job or arguments')
        executable = ntpath.normpath(argv[0])
        drive, tail = ntpath.splitdrive(executable)
        if not re.fullmatch(r'[A-Za-z]:', drive) or not tail.startswith('\\') or '..' in argv[0].replace('/', '\\').split('\\'):
            raise ValueError('executable must be an absolute local path')
        parent, name = ntpath.split(executable)
        k = self._kernel
        k.InitializeProcThreadAttributeList.argtypes = [ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.c_size_t)]
        k.InitializeProcThreadAttributeList.restype = wintypes.BOOL
        k.UpdateProcThreadAttribute.argtypes = [ctypes.c_void_p, wintypes.DWORD, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p]
        k.UpdateProcThreadAttribute.restype = wintypes.BOOL
        k.DeleteProcThreadAttributeList.argtypes = [ctypes.c_void_p]
        k.DeleteProcThreadAttributeList.restype = None
        k.CreateProcessW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, ctypes.c_void_p, ctypes.c_void_p,
                                     wintypes.BOOL, wintypes.DWORD, ctypes.c_void_p, wintypes.LPCWSTR,
                                     ctypes.POINTER(_StartupInfoEx), ctypes.POINTER(_ProcessInformation)]
        k.CreateProcessW.restype = wintypes.BOOL
        k.ResumeThread.argtypes = [wintypes.HANDLE]
        k.ResumeThread.restype = wintypes.DWORD
        k.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
        k.TerminateProcess.restype = wintypes.BOOL
        k.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        k.WaitForSingleObject.restype = wintypes.DWORD
        k.GetWindowsDirectoryW.argtypes = [wintypes.LPWSTR, wintypes.UINT]
        k.GetWindowsDirectoryW.restype = wintypes.UINT
        k.GetSystemDirectoryW.argtypes = [wintypes.LPWSTR, wintypes.UINT]
        k.GetSystemDirectoryW.restype = wintypes.UINT
        win_dir, sys_dir = ctypes.create_unicode_buffer(32768), ctypes.create_unicode_buffer(32768)
        for function, buffer in ((k.GetWindowsDirectoryW, win_dir), (k.GetSystemDirectoryW, sys_dir)):
            length = function(buffer, len(buffer))
            if not length or length >= len(buffer):
                raise ctypes.WinError(ctypes.get_last_error())
        environment = ctypes.create_unicode_buffer('PATH=' + sys_dir.value + '\0SystemRoot=' + win_dir.value + '\0WINDIR=' + win_dir.value + '\0\0')
        all_fds = []
        parent_fds = []
        child_fds = []
        attribute_list = None
        initialized = False
        info = _ProcessInformation()
        transferred = False
        streams = []
        try:
            if pipes:
                stdin_read, stdin_write = os.pipe()
                all_fds.extend((stdin_read, stdin_write))
                stdout_read, stdout_write = os.pipe()
                all_fds.extend((stdout_read, stdout_write))
                stderr_read, stderr_write = os.pipe()
                all_fds.extend((stderr_read, stderr_write))
                parent_fds = [stdin_write, stdout_read, stderr_read]
                child_fds = [stdin_read, stdout_write, stderr_write]
            size = ctypes.c_size_t()
            count = 2 if pipes else 1
            k.InitializeProcThreadAttributeList(None, count, 0, ctypes.byref(size))
            if not size.value:
                raise ctypes.WinError(ctypes.get_last_error())
            buffer = ctypes.create_string_buffer(size.value)
            attribute_list = ctypes.cast(buffer, ctypes.c_void_p)
            if not k.InitializeProcThreadAttributeList(attribute_list, count, 0, ctypes.byref(size)):
                raise ctypes.WinError(ctypes.get_last_error())
            initialized = True
            handle = wintypes.HANDLE(self._handle)
            if not k.UpdateProcThreadAttribute(attribute_list, 0, 0x0002000D, ctypes.byref(handle), ctypes.sizeof(handle), None, None):
                raise ctypes.WinError(ctypes.get_last_error())
            startup = _StartupInfoEx()
            startup.StartupInfo.cb = ctypes.sizeof(startup)
            startup.lpAttributeList = attribute_list
            if pipes:
                child_handles = (wintypes.HANDLE * 3)(*(msvcrt.get_osfhandle(fd) for fd in child_fds))
                if not k.UpdateProcThreadAttribute(attribute_list, 0, 0x00020002, child_handles, ctypes.sizeof(child_handles), None, None):
                    raise ctypes.WinError(ctypes.get_last_error())
                startup.StartupInfo.dwFlags |= 0x00000100
                startup.StartupInfo.hStdInput, startup.StartupInfo.hStdOutput, startup.StartupInfo.hStdError = child_handles
            command = ctypes.create_unicode_buffer(subprocess.list2cmdline(argv))
            flags = 0x00080000 | 0x00000004 | 0x08000000 | 0x00000400
            with native.open_root_chain_read(parent) as (root, stack):
                native._reader_open_relative(root, stack, name, native._reader_close_relative)
                try:
                    for fd in child_fds:
                        os.set_inheritable(fd, True)
                    if not k.CreateProcessW(executable, command, None, None, bool(pipes), flags, environment, sys_dir.value,
                                            ctypes.byref(startup), ctypes.byref(info)):
                        raise ctypes.WinError(ctypes.get_last_error())
                finally:
                    restore_errors = []
                    for fd in child_fds:
                        try:
                            os.set_inheritable(fd, False)
                        except OSError as exc:
                            restore_errors.append(exc)
                    if restore_errors:
                        raise OSError('unable to restore pipe inheritance') from restore_errors[0]
            for fd in child_fds:
                all_fds.remove(fd)
                os.close(fd)
            if pipes:
                for fd, mode in zip(parent_fds, ('wb', 'rb', 'rb')):
                    stream = _Pipe(fd)
                    streams.append(stream)
                    all_fds.remove(fd)
            prior_count = k.ResumeThread(info.hThread)
            if prior_count == 0xffffffff:
                resume_error = ctypes.get_last_error()
                raise ctypes.WinError(resume_error)
            if prior_count != 1:
                raise OSError('unexpected primary thread suspend count')
            owned = _OwnedProcess(k, info.hProcess, info.dwProcessId)
            if pipes:
                owned.stdin, owned.stdout, owned.stderr = streams
            transferred = True
            return owned
        finally:
            import sys
            active_error = sys.exc_info()[1]
            cleanup_errors = []
            stream_fds = {stream.fileno() for stream in streams if not stream.closed}
            def cleanup(action):
                try:
                    action()
                except BaseException as exc:
                    cleanup_errors.append(exc)
            if info.hProcess and not transferred:
                def terminate_and_close():
                    if not k.TerminateProcess(info.hProcess, 1) and k.WaitForSingleObject(info.hProcess, 0) != 0:
                        raise OSError('unable to terminate suspended child')
                    if k.WaitForSingleObject(info.hProcess, 5000) != 0:
                        raise OSError('unable to reap suspended child')
                cleanup(terminate_and_close)
                cleanup(lambda: k.CloseHandle(info.hProcess) or (_ for _ in ()).throw(OSError('process handle close failed')))
            if info.hThread:
                cleanup(lambda: k.CloseHandle(info.hThread) or (_ for _ in ()).throw(OSError('thread handle close failed')))
            if not transferred:
                for stream in streams:
                    cleanup(stream.close)
            for fd in all_fds:
                if fd not in stream_fds:
                    cleanup(lambda fd=fd: os.close(fd))
            if initialized:
                cleanup(lambda: k.DeleteProcThreadAttributeList(attribute_list))
            if cleanup_errors:
                if transferred:
                    cleanup(self.close)
                    cleanup(lambda: k.CloseHandle(info.hProcess))
                    for stream in streams:
                        cleanup(stream.close)
                if active_error is not None and hasattr(active_error, 'add_note'):
                    active_error.add_note('one or more Windows job cleanup operations failed')
                else:
                    raise OSError('Windows job cleanup failed') from cleanup_errors[0]

    def close(self):
        if self._handle:
            if not self._kernel.CloseHandle(self._handle):
                raise ctypes.WinError(ctypes.get_last_error())
            self._handle = None
