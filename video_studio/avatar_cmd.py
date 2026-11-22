"""Lệnh avatar: doctor | render | optimize | qa | profile (LatentSync mặc định, MuseTalk bản nháp)."""

import argparse
from pathlib import Path

from . import contract

ENGINES = ("latentsync", "musetalk")


def _doctor(args):
    from .avatar import latentsync
    from .musetalk import runner

    wanted = ENGINES if args.engine == "all" else (args.engine,)
    checks = {"latentsync": latentsync.doctor, "musetalk": runner.doctor}
    info = {name: checks[name]() for name in wanted}
    ready = [name for name, item in info.items() if item.get("ready")]
    if not ready:
        reasons = "; ".join(f"{name}: {item.get('reason')}" for name, item in info.items())
        raise contract.StationMissing(f"Không engine avatar nào sẵn sàng ({reasons}). Xem docs/LATENTSYNC.md, docs/MUSETALK.md.")
    contract.log(f"Engine sẵn sàng: {', '.join(ready)}.")
    return {"engines": info, "ready": ready}


def _render(args):
    from .avatar import latentsync, profile
    from .musetalk import runner

    engine = dict(profile.DEFAULT_ENGINE)
    source = args.source
    if args.profile:
        gate = profile.for_render(args.profile)
        engine.update(gate["engine"])
        source = source or gate["clip"]
    if not source:
        raise contract.ContractError("Cần --source hoặc --profile.")
    name = args.engine or engine.get("name") or "latentsync"
    if name == "musetalk":
        shift = engine.get("bbox_shift", 0) if args.bbox_shift is None else args.bbox_shift
        result = runner.run(source, args.audio, args.out, shift) or {}
        result = {"engine": "musetalk", "bbox_shift": shift, **result}
    else:
        if args.bbox_shift:
            raise contract.ContractError("--bbox-shift chỉ dùng với --engine musetalk.")
        result = latentsync.render(
            source, args.audio, args.out,
            guidance=engine["guidance"] if args.guidance is None else args.guidance,
            steps=engine["steps"] if args.steps is None else args.steps,
            seed=engine["seed"] if args.seed is None else args.seed)
    contract.log(f"Đã xuất avatar: {args.out}. Bước tiếp: `avatar optimize --task mouth` (LatentSync) rồi `avatar qa`.")
    return {**result, "output": str(args.out), "profile": args.profile}


def _optimize(args):
    from .avatar import optimize

    if args.task == "normalize":
        result = optimize.normalize(args.input, args.out, crop=args.crop)
    else:
        result = optimize.restore_mouth(args.input, args.out, strength=args.strength)
    contract.log(f"Đã xuất: {args.out}")
    return {**result, "output": str(args.out)}


def _qa(args):
    from .avatar import latentsync, profile

    result = latentsync.syncnet(args.video)
    verdict = "ĐẠT" if result["passed"] else "CHƯA ĐẠT"
    contract.log(f"SyncNet: độ tin cậy {result['confidence']:.2f}, lệch {result['av_offset']} khung → {verdict} "
                 f"(cần lệch 0 và ≥ {result['threshold']['confidence']:g}). Vẫn phải soi mắt theo avatar-quality.")
    if args.profile:
        result["recorded"] = profile.record_qa(args.profile, args.video, result)
    return result


def _profile(args):
    from .avatar import profile

    if args.profile_action == "list":
        return profile.search(args.query)
    if args.profile_action == "show":
        return {"profile": profile.load(args.id)}
    if args.profile_action == "new":
        return profile.create(args.id, args.name, args.relation, args.consent_quote, args.scope,
                              clip=args.clip, voice=args.voice, crop=args.crop)
    if args.profile_action == "update":
        engine = {"name": args.engine, "guidance": args.guidance, "steps": args.steps, "seed": args.seed,
                  "mouth_strength": args.strength, "bbox_shift": args.bbox_shift}
        return profile.update(args.id, clip=args.clip, voice=args.voice, crop=args.crop, engine=engine)
    return profile.revoke(args.id)


def _execute(args):
    return {"doctor": _doctor, "render": _render, "optimize": _optimize, "qa": _qa,
            "profile": _profile}[args.action](args)


