from typing import TypedDict


class City(TypedDict):
    city_id: str
    city_name: str


list_of_city: list[City] = [
    {"city_id": "01", "city_name": "台北市"},
    {"city_id": "02", "city_name": "基隆市"},
    {"city_id": "03", "city_name": "新北市"},
    {"city_id": "04", "city_name": "桃園市"},
    {"city_id": "05", "city_name": "新竹市"},
    {"city_id": "06", "city_name": "新竹縣"},
    {"city_id": "07", "city_name": "苗栗縣"},
    {"city_id": "08", "city_name": "台中市"},
    {"city_id": "10", "city_name": "彰化縣"},
    {"city_id": "11", "city_name": "南投縣"},
    {"city_id": "12", "city_name": "雲林縣"},
    {"city_id": "13", "city_name": "嘉義市"},
    {"city_id": "14", "city_name": "嘉義縣"},
    {"city_id": "15", "city_name": "台南市"},
    {"city_id": "17", "city_name": "高雄市"},
    {"city_id": "19", "city_name": "屏東縣"},
    {"city_id": "20", "city_name": "宜蘭縣"},
    {"city_id": "21", "city_name": "花蓮縣"},
    {"city_id": "22", "city_name": "台東縣"},
    {"city_id": "23", "city_name": "澎湖縣"},
    {"city_id": "24", "city_name": "連江縣"},
    {"city_id": "25", "city_name": "金門縣"},
]
