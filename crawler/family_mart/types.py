from enum import Enum


class FamilyMartService(str, Enum):
    # FamilyMart 店內服務
    LCOFFEE = "lcoffee"  # 咖啡複合店
    RPOTATO = "rpotato"  # 烤馬鈴薯
    HD = "hd"  # 哈逗堡
    SMART = "smart"  # 智能咖啡機
    TEA = "tea"  # 福爾摩沙茶館
    SWEETPOTATO = "sweetpotato"  # 夯番薯
    PHOTO = "photo"  # 相片立可得
    CS = "cs"  # ChargeSPOT
    GORO = "goro"  # gogoro電池交換站
    ICE = "ice"  # Fami!ce(有販售店)
    ICECREAM = "icecream"  # Fami!ce(單口味店)
    TWOICE = "twoice"  # Fami!ce(雙口味店)
    FAMIICE = "famiice"  # Fami!ce(特殊造型店)
    CARD = "card"  # picard (Picard- 法國優質冷凍食品)
    SUPER = "super"  # FamiSuper (全家FamiSuper選品超市店)
    TANHOU = "tanhou"  # 天和鮮物
    REST = "rest"  # 休憩區
    TOILET = "toilet"  # 廁所
    VEG = "veg"  # 生鮮蔬菜
    LAUNDRY = "laundry"  # Fami自助洗衣
    DESSERT = "dessert"  # SOHOT炎選-現烤點心
    COSTCO = "costco"  # 好市多專區
    HADA = "hada"  # 哈根達斯冰箱
    TRIPK = "tripk"  # 鼎王麻辣蛋
    FRESH = "fresh"  # 蒸新鮮
    ECO = "eco"  # 塑環真®循環杯
    GRILL = "grill"  # SOHOT炎選-炸烤物
    COOKNOW = "cooknow"  # 馬尚煮
    HOGAN = "hogan"  # 哈肯舖
    BEAR = "bear"  # 小熊菓子
    MUSL = "musl"  # 穆斯林友善商品店舖
    NPORK = "npork"  # 無豬肉熱食友善店
    UNKNOW = "unknow"  # 未知