def _engine_options(parser):
    parser.add_argument("--guidance", type=float, help="LatentSync guidance (1.0-4.0, mặc định 2.5)")
    parser.add_argument("--steps", type=int, help="LatentSync số bước (10-60, mặc định 30)")
    parser.add_argument("--seed", type=int, help="LatentSync seed (mặc định 1247)")
    parser.add_argument("--bbox-shift", type=int, help="MuseTalk: dịch điểm giữa mặt (px, -30..30)")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="video-studio avatar", description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)

    doctor = actions.add_parser("doctor", help="Kiểm engine, model và GPU")
    doctor.add_argument("--engine", choices=("all",) + ENGINES, default="all")
    doctor.add_argument("--json", action="store_true")

    render = actions.add_parser("render", help="Ghép khẩu hình theo file WAV")
    render.add_argument("--engine", choices=ENGINES, help="latentsync (mặc định, bản dùng thật) | musetalk (bản nháp nhanh)")
    render.add_argument("--profile", help="Hồ sơ avatar trong trạm: lấy clip, tham số và kiểm đồng ý")
    render.add_argument("--source", "--video", type=Path, help="Ảnh hoặc video local (bỏ qua khi có --profile)")
    render.add_argument("--audio", required=True, type=Path, help="File WAV lời thoại")
    render.add_argument("--out", required=True, type=Path, help="File MP4 mới")
    _engine_options(render)
    render.add_argument("--json", action="store_true")

    optimize = actions.add_parser("optimize", help="normalize clip nền trước lip-sync | mouth làm nét miệng sau lip-sync")
    optimize.add_argument("--task", required=True, choices=("normalize", "mouth"))
    optimize.add_argument("--input", required=True, type=Path, help="Video vào")
    optimize.add_argument("--out", required=True, type=Path, help="File MP4 mới")
    optimize.add_argument("--crop", help="normalize: cắt W:H:X:Y theo pixel nguồn, ví dụ 720:720:0:180")
    optimize.add_argument("--strength", type=float, default=0.85, help="mouth: độ mạnh GFPGAN (0-1, mặc định 0.85)")
    optimize.add_argument("--json", action="store_true")

    qa = actions.add_parser("qa", help="Chấm SyncNet: đạt khi lệch 0 khung và độ tin cậy ≥ 7")
    qa.add_argument("--video", required=True, type=Path)
    qa.add_argument("--profile", help="Ghi kết quả vào lịch sử QA của hồ sơ")
    qa.add_argument("--json", action="store_true")

    prof = actions.add_parser("profile", help="Tìm, xem, tạo, cập nhật, thu hồi hồ sơ avatar trong trạm")
    sub = prof.add_subparsers(dest="profile_action", required=True)
    listing = sub.add_parser("list", help="Tìm hồ sơ theo id hoặc tên")
    listing.add_argument("query", nargs="?")
    show = sub.add_parser("show")
    show.add_argument("id")
    new = sub.add_parser("new", help="Tạo hồ sơ mới; bắt buộc có bản ghi đồng ý")
    new.add_argument("id")
    new.add_argument("--name", required=True)
    new.add_argument("--relation", required=True, choices=("self", "consented"))
    new.add_argument("--consent-quote", required=True, help="Nguyên văn lời đồng ý của người trong hình")
    new.add_argument("--scope", required=True, help="Phạm vi được dùng, ví dụ 'bài giảng nội bộ'")
    new.add_argument("--clip", type=Path, help="Clip nền đã duyệt (trong trạm)")
    new.add_argument("--voice", help="Tên profile giọng ở voice-studio")
    new.add_argument("--crop", help="Khung cắt đã chốt W:H:X:Y")
    update = sub.add_parser("update", help="Đổi clip, giọng, khung cắt hoặc tham số engine")
    update.add_argument("id")
    update.add_argument("--clip", type=Path)
    update.add_argument("--voice")
    update.add_argument("--crop")
    update.add_argument("--engine", choices=ENGINES)
    update.add_argument("--strength", type=float)
    _engine_options(update)
    revoke = sub.add_parser("revoke", help="Thu hồi đồng ý: hồ sơ không render được nữa")
    revoke.add_argument("id")
    for p in (listing, show, new, update, revoke):
        p.add_argument("--json", action="store_true")

    args, rc = contract.parse(parser, argv)
    if args is None:
        return rc
    return contract.run(_execute, args, as_json=args.json)
