# Nhật ký phát triển mô hình — Lab02 House Prices

Metric: RMSLE trên thang log(SalePrice). CV: 5-fold, seed cố định.

| exp_id | Mô hình | Siêu tham số chính | CV-RMSLE mean ± std | Nhận xét | Quyết định |
|---|---|---|---|---|---|
| M1b_linear_top20 | Linear-OLS (top-20) | `{"k": 20, "solver": "lstsq", "cols": ["OverallQual", "GrLivArea", "GarageCars", "GarageArea", "TotalBsmtSF", "1stFlrSF", "FullBath", "YearBuilt", "YearRemodAdd", "GarageYrBlt", "TotRmsAbvGrd", "Fireplaces", "MasVnrArea", "BsmtFinSF1", "LotFrontage", "WoodDeckSF", "OpenPorchSF", "2ndFlrSF", "HalfBath", "LotArea"]}` | 0.13556 ± 0.01097 | ablation: chi 20 bien so manh nhat | giữ full 302 đặc trưng, chờ M1 đối chứng |
| M0_mean | Baseline-mean | `{}` | 0.39604 ± 0.01831 | mốc sàn | mốc sàn, loại |
| M0_median | Baseline-median | `{}` | 0.39699 ± 0.01782 | mốc sàn | mốc sàn, loại |
| M2_ridge_l0.001_scr | Ridge-screen | `{"l2": 0.001}` | 0.14753 ± 0.0 | screening fold0 | loại (screening) |
| M2_ridge_l0.01_scr | Ridge-screen | `{"l2": 0.01}` | 0.12681 ± 0.0 | screening fold0 | loại (screening) |
| M2_ridge_l0.1_scr | Ridge-screen | `{"l2": 0.1}` | 0.12449 ± 0.0 | screening fold0 | loại (screening) |
| M2_ridge_l1_scr | Ridge-screen | `{"l2": 1.0}` | 0.11979 ± 0.0 | screening fold0 | loại (screening) |
| M2_ridge_l10_scr | Ridge-screen | `{"l2": 10.0}` | 0.11834 ± 0.0 | screening fold0 | loại (screening) |
| M2_ridge_l100_scr | Ridge-screen | `{"l2": 100.0}` | 0.12234 ± 0.0 | screening fold0 | loại (screening) |
| M2_ridge_l1000_scr | Ridge-screen | `{"l2": 1000.0}` | 0.14157 ± 0.0 | screening fold0 | loại (screening) |
| M2_ridge_l10 | Ridge | `{"l2": 10.0}` | 0.11193 ± 0.00794 | refine 5-fold | giữ → ensemble (vô địch GĐ2a) |
| M2_ridge_l1 | Ridge | `{"l2": 1.0}` | 0.1156 ± 0.00709 | refine 5-fold | dự phòng |
| M1_linear_full | Linear-OLS (full) | `{"solver": "solve"}` | 0.12826 ± 0.01044 | full 302 đặc trưng | giữ làm mốc, chờ ensemble |
| M3_enet_a1.0_l1e-05_scr | ElasticNet-screen | `{"alpha": 1.0, "l2": 1e-05}` | 0.12496 ± 0.0 | screening fold0 | loại (screening) |
| M3_enet_a1.0_l0.0001_scr | ElasticNet-screen | `{"alpha": 1.0, "l2": 0.0001}` | 0.13062 ± 0.0 | screening fold0 | loại (screening) |
| M3_enet_a1.0_l0.001_scr | ElasticNet-screen | `{"alpha": 1.0, "l2": 0.001}` | 0.14398 ± 0.0 | screening fold0 | loại (screening) |
| M3_enet_a0.5_l1e-05_scr | ElasticNet-screen | `{"alpha": 0.5, "l2": 1e-05}` | 0.12797 ± 0.0 | screening fold0 | loại (screening) |
| M3_enet_a0.5_l0.0001_scr | ElasticNet-screen | `{"alpha": 0.5, "l2": 0.0001}` | 0.12779 ± 0.0 | screening fold0 | loại (screening) |
| M3_enet_a0.5_l0.001_scr | ElasticNet-screen | `{"alpha": 0.5, "l2": 0.001}` | 0.14227 ± 0.0 | screening fold0 | loại (screening) |
| M3_enet_a0.2_l1e-05_scr | ElasticNet-screen | `{"alpha": 0.2, "l2": 1e-05}` | 0.12659 ± 0.0 | screening fold0 | loại (screening) |
| M3_enet_a0.2_l0.0001_scr | ElasticNet-screen | `{"alpha": 0.2, "l2": 0.0001}` | 0.12935 ± 0.0 | screening fold0 | loại (screening) |
| M3_enet_a0.2_l0.001_scr | ElasticNet-screen | `{"alpha": 0.2, "l2": 0.001}` | 0.13286 ± 0.0 | screening fold0 | loại (screening) |
| M3_enet_a1.0_l1e-05 | ElasticNet | `{"alpha": 1.0, "l2": 1e-05}` | 0.12392 ± 0.01058 | refine 5-fold | dự phòng |
| M3_enet_a0.2_l1e-05 | ElasticNet | `{"alpha": 0.2, "l2": 1e-05}` | 0.12389 ± 0.01054 | refine 5-fold | giữ → ensemble |
