# Công thức GSAP đang thử nghiệm

## Phạm vi và nguồn

Bảy module do dự án tự viết, đặt trong `assets/gsap-recipes/`. Các ví dụ giả định GSAP và plugin cần thiết đã nạp cục bộ và `timeline` đã tạo ở trạng thái paused. Chúng hiện là bản thử nghiệm: đã render fixture tổng hợp và kiểm tua snapshot trên Windows; chưa xác minh tái sử dụng độc lập hoặc đa nền tảng. Không dùng kết quả kiểm tĩnh làm bằng chứng render.

## Giấy phép

Mã recipe thuộc giấy phép MIT của repo. GSAP có điều khoản riêng: [GreenSock Standard License](https://gsap.com/community/standard-license/). Phạm vi cấp phép được mô tả cho website, web app và digital interface; chưa xác định nó bao trùm mọi cách sử dụng video hoặc phân phối. Repo không vendor GSAP; người dùng tự cấp runtime. Cần xem điều khoản hiện hành và làm rõ với bên cấp phép khi triển khai thương mại. Ngày đọc trước đây: 2026-11-14; điều khoản ghi hiệu lực 30/04/2025. Không suy rằng mã sinh bởi agent được phép trong mọi mô hình sản phẩm.

## Nạp runtime

GSAP core và plugin dùng cùng gói 3.15.0 đã ghim. Dùng `video-studio libs plan` để xem tên, và cấp file theo hợp đồng `runtime-libs`; không tải hoặc dùng CDN trong khi render. Với project chỉ import trong JavaScript, khai `--lib NAME` vì bộ nhận diện không phân tích mọi JavaScript. Project có file lib được nhận diện hoặc khai rõ phải khớp hash khóa.

## Tất định

Dùng timeline paused, khởi tạo trạng thái và tua tại thời điểm cụ thể. Với ứng dụng tự quản nhịp, kiểm `gsap.ticker.lagSmoothing(0)` và cách quản ticker; kiểm `totalTime(t, true)` trong chính môi trường render. Tránh `repeat: -1`, ngẫu nhiên không seed và hiệu ứng phụ theo thứ tự cập nhật. Chạy mỗi thứ tự tua với fixture mới và kiểm cả đối chứng sai. Không mặc định kết luận Chromium đại diện cho HyperFrames hoặc hệ điều hành khác.

## Recipe

### DrawSVG — `VE-gsap-drawsvg`

```js
import * as recipe from "./draw-svg.mjs";
recipe.register(gsap, window);
recipe.build(timeline, {gsap, targets: "#path", duration: 1});
```

Đăng ký `DrawSVGPlugin`, truyền path và timeline cho `build`; hữu ích khi vẽ nét. Tại mốc 0 cần kiểm offset thực tế.

### MorphSVG — `VE-gsap-morphsvg`

```js
import * as recipe from "./morph-svg.mjs";
recipe.register(gsap, window);
recipe.build(timeline, {gsap, target: "#path", shape: "#destination", shapeIndex: 0});
```

Đăng ký `MorphSVGPlugin`, truyền path nguồn và hình đích. Cố định `shapeIndex` khi hình trung gian quan trọng; mã biểu diễn path có thể khác dù hình tương tự.

### MotionPath — `VE-gsap-motionpath`

```js
import * as recipe from "./motion-path.mjs";
recipe.register(gsap, window);
recipe.build(timeline, {gsap, target: "#dot", path: "#route"});
```

Đăng ký `MotionPathPlugin`, truyền đối tượng, path và căn chỉnh. Kiểm transform tại các mốc và vị trí tương đối của SVG.

### SplitText — `VE-gsap-splittext`

```js
import * as recipe from "./split-text.mjs";
recipe.register(gsap, window);
const parts = recipe.prepare(SplitText, document.querySelector("#title"));
recipe.build(timeline, {gsap, split: parts});
```

Đăng ký `SplitText`; gọi `prepare` một lần sau khi font sẵn sàng, rồi `build`. Không bật tự tách lại; bố cục phụ thuộc font và máy.

### Flip — `VE-gsap-flip`

```js
import * as recipe from "./flip.mjs";
recipe.register(gsap, window);
recipe.build(timeline, {gsap, Flip, targets: "#card", change: () => document.querySelector("#card").classList.add("moved")});
```

Đăng ký `Flip`. `change` chỉ đổi bố cục một cách xác định ở lúc tạo; đo hình học đầu, giữa và cuối chứ không chỉ opacity.

### CustomEase — `VE-gsap-customease`

```js
import * as recipe from "./custom-ease.mjs";
recipe.register(gsap, window);
const curves = recipe.registerEases(gsap, CustomEase);
timeline.fromTo("#card", {opacity: 0}, {opacity: 1, duration: 1, ease: curves.softOvershoot}, 0);
```

Đăng ký `CustomEase`, gọi `registerEases`, dùng tên trả về trong tween. Hai đường được dự án tự thiết kế; kiểm giá trị giữa chừng trên phần tử riêng.

### Scramble tất định — `VE-gsap-seededscramble`

```js
import * as recipe from "./seeded-scramble.mjs";
recipe.build(timeline, {gsap, target: document.querySelector("#title"), text: "HELLO", seed: 1});
```

Truyền text, bảng ký tự và seed vào `build`. Giá trị tại một thời điểm được tính không dựa vào số lần cập nhật; `revealDelay` phải trong khoảng [0, 1). Kiểm text ở cuối và ký tự Unicode.

## Cách thử

`python -m pytest tests/test_node_suite.py -q` chạy kiểm seek và các phép thử JavaScript. `GSAP_TEST_TARBALL` có thể trỏ tới gói cục bộ đúng hash để chạy `tests/test_gsap_recipes_browser.py`; thiếu gói thì SKIP, không tính đạt. Bộ Chromium kiểm ba thứ tự với fixture riêng. DrawSVG so pixel của SVG trong fixture; MorphSVG so năm điểm hình học với độ chính xác 0,1 px. Phạm vi này chưa chứng minh tính tất định của mọi hình hoặc render HyperFrames.
