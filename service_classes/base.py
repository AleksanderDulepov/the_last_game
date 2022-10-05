from typing import Optional

from service_classes.unit import BaseUnit, PlayerUnit, EnemyUnit

class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False


    def start_game(self, player: PlayerUnit, enemy: EnemyUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True


    def next_turn(self) -> str:
        if self.check_hp() is None:
            self.recover_stamina(self.player)
            self.recover_stamina(self.enemy)
            return self.enemy.do_hit(self.player)
        return self.check_hp()


        # self.check_hp()
        # if self.battle_result is None:
        #     self.recover_stamina(self.player)
        #     self.recover_stamina(self.enemy)
        #     return self.enemy.do_hit(self.player)
        # self.game_over()
        # return self.battle_result

    def check_hp(self) -> Optional[str]:
        battle_result = None
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            battle_result = f"Ничья"
        if self.player.hp <= 0:
            battle_result = f"Игрок проиграл битву"
        if self.enemy.hp <= 0:
            battle_result = f"Игрок выиграл битву"

        if battle_result is not None:
            self.game_over()
            return battle_result
        return None

    def game_over(self) -> None:
        self._instances = {}
        self.game_is_running = False

    def recover_stamina(self, instance: BaseUnit) -> None:
        value = self.STAMINA_PER_ROUND * instance.unit_class.stamina
        instance.stamina=round(instance.stamina+value,1)
        if instance.stamina > instance.unit_class.max_stamina:
            instance.stamina = instance.unit_class.max_stamina

    def do_players_hit(self) -> str:
        if self.check_hp() is None:
            result_player_hit = self.player.do_hit(self.enemy)
            result_enemy_hit = self.next_turn()
            return f"{result_player_hit} {result_enemy_hit}"
        return self.check_hp()

    def do_players_skill(self) -> str:
        if self.check_hp() is None:
            result_player_skill = self.player.use_skill(self.enemy)
            result_enemy_hit = self.next_turn()
            return f"{result_player_skill} {result_enemy_hit}"
        return self.check_hp()