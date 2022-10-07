from abc import ABC, abstractmethod
from random import randint

from service_classes.classes import UnitClass
from service_classes.equipment import Weapon, Armor


class BaseUnit(ABC):

    def __init__(self, name: str, unit_class: UnitClass):
        self.name: str = name
        self.unit_class: UnitClass = unit_class
        self.hp: float = self.unit_class.max_health
        self.stamina: float = self.unit_class.max_stamina
        self.weapon: Weapon
        self.armor: Armor
        self._is_skill_used: bool = False

    def equip_weapon(self, weapon: Weapon) -> None:
        self.weapon = weapon
        # return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> None:
        self.armor = armor
        # return f"{self.name} экипирован броней {self.weapon.name}"

    def _calc_output_damage(self, target: type(__init__)) -> float:

        # урон атакующего
        attacker_damage = round(self.weapon.weapon_damage() * self.unit_class.attack, 1)

        # броня цели:
        if target.stamina > target.armor.stamina_per_turn:
            target_armor = round(target.armor.defence * target.unit_class.armor, 1)
        else:
            target_armor = 0

        # результирующий урон
        damage_common = round(attacker_damage - target_armor,1)
        # вычет выносливости атакующего после удара
        self.reduce_stamina(self.weapon.stamina_per_hit)
        # вычет выносливости цели после удара
        target.reduce_stamina(target.armor.stamina_per_turn)

        return damage_common

    def get_damage(self, damage: float) -> None:
        self.hp = round(self.hp -damage,1)
        if self.hp < 0:
            self.hp = 0

    def reduce_stamina(self, stamina: float) -> None:
        self.stamina=round(self.stamina-stamina,1)
        if self.stamina < 0:
            self.stamina = 0

    def use_skill(self, target: type(__init__)) -> str:
        if self._is_skill_used:
            return f"{self.name} захотел повторно использовать умение, но не потянул."

        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)

    @abstractmethod
    def do_hit(self, target: type(__init__)) -> str:
        pass

class PlayerUnit(BaseUnit):

    def do_hit(self, target: BaseUnit) -> str:
        # логика вычисления выносливости перед ударом атакующего
        if self.stamina > self.weapon.stamina_per_hit:
            damage = self._calc_output_damage(target)
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        # вычет здоровья цели после удара
        # если урон больше защиты
        if damage > 0:
            target.get_damage(damage)
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
        else:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} соперника его останавливает."

class EnemyUnit(BaseUnit):

    def do_hit(self, target: BaseUnit) -> str:
        # логика применения умения компьютером
        if randint(1, 10) == 1:
            if self._is_skill_used:
                return self._hit(target)
            else:
                return self.use_skill(target)
        return self._hit(target)

    def _hit(self, target: BaseUnit) -> str:

        if self.stamina > self.weapon.stamina_per_hit:
            damage = self._calc_output_damage(target)
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        # вычет здоровья цели после удара
        # если урон больше защиты
        if damage > 0:
            target.get_damage(damage)
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
        else:
            return f"{self.name} используя {self.weapon.name} наносит удар, но  Ваш(а) {target.armor.name} его останавливает."