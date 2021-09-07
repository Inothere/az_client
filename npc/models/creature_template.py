import enum
from sqlalchemy.sql.expression import null, nullslast
from base import WorldBase
import sqlalchemy as sa
from sqlalchemy_utils import ChoiceType
from npc import enums


class CreatureTemplate(WorldBase):
    __tablename__ = "creature_template"
    # 主键
    entry = sa.Column(sa.Integer(), primary_key=True, autoincrement=False)

    # difficaulty_entry_x: 指向不同难度的entry值
    difficulty_entry_1 = sa.Column(sa.Integer(), default=0)
    difficulty_entry_2 = sa.Column(sa.Integer(), default=0)
    difficulty_entry_3 = sa.Column(sa.Integer(), default=0)

    # 待确认参数
    KillCredit1 = sa.Column(sa.Integer(), default=0)
    KillCredit2 = sa.Column(sa.Integer(), default=0)

    # npc模型ID
    modelid1 = sa.Column(sa.Integer(), default=0)
    modelid2 = sa.Column(sa.Integer(), default=0)
    modelid3 = sa.Column(sa.Integer(), default=0)
    modelid4 = sa.Column(sa.Integer(), default=0)

    # 名称
    name = sa.Column(sa.String(100), nullable=False, default="0")
    # <>里的名称
    subname = sa.Column(sa.String(100), nullable=True)
    # 鼠标展示类型
    iconName = sa.Column(ChoiceType(enums.IconEnum, impl=sa.String(100)), nullable=True)
    # 逻辑外键，指向表gossip_menu.MenuID
    gossip_menu_id = sa.Column(sa.Integer(), default=0)
    # 最低等级
    minlevel = sa.Column(sa.Integer(), nullable=False, default=1)
    # 最高等级
    maxlevel = sa.Column(sa.Integer(), nullable=False, default=1)
    # 计算npc血量的扩展表，配合 creature_classlevelstats表
    exp = sa.Column(
        ChoiceType(enums.ExpansionEnum, impl=sa.Integer()),
        nullable=False,
        default=enums.ExpansionEnum.Classic,
    )
    # npc阵营逻辑外键，配合FactionTemplate.dbc工作
    faction = sa.Column(sa.Integer(), nullable=False, default=0)
    # npc类型位图，参考 https://www.azerothcore.org/wiki/creature_template#npcflag
    npcflag = sa.Column(sa.Integer(), nullable=False, default=0)
    # 行走速度，对于载具(vehicle)来说，决定了它的飞行速度
    speed_walk = sa.Column(sa.Float(), nullable=False, default=1.0)
    # 跑步速度，对于载具(vehicle)来说，决定了它的地面移动速度
    speed_run = sa.Column(sa.Float(), nullable=False, default=1.14286)
    # npc大小，如果是0的话，使用dbc默认大小
    scale = sa.Column(sa.Float, nullable=False, default=1)
    # npc品级，仅影响刷新时间
    rank = sa.Column(
        ChoiceType(enums.NpcRankEnum, impl=sa.Integer()), default=enums.NpcRankEnum
    )
    # 近战伤害类型
    dmgschool = sa.Column(
        ChoiceType(enums.MeleeDmgEnum, impl=sa.Integer()),
        default=enums.MeleeDmgEnum.SPELL_SCHOOL_NORMAL,
    )

    # 系数字段集合
    # 伤害系数,具体计算方式见 https://www.azerothcore.org/wiki/creature_template#damagemodifier
    DamageModifier = sa.Column(sa.Float(), default=1.0)
    # todo
    HealthModifier = sa.Column(sa.Float(), default=1.0)
    # todo
    ManaModifier = sa.Column(sa.Float(), default=1.0)
    # todo
    ArmorModifier = sa.Column(sa.Float(), default=1.0)

    # 近战攻击间隔 ms
    BaseAttackTime = sa.Column(sa.Integer(), nullable=False, default=0)
    # 远程攻击间隔 ms
    RangeAttackTime = sa.Column(sa.Integer(), nullable=False, default=0)
    # 近战伤害计算相关
    BaseVariance = sa.Column(sa.Float(), default=1.0)
    # 远程伤害计算相关
    RangeVariance = sa.Column(sa.Float(), default=1.0)
    # npc职业
    unit_class = sa.Column(
        ChoiceType(enums.NpcClassEnum, impl=sa.Integer()),
        default=enums.NpcClassEnum.CLASS_WARRIOR,
    )
    # https://www.azerothcore.org/wiki/creature_template#unit_flags
    unit_flags = sa.Column(sa.Integer(), default=0)
    # https://www.azerothcore.org/wiki/creature_template#unit_flags2
    unit_flags2 = sa.Column(sa.Integer(), default=0)
    # https://www.azerothcore.org/wiki/creature_template#dynamicflags
    dynamicflags = sa.Column(sa.Integer(), default=0)
    # npc家族(例如猫、狼、熊等等，枚举值太多，不做枚举了),
    # https://www.azerothcore.org/wiki/creature_template#family
    family = sa.Column(sa.Integer(), default=0)

    ## 训练相关
    # https://www.azerothcore.org/wiki/creature_template#trainer_type
    trainer_type = sa.Column(
        sa.Integer(), default=0  # 0: 职业技能训练师，1: 骑术训练师，2: 专业技能训练师，3: 宠物训练师
    )
    trainer_spell = sa.Column(
        sa.Integer(), default=0  # trainer_type = 2时有效，必须指定是哪种专业技能ID
    )
    trainer_class = sa.Column(
        sa.Integer(), default=0  # trainer_type = 0, 3 时有效，必须指定职业ID
    )
    trainer_race = sa.Column(
        sa.Integer(), default=0  # trainer_type = 1时有效，坐骑训练师的种族ID必须和玩家种族ID相同
    )

    # 生物类型 https://www.azerothcore.org/wiki/creature_template#type
    type = sa.Column(sa.Integer(), default=0)
    # 是否可挖矿/采集草药，是否是boss等级等等
    # https://www.azerothcore.org/wiki/creature_template#type_flags
    type_flags = sa.Column(sa.Integer(), default=0)

    # todo
    lootid = sa.Column(sa.Integer(), default=0)
    # todo
    pickpocketloot = sa.Column(sa.Integer(), default=0)
    # todo
    skinloot = sa.Column(sa.Integer(), default=0)
    # todo
    PetSpellDataId = sa.Column(sa.Integer(), default=0)
    # todo
    VehicleId = sa.Column(sa.Integer(), default=0)
    # 最小掉落铜币数量
    mingold = sa.Column(sa.Integer(), default=0)
    # 最大掉落铜币数量
    maxgold = sa.Column(sa.Integer(), default=0)

    # ai类型 https://www.azerothcore.org/wiki/creature_template#ainame
    AIName = sa.Column(sa.String(64), default="")
    # movement type
    MovementType = sa.Column(
        ChoiceType(enums.MovementTypeEnum, impl=sa.Integer()),
        default=enums.MovementTypeEnum.IDLE,
    )
    # todo https://www.azerothcore.org/wiki/creature_template#inhabittype
    InhabitType = sa.Column(sa.Integer(), default=0)
    # todo
    HoverHeight = sa.Column(sa.Float(), default=1.0)
    # 是否正营领袖，杀死阵营领袖能够给与玩家100荣誉值
    RacialLeader = sa.Column(sa.Integer(), default=0)
    # todo
    movementId = sa.Column(sa.Integer(), default=0)
    # 1: 可以恢复生命，0: 不能恢复生命
    RegenHealth = sa.Column(sa.Integer(), default=0)
    # 决定能够免疫哪种类型技能（缴械、眩晕等等）https://www.azerothcore.org/wiki/creature_template#mechanic_immune_mask
    mechanic_immune_mask = sa.Column(sa.Integer(), default=0)
    # 决定能够免疫哪种伤害类型（物理、神圣等等）https://www.azerothcore.org/wiki/creature_template#spell_school_immune_mask
    spell_school_immune_mask = sa.Column(sa.Integer(), default=0)
    # todo https://www.azerothcore.org/wiki/creature_template#flags_extra
    flags_extra = sa.Column(sa.Integer(), default=0)
    # 可以覆盖AIName字段
    ScriptName = sa.Column(sa.String(64), default="")
    # 标识和哪个客户端版本号匹配 https://www.azerothcore.org/wiki/creature_template#verifybuild
    VerifiedBuild = sa.Column(sa.Integer(), default=0)
