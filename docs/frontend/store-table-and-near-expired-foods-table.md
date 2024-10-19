# 店家與庫存 Table

## 資料

type 即期品 = {
    品名
    品項
    數量
}

type 店家 = {
    店號
    店名
    地址
    與用戶的直線距離 (nullable, default: --)
}

type 店家即期品資訊 = 店家 & { list of 即期品 }

## Definition

### input

- 店號
- 用戶的當前位置 (optional)

### output

店家即期品資訊
