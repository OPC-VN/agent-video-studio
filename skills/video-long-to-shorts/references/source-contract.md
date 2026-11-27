# Hợp đồng dữ liệu: `source-map.json`, `beats.json`, `subs.json`

> **Kết luận:** mọi bước sau bước 1 chỉ đọc `source-map.json`, không đọc lại composition nguồn. Repo giữ **hợp đồng trung tính** và bộ đọc HyperFrames chung; bộ đọc định dạng riêng của một tập (bảng thời gian tự chế, tên class riêng) viết ở trạm và xuất ra đúng hợp đồng này.

## Contents
- `source-map.json`
- Bộ đọc HyperFrames chung nhận gì
- Nguồn không khớp bộ đọc
- `beats-plan.json` và `beats.json`
- `asr-words.json`
- `subs.json`

## `source-map.json`

```json
{
  "schema_version": 1,
  "source": "index.html",
  "duration": 560.07,
  "time_base": "timeline",
  "word_time_kind": "display_cue",
  "sections": [{"id": "c14", "class": "scene", "start": 216.05, "end": 244.93}],
  "audio": [{"id": "voiceB", "src": "assets/voice.wav", "start": 353.3, "end": 445.3,
             "media_start": 339.7, "volume": 1.0}],
  "videos": [{"id": "take10", "src": "assets/avatar/take10.webm", "start": 445.6, "end": 466.6,
              "media_start": 0.0, "avatar": true}],
  "lines": [{"id": "k96", "text": "…", "start": 251.82, "end": 253.4, "word_ids": ["k96w0", "k96w1"]}],
  "words": [{"id": "k96w0", "text": "mặc", "line": "k96", "t": 251.82}],
  "warnings": []
}
```

| Trường | Bắt buộc | Nghĩa |
|---|---|---|
| `schema_version` | có | `1` |
| `source` | có | **tên file** nguồn, không phải đường dẫn (file này có thể được chia sẻ) |
| `duration` | không | giây của bản dài nếu composition khai |
| `time_base` | có | `timeline`: mọi mốc là giây trên timeline bản dài |
| `word_time_kind` | có | `display_cue` (mốc tô chữ, có thể lệch giọng) hoặc `speech` (mốc từ nhận dạng giọng đã quy về timeline) |
| `audio[]` | có | `id`, `src` (tương đối so với thư mục nguồn), `start`, `end`, `media_start`, `volume` |
| `videos[]` | không | như audio, thêm `avatar` (đúng/sai) |
| `sections[]` | không | cảnh của bản dài; dùng để biết beat thuộc cảnh nào, lấy icon nào |
| `lines[]` | có | dòng lời: `id` ổn định, `text`, `start`, `end` (có thể `null`), `word_ids` |
| `words[]` | có | `id` ổn định, `text` **nguyên văn kể cả dấu câu**, `line`, `t` (có thể `null`) |

Quy đổi duy nhất: `giây trong file = t − start + media_start` của clip phủ `t`. `id` của dòng và từ là **mã trích dẫn**: kế hoạch, phụ đề và báo cáo dẫn lời bằng mã này.

## Bộ đọc HyperFrames chung nhận gì

`scripts/source_map.py` đọc:

- `section`, `audio`, `video` có `data-start` + `data-duration` (+ `data-media-start`, `data-volume`);
- dòng lời = phần tử có `id` và class `--line-class` (mặc định `kara`); từ = phần tử con có `id` và class `--word-class` (mặc định `w`);
- mốc từ = vị trí của lệnh GSAP **đầu tiên** nhắm `'#<id từ>'` dạng `.to('#id',{…},T)`, `.set(…)`, `.fromTo('#id',{…},{…},T)`;
- avatar = video có class `--avatar-class` (mặc định `avatar`) hoặc `data-role="avatar"`.

Nó không đọc: mốc đặt bằng nhãn (`'label+=0.2'`), vị trí tương đối (`'<'`, `'>'`), mảng dựng bằng vòng lặp trong JavaScript, phụ đề đốt sẵn vào video. Gặp các trường hợp đó `t` là `null` và mã thoát là 1.

## Nguồn không khớp bộ đọc

| Nguồn có | Cách ra hợp đồng |
|---|---|
| HyperFrames, class khác | truyền `--line-class` / `--word-class` / `--avatar-class` |
| HyperFrames, mốc đặt bằng nhãn hoặc bảng thời gian riêng | chạy bộ đọc chung lấy clip + chữ; bộ chuyển ở trạm điền `t` từ bảng riêng |
| Chỉ có file giọng + bản lời | nhận dạng giọng cấp từ → `words[].t` với `word_time_kind: "speech"`; `audio[]` một clip `start: 0` |
| Có SRT/VTT | mỗi cue một dòng; từ chia đều trong cue, đánh dấu `display_cue` |
| Chỉ có mp4 | ngoài phạm vi skill (không dựng lại được từ nguồn); chuyển `video-edit` |

Bộ chuyển viết ở trạm phải giữ chữ nguyên văn và không ghi đường dẫn tuyệt đối vào file.

## `beats-plan.json` và `beats.json`

Plan (người/agent viết, mẫu `assets/templates/beats.json`):

```json
{"lead": 0.30, "gap": 0.30, "fade_ms": 25, "tail": 2.4,
 "segments": [{"id": "S1", "tl_in": 246.92, "tl_out": 254.95, "clip": "voice",
               "first_word": "k93w7", "last_word": "k97w5", "gap_after": 0.30,
               "note": "vào tại trũng −25 dB, cần người nghe"}]}
```

Kết quả (`cut_voice.py` ghi): thêm cho mỗi đoạn `clip`, `src`, `media_in`, `media_out`, `short_in`, `short_out`, `avatar` (`id`, `src`, `media_start`, `covers_segment` hoặc `null`); mức file có `total`, `sample_rate`, `channels`, `peak`. Mọi bước dựng đọc mốc từ `beats.json`, không tự tính lại.

## `asr-words.json`

Mảng `[start, end, "từ"]` theo giây của `voice.wav`, từ công cụ nhận dạng giọng của trạm. Chữ ở đây **không bao giờ lên hình**; chỉ mượn mốc.

## `subs.json`

```json
{"schema_version": 1, "timing": "asr", "words_total": 96, "words_interpolated": 3,
 "subs": [{"segment": "S1", "t0": 0.30, "t1": 1.62, "text": "ngoài nhóm cũ thì",
           "words": [["ngoài", 0.30], ["nhóm", 0.71], ["cũ", 1.02], ["thì", 1.24]]}],
 "warnings": []}
```

`timing: "source"` nghĩa là mốc chưa đối chiếu giọng: chỉ dùng cho bản nháp, không dùng cho bản gửi Cổng 2.
