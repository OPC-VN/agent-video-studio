# Phân rã âm thanh

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · skills/rea-video/references/audio.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Sản phẩm của công cụ: `audio` (số đo) và `audio_plan` (kết quả hợp nhất với VLM cùng phương án phục dựng) trong `breakdown.json`, cùng biểu đồ thời gian `audio.png`.

## Mức tin cậy

| Hạng mục | Phương pháp | Độ tin cậy (mẫu capsule-cinema) |
|---|---|---|
| Có hay không có giọng người | Điều chế âm tiết trên dải tần giọng (3–8 Hz), cộng với khoảng nghỉ giữa các câu | Cao |
| Có hay không có BGM | Giữa các đoạn thoại vẫn còn âm thanh to, có cao độ (tỉ lệ hài âm > 0.62); khi không có giọng người thì xét mức duy trì liên tục của hài âm; hoặc có chu kỳ nhịp rõ rệt. Đoạn chỉ có một cao độ duy nhất (âm thử, còi, tiếng ù điện có hài âm, dù có chút nhiễu nền) không tính là nhạc, ghi là `steady_tone` | Cao |
| BPM | Tự tương quan của đường bao khởi âm thành phần gõ, đồng thời đưa ra ứng viên nửa tốc/gấp đôi tốc; âm giữ đều, âm dài làm nền (gần như không có thành phần gõ) thì báo "không có nhịp rõ" và không cho BPM; thành phần gõ ít, chu kỳ cũng yếu (nền không có trống) cũng vậy | Cao (trứng vịt muối 110.0 so với giá trị thật 110.15) |
| Tông (key) | Chroma + profile tông Krumhansl | Trung bình khá (hai giá trị thật đều đúng: D major) |
| Chuyển đoạn nhạc | Đỉnh độ mới (novelty) của chroma và độ to (loudness) | Trung bình |
| Hiệu ứng âm thanh (SFX) | Transient rất nổi bật nằm ngoài đoạn có giọng, không trùng nhịp; khi có BGM thì yêu cầu transient còn nổi hơn; tại điểm transient phải có năng lượng gõ thật (nhiễu nén của âm ngân dài không tính), tiếng cụt do track bị cắt ở 0.1 giây cuối cũng không tính | **Thấp**: trong bản trộn giọng + BGM, đo thực tế precision ở tầng tín hiệu chỉ khoảng 0.2; hiệu ứng nhẹ gần như không đo được. Danh sách SFX lấy theo VLM |
| TTS hay người thật | Giao cho VLM | — |
| Giọng nam / nữ | Trung vị tần số cơ bản (< 150 Hz thiên nam, > 200 Hz thiên nữ) | Trung bình, chỉ tham khảo |
| Cắt theo nhịp nhạc | Tỉ lệ điểm cắt rơi đúng nhịp so với xác suất ngẫu nhiên | Trung bình khá |

## Tách track âm thanh

`decompose` mặc định tách âm thanh thành ba track, đặt trong `stems/` (`rea-video stems <video>` có thể chỉ chạy bước này):

| Tệp | Nội dung |
|---|---|
| `original.wav` | Âm gốc (bản trộn đầy đủ trong video) |
| `vocals.wav` | Giọng người đã tách (giọng khô): thuyết minh, lời nói trước camera, giọng hát. Lưu ý: tiếng gõ phím, các hiệu ứng dạng transient như tiếng "đinh" cũng sẽ nằm ở track này |
| `music.wav` | Nhạc nền + âm môi trường |
| `voice_S1.wav`, `voice_S2.wav` … | Khi có từ hai người nói trở lên, mỗi người một track: trong track giọng khô chỉ giữ các đoạn người đó nói, độ dài bằng bản gốc |

Mô hình là UVR MDX-Net Inst HQ 3 (ONNX, chạy CPU là đủ; lần chạy đầu tải khoảng 67 MB từ GitHub, lưu cache ở `~/.cache/rea-video/models`, có thể đổi vị trí bằng `REA_VIDEO_MODELS`). Đo thực tế: trên bản trộn TTS + BGM Suno, SDR khi tách đạt khoảng 19.7 dB; BGM thuần lọt vào track giọng là −42 dB. Tốc độ khoảng 0.6 lần thời gian thực (4 nhân).

Khi review, **nghe trực tiếp `vocals.wav` và `music.wav`**, dễ phán đoán hơn nghe bản trộn: giọng là hát hay nói, có phải TTS không, nhạc nền có lẫn giọng người không, phần kết có bị cắt cụt không.

