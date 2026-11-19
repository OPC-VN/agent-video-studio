# Bản đồ nguồn video dùng lại

Tra nguồn theo việc cần làm; đây là chỉ mục điều phối, không sao chép hay thay thế dữ liệu nguồn.

## Mục lục

- [Các nguồn theo nhu cầu](#các-nguồn-theo-nhu-cầu)
- [Tiếp nhận nguồn hiệu ứng mới](#tiếp-nhận-nguồn-hiệu-ứng-mới)
- [Ranh giới file theo cách tích hợp](#ranh-giới-file-theo-cách-tích-hợp)
- [Liên kết đến agent-design-studio](#liên-kết-đến-agent-design-studio)
- [Lưu và dùng lại trên Windows](#lưu-và-dùng-lại-trên-windows)
- [Template nhiều file](#template-nhiều-file)
- [Ví dụ kiểm luồng với dữ liệu tổng hợp](#ví-dụ-kiểm-luồng-với-dữ-liệu-tổng-hợp)

## Các nguồn theo nhu cầu

| Nhu cầu | Nguồn hiện hữu | Phạm vi và giới hạn |
|---|---|---|
| Layout và template | `THEME-LIBRARY.md` của trạm; nếu thiếu dùng [catalog repo](../../../docs/THEME-LIBRARY.md) | Chọn theo vai trò, tỷ lệ và tier. Catalog trạm và repo không trộn. |
| Prompt và ý tưởng motion | [Prompt Motion](../assets/prompt-motion/INDEX.md), `scripts/motion_find.py` | 240 thẻ tham chiếu; ID `PM-*`, nguồn và trạng thái kiểm giữ nguyên. Không phải 240 component chạy được. |
| Tia sáng / overlay ảnh | [photo-ambient-effects](../../photo-ambient-effects/SKILL.md) | Code, clock, mask và phạm vi kiểm do skill chuyên đề sở hữu. |
| Chữ lyric | [lyric-video-effects](../../lyric-video-effects/SKILL.md) | Preset chữ và hướng dẫn glyph do skill chuyên đề sở hữu; không mang font hoặc lời riêng vào repo. |
| Phân tích mẫu online | [video-reference-analysis](../../video-reference-analysis/SKILL.md) | Có liên kết tham khảo EditAtlas video-breakdown tại commit đã ghim; chỉ tham khảo tùy chọn, không mặc định tải hay sao chép. |
| Earshot — nghiên cứu âm thanh video ra mắt | [sound-design](../../hyperframes/media-use/references/sound-design.md) · `VE-earshot-sound` | Ba liên kết nguồn ghim commit về launch, cue và real-sound; chỉ tham khảo, chưa cài hay chạy Earshot. |
| vtake — card đồ họa cho video | [upstream.json](../../../upstream.json) · `VE-vtake-cards` | Hệ card của skill upstream phỏng theo vtake-skills; tham khảo provenance và ghi công, không coi thẻ là component đã kiểm. |
| video-use — chỉnh sửa footage | [video-edit](../../video-edit/SKILL.md) · `VE-video-use-editing` | Nguồn cho helper đã chưng cất; backend vendored cần cài riêng cùng phụ thuộc, không tự cài. |
| Ý tưởng SFX | [sound-design](../../hyperframes/media-use/references/sound-design.md) | Có tham khảo EditAtlas sound-design; quyền từng âm thanh phải được kiểm riêng. |
| Chép lời / chỉnh footage | [video-edit](../../video-edit/SKILL.md) | Có tham khảo EditAtlas transcribe, quy trình và backend local thuộc skill sở hữu. |
| Công cụ và kỹ thuật FFmpeg | [ffmpeg-tool-index](../../video-edit/references/ffmpeg-tool-index.md) | Danh mục định tuyến, không khẳng định mọi kỹ thuật đã có implementation. |
| Kỹ thuật sản xuất và Hypit | [production-techniques](../../video-routing/references/production-techniques.md) | Thẻ tình huống và workflow hiện có; kiểm từng năng lực trước khi hứa thực thi. |
| Composition HyperFrames | [hyperframes](../../hyperframes/hyperframes/SKILL.md) | Điểm vào các skill chưng cất; nguồn và bản ghim trong `upstream.json`. |
| FlowKit | [upstream.json](../../../upstream.json) | Tra provenance và trạng thái thực tế; roadmap không tự chứng minh đã có implementation. |
| React Bits — chữ, nền và chuyển động | [Danh mục React Bits](https://reactbits.dev/) · [repo](https://github.com/DavidHDev/react-bits) · `VE-react-bits` | Tham khảo online cho text animation, nền, particle và gradient. Code gốc dành cho React; từng mẫu có thể cần GSAP, Motion, Three.js hoặc OGL. Giấy phép repo MIT + Commons Clause có hạn chế; kiểm license và tài nguyên riêng trước khi dùng. Không coi là component video đã kiểm. |
| Magic UI — hiệu ứng sản phẩm | [Danh mục Magic UI](https://magicui.design/docs) · [repo](https://github.com/magicuidesign/magicui) · `VE-magic-ui` | Tham khảo text reveal, marquee, beam; code React và tùy mẫu có thể cần Tailwind CSS hoặc Motion. Repo dùng MIT; template Pro và tài nguyên riêng phải kiểm quyền riêng. |
| Motion Primitives — chuyển động giao diện | [Danh mục Motion Primitives](https://motion-primitives.com/docs) · [repo](https://github.com/ibelick/motion-primitives) · `VE-motion-primitives` | Tham khảo transition và chuyển động tinh tế. Code React, tùy mẫu có thể cần Motion và Tailwind CSS; repo MIT. Trang online có thể không truy cập được; dùng repo làm đường dự phòng. |

## Tiếp nhận nguồn hiệu ứng mới

Đây là cách tổ chức và kiểm từng nguồn, không phải lệnh tự tải hoặc cài repo mới:

1. Tra catalog hiện có trước; xác định mục đích, phiên bản hoặc commit, tác giả, giấy phép,
   quyền từng asset và phụ thuộc. Nguồn chưa rõ quyền chỉ giữ metadata và link với `reference_only`,
   `unknown`; không chép mã, prompt hay media. Nguồn bị loại không được dùng.
2. Phân loại theo sản phẩm thực tế: link/ý tưởng là `reference`, hướng dẫn là tài liệu,
   mã một file là `component` hoặc `preset`, còn project nhiều file là `template` theo contract.
   Không gọi reference là component đã render. Tài nguyên riêng và project thử đặt ở trạm
   được chọn; skill và mã dùng chung thuộc repo sau khi kiểm quyền và dữ liệu riêng.
3. Trong repo, đặt tài liệu tại `skills/video-theme-library/references/`, mã tái dùng theo nhóm
   trong `skills/video-theme-library/assets/`, và thẻ tìm kiếm tại `assets/effect-library/entries.json`.
   Ví dụ đang có: [GSAP core draw](gsap-core-draw.md) và `assets/gsap-recipes/core-draw.js`.
   `assets/prompt-motion/` là tập tham khảo riêng; không đưa mọi nguồn mới vào thư mục GSAP.
   Template nhiều file phải theo [contract](template-contract.md); writer hiện bị chặn, không hứa
   materialize thành project. Không tạo thư mục rỗng trước khi có nội dung đủ điều kiện.
4. Mỗi thẻ ghi ID, mô tả, nguồn, quyền, runtime, trạng thái và bằng chứng tương ứng; file có hash.
   Thẻ trong trạm dùng lệnh capture khi được phép, sau đó tìm lại; mục phân phối trong repo phải
   được review, cập nhật manifest/hash và kiểm gói. Runtime ngoài dùng cơ chế `libs` đã ghim,
   không tự vendor hoặc tải. Quyền của mã tự viết không thay quyền runtime hay asset bên thứ ba.
5. Kiểm theo công dụng: tìm lại, hash và gói; nếu khai render hoặc tua đạt thì có bằng chứng
   tương ứng. Chưa chạy ghi `not_run`; `candidate` không đồng nghĩa đã xác minh tái dùng.

## Ranh giới file theo cách tích hợp

Các đường dưới đây tính từ **gốc repo Video Studio**, trừ khi nói rõ là trạm hoặc repo khác.
Đây là bản đồ để chọn nơi ghi sau khi đã kiểm nguồn và quyền, không tự động tích hợp repo mới.

| Loại nội dung | Nơi đặt hoặc tìm | Điều cần ghi / giới hạn |
|---|---|---|
| Skill do Video Studio sở hữu | `skills/<tên>/SKILL.md`; tài liệu phụ trong `references/`, tài nguyên dùng chung trong `assets/` của skill sở hữu | Frontmatter tiếng Anh, nội dung tiếng Việt; không chép skill vào trạm. Nếu tạo hoặc đổi mô tả skill, sinh lại adapter bằng `scripts/build_host_adapters.py`. |
| Adapter cho host | `.agents/skills/<tên>/SKILL.md` và `.claude/skills/<tên>/SKILL.md` | File sinh chỉ trỏ về skill gốc; không đặt implementation hay sửa tay adapter. |
| Skill upstream đã chưng cất | Skill đích thuộc repo này, ví dụ `skills/hyperframes/<tên>/SKILL.md` | Ghi repo, bản ghim, đường nguồn/đích và hash phù hợp trong `upstream.json`; giữ ghi công trong `NOTICE`. Không tự chép cả thư mục upstream. |
| Tài liệu, mã hoặc asset upstream được phép đưa vào | Đặt trong skill hoặc module **sở hữu chức năng**, ví dụ tài liệu thư viện ở `skills/video-theme-library/references/`, asset hiệu ứng ở `skills/video-theme-library/assets/<nhóm>/` | Chỉ chép/chuyển thể phần được phép; ghi nguồn, giấy phép, thay đổi, hash và phụ thuộc; kiểm dữ liệu riêng và manifest phân phối. Chọn theo chức năng, không mặc định tạo một skill cho mỗi repo. |
| Repo khác chỉ tham khảo | Metadata/link trong catalog hoặc tài liệu tham khảo; hồ sơ nguồn trong `upstream.json` khi schema phù hợp | Repo, skill và folder gốc vẫn thuộc repo khác. Link không cấp quyền chép; chưa có mã thì không gọi là tích hợp chạy được. |
| Repo/plugin là phụ thuộc độc lập | Giữ trong repo hoặc môi trường do nó sở hữu; ví dụ `agent-voice-studio` là trạm giọng riêng | Tài liệu Video Studio mô tả giao diện, cách phát hiện và lỗi thiếu phụ thuộc; không sao chép skill của repo đó vào Video Studio hoặc tự cài. |
| Runtime thư viện ngoài | Khóa và hợp đồng tại `video_studio/locks/runtime-libs.json` và `video_studio/runtime_libs.py`; file runtime do người dùng cấp theo cơ chế tương ứng | Ví dụ GSAP core ghim hash, không vendor. Không suy plugin cùng gói đã có khóa hay quyền phân phối; kiểm từng phụ thuộc. |
| Project, media và dữ liệu riêng | `projects/` và thư viện của **trạm video được chọn**, không phải `skills/` hay mã theo dõi Git | Giữ provenance và quyền theo từng asset; không đưa dữ liệu khách hàng hoặc file render vào repo công khai. |

Ví dụ hiện có: HyperFrames là bộ skill đã chưng cất trong `skills/hyperframes/`; React Bits là
thẻ nguồn tham khảo, không phải component video đã port; `agent-design-studio` là plugin riêng,
chỉ tra tài nguyên của nó khi hiện diện. Trạng thái từng nguồn nằm trong bảng phía trên và
`upstream.json`; không suy repo gốc đã được cài hay toàn bộ nội dung đã được tích hợp.

## Liên kết đến agent-design-studio

Khi plugin `agent-design-studio` hiện diện, tra `skills/design-routing/resources/uiux-catalog.json`
(mục 07 React Bits, `link_only`) để dùng lại chỉ mục nguồn gốc thay vì tạo bản sao. Có thể tra
`skills/design-routing/references/motion-patterns.md` cho sáu recipe chuyển động viết lại (tra
`VE-design-studio-motion-patterns`, `MP01`–`MP06`) và
`skills/design-routing/templates/06-motion-spec.md` cho mẫu mô tả (tra
`VE-design-studio-motion-spec`); các đường trên tính từ **gốc plugin agent-design-studio**.
Thẻ video trỏ về bản đồ này, không chứa bản sao recipe hay template. Chúng là tài liệu thiết kế,
không phải component video đã kiểm hay React Bits đã port sang video. Nếu plugin không có, hai
nguồn nội bộ đó chưa sẵn có; link React Bits trong bảng trên chỉ là nguồn tham khảo khác, không
thay thế nội dung của hai tài liệu đó. Mỗi nguồn trong bảng là tham khảo: xem online không yêu cầu cài thêm engine;
muốn chuyển thành video, chọn một mẫu, kiểm quyền và phụ thuộc cụ thể, rồi dựng lại và kiểm render,
seek và tỷ lệ bằng runtime video của dự án. Không tự chạy script/cài thư viện hoặc hứa hoạt động offline.

Với nguồn online khác: lưu URL ổn định, tên tác giả, mục đích, ngày kiểm, điều kiện quyền và bằng
chứng nếu được phép; không coi website hoặc prompt bên thứ ba là asset được phân phối. Không đưa
đường riêng, hình, nhạc, font hay lời dự án vào plugin. Khi chỉ nghiên cứu, không tự tải hoặc ghi.

## Lưu và dùng lại trên Windows

Tra cứu từ khóa không phân biệt dấu tiếng Việt và yêu cầu **tất cả từ** trong truy vấn xuất hiện
trong metadata; cụm từ liên tiếp được ưu tiên. Nếu không có kết quả, thử bỏ bớt từ hoặc dùng từ
đồng nghĩa Việt/Anh. Đây là tìm theo từ khóa, không suy luận ngữ nghĩa hay tự dịch truy vấn.

CLI search trả danh sách JSON gồm các envelope `entry`, `prompt_text_truncated`,
`prompt_text_chars`, `truncated_fields`, `omitted_fields`, `retrieve`. Mặc định `entry` là bản
tóm tắt; các danh sách rút/ẩn báo chỗ chưa đầy đủ. Đây là thay đổi giao diện JSON CLI: consumer
trước đọc `row["id"]` cần chuyển sang `row["entry"]["id"]`. `--full-prompt` chỉ khôi phục toàn
bộ `prompt_text`, còn các trường khác vẫn được tóm tắt; `--full-record` trả record đầy đủ. Khi cần
một mục, tìm theo ID với `--limit 1`, rồi kiểm ID trả về vì so khớp theo từ khóa, không phải
tra ID chính xác. Mặc định mỗi envelope được giới hạn 8.192 byte theo phép tính JSON escape
bảo thủ; tổng output còn phụ thuộc `--limit`. Cả hai cờ có thể tạo output lớn. Nếu ID dài hơn
240 ký tự, tìm dạng tóm tắt trả mã 2; dùng `--full-record` để giữ nguyên ID. API Python
`search()` vẫn trả record gốc.

Trên Windows, CLI đọc trực tiếp hai tài liệu canonical: 42 tên FFmpeg upstream và chín thẻ kỹ
thuật do repo viết từ ý tưởng Hypit; ID kết quả có dạng `VE-ref-ffmpeg-*` hoặc `VE-ref-hypit-t*`.
Không tạo bản sao chỉ mục và không coi tên upstream là lệnh local đã cài. Nếu cấu trúc nguồn hoặc
provenance không hợp lệ, tìm kiếm báo lỗi. Trên hệ khác, CLI giữ tìm kiếm các nguồn cũ và cảnh báo
trên stderr rằng hai nguồn distill bị bỏ, nên kết quả chưa đầy đủ. `--no-distilled` cũng bỏ hai
nguồn và báo cảnh báo. API Python chỉ nạp hai nguồn khi truyền `distilled_root` tường minh.

Để lọc từng kết quả kiểm, dùng `--check render=pass`; có thể lặp để kết hợp điều kiện, ví dụ
`--check render=pass --check reuse_evidence=pass`. Các tên hợp lệ: `static_check`, `preview`,
`render`, `audio`, `ratio_test`, `reuse_evidence`; trạng thái là `not_run`, `pass` hoặc `fail`.
`pass` là metadata khai có bằng chứng, không tự chứng minh bằng chứng chính xác. Prompt Motion
được hiển thị sáu cờ `not_run` với `checks_origin: default_not_run`; index gốc không bị sửa.
Không suy trạng thái của một phép kiểm từ phép kiểm khác.

Dùng `--runtime "HyperFrames 0.8.54"` để lọc các từ và phiên bản khớp trong metadata runtime;
đây không phải bộ giải phiên bản và không chứng minh engine đã cài. Mặc định `--ratio 16:9` chỉ
trả entry có tỷ lệ phù hợp được khai báo. Thêm `--include-unknown-ratio` để xem cả ứng viên chưa
có thông tin cho tỷ lệ đó; không suy chúng tương thích. Với Prompt Motion, `ratio_fit` gốc vẫn
được trả về: `requires_redesign` không phải tỷ lệ chưa biết và không được thêm theo tùy chọn này.

Lệnh và API dưới đây chạy từ gốc của **chính plugin chứa skill đang được host nạp**, có thể nằm
trong cache. Xác định gốc từ đường dẫn `SKILL.md` mà host cung cấp: gốc đó chứa cả `skills/` và
`video_studio/`. Không suy theo cwd project hay gắn cứng version cache; nếu thiếu cấu trúc, báo
thiếu plugin và dừng. Khi gọi từ project khác, đặt cwd tiến trình CLI vào gốc plugin và truyền
project/station bằng đường tuyệt đối; việc đổi cwd chỉ áp cho tiến trình lệnh. Không tự cài mã.

API Python thử nghiệm `video_studio.effect_library` gồm `capture(project, station, manifest)`,
`search(query, station=station)`, `read_bundle(station, identifier)`,
`materialize(station, identifier, project, name)` và `materialize_repo(identifier, project, name)`.
`materialize_repo` chỉ chọn catalog repo canonical, không lùi sang station khi thiếu ID; chỉ nhận
component/preset có một file và quyền khai báo `owned` hoặc `licensed`, kiểm SHA-256 trước khi ghi
tên mới không ghi đè. Reference, prompt metadata và bundle nhiều file bị từ chối. Quyền khai báo
không tự chứng minh quyền sử dụng. Truyền
đường project và station tường minh; station phải có sẵn thư mục `effect-library/entries`. Mỗi
capture có thể lưu một file, một bundle nhiều file hoặc metadata-only cho reference hay prompt. File cần ID, metadata
bắt buộc, đường tương đối, SHA-256 đúng và quyền `owned` hoặc `licensed` kèm metadata license.
Reference metadata-only cho liên kết yêu cầu `source` là URL HTTP(S) online; không nhận đường file local làm
source và không tải nội dung từ URL. Riêng ý tưởng tự tạo có `rights=owned` và `maturity=reference_only`
được dùng mã logic đúng `urn:avs:idea:<ID>` (ID phải trùng ID thẻ), không đọc file hay URL từ mã này.
Mã chỉ xác định thẻ, không chứng minh quyền; hai ID khác vẫn có thể mô tả cùng ý tưởng. Quyền `unknown` chỉ phù hợp cho thẻ liên kết, không chép
prompt hay media nguồn. Prompt metadata-only cần `prompt_text` và quyền `owned` hoặc `licensed`.
Khi capture component hoặc prompt mới, điền `description` bằng chuỗi ngắn nêu mục đích, đầu vào,
đầu ra, tham số, cách dùng và giới hạn nếu đã biết; ghi “chưa biết” thay vì bịa phần chưa xác minh.
Đây là hướng dẫn làm thẻ hữu ích, không phải thay đổi schema hoặc yêu cầu áp lại cho thẻ cũ.
Đọc contract/schema trong
module trước khi tạo manifest; khai metadata không thay thế việc kiểm quyền thực tế. Materialize
ghi sang tên mới, không thay file đã có. Truy vấn và chọn kết quả trước khi đưa vào project.

Đường này mới được kiểm bằng dữ liệu synthetic trên Windows; macOS hiện từ chối ghi, wheel Python
thuần và tự dọn staging khi tiến trình chết chưa được xác minh. Chưa có bằng chứng dùng lại bởi
người dùng thật. Ngoài tìm kiếm, CLI hỗ trợ ba thao tác trên Windows. Hai thao tác station cần
station đã có `effect-library/entries`; capture cần manifest JSON UTF-8 nằm trong project:

```text
python -m video_studio.effect_library capture --project <project> --station <station> --manifest <duong-tuong-doi.json>
python -m video_studio.effect_library materialize --project <project-dich> --station <station> --id <VE-id> --name <ten-file-moi>
python -m video_studio.effect_library materialize-repo --project <project-dich> --id <VE-id> --name <ten-file-moi>
```

Với ba thao tác này, mã 0 là thành công, mã 2 là lỗi trước khi công bố, mã 3 là đã công bố nhưng
không hoàn tất bước kết thúc hoặc báo kết quả. Khi nhận mã 3, kiểm trạm hoặc file đích trước khi
thử lại; không tự giả định rollback. Ba lệnh này không materialize bundle nhiều file.

Bundle trạm dùng `assets` thay cho `asset`, gồm 2–64 mục; mỗi mục có `path` tương đối chuẩn,
`sha256` và `rights` riêng (`owned` hoặc `licensed`, kèm `license` nếu cần). Tổng nội dung giới
hạn 64 MiB; không trộn `asset` với `assets`. `read_bundle` trả mapping đường tương đối → bytes
đã kiểm, trong bộ nhớ. **Chưa hỗ trợ** `materialize` bundle thành thư mục project; API từ chối
trước khi ghi. Trên Windows, tìm kiếm và capture kiểm quyền khai báo, đường dẫn và hash của từng
file trong bundle repo; tổng nội dung mỗi entry tối đa 64 MiB. Search có nhánh đọc bundle POSIX,
nhưng chưa có bằng chứng chạy thật trên macOS/Linux; thiếu khả năng đọc an toàn thì từ chối.
Hai nguồn FFmpeg/Hypit vẫn bị bỏ trên POSIX như mô tả ở trên. Không coi đọc bundle là bằng chứng
đã phục hồi hoặc render dự án.

## Template nhiều file

Giao diện dự kiến chạy từ gốc plugin:

```text
python -m video_studio.effect_library materialize-template --id VE-x --into DIR
```

**Hiện bị chặn ghi:** writer Windows fail-closed vì chưa chứng minh quyền riêng và hoàn tác đúng
đối tượng; tổ hợp no-recall với tạo mới cũng chưa được chứng minh hoặc được Windows chấp nhận.
Writer macOS/Linux bị chặn cho đến khi chứng minh thao tác an toàn. Chưa có bằng chứng
kiểm host, render hoặc chạy thật trên POSIX; không dùng lệnh này như một tính năng đã sẵn sàng.
Lệnh chỉ chọn template trong catalog repo, không nhận `--station`; template của trạm chưa hỗ trợ.

Hợp đồng đòi `template_root`, `contract_path`, `contract_sha256` và bundle `assets` với SHA-256
cho từng file. Contract ở ngoài cây project; xem [khuôn contract](template-contract.md). Nội dung
contract và asset được kiểm digest, giữ snapshot bytes và dùng chính bytes đó khi ghi. Đích phải
hoàn toàn mới, thư mục cha đã tồn tại; không ghi đè hay gộp project. Giới hạn tổng asset 64 MiB.
Các đuôi `.glb`, `.gltf`, `.geojson`, `.wasm`, `.pmtiles`, `.pbf`, `.hdr`, `.bin` vẫn bị khóa.

Theo hợp đồng, mã 0 trả JSON `ok`, `id`, `into`, `files`, `bytes`; hai số chỉ đếm asset, không
gồm contract. Mã 2 nghĩa là chưa hoàn tất và đã dọn sạch; sửa lỗi trước khi thử lại. Mã 3 nghĩa là
trạng thái đích chưa chắc chắn hoặc khâu hoàn tất/báo kết quả lỗi: kiểm đích trước khi thử lại,
không tự giả định rollback hay xóa file không rõ sở hữu. Crash cũng có thể để lại cây dở; kiểm thủ
công trước khi xử lý. Kiểm `_scan_project` chỉ là kiểm tĩnh, không chứng minh đã render; render
cần chạy engine riêng và ghi bằng chứng riêng.

## Ví dụ kiểm luồng với dữ liệu tổng hợp

Đoạn sau tạo trạm và hai project **trong thư mục tạm**, lưu một component do ví dụ tạo, một prompt
do ví dụ viết và một link chỉ để tham khảo; sau đó tìm lại và đưa component vào project thứ hai.
URL là dữ liệu mẫu, không được tải. Chạy từ checkout trên Windows; `TemporaryDirectory` thu dọn
riêng dữ liệu của ví dụ sau khi chạy. Với project thật, thay đường trạm/project và metadata bằng
giá trị đã được giao; không dùng `owned` chỉ vì một file có thể đọc được.

```python
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from video_studio.effect_library import capture, materialize, search

with TemporaryDirectory(prefix="video-library-example-") as temp:
    root = Path(temp)
    project_a, project_b, station = root / "project-a", root / "project-b", root / "station"
    project_a.mkdir()
    project_b.mkdir()
    (station / "effect-library" / "entries").mkdir(parents=True)
    content = b"export const syntheticGlow = 1;\n"
    (project_a / "glow.js").write_bytes(content)
    checks = dict.fromkeys(("static_check", "preview", "render", "audio", "ratio_test", "reuse_evidence"), "not_run")
    common = {"tags": ["synthetic"], "roles": [], "techniques": [], "ratios": [], "checks": checks}
    component = dict(common, id="VE-example-glow", name="Synthetic glow", kind="component",
                     maturity="candidate", rights="owned", source="synthetic example", runtime="js",
                     description="Ví dụ JS: không có đầu vào hay tham số; xuất hằng syntheticGlow. Import hằng; không tạo hiệu ứng hình ảnh.",
                     asset={"path": "glow.js", "sha256": sha256(content).hexdigest()})
    prompt = dict(common, id="VE-example-prompt", name="Synthetic prompt", kind="prompt",
                  maturity="candidate", rights="owned", source="synthetic example", runtime="text",
                  description="Prompt mẫu mô tả glow; đầu vào và tham số chưa biết; đầu ra phụ thuộc công cụ. Kiểm quyền và kết quả trước khi dùng.",
                  prompt_text="Slow glow over a dark background.")
    reference = dict(common, id="VE-example-reference", name="Synthetic reference", kind="reference",
                     maturity="reference_only", rights="unknown", source="https://example.org/video-reference",
                     runtime="online reference")
    for entry in (component, prompt, reference):
        capture(project_a, station, entry)
    assert {entry["id"] for entry in search("synthetic", station=station)} >= {
        "VE-example-glow", "VE-example-prompt", "VE-example-reference"
    }
    materialize(station, "VE-example-glow", project_b, "glow.js")
    assert (project_b / "glow.js").read_bytes() == content
```

`reference` và `prompt` không có file để materialize; dùng metadata sau khi kiểm nguồn và quyền.
Không ghi đè khi ID, tên hoặc nội dung trùng. Nếu tiến trình chết giữa capture, thư mục `stage-*`
được cách ly, không được coi là entry hoàn chỉnh; việc có marker không chứng minh quyền tự xóa.
Không tự xóa stage không rõ sở hữu. Ngoại lệ hoặc mã lỗi phải được xử lý và báo rõ, không thay
bằng kết luận đã lưu thành công.


Recipe GSAP thử nghiệm và giới hạn xác minh: [gsap-recipes.md](gsap-recipes.md).
