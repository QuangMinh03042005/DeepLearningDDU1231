"""Vẽ sơ đồ kiến trúc CNN baseline bằng VisualTorch (kiểu LeNet / chồng feature map).

Script chỉ để xuất hình cho báo cáo, không tham gia huấn luyện. Kiến trúc ở đây giống hệt
`SmallCNN` trong notebooks/cnn_fer.ipynb:

    Conv3x3 (1->32)  + BN + ReLU + MaxPool2
    Conv3x3 (32->64) + BN + ReLU + MaxPool2
    Conv3x3 (64->128)+ BN + ReLU + MaxPool2
    GlobalAvgPool -> Dropout 0.3 -> Linear 128->7

Vì VisualTorch lấy tên lớp làm nhãn, ta đặt lớp con với tên ngắn (Conv, MaxPool, GAP, FC)
cho nhãn khỏi dài dòng. Lớp con vẫn kế thừa lớp torch gốc nên cấu trúc mô hình không đổi.

Chạy: .\\.venv\\Scripts\\python report\\figures\\ve_kien_truc_visualtorch.py
"""

from pathlib import Path

import matplotlib
import torch
from PIL import ImageFont
from torch import nn
from visualtorch import render

HERE = Path(__file__).parent
FONT_PATH = Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans.ttf"


# --- Lớp con chỉ để đổi tên hiển thị trên hình ---
class Conv(nn.Conv2d):
    pass


class MaxPool(nn.MaxPool2d):
    pass


class GAP(nn.AdaptiveAvgPool2d):
    pass


class FC(nn.Linear):
    pass


def khoi(c_in: int, c_out: int) -> list[nn.Module]:
    """Một khối tích chập: Conv 3x3 -> BN -> ReLU -> MaxPool."""
    return [
        Conv(c_in, c_out, kernel_size=3, padding=1, bias=False),
        nn.BatchNorm2d(c_out),
        nn.ReLU(inplace=True),
        MaxPool(2),
    ]


class SmallCNN(nn.Module):
    """Giống hệt mô hình trong notebook (93.799 tham số)."""

    def __init__(
        self, channels=(32, 64, 128), n_classes: int = 7, p_dropout: float = 0.3
    ):
        super().__init__()
        layers, c_in = [], 1
        for c_out in channels:
            layers += khoi(c_in, c_out)
            c_in = c_out
        self.features = nn.Sequential(*layers)
        self.pool = GAP(1)
        self.dropout = nn.Dropout(p_dropout)
        self.fc = FC(c_in, n_classes)

    def forward(self, x):
        x = self.pool(self.features(x))
        return self.fc(self.dropout(torch.flatten(x, 1)))


def main() -> None:
    model = SmallCNN().eval()
    print(f"Số tham số: {sum(p.numel() for p in model.parameters()):,}")

    chung = {
        "model": model,
        "input_shape": (1, 1, 48, 48),
        "style": "lenet",
        # Ẩn BN/ReLU (đã ghi trong chú thích hình) cho hình khỏi rối
        "type_ignore": [nn.BatchNorm2d, nn.ReLU, nn.Dropout],
        "max_channels": 8,  # chỉ vẽ 8 mặt mỗi chồng cho gọn
        "scale_xy": 2.2,
    }

    # Bản đầy đủ: có kích thước tensor dưới mỗi lớp
    anh = render(
        **chung,
        spacing=190,
        font=ImageFont.truetype(str(FONT_PATH), 26),
        show_dimension=True,
        legend=False,
        to_file=str(HERE / "kien_truc_visualtorch.png"),
    )
    print("Kích thước ảnh:", anh.size)
    print("Đã lưu:", HERE / "kien_truc_visualtorch.png")


if __name__ == "__main__":
    main()
