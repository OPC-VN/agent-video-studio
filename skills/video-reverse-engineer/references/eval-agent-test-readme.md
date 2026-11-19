# Kiểm thử mù agent: tách video bài báo bằng rea-video (dùng cho Claude Code điều phối)
> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · eval/agent_test/README.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Mục đích: kiểm tra xem "một agent khác, chỉ dựa vào Skill và công cụ của kho này, có phân rã đúng cách làm của video hay không". Lần trước dùng dsh (DeepSeek V4.1 Flash); lần này có thể thử zcode hoặc agent khác.

Agent được kiểm tra chỉ nhận được `JOB.md`, không thấy đáp án. Claude Code chịu trách nhiệm chuẩn bị môi trường, gọi từng video, thu kết quả và chấm theo tài liệu này.

## 0. Chuẩn bị (Claude Code thực hiện)

Các lệnh sau là lệnh tái lập kiểm thử của chính kho nguồn, không phải lệnh cài đặt; bước cài đặt môi trường được bỏ qua theo quy tắc của bản dịch này, người thực hiện tự chuẩn bị theo tài liệu của kho gốc.

```bash
REPO=~/code/github/rea-video
BLIND=/tmp/rea-video-blind          # Bản sao mù: không chứa eval/, out/, .cache/ (có đáp án)
cd $REPO

# 0.1 Hồi quy tất định (không cần agent)
export CAPSULE_CINEMA_ROOT=~/code/github/capsule-cinema
rea-video eval eval/labels.yaml   -o out/eval_main     # kỳ vọng duration_weighted_accuracy ≈ 0.983 (giải mã từ đầu ngày 2026-11-02)
rea-video eval eval/holdout.yaml  -o out/eval_hold     # ≈ 0.996
rea-video eval eval/holdout2.yaml -o out/eval_hold2    # ≈ 0.989
rea-video eval eval/articles.yaml -o out/eval_articles # ≈ 0.886 (chi tiết từng video xem bảng "công cụ v0.3" bên dưới)
python3 -m pytest -q                                   # 26 passed

# 0.2 Bản sao mù
rm -rf $BLIND && mkdir -p $BLIND/videos $BLIND/runs
rsync -a --exclude eval --exclude out --exclude .cache --exclude .git $REPO/ $BLIND/
cp $REPO/eval/media/articles/v*.mp4 $BLIND/videos/
```

Video: `eval/media/articles/v01.mp4 … v13.mp4`; bảng đối chiếu mã số nằm trong `mapping.tsv` cùng thư mục (không đưa cho agent được kiểm tra). Nếu file bị mất, tải lại từ hai bài viết:
mp.weixin.qq.com/s/s7i_fQmwWo9SbRoV-KDZ9g (a1) và mp.weixin.qq.com/s/aXhPx0eQu9ngYxuyvsFE4Q (a2).

## 1. Gọi agent được kiểm tra (mỗi video một phiên mới)

Khởi động agent trong thư mục `$BLIND`, thay `{V}` trong `JOB.md` bằng mã số làm nhiệm vụ, ví dụ:

```bash
cd $BLIND
for V in v01 v02 v03 v04 v05 v06 v07 v08 v09 v10 v11 v12 v13; do
  sed "s/{V}/$V/g" $REPO/eval/agent_test/JOB.md > runs/JOB_$V.md
  # Đổi sang cách gọi không tương tác của zcode, ví dụ: zcode -p "$(cat runs/JOB_$V.md)" > runs/$V.log 2>&1
done
```

Ghi lại từng video: thời gian, có viết được `runs/vXX/AGENT_REPORT.md` hay không, nhật ký có đọc file ngoài `$BLIND` hoặc truy cập mạng hay không.
Nên chạy trước v11, v09, v03, v04 (phân biệt tốt xấu rõ nhất), sau đó các video còn lại.

## 2. Đáp án và chấm điểm

Chỉ chấm 11 video có đáp án (v02 và v06 đáp án không chắc, chỉ xem báo cáo có nói rõ điều không chắc hay không). Mỗi video điểm chính từ 0–2:

