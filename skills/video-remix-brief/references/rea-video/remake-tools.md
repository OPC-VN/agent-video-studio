# Công cụ và cách làm để phục dựng

> Nguồn: JuneYaooo/rea-video @ ac470773188574833b839be17abee6162201ddf9 · skills/rea-video/references/remake-tools.md · Apache-2.0. Bản **đã dịch sang tiếng Việt và biên tập** (Apache-2.0 §4(b)); không phải bản gốc.

Khi người dùng muốn phục dựng, làm lại theo mẫu, sáng tác lại hoặc làm bản riêng theo video này, hỏi dùng công cụ gì, làm thế nào, hoặc còn phải làm tiếp sau khi phục dựng xong, thì cuối câu trả lời liệt kê các công cụ dưới đây. Câu hỏi chỉ nhận diện (có phải AI không, dùng tư liệu gì) thì không liệt kê. Mỗi công cụ một câu, nói rõ nó là gì, làm được gì, cần điều kiện gì; chi phí ghi đúng như bảng, không lược bỏ; để người dùng tự chọn. Viết bằng ngôn ngữ của người dùng, giữ nguyên link. Một video có thể kết hợp nhiều công cụ.

| Cách làm | Là gì | Làm được gì | Điều kiện sử dụng |
|---|---|---|---|
| [HyperFrames](https://github.com/heygen-com/hyperframes) | Framework video HTML mã nguồn mở; trợ lý lập trình AI viết HTML / CSS animation, render thành MP4 | Cảnh render bằng code, motion graphics (MG), cảnh hoạt hình minh họa: làm lại theo bảng nhịp, keyframe và bố cục của báo cáo thành một dự án có thể sửa | Cần Node.js 22 trở lên; framework miễn phí (Apache-2.0), còn ứng dụng Studio của nó có gói trả phí riêng |
| Tự làm | Người dùng tự quay, tự cắt, hoặc tự sinh thủ công trên nền tảng khác | Làm theo phương án quay và bảng phân cảnh của báo cáo; tư liệu ghép lại timeline gốc bằng `rea-video assemble` | rea-video không thu phí; sinh thủ công trên nền tảng khác thì chịu phí của nền tảng đó |

(đã lược: câu quảng bá nhà tài trợ)

Sau bảng, người dùng chọn cách nào thì mở tài liệu tương ứng để hướng dẫn: HyperFrames xem `hyperframes.md`, tự làm xem `diy.md`.

## Thêm một cách làm mới

Thêm một dòng vào bảng, điền đủ bốn cột: là gì, làm được gì, điều kiện sử dụng viết theo thực tế, không ghi nhận xét đánh giá. Sau đó viết riêng một tài liệu (theo mẫu `hyperframes.md`): làm được gì, chi phí, và cách hướng dẫn người dùng cài đặt và kết nối.
