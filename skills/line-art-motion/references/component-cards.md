# Thẻ component

| Component | Bất biến | Tham số | Vật liệu | Kiểm |
|---|---|---|---|---|
| walker | Tư thế từ thời gian, tạo node một lần | `kind`, vị trí, tỷ lệ, hướng | SVG, helper | Kiểm hình chân và tua |
| hanging | Góc từ thời gian | điểm treo, chiều dài, gió, hích | SVG, helper | Kiểm biên và tua |
| ink-scene | Filter chỉ lên nhóm nét | kích thước, filterId, ngày, nét vẽ | SVG, nhóm `data-ink-layer`, helper | Kiểm nền, màu và tua |

Không component nào tự tạo timeline; GSAP core có thể cấp thời gian tuyệt đối.

## Lắp một cảnh SVG

Chép `line-art.mjs` và ba module cần dùng từ `assets/` của skill vào cùng thư mục `assets/` trong project. `materialize-repo` chỉ cấp file component; không tự kèm helper. Ví dụ dưới cần GSAP core cục bộ đã được cấp hợp lệ và gốc composition HyperFrames có `data-composition-id="master"`, kích thước cùng thời lượng phù hợp. Nền giấy đặt ngoài `data-ink-layer`; mỗi walker và vật treo có nhóm `<g>` riêng vì component ghi transform hoặc thêm node vào nhóm đó.

```html
<svg id="scene" width="320" height="180" xmlns="http://www.w3.org/2000/svg">
  <rect width="320" height="180" fill="var(--paper)"/>
  <g data-ink-layer style="color:var(--ink)">
    <g id="walker"></g><g id="lamp"></g>
    <path id="draw" d="M18 150 L250 150" fill="none" stroke="currentColor"/>
  </g>
</svg>
<script src="./gsap.js"></script>
<script type="module">
import {createWalker} from './assets/walker.mjs';
import {createHanging} from './assets/hanging.mjs';
import {createInkScene} from './assets/ink-scene.mjs';
const el = id => document.getElementById(id);
const parts = [
  [createWalker({x0:100, ground:120, scale:1, direction:1}), el('walker')],
  [createHanging({anchor:{x:260,y:20}, length:40}), el('lamp')],
  [createInkScene({width:320, height:180, filterId:'roomInk', dayLength:3,
    draws:[{el:el('draw'), start:1, duration:2}]}), el('scene')]
];
for (const [part, node] of parts) { part.mount(node); part.render(0); }
let now = 0;
const clock = {get elapsed(){return now;}, set elapsed(next){
  now = Number(next); for (const [part] of parts) part.render(now);
}};
const duration = 4;
const tl = gsap.timeline({paused:true});
tl.to(clock, {elapsed:duration, duration, ease:'none'}, 0);
window.__timelines ??= {};
window.__timelines.master = tl;
</script>
```

Chọn `filterId` duy nhất trên toàn document; mỗi nét `draws` phải là phần tử path đã có và thời lượng dương. `drawOn` ẩn path ở tiến độ 0 để đầu nét tròn không hiện thành chấm; nếu một hiệu ứng khác cũng điều khiển ẩn/hiện, đặt hiệu ứng đó lên nhóm cha để hai bên độc lập. Setter cập nhật trạng thái khi timeline đổi giá trị, kể cả khi thao tác seek bỏ qua callback; không dựa riêng vào `onUpdate`. Ví dụ là điểm bắt đầu: điều chỉnh tốc độ, khung hình, độ tương phản và kiểm theo [verify.md](verify.md) trước khi dùng. Kiểm browser DOM/CSS không thay cho render qua HyperFrames.
