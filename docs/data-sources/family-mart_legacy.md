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

## 店家服務

lcoffeey: 咖啡複合店
rpotatoy: 烤馬鈴薯
hdy: 哈逗堡
smarty: 智能咖啡機
teay: 福爾摩沙茶館
sweetpotatoy: 夯番薯
photoy: 相片立可得
csy: ChargeSPOT
goroy: gogoro電池交換站
icey: Fami!ce(有販售店)
icecreamy: Fami!ce(單口味店)
twoicey: Fami!ce(雙口味店)
famiicey: Fami!ce(特殊造型店)
cardy: Picard (法國優質冷凍食品)
supery: 全家FamiSuper選品超市店
tanhouy: 天和鮮物
resty: 休憩區
toilety: 廁所
vegy: 生鮮蔬菜
laundryy: Fami自助洗衣
desserty: SOHOT炎選-現烤點心
costcoy: 好市多專區
haday: 哈根達斯冰箱
tripky: 鼎王麻辣蛋
freshy: 蒸新鮮
ecoy: 塑環真®循環杯
grilly: SOHOT炎選-炸烤物
cooknowy: 馬尚煮
hogany: 哈肯舖
beary: 小熊菓子
musly: 穆斯林友善商品店舖
nporky: 無豬肉熱食友善店
unknow: 未知