### Người nói

Khi đã cài `rea-video[asr]`, `decompose` sẽ phân xem ai nói vào lúc nào trên track giọng khô; kết quả nằm trong `speakers` của `breakdown.json`:

- `speakers`: mỗi giọng (`S1`, `S2`… theo thứ tự xuất hiện) có số giây, tỉ lệ, tần số cơ bản và gợi ý nam / nữ; giọng chỉ xuất hiện vài giây được gắn `minor`.
- `turns`: thời điểm bắt đầu và kết thúc của từng đoạn cùng người nói; `overlaps`: các khoảng hai người nói cùng lúc.
- Lời thoại `speech.lines` mỗi câu có `speaker`; khi bật VLM, tên nhân vật được ghép với giọng theo thời gian (`name`).

Hai người có giọng rất giống nhau có thể bị gộp thành một, còn một người đổi giọng điệu có thể bị tách thành hai: khi số người quan trọng, hãy nghe track của từng người để xác nhận. Dùng `--no-speakers` để bỏ qua bước này.

## Nguồn gốc âm thanh: do AI tạo hay có sẵn?

**Kết luận một câu** nằm ở `sound_sources.summary_zh`, theo định dạng "loại video → nguồn giọng người / nhạc / hiệu ứng":

| Loại video | Giọng người | Nhạc | Hiệu ứng |
|---|---|---|---|
| MV ca nhạc / video dạng bài hát | Giọng hát nằm sẵn trong bài | **AI tạo** (Suno v.v.) là chính | Thư viện hiệu ứng |
| Video AI tự sinh tiếng | Do mô hình video sinh | Nhạc ghép ở hậu kỳ | Do mô hình video sinh |
| Quay thật | Tiếng thu trực tiếp / người thật lồng tiếng | Nhạc có sẵn | Tiếng thu trực tiếp |
| Thuyết minh/nói trước camera + nhạc nền | TTS hoặc người lồng tiếng | **Thư viện nhạc có sẵn** là chính (quy trình AI cũng hay dùng Suno làm nhạc lót) | Thư viện hiệu ứng |
| Chỉ có nhạc | — | Thư viện nhạc có sẵn | Thư viện hiệu ứng |

Sản phẩm của công cụ: `sound_sources` trong `breakdown.json` (music / voice / sfx, mỗi mục có `source`, `leaning`, `probs`, `evidence`, `how_to_confirm`).

### Bước 1: xem hình thức video trước (quyết định xác suất tiên nghiệm)

| Hình thức | Nhận biết | Xác suất tiên nghiệm về nguồn nhạc |
|---|---|---|
| **MV ca nhạc AI** (cả video là một bài hát có lời) | VLM cho format=MV; hoặc lớp tất định: nhạc phủ kín video (> 85%) **và giọng là hát** (`voice.style` = singing / rap_or_rhythmic, đo trên track giọng khô đã tách) | AI tạo 60% (nếu không bật VLM thì giảm còn 45%) |
| **Nhạc nền video thường** (thuyết minh/nói trước camera + BGM lót, hoặc chỉ có nhạc, không có giọng người) | Giọng là nói (`voice.style` = speech), hoặc không có giọng | Thư viện nhạc có sẵn 60% |

"Hát" và "nói" được xét trên **track giọng khô**, dựa trên hai tín hiệu:

- Cao độ ngân giữ (`sustained_note_ratio`): khi hát, giọng dừng ở một cao độ ≥ 160 ms; > 0.3 thì tính là hát. Thực tế: thuyết minh TTS đạt 0.14–0.15, rap đạt 0.24 (rap vốn không kéo dài nốt).
- Điệp khúc lặp (`chorus_repeat_share`): đoạn giai điệu giọng dài 4 giây xuất hiện lại sau mốc 6 giây. > 0.1 thì tính là bài hát (kể cả rap). Thực tế: MV rap AI đạt 0.26, thuyết minh TTS đạt 0.00. Với video ngắn chỉ cắt một đoạn, không có điệp khúc lặp, tín hiệu này mất tác dụng.

### Bước 2: hiệu chỉnh bằng bằng chứng

