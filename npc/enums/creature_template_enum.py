from enum import Enum


class ExpansionEnum(Enum):
    Classic = 0
    TBC = 1
    WLK = 2


class IconEnum(Enum):
    Directions = "Directions"  # 卫兵和飞行点npc类型
    Gunner = "Gunner"  # 炮塔类
    VehichleCursor = "vehichleCursor"  # 载具类
    Driver = "Driver"  # 展示驾驶图标
    Attack = "Attack"  # 展示剑的图标
    Buy = "Buy"  # 购买图标
    Speak = "Speak"  # 聊天图标
    Pickup = "Pickup"  # 手掌图标
    Interact = "Interact"  # 齿轮图标
    Trainer = "Trainer"  # 书图标
    Taxi = "Taxi"  # 飞鞋图标
    Repair = "Repair"  # 铁砧图标
    LootAll = "LootAll"  # 购买图标
    Quest = "Quest"  # 无用
    PVP = "PVP"  # 无用


class NpcRankEnum(Enum):
    Normal = 0
    Elite = 1
    RareElite = 2
    Boss = 3
    Rare = 4


class MeleeDmgEnum(Enum):
    # 近战伤害类型
    SPELL_SCHOOL_NORMAL = 0
    SPELL_SCHOOL_HOLY = 1
    SPELL_SCHOOL_FIRE = 2
    SPELL_SCHOOL_NATURE = 3
    SPELL_SCHOOL_FROST = 4
    SPELL_SCHOOL_SHADOW = 5
    SPELL_SCHOOL_ARCANE = 6


class NpcClassEnum(Enum):
    # npc职业
    CLASS_WARRIOR = 1
    CLASS_PALADIN = 2
    CLASS_ROGUE = 3
    CLASS_MAGE = 4


class MovementTypeEnum(Enum):
    # npc移动类型
    IDLE = 0
    RANDOM = 1
    WAYPOINT = 2
