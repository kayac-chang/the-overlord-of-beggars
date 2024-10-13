# Product Requirement Document

## 用戶需求

### 第一階段

關鍵字查詢門市的即期品庫存情況
    - 關鍵字：商品名稱、商品類別、地點
    - 自然語言判斷 (optional)

### 第二階段

- 願望清單的剩食通知
  有收藏的剩食，出現在店鋪的時候通知使用者

### 第三階段

- 剩食圖鑑
  剩食詳細資訊：營養標示

- 小資紀錄
  省了多少錢做個紀錄（小資族看到自己省了多少錢會很開心）

- 剩食排行榜
  標記全台剩食出現次數，統計哪個是大家最不喜歡吃的商品（可以延伸出來讓商家知道你這個東西銷量不好）

- 剩食店家排名
  讓使用者知道哪邊平均出現剩食最多店家

## 流程

### 地址查詢門市的即期品庫存情況

using the address search function

submit the query to the server

search the stores from data sources ( 7-11, FamilyMart, ...etc )
    -> background. save the stores to the database

search the stock of the stores from data sources
    -> background. save the stock information to the database

summary the stock and return the result to the user

### 背景追蹤門市庫存

background job to track the stock of the stores every 5 mins

loop through the stores in the database

search the stock of the stores from data sources

save the stock information to the database

### 附近門市的即期品庫存情況

using the geolocation search function

submit the query to the server

search the stores from data sources ( 7-11, FamilyMart, ...etc )
    -> background. save the stores to the database

search the stock of the stores from data sources
    -> background. save the stock information to the database

summary the stock and return the result to the user


## 資料庫

### Store 門市

```
Store {
    id
    name
    address
    geolocation: {
        latitude
        longitude
    }
}
```

### Stock 門市即期品庫存

```
Stock {
    store_id -> Store.id
    product_id -> Product.id
    quantity
}
```

### 即期品

```
Near Expired Food {
    id
    name
    category_id -> Category.id
}
```

### 商品類別

```
Category {
    id
    name
}
```

## 技術細節

### 後端語言，框架

python, fastapi, fly.io

### 資料庫

postgres, supabase

### 前端框架，部署

react, remix, fly.io

### 背景任務

github action


## 前端呈現

###

