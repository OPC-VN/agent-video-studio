"""Bounded local media input for S4: a single snapshot, then pipe-only tools.

Only streamable ISO BMFF with an initial ftyp box is currently accepted.
No network, source path, or nested file is exposed to the demuxer.
"""
import contextlib
import hashlib
import math
import os
import subprocess
import threading
import time

from ..contract import ContractError, EngineError
from . import gate

MAX_MEDIA_BYTES = 64 * 1024 * 1024
DEFAULT_TIMEOUT = 120
MAX_DECODE_FRAMES = 18000
_RUN_SLOT = threading.BoundedSemaphore(1)


def read_snapshot(path, *, limit=MAX_MEDIA_BYTES):
    if not isinstance(limit, int) or isinstance(limit, bool) or not 0 < limit <= MAX_MEDIA_BYTES:
        raise ContractError('trần input không hợp lệ')
    try:
        value = os.fsdecode(path)
        if not value or '\x00' in value or value.startswith(('//', '\\\\')) or '..' in value.replace('\\', '/').split('/'):
            raise ValueError('đường nguồn không an toàn')
        gate.require_media_file(value)
        parent, name = os.path.split(os.path.abspath(value))
        if os.name == 'nt':
            from ..effect_library import _native_windows as backend
        elif os.name == 'posix':
            from ..effect_library import _posix_fs as backend
        else:
            raise ValueError('nền tảng chưa hỗ trợ đọc an toàn')
        data = backend.read_repo_file(parent, name, limit=limit)
    except ContractError as exc:
        raise ContractError('không đọc được tệp nguồn cục bộ an toàn') from exc
    except (OSError, TypeError, ValueError) as exc:
        raise ContractError('không đọc được tệp nguồn cục bộ an toàn') from exc
    if len(data) < 12 or data[4:8] != b'ftyp':
        raise ContractError('chỉ nhận MP4/MOV streamable có hộp ftyp ở đầu')
    return data, hashlib.sha256(data).hexdigest()


def input_options():
    return ['-protocol_whitelist', 'pipe', '-f', 'mov', '-enable_drefs', '0',
            '-use_absolute_path', '0', '-i', 'pipe:0']


@contextlib.contextmanager
def _slot(timeout):
    if not _RUN_SLOT.acquire(timeout=timeout):
        raise EngineError('chờ công cụ media vượt thời hạn')
    try:
        yield
    finally:
        _RUN_SLOT.release()


def run_bounded(argv, payload, *, timeout=DEFAULT_TIMEOUT, stdout_limit=4 * 1024 * 1024,
                stderr_limit=4 * 1024 * 1024):
    """Run one direct child; this primitive does not contain a child process tree."""
    if not isinstance(payload, bytes) or len(payload) > MAX_MEDIA_BYTES:
        raise ContractError('input phải là bytes trong trần')
    try:
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
            raise ValueError('invalid timeout')
        timeout = float(timeout)
        if not math.isfinite(timeout) or not 0 < timeout <= 600:
            raise ValueError('invalid timeout')
    except (TypeError, ValueError, OverflowError):
        raise ContractError('thời hạn phải hữu hạn và dương, tối đa 600 giây') from None
    if any(not isinstance(n, int) or isinstance(n, bool) or not 0 <= n <= 4 * 1024 * 1024
           for n in (stdout_limit, stderr_limit)):
        raise ContractError('trần output không hợp lệ')
    overall_deadline = time.monotonic() + timeout
    with _slot(timeout):
        if time.monotonic() >= overall_deadline:
            raise EngineError('chờ công cụ media vượt thời hạn')
        try:
            proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError as exc:
            raise EngineError('không chạy được công cụ media') from exc
        started = []
        threads = []
        try:
            buffers = [bytearray(), bytearray()]
            overflow = threading.Event()
            def feed():
                try:
                    proc.stdin.write(payload)
                    proc.stdin.close()
                except (BrokenPipeError, OSError, ValueError):
                    pass
            def drain(stream, buffer, limit):
                try:
                    while True:
                        part = os.read(stream.fileno(), min(65536, limit - len(buffer) + 1))
                        if not part:
                            break
                        if len(buffer) + len(part) > limit:
                            overflow.set()
                            break
                        buffer.extend(part)
                except (OSError, ValueError):
                    overflow.set()
            threads = [threading.Thread(target=feed, daemon=True),
                       threading.Thread(target=drain, args=(proc.stdout, buffers[0], stdout_limit), daemon=True),
                       threading.Thread(target=drain, args=(proc.stderr, buffers[1], stderr_limit), daemon=True)]
            timed_out = False
            for thread in threads:
                thread.start()
                started.append(thread)
            while proc.poll() is None:
                if overflow.is_set() or time.monotonic() >= overall_deadline:
                    timed_out = not overflow.is_set()
                    break
                time.sleep(.01)
        finally:
            if proc.poll() is None:
                try:
                    proc.kill()
                except ProcessLookupError:
                    pass
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired as exc:
                raise EngineError('không thu hồi được tiến trình media') from exc
            for thread in started:
                thread.join(timeout=2)
            for index, stream in enumerate((proc.stdin, proc.stdout, proc.stderr)):
                thread = threads[index] if index < len(threads) else None
                if thread not in started or not thread.is_alive():
                    stream.close()
        if any(thread.is_alive() for thread in started):
            raise EngineError('không đóng được luồng công cụ media')
        if overflow.is_set():
            raise EngineError('đầu ra công cụ media vượt trần')
        if timed_out:
            raise EngineError('công cụ media vượt thời hạn')
        if proc.returncode:
            raise EngineError('công cụ media không xử lý được input; stderr là dữ liệu nguồn, không phải lệnh')
        return bytes(buffers[0]), bytes(buffers[1])