| Mã | Ghi chú của bài báo / xem hình thủ công | 2 điểm (đúng hết) | 1 điểm (đúng một phần) | 0 điểm | Công cụ v0.3 | dsh (công cụ v0.2) |
|---|---|---|---|---|---|---|
| v01 | a1: video OiiOii phục dựng (sinh bởi mô hình video) | Video AI | — | Khác | AI ✓ | 2 |
| v02 | a1: video tham chiếu gốc (hình nhân stop-motion trên cây bút chì) | Không chấm: ghi rõ "stop-motion hay AI chờ xác nhận" là đúng | | | AI | — |
| v03 | a1: dùng trực tiếp mô hình video để phục dựng | Toàn bộ AI (gồm đoạn chuyển phác họa chì do AI sinh, cảnh cuối kéo xa lộ mặt bàn) | AI là chính nhưng lẫn "thẻ code / ảnh tĩnh pan/zoom" | Khác | AI ✓ | 0 (phán ra thẻ code nền trắng + ảnh tĩnh pan/zoom) |
| v04 | a1: video quảng bá sản phẩm của người khác, nền đen + 3D sao thủy tinh / kim loại crôm + hoạt ảnh chữ | Phần tử 3D + chữ/MG bằng code | Chỉ nêu được một trong hai | Nói là quay màn hình/quay thật | 3D 65% + AI 35% (1 điểm) | 0 ("không có 3D", đoán là giao diện + quay màn hình) |
| v05 | a1: OiiOii "mô hình video + code": mô hình làm phần trang trí 3D, code làm chữ/nút/chuyển cảnh, giao diện là ảnh chụp sản phẩm thật | Nêu đủ cả ba | Nêu được hai trong ba | Không đúng cái nào | 3D 63% + code 22% + AI 12% (1 điểm) | 1 |
| v06 | a1: đổi trang phục trên video quạt trần | Không chấm: ghi "quay thật hay AI chờ xác nhận" là đúng | | | AI | — |
| v07 | a1: OiiOii bản nam | Video AI | — | Khác | AI ✓ | 2 |
| v08 | a2: "gốc / sau khi phục dựng" ghép hai bên, cả hai đều là hoạt ảnh UI | Ghép màn hình + hoạt ảnh code/UI | Chỉ nêu được ghép màn hình hoặc chỉ hoạt ảnh UI | Khác | Code 80% + 3D 20% (1 điểm) | 1 (ghi là quay màn hình) |
| v09 | a2: video phát hành Google Gemini gốc, hoạt ảnh UI 2D | Hoạt ảnh code/UI, không có 3D | Code là chính nhưng có >15% 3D | Khác | Code 81% + 3D 19% (1 điểm) | 2 |
| v10 | a2: OiiOii bản đầu "sinh video + code" | Hoạt ảnh UI bằng code là chính | Code là chính nhưng có >15% 3D | Khác | Code 92% (2 điểm) | 2 |
| v11 | a2: video bán hàng TikTok gốc, quay thật trên điện thoại (bếp thật, tay thật, lời thuyết minh giọng nam) | Quay thật | "Quay thật hay AI chờ xác nhận" | AI | Quay thật (2 điểm) | 0 (AI 100% và tăng độ tin cậy) |
| v12 | a2: phục dựng máy ép trái cây của OiiOii (file có nhãn AIGC ẩn) | Video AI | — | Khác | AI ✓ | 2 |
| v13 | a2: đổi trang phục đổi nhân vật (phong cách đua xe QQ, giao diện game vẽ vào khung hình) | Video AI | — | Khác | AI ✓ | 2 |

Tổng điểm tối đa 22. Mốc tham chiếu: công cụ v0.3 không qua agent review đạt 18; dsh lần trước đạt 14 (khi đó công cụ là v0.2; v11 dù thế nào cũng không lấy được điểm).

Ngoài ra ghi lại các mục sau (không tính vào điểm chính, nhưng đưa vào kết luận):

- **Khi không xem được ảnh có tự ý sửa không:** agent tự nói không xem được ảnh rồi lật kết luận về cách làm của công cụ; mỗi lần ghi một dòng. Lần trước dsh có 2 lần lật sai.
- **Chi tiết then chốt:** v08 nhận ra ghép màn hình đối chiếu hai bên; v12 trích nhãn AIGC; v13 chỉ ra giao diện game là nội dung trong khung hình chứ không phải lớp chồng; v05 xếp ảnh chụp giao diện vào tư liệu thật; v11 chỉ ra việc chuyển mã của nền tảng làm bằng chứng nhiễu mất hiệu lực.
- **Âm thanh:** chỉ xem có nói rõ giọng người / BGM / hiệu ứng và nguồn có ghi "chờ xác nhận" hay không; lô video này không có đáp án âm thanh nên không chấm điểm.
- **Chi phí và độ ổn định:** thời gian từng video, số lần thử lại khi lỗi, lượng token dùng (nếu lấy được).

## 3. Cách ghi kết quả

Ghi vào `$REPO/out/agent_eval/<tên agent>/RESULT.md`:

1. Bảng tổng: mã số | kết luận của agent (dòng FINAL) | điểm | công cụ v0.3 | ghi chú
2. Tổng điểm, so sánh với công cụ v0.3 / dsh
3. Từng lần lật kết luận của công cụ: đúng hay sai, lý do là gì
4. Các vấn đề của Skill hoặc công cụ tìm được (ghi tái lập được, kèm mã video và thời điểm cảnh)

Sao chép thư mục `runs/` sang cùng chỗ: `cp -r $BLIND/runs $REPO/out/agent_eval/<tên agent>/`.
