import requests
import os
from rosu_pp_py import Beatmap, Calculator


def calculate_pp(map_id: str, combo: int, count_300: int, count_100: int, count_50: int, count_miss: int, mods):
    downloaded_map = requests.get(f"https://osu.ppy.sh/osu/{map_id}")
    open(f"./Temp/map-{map_id}.osu", "wb").write(downloaded_map.content)
    mods_num = 0
    for x in mods:
        if x == "HD":
            mods_num += 8
        elif x == "HR":
            mods_num += 16
        elif x == "DT":
            mods_num += 64
        elif x == "NC":
            mods_num += 64
        elif x == "EZ":
            mods_num += 2
    osu_map = Beatmap(path=f"./Temp/map-{map_id}.osu")
    calculator = Calculator()
    calculator.set_mods(mods_num)
    max_performance = calculator.performance(osu_map)
    calculator.set_n_misses(count_miss)
    calculator.set_n300(count_300)
    calculator.set_n100(count_100)
    calculator.set_n50(count_50)
    calculator.set_combo(combo)
    calculator.set_difficulty(max_performance.difficulty)
    performance = calculator.performance(osu_map)
    os.remove(f"./Temp/map-{map_id}.osu")
    return performance, max_performance


def calculate_ss_pp(map_id: str, mods):
    downloaded_map = requests.get(f"https://osu.ppy.sh/osu/{map_id}")
    open(f"./Temp/map-{map_id}.osu", "wb").write(downloaded_map.content)
    mods_num = 0
    for x in mods:
        if x == "HD":
            mods_num += 8
        elif x == "HR":
            mods_num += 16
        elif x == "DT":
            mods_num += 64
        elif x == "NC":
            mods_num += 64
        elif x == "EZ":
            mods_num += 2
    osu_map = Beatmap(path=f"./Temp/map-{map_id}.osu")
    calculator = Calculator()
    calculator.set_mods(mods_num)
    max_performance = calculator.performance(osu_map)
    os.remove(f"./Temp/map-{map_id}.osu")
    return max_performance
