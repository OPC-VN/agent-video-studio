---
name: video-reverse-engineer
description: Use when a reference video must be taken apart shot by shot before remaking it - which shots are filmed, AI-generated, 3D, code-rendered or screen recordings, where cuts, transitions and key frames fall, what text, stickers and sound effects sit on top, camera, light and colour - and when a rebuilt video must be compared against the original. Runs the pinned rea-video analyser offline through `video-studio reference decompose` and turns its VIDEO.md pack into the reference map. Also when several long reference videos of one genre must be distilled into a reusable pattern library of layouts, transitions, text motion and idea-to-visual recipes. Not for downloading videos, not for editing footage, and never with a vision-model (VLM) endpoint switched on.
---

# video-reverse-engineer — adapter nguồn

Đọc toàn bộ [SKILL.md](../../../skills/video-reverse-engineer/SKILL.md) gốc trong chính plugin chứa adapter trước khi làm. Mọi reference, script và template của skill phải mở trực tiếp từ thư mục gốc đó; không dùng bản chép trong trạm video. Bản plugin do host cài có thể nằm trong cache. Nếu không mở được file gốc, báo thiếu source và dừng tác vụ này.
