"""Lệnh avatar chạy engine MuseTalk cục bộ."""

import argparse
from pathlib import Path

from . import contract


def _execute(args):
    from .musetalk import runner

    if args.action == "doctor":
        info = runner.doctor()
        if not info.get("ready", False):
            raise contract.StationMissing(info.get("reason") or "MuseTalk chưa sẵn sàng. Xem docs/MUSETALK.md.")
        contract.log("MuseTalk 1.5 sẵn sàng.")
        return info

    result = runner.run(args.source, args.audio, args.out, args.bbox_shift) or {}
    contract.log(f"Đã xuất avatar: {args.out}")
    return {**result, "output": str(args.out)}


def main(argv=None):
    parser = argparse.ArgumentParser(prog="video-studio avatar", description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    doctor = actions.add_parser("doctor", help="Kiểm engine, model và GPU")
    doctor.add_argument("--json", action="store_true")
    render = actions.add_parser("render", help="Ghép khẩu hình theo file âm thanh")
    render.add_argument("--source", "--video", required=True, type=Path, help="Ảnh hoặc video local")
    render.add_argument("--audio", required=True, type=Path, help="File WAV lời thoại")
    render.add_argument("--out", required=True, type=Path, help="File MP4 mới")
    render.add_argument("--bbox-shift", type=int, default=0,
                        help="Dịch điểm giữa mặt (px, -30..30): âm = miệng mở ít hơn, dương = mở nhiều hơn")
    render.add_argument("--json", action="store_true")
    args, rc = contract.parse(parser, argv)
    if args is None:
        return rc
    return contract.run(_execute, args, as_json=args.json)
