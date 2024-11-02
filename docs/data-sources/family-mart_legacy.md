# Family Mart (舊版門市搜尋)

## Get Towns By City Name 透過城市名取得行政區

```sh
key=6F30E8BF706D653965BDE302661D1241F8BE9EBC
searchType=ShowTownList
city=台北市
fun=storeTownList
curl 'https://api.map.com.tw/net/familyShop.aspx' \
    -H 'Referer: https://www.family.com.tw/' \
    --data "searchType=$searchType" \
    --data "type=" \
    --data "fun=$fun" \
    --data-urlencode "city=$city" \
    --data "key=$key"
```

```
StoreTownList = {
    "post": str // 郵遞區號
    "town": str // 行政區名
    "city": str // 城市名
}[]
```

### list of city
```
台北市
基隆市
新北市
桃園市
新竹市
新竹縣
苗栗縣
台中市
彰化縣
南投縣
雲林縣
嘉義市
嘉義縣
台南市
高雄市
屏東縣
宜蘭縣
花蓮縣
台東縣
澎湖縣
連江縣
金門縣
```

## Get Stores By City And Town 透過行政區取得門市資訊

```sh
key=6F30E8BF706D653965BDE302661D1241F8BE9EBC
searchType=ShopList
city=台北市
area=中正區
fun=showStoreList
curl 'https://api.map.com.tw/net/familyShop.aspx' \
    -H 'Referer: https://www.family.com.tw/' \
    -d "searchType=$searchType" \
    -d 'type=' \
    -d "fun=$fun" \
    --data-urlencode "city=$city" \
    --data-urlencode "area=$area" \
    --data-urlencode "road=" \
    -d "key=$key"
```

```
showStoreList = {
    "NAME": str // 門市名稱
    "px": float // 經度
    "py": float // 緯度
    "addr": str // 地址
    "oldpkey": str // 門市編號
    "post": str // 郵遞區號
    "road": str // 道路名稱
}[]
```

