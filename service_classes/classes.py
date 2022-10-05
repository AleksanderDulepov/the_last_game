from dataclasses import dataclass
from typing import Dict

from service_classes.skills import Skill, FuryPunch, HardShot
import marshmallow


@dataclass
class UnitClass:
	name:str
	max_health:float
	max_stamina:float
	attack:float
	stamina:float
	armor:float
	skill:Skill

	class Meta:
		unknown=marshmallow.EXCLUDE


#создание возможных классов персонажей для выбора
WarriorClass=UnitClass(name="Воин", max_health=60, max_stamina=30, attack=0.8, stamina=0.9, armor=1.2, skill=FuryPunch())
ThiefClass=UnitClass(name="Вор", max_health=50, max_stamina=25, attack=1.5, stamina=1.2, armor=1, skill=HardShot())

#экземпляры классов героев по имени
unit_classes:Dict[str, UnitClass]={WarriorClass.name:WarriorClass, ThiefClass.name:ThiefClass}
