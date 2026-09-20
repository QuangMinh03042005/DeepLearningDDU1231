# Nhật ký phát triển mô hình — Lab02 House Prices

Metric: RMSLE trên thang log(SalePrice). CV: 5-fold, seed cố định.

| exp_id | Mô hình | Siêu tham số chính | CV-RMSLE mean ± std | Nhận xét | Quyết định |
|---|---|---|---|---|---|
| M1b_linear_top20 | Linear-OLS (top-20) | `{"k": 20, "solver": "lstsq", "cols": ["OverallQual", "GrLivArea", "GarageCars", "GarageArea", "TotalBsmtSF", "1stFlrSF", "FullBath", "YearBuilt", "YearRemodAdd", "GarageYrBlt", "TotRmsAbvGrd", "Fireplaces", "MasVnrArea", "BsmtFinSF1", "LotFrontage", "WoodDeckSF", "OpenPorchSF", "2ndFlrSF", "HalfBath", "LotArea"]}` | 0.13556 ± 0.01097 | ablation: chi 20 bien so manh nhat | giữ full 302 đặc trưng, chờ M1 đối chứng |
