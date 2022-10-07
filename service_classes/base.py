from typing import Optional, Dict, Any

from service_classes.unit import BaseUnit, PlayerUnit, EnemyUnit


class BaseSingleton(type):
    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player: PlayerUnit
    enemy: EnemyUnit
    game_is_running: bool = False
    battle_result: str = ""

    def start_game(self, player: PlayerUnit, enemy: EnemyUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def next_turn(self) -> str:
        self.check_hp()
        if self.battle_result == "":
            self.recover_stamina(self.player)
            self.recover_stamina(self.enemy)
            return self.enemy.do_hit(self.player)
        self.game_over()
        return self.battle_result

    def check_hp(self) -> None:
        self.battle_result = ""
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = f"Ничья"
        if self.player.hp <= 0:
            self.battle_result = f"Игрок проиграл битву"
        if self.enemy.hp <= 0:
            self.battle_result = f"Игрок выиграл битву"

    def game_over(self) -> None:
        self._instances: Dict[type, Any] = {}
        self.game_is_running = False

    def recover_stamina(self, instance: BaseUnit) -> None:
        value = self.STAMINA_PER_ROUND * instance.unit_class.stamina
        instance.stamina = round(instance.stamina + value, 1)
        if instance.stamina > instance.unit_class.max_stamina:
            instance.stamina = instance.unit_class.max_stamina

    def do_players_hit(self) -> str:
        self.check_hp()
        if self.battle_result == "":
            result_player_hit = self.player.do_hit(self.enemy)
            result_enemy_hit = self.next_turn()
            return f"{result_player_hit} {result_enemy_hit}"
        self.game_over()
        return self.battle_result

    def do_players_skill(self) -> str:
        self.check_hp()
        if self.battle_result == "":
            result_player_skill = self.player.use_skill(self.enemy)
            result_enemy_hit = self.next_turn()
            return f"{result_player_skill} {result_enemy_hit}"
        self.game_over()
        return self.battle_result
