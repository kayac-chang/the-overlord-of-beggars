# Family Mart

Website: <https://foodmap.family.com.tw/>

- [Family Mart](#family-mart)
  - [MapList](#maplist)
  - [MapClassificationInfo](#mapclassificationinfo)
  - [MapProductInfo](#mapproductinfo)
    - [query by postcode](#query-by-postcode)
    - [query by store id](#query-by-store-id)
    - [query by lat-lng](#query-by-lat-lng)

## MapList

```sh
curl -s 'https://stamp.family.com.tw/api/maps/MapList' \
  | jq
```

<details>
  <summary><strong>Response Type Definition</strong></summary>

```ts
export interface Root {
  code: number
  data: Daum[]
  message: string
}

export interface Daum {
  projectCode: string
  name: string
  copyWrite: string
  hexList: HexList[]
  iconCount: number
  mapimgUrl: string
  popimgUrl: string
  mapUrl: string
  status: number
  sort: number
  longestDistance: string
  specifiedUrl: string
}

export interface HexList {
  hex0: string
  hex1: string
  hex2: string
  hex3: string
}
```

</details>

## MapClassificationInfo

```sh
PROJECT_CODE=202106302
curl -s "https://stamp.family.com.tw/api/maps/MapClassificationInfo?ProjectCode=${PROJECT_CODE}" \
  | jq
```

<details>
  <summary><strong>Response Type Definition</strong></summary>

```ts
export interface Root {
  code: number
  data: Daum[]
  message: string
}

export interface Daum {
  groupCode: string
  groupName: string
  iconURL: string
  categories: Category[]
}

export interface Category {
  categoryCode: string
  categoryName: string
  products: Product[]
}

export interface Product {
  productCode: string
  productName: string
}
```

</details>

## MapProductInfo

### query by postcode

```sh
PROJECT_CODE=202106302
POST_INFO=105
PAYLOAD=$(jq -nc \
  --arg PROJECT_CODE "${PROJECT_CODE}" \
  --arg POST_INFO "${POST_INFO}" \
  '{ProjectCode:$PROJECT_CODE, PostInfo:$POST_INFO}'
)
curl -s 'https://stamp.family.com.tw/api/maps/MapProductInfo' \
  -X 'POST' \
  -H 'Content-Type: application/json;charset=utf-8' \
  --data-raw "${PAYLOAD}" \
  | jq
```

### query by store id

```sh
PROJECT_CODE=202106302   # 乞丐時光
OLD_P_KEYS=000009,000686 # 分店id
PAYLOAD=$(jq -nc \
  --arg PROJECT_CODE "${PROJECT_CODE}" \
  --arg OLD_P_KEYS "${OLD_P_KEYS}" \
  '{ProjectCode:$PROJECT_CODE, OldPKeys:$OLD_P_KEYS|split(",")}'
)
curl -s 'https://stamp.family.com.tw/api/maps/MapProductInfo' \
  -X 'POST' \
  -H 'Content-Type: application/json;charset=utf-8' \
  --data-raw "${PAYLOAD}" \
  | jq
```

### query by lat-lng

```sh
PROJECT_CODE=202106302   # 乞丐時光
LAT=25.0352
LNG=121.55765
PAYLOAD=$(jq -nc \
  --arg PROJECT_CODE "${PROJECT_CODE}" \
  --arg LAT "${LAT}" \
  --arg LNG "${LNG}" \
  '{ProjectCode:$PROJECT_CODE, latitude:$LAT|tonumber, longitude:$LNG|tonumber}'
)
curl -s 'https://stamp.family.com.tw/api/maps/MapProductInfo' \
  -X 'POST' \
  -H 'Content-Type: application/json;charset=utf-8' \
  --data-raw "${PAYLOAD}" \
  | jq
```

<details>
  <summary><strong>Response Type Definition</strong></summary>

```ts
export interface Root {
  code: number
  data: Daum[]
  message: string
}

export interface Daum {
  oldPKey: string
  name: string
  tel: string
  post: any
  city: any
  areaCode: any
  periodType: number
  longitude: number
  latitude: number
  distance: number
  address: string
  updateDate: string
  info: Info[]
}

export interface Info {
  code: string
  name: string
  iconURL: string
  qty: number
  categories: Category[]
}

export interface Category {
  code: string
  name: string
  qty: number
  products: Product[]
}

export interface Product {
  code: string
  name: string
  qty: number
}
```

</details>
