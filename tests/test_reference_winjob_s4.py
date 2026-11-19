"""Windows job smoke: only processes explicitly attached are contained."""
import os
import subprocess
import sys
import time

import pytest

pytestmark = pytest.mark.skipif(os.name != 'nt', reason='Windows Job Object only')


def test_atomic_job_list_creates_child_inside_job(tmp_path):
    from video_studio.reference._winjob_s4 import Job
    marker = tmp_path / 'marker'
    job = Job(memory_bytes=512 * 1024 * 1024, active_processes=4)
    try:
        child = job.spawn([sys.executable, '-c', 'import pathlib,sys;pathlib.Path(sys.argv[1]).write_text("ok")', str(marker)])
        try:
            assert child.wait(10) == 0
            assert marker.read_text() == 'ok'
        finally:
            child.close()
    finally:
        job.close()


def test_atomic_job_active_process_cap_blocks_grandchild(tmp_path):
    from video_studio.reference._winjob_s4 import Job
    marker = tmp_path / 'result'
    code = '''import pathlib,subprocess,sys
try:
    p=subprocess.Popen([sys.executable,'-c','pass'])
except OSError:
    pathlib.Path(sys.argv[1]).write_text('blocked')
else:
    p.wait(); pathlib.Path(sys.argv[1]).write_text('started')
'''
    job = Job(memory_bytes=512 * 1024 * 1024, active_processes=1)
    try:
        child = job.spawn([sys.executable, '-c', code, str(marker)])
        try:
            assert child.wait(10) == 0
            assert marker.read_text() == 'blocked'
        finally:
            child.close()
    finally:
        job.close()


def test_atomic_job_memory_cap_has_unconstrained_control():
    from video_studio.reference._winjob_s4 import Job
    for limit, expected_success in [(128, False), (512, True)]:
        job = Job(memory_bytes=limit * 1024 * 1024, active_processes=2)
        try:
            child = job.spawn([sys.executable, '-c', 'x=bytearray(256*1024*1024)'])
            try:
                assert (child.wait(20) == 0) is expected_success
            finally:
                child.close()
        finally:
            job.close()


def test_job_close_does_not_terminate_unrelated_process():
    from video_studio.reference._winjob_s4 import Job
    unrelated = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(30)'])
    job = Job(memory_bytes=512 * 1024 * 1024, active_processes=2)
    try:
        child = job.spawn([sys.executable, '-c', 'import time;time.sleep(30)'])
        try:
            job.close()
            child.wait(10)
            assert unrelated.poll() is None
        finally:
            child.close()
    finally:
        job.close()
        if unrelated.poll() is None:
            unrelated.terminate()
            unrelated.wait(timeout=5)


def test_atomic_job_rejects_relative_executable():
    from video_studio.reference._winjob_s4 import Job
    job = Job(memory_bytes=512 * 1024 * 1024, active_processes=2)
    try:
        with pytest.raises(ValueError):
            job.spawn(['python', '-c', 'pass'])
    finally:
        job.close()


def test_owned_process_rejects_invalid_wait_timeout():
    from video_studio.reference._winjob_s4 import Job
    job = Job(memory_bytes=512 * 1024 * 1024, active_processes=2)
    try:
        child = job.spawn([sys.executable, '-c', 'pass'])
        try:
            for bad in (-1, float('inf'), True, 10**1000):
                with pytest.raises(ValueError): child.wait(bad)
        finally:
            child.close()
    finally:
        job.close()


def test_atomic_job_close_kills_grandchild(tmp_path):
    import ctypes
    from ctypes import wintypes
    from video_studio.reference._winjob_s4 import Job
    marker = tmp_path / 'grandchild.pid'
    code = ('import subprocess,sys,time; '
            'p=subprocess.Popen([sys.executable,"-c","import time;time.sleep(30)"]); '
            'open(sys.argv[1],"w").write(str(p.pid)); time.sleep(30)')
    job = Job(memory_bytes=512 * 1024 * 1024, active_processes=4)
    child = None
    try:
        child = job.spawn([sys.executable, '-c', code, str(marker)])
        for _ in range(100):
            if marker.exists() and marker.read_text().strip():
                break
            time.sleep(.05)
        assert marker.exists()
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel.WaitForSingleObject.restype = wintypes.DWORD
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        grandchild = kernel.OpenProcess(0x00100000, False, int(marker.read_text()))
        assert grandchild
        try:
            assert kernel.WaitForSingleObject(grandchild, 0) == 258
            job.close()
            child.wait(10)
            assert kernel.WaitForSingleObject(grandchild, 10000) == 0
        finally:
            kernel.CloseHandle(grandchild)
    finally:
        job.close()
        if child is not None:
            child.close()


