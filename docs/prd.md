# Product Requirement Document

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