| Bằng chứng | Chỉ về | Trọng số |
|---|---|---|
| Lời hát nói đúng về nhân vật/sản phẩm/cốt truyện của chính video này (VLM `lyrics_match_content`) | AI tạo (bài hát đặt riêng) | Mạnh |
| VLM nhận ra tên bài (`song_guess`) | Bài hát nổi tiếng | Mạnh |
| Nhãn nhạc của nền tảng là tên bài cụ thể (`--meta`) | Bản nhạc có sẵn | Mạnh |
| Nhãn nền tảng là "âm thanh gốc do @tác giả sáng tác" | Không phải thư viện của nền tảng; với loại MV thường là bài AI | Trung bình |
| Nhạc cuối video đang ở mức âm lượng đầy thì bị cắt cứng | Bản nhạc có sẵn được trích một đoạn | Yếu |
| Nhạc và video cùng kết thúc | Làm riêng hoặc cắt theo độ dài video (cả hai khả năng đều có) | Rất yếu |
| Tệp có dấu nhận diện ẩn AIGC | Cả video có khai báo chứa nội dung AI | Rất yếu |

Khi xác suất cao nhất < 45%, xuất "chờ xác nhận" và đưa kèm xu hướng (`leaning`).

### Bẫy đã biết (bắt buộc nhắc trong câu trả lời)

**Video thông thường làm bằng quy trình AI cũng hay dùng BGM do Suno sinh** (các video của chính capsule-cinema như monkey_wine, trứng vịt muối, tổ chim đều vậy). Tiên nghiệm "nhạc nền thường = thư viện" sẽ sai với loại video này, và chỉ nghe bằng tai hay dựa vào đặc trưng tín hiệu thì không phân biệt được nhạc không lời của Suno với nhạc không lời của thư viện. Vì vậy kết luận về nhạc nền thường phải ghi là "nghiêng về thư viện, chờ xác nhận", kèm cách xác nhận:

1. Nhãn nhạc ở trang gốc của Douyin / Xiaohongshu (tốt nhất truyền qua `--meta`).
2. Tính năng nhận diện bài hát của Qishui Music (Soda Music) / QQ Music, hoặc ACRCloud: nhận ra được thì là bài có sẵn; không nhận ra thì **không có nghĩa là AI** (bản thư viện ít phổ biến cũng thường không nhận ra được).
3. Cảm nhận nghe: bài AI thường nhả chữ không rõ, dải cao mỏng và có chất kim loại, lời bám sát hình ảnh; nhạc không lời do AI thường có cấu trúc không đổi, kết thúc đột ngột hoặc ghép vòng lặp.

### Nguồn của giọng người và hiệu ứng

- **Giọng người**: TTS / giọng do video AI tự sinh / người thật thu âm. Tại các điểm cắt cảnh, nếu nhiễu nền nhảy bậc (`per_clip_audio.resets_at_cuts`) thì cho thấy mỗi đoạn âm thanh đi theo đoạn hình, tức là tiếng do mô hình video AI tự sinh (như Veo, Seedance có âm thanh) hoặc tiếng thu trực tiếp của quay thật.
- **Hiệu ứng**: đa số lấy từ thư viện hiệu ứng có sẵn (mixkit, Aigei v.v.); khi mô hình video AI tự sinh âm thanh thì hiệu ứng cũng đi theo đoạn hình. Lớp tất định chỉ đưa ra xu hướng; danh sách vẫn lấy theo VLM.

## Cách review

1. Xem `audio.png`: thanh giọng, thanh nhạc và vạch cắt cảnh có khớp với trực giác không.
2. Khi nghi ngờ một hiệu ứng, trích khung hình đoạn đó để xem có sự kiện tương ứng không (chữ hiện ra, chuyển cảnh, động tác): `rea-video tiles`.
3. Khi VLM cho `source_guess=popular_song`, hoặc nhãn nền tảng là tên bài cụ thể, thì trong phương án phục dựng phải ghi rõ "cần cấp phép hoặc thay thế".
4. Viết nguồn nhạc theo mục "Nguồn gốc âm thanh" ở trên; không viết nhạc nền thường thành "thư viện" một cách chắc chắn.

## Phục dựng

- **Giọng người**: DoubaoTTSTool / UniversalTTSTool của capsule-cinema hoặc nhân bản giọng MiniMax; khi cần khớp đúng khung thời gian gốc thì dùng TTS có kiểm soát độ dài.
- **BGM**: theo BPM, tông và cảm xúc, dùng Suno (UniversalMusicGenerationTool) hoặc thư viện nhạc; căn các điểm chuyển đoạn nhạc trùng với điểm đổi cảnh.
- **Hiệu ứng**: đặt theo mốc thời gian; hiệu ứng có cao độ thì căn theo tông của BGM (sfx.py / cues.py trong công thức plush của capsule-cinema làm đúng như vậy).
