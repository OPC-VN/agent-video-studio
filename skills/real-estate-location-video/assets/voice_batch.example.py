#!/usr/bin/env python3
"""VÍ DỤ: thu lời dẫn theo từng câu (nạp engine MỘT lần), ghim seed, tự tăng tốc nếu vượt thời lượng cảnh.

Chạy bằng python của venv engine voice-studio:
    VOICE_STATION=<trạm giọng> <venv>/python voice_batch.py <thư mục ra> [profile] [seed]
Ra: <ra>/V*.wav + manifest.json (id, text, start, allot, dur, speed). Lời đã viết lại cho engine (tên tiếng Anh phiên âm,
số viết bằng chữ) theo voice-routing/vietnamese-tts-script.md.
"""
import json
import os
import sys

from voice_studio import engine, speak

LINES = [  # id, bắt đầu (s), thời lượng cảnh được phép (s), lời đọc
    ("V01", 1.0, 3.0, "Xoan Lếch Ôn-sen Rê-di-đần-xơ, ven hồ Thiên Nga."),
    ("V02", 4.0, 4.4, "Dự án thuộc tỉnh Hưng Yên mới, xã Phụng Công, khu đô thị Ê-cô-pác."),
    ("V03", 8.5, 5.4, "Phụng Công hơn bốn mươi lăm nghìn dân. Hưng Yên tăng trưởng hơn mười phần trăm nửa đầu năm hai không hai sáu."),
    ("V04", 14.0, 2.9, "Giờ dum dần vào đúng vị trí dự án."),
    ("V05", 17.0, 3.9, "Phía Bắc là hồ Thiên Nga; công viên cách chưa tới ba trăm mét chim bay."),
    ("V06", 21.0, 1.9, "Xung quanh là các phân khu Ê-cô-pác."),
    ("V07", 23.0, 4.9, "Nhìn khối ba chiều: bố cục các tòa tháp và mặt hồ."),
    ("V08", 28.0, 1.9, "Các tuyến đường bao quanh dự án."),
    ("V09", 30.0, 8.4, "Đường chim bay: bệnh viện Cu-su-mi một phẩy một cây số, Đại học Anh Quốc một phẩy ba, Vin-com Ô-sần Xi-ti bốn phẩy ba, cầu Thanh Trì năm phẩy năm."),
    ("V10", 38.5, 2.4, "Hồ Hoàn Kiếm: khoảng mười hai cây số chim bay."),
    ("V11", 41.0, 3.9, "Muốn xem kỹ hơn, hãy liên hệ ngay."),
]


def main():
    out = sys.argv[1]
    profile = sys.argv[2] if len(sys.argv) > 2 else None  # None = profile mặc định của trạm
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1234
    os.makedirs(out, exist_ok=True)
    model = engine.load()
    prof = speak.resolve_profile(profile)
    man = []
    for vid, start, allot, text in LINES:
        speed = 1.0
        for _ in range(3):
            wav, sr = speak.synthesize(text, prof, seed=seed, speed=speed, model=model)
            dur = len(wav) / float(sr)
            if dur <= allot or speed >= 1.3:
                break
            speed = round(min(1.3, speed * dur / allot * 1.03), 3)
        path = engine.save(wav, os.path.join(out, vid + ".wav"), sr)
        man.append({"id": vid, "text": text, "start": start, "allot": allot, "dur": round(dur, 3), "speed": speed, "fits": dur <= allot})
        print(json.dumps(man[-1], ensure_ascii=False), flush=True)
    json.dump(man, open(os.path.join(out, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
