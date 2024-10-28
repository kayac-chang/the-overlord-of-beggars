# 7-11 (舊版門市搜尋)

## Get Town By City ID 透過城市編號取得行政區

```sh
commandid=GetTown
cityid=01
curl 'https://emap.pcsc.com.tw/EMapSDK.aspx' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  --data-raw "commandid=$commandid&cityid=$cityid" | xmllint --format -
```

```
iMapSDKOutput {
    MessageID: str
    CommandID: GetTown
    Status: str
    TimeStamp: str
    GeoPosition: {
        TownID: str // 行政區編號
        TownName: str // 行政區名稱
        X: number // should divide by 1_000_000
        Y: number // should divide by 1_000_000
    }[]
}
```

### cityid
```
台北市: 01
基隆市: 02
新北市: 03
桃園市: 04
新竹市: 05
新竹縣: 06
苗栗縣: 07
台中市: 08
彰化縣: 10
南投縣: 11
雲林縣: 12
嘉義市: 13
嘉義縣: 14
台南市: 15
高雄市: 17
屏東縣: 19
宜蘭縣: 20
花蓮縣: 21
台東縣: 22
澎湖縣: 23
連江縣: 24
金門縣: 25
```

## Search Store By City And Town 透過行政區取得門市資訊

```sh
commandid=SearchStore
city=台北市
town=松山區
encoded_city=$(printf $city | jq -sRr @uri)
encoded_town=$(printf $town | jq -sRr @uri)
curl 'https://emap.pcsc.com.tw/EMapSDK.aspx' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  --data-raw "commandid=$commandid&city=$encoded_city&town=$encoded_town" | xmllint --format -
```

```
iMapSDKOutput {
    MessageID: str
    CommandID: SearchStore
    Status: str
    TimeStamp: str
    GeoPosition: {
        POIID: str // 店號
        POIName: str // 店名
        X: number // should divide by 1_000_000
        Y: number // should divide by 1_000_000
        Telno: str
        FaxNo: str
        Address: str
    }[]
}
```

## Get Store By Store ID 透過門市號碼取得門市資訊

```sh
commandid=SearchStore
id=253565
curl 'https://emap.pcsc.com.tw/EMapSDK.aspx' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  --data-raw "commandid=$commandid&ID=$id" | xmllint --format -
```

```
iMapSDKOutput {
    MessageID: str
    CommandID: str
    Status: str
    TimeStamp: str
    GeoPosition: {
        POIID: str // 店號
        POIName: str // 店名
        X: number // should divide by 1_000_000
        Y: number // should divide by 1_000_000
        Telno: str
        FaxNo: str
        Address: str
    }
}
```
