# 前端 PRD

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


## 附近店家即期品搜尋

### input

- 用戶的當前位置
- 搜索範圍 (default: 1 公里內)

### output

list of 店家即期品資訊
sort by 與用戶的直線距離 (近到遠)

## 關鍵字搜尋

### input

- 關鍵字 (店名，地址，品名)
- 用戶的當前位置 (optional)

### output

list of 店家即期品資訊
sort by 關鍵字 match 到的字數 (多到少)

## 品項搜索

### input

- 品項
- 用戶的當前位置

### output

list of 店家即期品資訊
sort by 與用戶的直線距離 (近到遠)

## 店家庫存詳情 (optional)

### input

- 店號
- 用戶的當前位置 (optional)

### output

店家即期品資訊
