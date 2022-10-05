from abc import ABC, abstractmethod



class Skill(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def damage(self) -> float:
        pass

    @property
    @abstractmethod
    def required_stamina(self) -> float:
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def use(self, user, target) -> str:
        self.user = user
        self.target = target

        if self.user.stamina > self.required_stamina:
            return self.skill_effect()
        return f"Персонаж {self.user.name} собирался использовать умение {self.name}, но ему не хватило выносливости."


class FuryPunch(Skill):
    name = "Яростный пинок"
    damage = 12
    required_stamina = 6

    def skill_effect(self) -> str:
        # вычет здоровья цели
        self.target.get_damage(self.damage)
        # уменьшение выносливости атакующего за умение
        self.user.reduce_stamina(self.required_stamina)
        # вывод
        return f"{self.user.name} используя секретное умение {self.name} наносит сопернику {self.damage} жесткого урона."


class HardShot(Skill):
    name = "Испепеляющий тычок"
    damage = 15
    required_stamina = 5

    def skill_effect(self) -> str:
        # вычет здоровья цели
        self.target.get_damage(self.damage)
        # уменьшение выносливости атакующего за умение
        self.user.reduce_stamina(self.required_stamina)
        # вывод
        return f"{self.user.name} используя секретное умение {self.name} наносит сопернику {self.damage} жесткого урона."
