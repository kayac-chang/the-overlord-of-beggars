# 7-11 (舊版門市搜尋)

## Get Store By Store ID 透過門市號碼取得門市資訊

```sh
curl 'https://emap.pcsc.com.tw/EMapSDK.aspx' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  --data-raw 'commandid=SearchStore&ID=253565'
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<iMapSDKOutput>
   <MessageID>00000</MessageID>
   <CommandID>SearchStore</CommandID>
   <Status>連線成功</Status>
   <TimeStamp>2024/10/25 下午 10:29:56</TimeStamp>
   <GeoPosition>
      <POIID>253565</POIID>
      <POIName>學城</POIName>
      <X>121455445</X>
      <Y>24987597</Y>
      <Telno>(02)22652690</Telno>
      <FaxNo>(02)22601907</FaxNo>
      <Address>新北市土城區學府路一段118號</Address>
   </GeoPosition>
</iMapSDKOutput>
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
