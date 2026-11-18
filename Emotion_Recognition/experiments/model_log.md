# Nhật ký thí nghiệm — CNN nhận dạng biểu cảm (FER2013)

File này ghi lại từng lần chạy: cấu hình gì, kết quả bao nhiêu, nhận xét và quyết định tiếp theo.
Số liệu thô nằm trong `runs.csv`, lịch sử loss/accuracy từng epoch nằm trong `logs/<exp_id>_history.csv`.

## Thiết lập chung

| Thành phần | Giá trị |
|---|---|
| Dữ liệu | 28.709 ảnh train, 7.178 ảnh test (48×48, 1 kênh) |
| Chia tập | stratified 90/10 trên train → 25.838 train / 2.871 validation |
| Seed | 42 (Python, numpy, torch) |
| Chuẩn hoá | trừ mean 0,5077, chia std 0,2551 (tính trên train) |
| Ngân sách mỗi cấu hình | 18 epoch, early stopping sau 6 epoch không cải thiện |
| Chọn mô hình | validation accuracy; **test chỉ dùng một lần** ở giai đoạn 4 |
| Metric phụ | F1 từng lớp (dữ liệu mất cân bằng 16,5 lần) |

Quy ước mã: `BASE` là baseline; `A2/A4` = số khối conv; `B1/B3` = độ rộng; `C1..C3` = optimizer
và tốc độ học; `D1..D4` = chống quá khớp và xử lý mất cân bằng.

## Bảng thí nghiệm (giai đoạn 2–3)

| exp_id | Mô hình | Thay đổi so với baseline | Val acc | Test acc | Gap train–val | Thời gian | Nhận xét | Quyết định |
|---|---|---|---:|---:|---:|---:|---|---|
| BASE | 32-64-128, dropout 0,3, Adam 1e-3 | — | 0,5385 | 0,5237 | +0,022 | 628 s | Chưa quá khớp, còn thiếu năng lực; `disgust` recall = 0 | Lấy làm mốc so sánh |
| A2 | 32-64 | 2 khối conv | 0,3299 | — | −0,002 | 496 s | Train 0,328 ≈ val 0,330 → **không học được gì**, thiếu năng lực nghiêm trọng (2 lần pool còn 12×12, GAP nén quá mạnh) | Loại, không dùng mạng quá nông |
| A4 | 32-64-128-256 | 4 khối conv | **0,5890** | — | +0,324 | 708 s | Cao nhất nhưng **quá khớp nặng** (train 0,908) | Chọn làm hướng cho mô hình cuối, kèm regularization |
| B1 | 16-32-64 | mạng hẹp | 0,4800 | — | −0,001 | 258 s | Train 0,473 ≈ val 0,480 → thiếu tham số, underfit | Loại |
| B3 | 64-128-256 | mạng rộng | 0,5730 | — | +0,062 | 1531 s | +3,5 điểm nhưng tốn 2,4 lần thời gian của A4 | Không chọn: hiệu quả/giây thấp hơn A4 |
| C1 | 32-64-128, SGD 0,9 | đổi optimizer | 0,5312 | — | −0,006 | 627 s | Chưa hội tụ (epoch tốt nhất 18/18) | Giữ Adam |
| C2 | 32-64-128, AdamW | đổi optimizer | 0,5374 | — | +0,020 | 625 s | Gần như trùng Adam (0,5385) | Weight decay không có ích ở quy mô này |
| C3 | 32-64-128, Adam 1e-4 | giảm lr | 0,4330 | — | −0,006 | 678 s | Quá chậm, 18 epoch chưa đi được bao xa | Loại |
| D1 | 32-64-128 + augmentation | thêm augmentation | 0,5110 | — | −0,010 | 567 s | Gap ≈ 0 → chặn quá khớp tốt, nhưng underfit vì thiếu epoch | Sẽ dùng cho mô hình cuối với nhiều epoch hơn |
| D2 | 32-64-128, dropout 0,5 | tăng dropout | 0,5190 | — | +0,029 | 556 s | Giảm nhẹ accuracy, gap không nhỏ hơn baseline | Không chọn |
| D3 | 32-64-128 + class weight | cân bằng lớp | 0,4977 | — | +0,007 | 552 s | Accuracy giảm 4,1 điểm; cần xem F1 mới kết luận được | Thử lại ở mô hình cuối, đánh giá bằng F1 |
| D4 | 32-64-128, aug + class weight | kết hợp | 0,4932 | — | −0,001 | 554 s | Thấp nhất nhóm D, epoch tốt nhất rơi vào 14 | Loại |

Tổng thời gian chạy 12 cấu hình: khoảng 2 giờ 10 phút (CPU, 16 luồng).

