# Nhật ký thí nghiệm — CNN nhận dạng biểu cảm (FER2013)

File này ghi lại từng lần chạy: dùng cấu hình gì, ra kết quả bao nhiêu, nhận xét và quyết định
tiếp theo. Số liệu thô (mọi cột) nằm trong `runs.csv`, còn lịch sử loss/accuracy từng epoch nằm
trong `logs/<exp_id>_history.csv`.

## Thiết lập chung

| Thành phần | Giá trị |
|---|---|
| Dữ liệu | 28.709 ảnh train, 7.178 ảnh test (48×48, 1 kênh) |
| Chia tập | stratified 90/10 trên train → 25.838 train / 2.871 validation |
| Seed | 42 (Python, numpy, torch) |
| Chuẩn hoá | trừ mean 0,5077, chia std 0,2551 (tính trên train) |
| Đánh giá | accuracy trên validation để chọn epoch; test chỉ dùng một lần |
| Metric phụ | F1 từng lớp, vì dữ liệu mất cân bằng 16,5 lần |

Quy ước mã thí nghiệm: `BASE` là baseline, các nhóm sau đánh số theo biến khảo sát
(`A2/A3/A4` = số khối conv, `B1/B2/B3` = độ rộng, `C1..C4` = optimizer và tốc độ học,
`D1..D4` = chống quá khớp).

## Bảng thí nghiệm

| exp_id | Mô hình | Siêu tham số chính | Val acc | Test acc | Nhận xét | Quyết định |
|---|---|---|---|---|---|---|
| BASE | CNN 3 khối 32-64-128, GAP, dropout 0,3 (93.799 tham số) | Adam 1e-3, batch 64, 18 epoch, không augmentation | 0,5385 (epoch 15) | **0,5237** | Loss train vẫn giảm đến epoch cuối, khoảng cách train–val chỉ 2 điểm % → **chưa quá khớp mà còn thiếu năng lực/thiếu epoch**. Lớp `disgust` có recall = 0, `fear` 0,23, `sad` 0,34 → mô hình nghiêng hẳn về lớp đa số. | Lấy làm mốc so sánh. Giai đoạn sau thử tăng độ sâu/rộng (A, B), đổi optimizer (C), thêm augmentation và class weight (D). |

## Ghi chú theo từng giai đoạn

### Giai đoạn 2 — baseline

- Thử 12 epoch trước: test 46,99%, loss vẫn giảm ở epoch cuối → kết luận là **cắt ngang quá
  sớm**, không phải quá khớp. Tăng lên 18 epoch được 52,37%.
- Validation loss dao động khá mạnh giữa các epoch (1,24 → 1,35 → 1,24), nguyên nhân là validation
  chỉ có 2.871 ảnh nên mỗi lần đổi epoch là đổi một mẫu ước lượng khá nhiễu.
- Early stopping chưa kích hoạt vì val accuracy vẫn còn tăng.
- F1 macro chỉ 0,428 trong khi accuracy 0,524 — chênh lệch này chính là hệ quả của mất cân bằng,
  và là lý do phải báo cáo thêm F1 chứ không chỉ accuracy.
