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
| M4_mlp_h64_lr0.01_do0.0_scr | MLP1-screen | `{"h": 64, "lr": 0.01, "do": 0.0}` | 0.1296 ± 0.0 | screening fold0 | loại (screening) |
| M4_mlp_h64_lr0.01_do0.1_scr | MLP1-screen | `{"h": 64, "lr": 0.01, "do": 0.1}` | 0.14094 ± 0.0 | screening fold0 | loại (screening) |
| M4_mlp_h64_lr0.003_do0.0_scr | MLP1-screen | `{"h": 64, "lr": 0.003, "do": 0.0}` | 0.12883 ± 0.0 | screening fold0 | loại (screening) |
| M4_mlp_h64_lr0.003_do0.1_scr | MLP1-screen | `{"h": 64, "lr": 0.003, "do": 0.1}` | 0.1477 ± 0.0 | screening fold0 | loại (screening) |
| M4_mlp_h128_lr0.01_do0.0_scr | MLP1-screen | `{"h": 128, "lr": 0.01, "do": 0.0}` | 0.13168 ± 0.0 | screening fold0 | loại (screening) |
| M4_mlp_h128_lr0.01_do0.1_scr | MLP1-screen | `{"h": 128, "lr": 0.01, "do": 0.1}` | 0.13666 ± 0.0 | screening fold0 | loại (screening) |
| M4_mlp_h128_lr0.003_do0.0_scr | MLP1-screen | `{"h": 128, "lr": 0.003, "do": 0.0}` | 0.12867 ± 0.0 | screening fold0 | loại (screening) |
| M4_mlp_h128_lr0.003_do0.1_scr | MLP1-screen | `{"h": 128, "lr": 0.003, "do": 0.1}` | 0.13176 ± 0.0 | screening fold0 | loại (screening) |
| M4_mlp_h128_lr0.003_do0.0 | MLP1 | `{"h": 128, "lr": 0.003, "do": 0.0}` | 0.12591 ± 0.00987 | refine 5-fold | dự phòng |
| M4_mlp_h64_lr0.003_do0.0 | MLP1 | `{"h": 64, "lr": 0.003, "do": 0.0}` | 0.1252 ± 0.0102 | refine 5-fold | giữ → ensemble |
| M5_mlp_a128x64_do0.1_bn0_scr | MLPdeep-screen | `{"arch": [128, 64], "do": 0.1, "bn": false}` | 0.15892 ± 0.0 | screening fold0 | loại (screening) |
| M5_mlp_a128x64_do0.1_bn1_scr | MLPdeep-screen | `{"arch": [128, 64], "do": 0.1, "bn": true}` | 0.4899 ± 0.0 | screening fold0 | loại (screening) |
| M5_mlp_a128x64_do0.2_bn0_scr | MLPdeep-screen | `{"arch": [128, 64], "do": 0.2, "bn": false}` | 0.17514 ± 0.0 | screening fold0 | loại (screening) |
| M5_mlp_a128x64_do0.2_bn1_scr | MLPdeep-screen | `{"arch": [128, 64], "do": 0.2, "bn": true}` | 0.49242 ± 0.0 | screening fold0 | loại (screening) |
| M5_mlp_a128x128_do0.1_bn0_scr | MLPdeep-screen | `{"arch": [128, 128], "do": 0.1, "bn": false}` | 0.1536 ± 0.0 | screening fold0 | loại (screening) |
| M5_mlp_a128x128_do0.1_bn1_scr | MLPdeep-screen | `{"arch": [128, 128], "do": 0.1, "bn": true}` | 0.45513 ± 0.0 | screening fold0 | loại (screening) |
| M5_mlp_a128x128_do0.2_bn0_scr | MLPdeep-screen | `{"arch": [128, 128], "do": 0.2, "bn": false}` | 0.17101 ± 0.0 | screening fold0 | loại (screening) |
| M5_mlp_a128x128_do0.2_bn1_scr | MLPdeep-screen | `{"arch": [128, 128], "do": 0.2, "bn": true}` | 0.44472 ± 0.0 | screening fold0 | loại (screening) |
| M5_mlp_a128x128_do0.1_bn0 | MLPdeep | `{"arch": [128, 128], "do": 0.1, "bn": false}` | 0.14114 ± 0.00867 | refine 5-fold | dự phòng ensemble |
| M5_mlp_a128x64_do0.1_bn0 | MLPdeep | `{"arch": [128, 64], "do": 0.1, "bn": false}` | 0.145 ± 0.00519 | refine 5-fold | loại (thua bản 128x128) |
| M6_emb_m0.25_w64_do0.15_scr | EmbMLP-screen | `{"mult": 0.25, "w": 64, "do": 0.15}` | 0.13362 ± 0.0 | screening fold0 | loại (screening) |
| M6_emb_m0.5_w64_do0.15_scr | EmbMLP-screen | `{"mult": 0.5, "w": 64, "do": 0.15}` | 0.14156 ± 0.0 | screening fold0 | loại (screening) |
| M6_emb_m0.25_w64_do0.15 | EmbMLP | `{"mult": 0.25, "w": 64, "do": 0.15}` | 0.13484 ± 0.0086 | refine 5-fold | giữ → ensemble (đa dạng) |
| M6_emb_m0.5_w64_do0.15 | EmbMLP | `{"mult": 0.5, "w": 64, "do": 0.15}` | 0.15778 ± 0.02221 | refine 5-fold | dự phòng |
| M7_blend | Blend-4 | `{"w": [0.9, 0.0, 0.0, 0.1], "members": ["Ridge-10", "Enet", "M4", "M6"]}` | 0.1114 ± 0.00787 | ensemble 4 mô hình, trọng số tune trên OOF | LB lan 1: 0.12581 | bản nộp Kaggle lần 1 |
| M2b_ridge_l3_scr | RidgeB-screen | `{"l2": 3.0, "feat": "308"}` | 0.11829 ± 0.0 | screening fold0, đặc trưng mới | loại (screening) |
| M2b_ridge_l10_scr | RidgeB-screen | `{"l2": 10.0, "feat": "308"}` | 0.11846 ± 0.0 | screening fold0, đặc trưng mới | loại (screening) |
| M2b_ridge_l30_scr | RidgeB-screen | `{"l2": 30.0, "feat": "308"}` | 0.11962 ± 0.0 | screening fold0, đặc trưng mới | loại (screening) |
| M2b_ridge_l100_scr | RidgeB-screen | `{"l2": 100.0, "feat": "308"}` | 0.12217 ± 0.0 | screening fold0, đặc trưng mới | loại (screening) |
| M2b_ridge_l3 | RidgeB | `{"l2": 3.0, "feat": "308"}` | 0.11361 ± 0.00732 | refine 5-fold, đặc trưng mới | loại (thua l10) |
| M2b_ridge_l10 | RidgeB | `{"l2": 10.0, "feat": "308"}` | 0.11201 ± 0.00786 | refine 5-fold, đặc trưng mới | thua Ridge cũ, chỉ để trộn thử |
| M7b_blend2 | Blend2 | `{"w_old": 1.0, "w_new": 0.0}` | 0.1114 ± 0.00787 | M7 cũ + Ridge đặc trưng mới | KHÔNG nộp (giống hệt lần 1) |
| M4b_mlp_h64_scr | MLP1B-screen | `{"h": 64, "feat": "308"}` | 0.13108 ± 0.0 | screening fold0, đặc trưng mới | loại (screening) |
| M4b_mlp_h128_scr | MLP1B-screen | `{"h": 128, "feat": "308"}` | 0.13361 ± 0.0 | screening fold0, đặc trưng mới | loại (screening) |
| M4b_mlp_h64 | MLP1B | `{"h": 64, "feat": "308"}` | 0.12397 ± 0.01216 | refine 5-fold, đặc trưng mới | giữ (thắng M4 cũ) -> trộn M7c |
| M7c_blend3 | Blend3 | `{"w_old": 0.9, "w_new": 0.1}` | 0.11128 ± 0.00845 | M7 cũ + M4b đặc trưng mới | bản nộp Kaggle lần 2 |
| M2c_ridge_l30_scr | RidgeC-screen | `{"l2": 30.0}` | 0.1195 ± 0.0 | screening fold0, phạt mạnh | loại (screening) |
| M2c_ridge_l100_scr | RidgeC-screen | `{"l2": 100.0}` | 0.12234 ± 0.0 | screening fold0, phạt mạnh | loại (screening) |
| M2c_ridge_l300_scr | RidgeC-screen | `{"l2": 300.0}` | 0.12816 ± 0.0 | screening fold0, phạt mạnh | loại (screening) |
| M2c_ridge_l30 | RidgeC | `{"l2": 30.0}` | 0.11222 ± 0.00835 | refine 5-fold, phạt mạnh | giữ để trộn (ít overfit hơn) |
| M7d_blend4 | Blend4 | `{"w_cur": 0.7, "w_new": 0.3}` | 0.11103 ± 0.00848 | M7 hiện tại + Ridge phạt mạnh | bản nộp Kaggle lần 3 |