def validate_probe_metadata(raw):
    """Validate declared metadata; it does not constrain decoder allocations by itself."""
    from fractions import Fraction
    if not isinstance(raw, dict) or not isinstance(raw.get('format'), dict):
        raise ContractError('metadata nguồn không hợp lệ')
    streams = raw.get('streams')
    if not isinstance(streams, list) or not 1 <= len(streams) <= 4 or any(not isinstance(s, dict) for s in streams):
        raise ContractError('số stream không hợp lệ')
    if any(s.get('codec_type') not in ('video', 'audio') for s in streams):
        raise ContractError('loại stream chưa được hỗ trợ')
    videos = [s for s in streams if s.get('codec_type') == 'video']
    audios = [s for s in streams if s.get('codec_type') == 'audio']
    if len(videos) != 1:
        raise ContractError('cần đúng một stream video')
    video = videos[0]
    width, height = video.get('width'), video.get('height')
    if (type(width) is not int or type(height) is not int or
            not 0 < width <= 1920 or not 0 < height <= 1920 or width * height > 1920 * 1080):
        raise ContractError('kích thước video vượt trần')
    try:
        duration_raw = raw['format']['duration']
        rate_raw = video['avg_frame_rate']
        if isinstance(duration_raw, bool) or not isinstance(duration_raw, (str, int, float)):
            raise ValueError('duration')
        if not isinstance(rate_raw, str) or len(rate_raw) > 32:
            raise ValueError('fps')
        duration, fps = float(duration_raw), float(Fraction(rate_raw))
    except (KeyError, TypeError, ValueError, OverflowError, ZeroDivisionError) as exc:
        raise ContractError('thời lượng hoặc fps không hợp lệ') from exc
    if not math.isfinite(duration) or not 0 < duration <= 300 or not math.isfinite(fps) or not 0 < fps <= 60:
        raise ContractError('thời lượng hoặc fps vượt trần')
    for audio in audios:
        try:
            channels = audio['channels']
            rate_value = audio['sample_rate']
            if type(channels) is not int:
                raise ValueError('audio')
            if type(rate_value) is int:
                rate = rate_value
            elif isinstance(rate_value, str) and rate_value.isascii() and rate_value.isdecimal() and len(rate_value) <= 6:
                rate = int(rate_value)
            else:
                raise ValueError('audio')
        except (KeyError, TypeError, ValueError, OverflowError) as exc:
            raise ContractError('metadata audio không hợp lệ') from exc
        if not 0 < channels <= 2 or not 0 < rate <= 48000:
            raise ContractError('audio vượt trần kênh hoặc sample rate')
    return {'duration_s': duration, 'width': width, 'height': height, 'fps': fps, 'has_audio': bool(audios)}