## Ghi chú theo từng giai đoạn

### Giai đoạn 2 — baseline

- Thử 12 epoch trước: test 46,99%, loss vẫn giảm ở epoch cuối → cắt ngang quá sớm chứ không phải
  quá khớp. Tăng lên 18 epoch được 52,37%.
- Validation loss dao động mạnh giữa các epoch vì validation chỉ có 2.871 ảnh.
- F1 macro 0,428 so với accuracy 0,524 — hệ quả trực tiếp của mất cân bằng lớp.
- Chạy lại lần hai cho đúng kết quả (val 0,5385 / test 0,5237), chỉ khác thời gian → pipeline
  tái lập được.

### Giai đoạn 3 — 11 cấu hình

- **Dung lượng mô hình là biến quan trọng nhất**: A4 +5,0 điểm, A2 −20,9 điểm, B3 +3,5 điểm.
- **Optimizer gần như không ảnh hưởng**: Adam 0,5385 / AdamW 0,5374 / SGD 0,5312; chỉ có lr quá
  nhỏ (1e-4) mới làm hỏng (0,4330).
- **Regularization giảm accuracy trong ngân sách 18 epoch**, nhưng A4 gap +0,324 chứng tỏ nó cần
  regularization. Hai kết luận này không mâu thuẫn: regularization cần thời gian để phát huy.
- **Class weight làm accuracy giảm** (0,4977) — chưa kết luận được vì chưa đo F1 từng lớp trong
  thí nghiệm này; sẽ đo ở giai đoạn 4.

### Quyết định cho giai đoạn 4

1. Mô hình cuối: **A4 (32-64-128-256) + augmentation**, huấn luyện ~40 epoch (thay vì 18) vì
   augmentation làm chậm hội tụ nhưng hãm được mức quá khớp rất lớn của A4.
2. Chạy 3 seed (42/43/44) để báo trung bình ± độ lệch chuẩn, tránh kết luận trên một lần chạy.
3. Đánh giá cuối bằng **accuracy + F1 từng lớp + confusion matrix**, và thử thêm biến thể có
   class weight để trả lời câu hỏi còn bỏ ngỏ ở D3.

### Giai đoạn 4 — mô hình cuối (A4 + augmentation, 40 epoch)

| ten | seed | class weight | Epoch tốt nhất | Val acc | Val macro F1 | Thời gian |
|---|---|---:|---:|---:|---:|---:|
| F42 | 42 | không | 36 / 40 | 0,6555 | 0,6087 | 1633 s |
| F43 | 43 | không | 29 / 37 | 0,6444 | 0,5961 | 1662 s |
| F44 | 44 | không | 37 / 40 | 0,6576 | 0,6138 | 1678 s |
| F42_cw | 42 | **có** | 39 / 40 | 0,6371 | 0,5869 | 1660 s |

- Trung bình 3 seed: **val accuracy 0,6525 ± 0,0071**, **macro F1 0,6062 ± 0,0091**.
- Khoảng cách train–validation của F44 chỉ còn **0,018** (train 0,675 / val 0,657), so với
  **0,324** của A4 ở 18 epoch → augmentation + ngân sách epoch dài đã hãm quá khớp đúng cách.
- **Class weight không có lợi**: F42_cw thấp hơn F42 ở cả accuracy (−1,8 điểm) lẫn macro F1
  (−2,2 điểm). Khi mô hình đã đủ năng lực và có augmentation, lớp hiếm tự học được.

Kết quả test của F44 (seed tốt nhất theo validation, chạy một lần):

| | Baseline | Mô hình cuối | Chênh |
|---|---:|---:|---:|
| Test accuracy | 0,5237 | **0,6503** | +12,7 điểm |
| Test macro F1 | 0,4278 | **0,6237** | +19,6 điểm |
| Recall Ghê tởm | 0,00 | **0,53** | +0,53 |
| Recall Sợ hãi | 0,23 | 0,38 | +0,15 |

Năm cặp nhầm nhiều nhất: Sợ hãi→Buồn 23,3%; Ghê tởm→Giận 18,9%; Bình thường→Buồn 17,8%;
Buồn→Bình thường 17,2%; Giận→Buồn 16,7%. Lớp `Buồn` xuất hiện trong 4/5 cặp — nó đóng vai trò
"lớp hút" khi mô hình phân vân.

Kết luận chung: yếu tố cải thiện lớn nhất là **ngân sách huấn luyện + augmentation**
(0,589 → 0,6525 val), sau đó là **dung lượng mô hình**; optimizer gần như không ảnh hưởng, còn
class weight và dropout lớn đều làm giảm chất lượng.
