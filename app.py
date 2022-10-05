from flask import Flask, render_template, request
from werkzeug.utils import redirect

from service_classes.base import Arena
from service_classes.classes import unit_classes
from service_classes.equipment import Equipment
from service_classes.unit import BaseUnit, PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()
all_equipment = Equipment()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=arena, result="Игра началась!")


@app.route("/fight/hit")
def hit():
    result = arena.do_players_hit()
    return render_template('fight.html', heroes=arena, result=result)


@app.route("/fight/use-skill")
def use_skill():
    result = arena.do_players_skill()
    return render_template('fight.html', heroes=arena, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    result = arena.next_turn()
    return render_template('fight.html', heroes=arena, result=result)


@app.route("/fight/end-fight")
def end_fight():
    arena.game_over()
    return render_template("index.html")


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    if request.method == 'GET':
        return render_template('hero_choosing.html', hero_or_enemy="Выберите героя", hero_or_enemy_page ="/choose-hero/",
                               result_classes=unit_classes.keys(), result_weapons = all_equipment.get_weapon_names(),\
                                                                                    result_armors =
                               all_equipment.get_armor_names())
    if request.method == 'POST':
        data = request.form
        player_instance = PlayerUnit(name=data.get("name"), unit_class=unit_classes.get(data.get("unit_class")))
        player_instance.equip_weapon(all_equipment.get_weapon(data.get("weapon")))
        player_instance.equip_armor(all_equipment.get_armor(data.get("armor")))
        heroes['player'] = player_instance
        return redirect('/choose-enemy/', code=302)

@app.route("/choose-enemy/", methods=['POST', 'GET'])
def choose_enemy():
    if request.method == 'GET':
        return render_template('hero_choosing.html', hero_or_enemy="Выберите врага", hero_or_enemy_page ="/choose-enemy/",
                               result_classes=unit_classes.keys(), result_weapons =
        all_equipment.get_weapon_names(), result_armors = all_equipment.get_armor_names())
    if request.method == 'POST':
        data = request.form
        enemy_instance = EnemyUnit(name=data.get("name"), unit_class=unit_classes.get(data.get("unit_class")))
        enemy_instance.equip_weapon(all_equipment.get_weapon(data.get("weapon")))
        enemy_instance.equip_armor(all_equipment.get_armor(data.get("armor")))
        heroes['enemy'] = enemy_instance
        return redirect('/fight/', code=302)

if __name__ == "__main__":
    app.run(debug=True)