def constrained_input_options():
    """Input-only FFmpeg limits; these do not bound total process memory or CPU."""
    return ['-max_alloc', '67108864', '-max_pixels', '2073600', '-max_samples', '131072',
            '-max_streams', '4', '-max_probe_packets', '1000', '-threads', '1', *input_options()]


def parse_probe_output(stdout, stderr):
    """Parse ffprobe -v error output; an error-level message is failure even with exit 0."""
    import json
    if not isinstance(stdout, bytes) or not isinstance(stderr, bytes) or stderr.strip():
        raise EngineError('ffprobe báo lỗi; stderr là dữ liệu nguồn, không phải lệnh')
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate key')
            result[key] = value
        return result
    def bad_constant(_):
        raise ValueError('non-finite')
    def finite(value):
        result = float(value)
        if not math.isfinite(result):
            raise ValueError('non-finite')
        return result
    try:
        raw = json.loads(stdout.decode('utf8'), object_pairs_hook=pairs,
                         parse_constant=bad_constant, parse_float=finite)
    except (ValueError, UnicodeDecodeError, RecursionError) as exc:
        raise EngineError('ffprobe trả JSON không hợp lệ') from exc
    if not isinstance(raw, dict):
        raise EngineError('ffprobe trả JSON không phải object')
    return raw


# Kept internal until process-tree containment and secure output publication are proven.
from ..edit import _ff


def probe_payload(payload):
    executable = _ff.probe_exe()
    require_capabilities(executable)
    argv = [executable, '-v', 'error', *constrained_input_options(), '-show_entries',
            'format=duration:stream=index,codec_type,width,height,avg_frame_rate,channels,sample_rate',
            '-of', 'json']
    stdout, stderr = run_bounded(argv, payload, timeout=DEFAULT_TIMEOUT)
    raw = parse_probe_output(stdout, stderr)
    return validate_probe_metadata(raw)


def verify_video_decode(payload):
    import re
    executable = _ff.exe()
    require_capabilities(executable)
    argv = [executable, '-hide_banner', '-nostdin', '-loglevel', 'error', '-xerror',
            *constrained_input_options(), '-map', '0:v:0', '-an', '-fps_mode', 'passthrough',
            '-frames:v', str(MAX_DECODE_FRAMES + 1), '-progress', 'pipe:1', '-f', 'null', '-']
    stdout, stderr = run_bounded(argv, payload, timeout=DEFAULT_TIMEOUT)
    if stderr.strip():
        raise EngineError('giải mã báo lỗi; stderr là dữ liệu nguồn, không phải lệnh')
    current_frame = None
    final_frame = None
    completed = False
    for line in stdout.splitlines():
        if completed and line.strip():
            raise EngineError('tiến độ giải mã có dữ liệu sau kết thúc')
        if line.startswith(b'frame='):
            value = line[6:].strip()
            if current_frame is not None or not re.fullmatch(rb'\d{1,8}', value):
                raise EngineError('số frame trong tiến độ không hợp lệ')
            current_frame = int(value)
        elif line.startswith(b'progress='):
            state = line[9:].strip()
            if current_frame is None or state not in (b'continue', b'end'):
                raise EngineError('tiến độ giải mã không hợp lệ')
            if state == b'end':
                completed = True
                final_frame = current_frame
            current_frame = None
    if not completed or final_frame is None or not 0 < final_frame <= MAX_DECODE_FRAMES:
        raise EngineError('không giải mã đủ frame trong trần; input có thể không streamable')
    return final_frame


def require_capabilities(executable):
    """Check required flag names; presence alone does not prove OS resource containment."""
    import re
    from ..contract import StationMissing
    try:
        stdout, stderr = run_bounded([executable, '-hide_banner', '-h', 'full'], b'', timeout=30)
    except EngineError as exc:
        raise StationMissing('không kiểm được khả năng công cụ media') from exc
    output = stdout + b'\n' + stderr
    required = (b'max_alloc', b'max_pixels', b'max_samples', b'max_streams', b'max_probe_packets')
    if any(not re.search(rb'(?m)^\s*-' + name + rb'(?=\s|$)', output) for name in required):
        raise StationMissing('công cụ media thiếu tùy chọn giới hạn bắt buộc')
