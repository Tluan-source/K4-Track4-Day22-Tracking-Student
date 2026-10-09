# Báo cáo lab: chọn tracker cho 5 video

**Nhóm:** Nhóm 01 **Thành viên:** Học viên

Detector cố định: `yolo26n.pt`, ảnh 640 px, Re-ID `osnet_x0_25_msmt17`. Không đổi các mục này trong bài nộp chính.

## 1. Cấu hình đã chọn

Mỗi video: tracker bạn nộp, `conf`, `iou`, điều bạn **nhìn thấy** trên video, và một cấu hình đã thử rồi loại.

| Video | Tracker | conf | iou | Quan sát khi xem video | Đã thử nhưng loại |
|---|---|---|---|---|---|
| video_1 (quảng trường, tĩnh, ban ngày) | bytetrack | 0.25 | 0.5 | Ít đổi ID, giữ track tốt khi người đi cắt nhau. | botsort (conf=0.5): Bỏ sót người ở xa/nhỏ. |
| video_2 (phố đêm, tĩnh, rất đông) | bytetrack | 0.25 | 0.5 | Mật độ đông nhưng ByteTrack ghép 2 giai đoạn giữ track ổn, ít bị nhiễu do ánh sáng đêm. | strongsort (conf=0.15): Xuất hiện nhiều hộp giả trên mặt đường chiếu sáng. |
| video_3 (camera di động, ảnh nhỏ) | botsort | 0.30 | 0.5 | Camera di chuyển và FPS thấp, BotSORT có CMC + Re-ID giúp duy trì ID khi camera lia. | bytetrack (conf=0.30): ID bị nhảy liên tục mỗi khi camera chuyển động. |
| video_4 (trong nhà, camera di chuyển) | strongsort | 0.35 | 0.5 | conf=0.35 loại bỏ hộp giả do bóng/phản chiếu kính; StrongSORT giữ ID tốt khi tiến gần. | ocsort (conf=0.15): Bị tạo nhiều hộp giả trên bề mặt kính phản chiếu. |
| video_5 (trên xe bus, giao lộ đông) | deepocsort | 0.25 | 0.5 | Xe bus rung lắc mạnh, DeepOCSORT kết hợp động lượng và Re-ID nối lại ID tốt sau khi rung. | bytetrack (conf=0.40): Rung lắc mạnh làm mất vệt track và đổi ID liên tục. |

## 2. Số liệu video_1

Dán bảng HOTA / MOTA / IDF1 do `scripts/evaluate_practice.py` in ra.

```
Evaluating nhom01_video1_final

HOTA: nhom01_video1_final-pedestrian
video_1    HOTA: 25.995 | DetA: 15.531 | AssA: 43.559 | DetRe: 15.773 | DetPr: 82.070 | AssRe: 45.707 | AssPr: 83.798 | LocA: 84.297

CLEAR: nhom01_video1_final-pedestrian
video_1    MOTA: 17.787 | MOTP: 82.265 | MODA: 17.927 | CLR_Re: 18.573 | CLR_Pr: 96.640 | IDSW: 26 | Frag: 72

Identity: nhom01_video1_final-pedestrian
video_1    IDF1: 25.966 | IDR: 15.478 | IDP: 80.538 | IDTP: 2876 | IDFN: 15705 | IDFP: 695
```

`video_2` đến `video_5` không có nhãn trong gói lab. Không điền số cho các video đó.

## 3. Phân tích

- **video_1 & video_2 (Cảnh camera tĩnh, mật độ đông/ban ngày và đêm)**: Tracker dựa trên chuyển động thuần túy hoặc ghép 2 giai đoạn như `bytetrack` tỏ ra rất hiệu quả. Ở video_1, khi hai người đi cắt nhau, ngưỡng conf=0.25 cho phép giữ lại các hộp độ tin cậy thấp ở giai đoạn 2 giúp track không bị đứt đoạn. Ở video_2 (ban đêm đông đúc), các mô hình Re-ID ngoại hình dễ bị ảnh hưởng bởi ánh sáng đèn và quần áo tối màu; việc dùng ByteTrack giúp duy trì liên kết quỹ đạo theo chuyển động ổn định hơn mà không bị gán nhầm ID do ngoại hình nhiễu.
- **video_3 & video_5 (Cảnh camera di chuyển, rung lắc)**: Khi camera di chuyển (`video_3`) hoặc rung lắc mạnh trên xe bus (`video_5`), giả định chuyển động tuyến tính của Kalman Filter chuẩn bị vi phạm. `botsort` (với Camera Motion Compensation - CMC) và `deepocsort` (kết hợp Re-ID và động lượng thích ứng) giúp tái kết nối (re-associate) danh tính người đi bộ ngay cả khi quỹ đạo bị gián đoạn do rung lắc khung hình.

## 4. Nếu có thêm thời gian

- Thử nghiệm quét mịn hơn các tham số nội bộ của tracker (ví dụ: `track_high_thresh`, `track_buffer`, `match_thresh`).
- Áp dụng mô hình Re-ID mạnh hơn hoặc fine-tune trên dữ liệu góc nhìn từ trên cao/ban đêm để cải thiện bài toán camera di chuyển và cảnh đêm đông đúc.
