import json
import random
from dataclasses import dataclass
from typing import List, Optional

import marshmallow
import marshmallow_dataclass


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    # урон от оружия
    def weapon_damage(self) -> float:
        return round(random.uniform(self.min_damage, self.max_damage), 1)

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]

    class Meta:
        unknown = marshmallow.EXCLUDE


class Equipment():

    def __init__(self):
        self.equipment: EquipmentData = self._upload_equipment_data()


    def get_weapon(self, weapon_name: str) -> Optional[Weapon]:
        for weapon in self.equipment.weapons:
            if weapon_name == weapon.name:
                return weapon
        return None

    def get_armor(self, armor_name: str) -> Optional[Armor]:
        for armor in self.equipment.armors:
            if armor_name == armor.name:
                return armor
        return None

    def get_weapon_names(self) -> List[str]:
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armor_names(self) -> List[str]:
        return [armor.name for armor in self.equipment.armors]

    # @staticmethod
    def _upload_equipment_data(self) -> EquipmentData:

        EquipmentSchema = marshmallow_dataclass.class_schema(EquipmentData)

        with open("$PWD/data/equipment.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        try:
            equipment_instance: EquipmentData = EquipmentSchema().load(data)
            return equipment_instance
        except marshmallow.exceptions.ValidationError:
            raise ValueError



