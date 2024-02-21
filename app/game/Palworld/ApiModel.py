from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

class PalGameWorldSettings(BaseModel):
    Difficulty: str
    DayTimeSpeedRate: float
    NightTimeSpeedRate: float
    ExpRate: float
    PalCaptureRate: float
    PalSpawnNumRate: float
    PalDamageRateAttack: float
    PalDamageRateDefense: float
    PlayerDamageRateAttack: float
    PlayerDamageRateDefense: float
    PlayerStomachDecreaceRate: float
    PlayerStaminaDecreaceRate: float
    PlayerAutoHPRegeneRate: float
    PlayerAutoHpRegeneRateInSleep: float
    PalStomachDecreaceRate: float
    PalStaminaDecreaceRate: float
    PalAutoHPRegeneRate: float
    PalAutoHpRegeneRateInSleep: float
    BuildObjectDamageRate: float
    BuildObjectDeteriorationDamageRate: float
    CollectionDropRate: float
    CollectionObjectHpRate: float
    CollectionObjectRespawnSpeedRate: float
    EnemyDropItemRate: float
    DeathPenalty: str
    bEnablePlayerToPlayerDamage: bool
    bEnableFriendlyFire: bool
    bEnableInvaderEnemy: bool
    bActiveUNKO: bool
    bEnableAimAssistPad: bool
    bEnableAimAssistKeyboard: bool
    DropItemMaxNum: int
    DropItemMaxNum_UNKO: int
    BaseCampMaxNum: int
    BaseCampWorkerMaxNum: int
    DropItemAliveMaxHours: float
    bAutoResetGuildNoOnlinePlayers: bool
    AutoResetGuildTimeNoOnlinePlayers: float
    GuildPlayerMaxNum: int
    PalEggDefaultHatchingTime: float
    WorkSpeedRate: float
    bIsMultiplay: bool
    bIsPvP: bool
    bCanPickupOtherGuildDeathPenaltyDrop: bool
    bEnableNonLoginPenalty: bool
    bEnableFastTravel: bool
    bIsStartLocationSelectByMap: bool
    bExistPlayerAfterLogout: bool
    bEnableDefenseOtherGuildPlayer: bool
    CoopPlayerMaxNum: int
    ServerPlayerMaxNum: int
    ServerName: str
    ServerDescription: str
    AdminPassword: str
    ServerPassword: str
    PublicPort: int
    PublicIP: str
    RCONEnabled: bool
    RCONPort: int
    Region: str
    bUseAuth: bool
    BanListURL: str
    