def test_job_dies_when_owner_process_exits_abruptly(tmp_path):
    import ctypes
    from ctypes import wintypes
    marker, signal = tmp_path / 'child.pid', tmp_path / 'release'
    code = '''import os,pathlib,sys,time
from video_studio.reference._winjob_s4 import Job
job=Job(memory_bytes=512*1024*1024,active_processes=2)
child=job.spawn([sys.executable,'-c','import time;time.sleep(30)'])
pathlib.Path(sys.argv[1]).write_text(str(child.pid))
while not pathlib.Path(sys.argv[2]).exists(): time.sleep(.02)
os._exit(0)
'''
    owner = subprocess.Popen([sys.executable, '-c', code, str(marker), str(signal)])
    try:
        for _ in range(100):
            if marker.exists() and marker.read_text().strip():
                break
            time.sleep(.05)
        assert marker.exists()
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel.WaitForSingleObject.restype = wintypes.DWORD
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.OpenProcess(0x00100000, False, int(marker.read_text()))
        assert handle
        try:
            assert kernel.WaitForSingleObject(handle, 0) == 258
            signal.write_text('go')
            assert owner.wait(timeout=10) == 0
            assert kernel.WaitForSingleObject(handle, 10000) == 0
        finally:
            kernel.CloseHandle(handle)
    finally:
        if owner.poll() is None:
            owner.kill()
            owner.wait(timeout=5)


def test_atomic_job_pipes_round_trip():
    from video_studio.reference._winjob_s4 import Job
    job = Job(memory_bytes=512 * 1024 * 1024, active_processes=2)
    child = None
    try:
        child = job.spawn([sys.executable, '-c', 'import sys;d=sys.stdin.buffer.read();sys.stdout.buffer.write(d);sys.stderr.write("done")'], pipes=True)
        child.stdin.write(b'hello'); child.stdin.close()
        assert child.wait(10) == 0
        assert child.stdout.read() == b'hello' and child.stderr.read() == b'done'
    finally:
        job.close()
        if child is not None:
            for stream in (child.stdin, child.stdout, child.stderr):
                if not stream.closed: stream.close()
            child.close()


def test_job_child_gets_only_listed_handles_and_no_parent_env(monkeypatch, tmp_path):
    import msvcrt
    from video_studio.reference._winjob_s4 import Job
    monkeypatch.setenv('S4_SYNTHETIC_SENTINEL', 'should-not-be-inherited')
    path = tmp_path / 'sentinel.txt'
    path.write_text('unused', encoding='utf8')
    with path.open('rb') as sentinel:
        os.set_inheritable(sentinel.fileno(), True)
        numeric_handle = msvcrt.get_osfhandle(sentinel.fileno())
        code = ('import ctypes,os,sys; '
                'k=ctypes.WinDLL("kernel32",use_last_error=True); '
                'k.GetFileType.argtypes=[ctypes.c_void_p];k.GetFileType.restype=ctypes.c_uint; '
                'print(int("S4_SYNTHETIC_SENTINEL" in os.environ),k.GetFileType(int(sys.argv[1])))')
        job = Job(memory_bytes=512 * 1024 * 1024, active_processes=2)
        child = None
        try:
            child = job.spawn([sys.executable, '-c', code, str(numeric_handle)], pipes=True)
            child.stdin.close()
            assert child.wait(10) == 0
            assert child.stdout.read().strip() == b'0 0'
        finally:
            job.close()
            if child is not None:
                for stream in (child.stdin, child.stdout, child.stderr):
                    if not stream.closed: stream.close()
                child.close()


def test_owned_pipe_retries_short_write(monkeypatch):
    from video_studio.reference._winjob_s4 import _Pipe
    read_fd, write_fd = os.pipe()
    pipe = _Pipe(write_fd)
    original = os.write
    monkeypatch.setattr(os, 'write', lambda fd, data: original(fd, data[:2]))
    try:
        assert pipe.write(b'abcdef') == 6
        pipe.close()
        assert os.read(read_fd, 20) == b'abcdef'
    finally:
        pipe.close()
        os.close(read_fd)


def test_atomic_spawn_pipe_setup_cancellation_never_resumes_child(monkeypatch, tmp_path):
    from video_studio.reference import _winjob_s4 as module
    marker = tmp_path / 'must-not-run'
    created = []
    original = module._Pipe
    def fail_second(fd):
        if created:
            raise KeyboardInterrupt()
        pipe = original(fd)
        created.append(pipe)
        return pipe
    monkeypatch.setattr(module, '_Pipe', fail_second)
    job = module.Job(memory_bytes=512 * 1024 * 1024, active_processes=2)
    try:
        with pytest.raises(KeyboardInterrupt):
            job.spawn([sys.executable, '-c', 'import pathlib,sys;pathlib.Path(sys.argv[1]).touch()', str(marker)], pipes=True)
        assert created and created[0].closed
        assert not marker.exists()
    finally:
        job.close()
