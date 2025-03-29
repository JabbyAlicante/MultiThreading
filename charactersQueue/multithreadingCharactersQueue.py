import json
import os
from threading import Lock, Thread, Semaphore
import time
import random

def read_json(file_path):
    if not os.path.exists(file_path):
        return {"active_characters": [None, None, None, None], "elemental_resonance": {}, "active_buffs": []}
    with open(file_path, "r") as f:
        return json.load(f)

def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def genshin_update_data(file_path, player_id, character_name, file_lock):
    print(f"Player {player_id} attempting to update character...")

    with file_lock:  # prevent race 
        data = read_json(file_path)

        data["active_characters"][player_id - 1] = f"Player{player_id}: {character_name}"
        print(f"Player {player_id} selected {character_name}.")

        # Characters element
        character_elements = {
            "Amber": "Pyro",
            "Diluc": "Pyro",
            "Jean": "Anemo",
            "Venti": "Anemo",
            "Fischl": "Electro",
            "Ningguang": "Geo",
            "Xinyan": "Pyro",
            "Xiangling": "Pyro",
            "Xiao": "Anemo",
            "Beidou": "Electro",
            "Furina": "Hydro",
        }

        # Party buffs
        party_buffs = {
            "Protective Canopy": {"condition": lambda elements: len(elements) == 4, "effect": "15% resistance to all elements"},
            "Fervent Flames": {"condition": lambda elements: elements.get("Pyro", 0) >= 2, "effect": "Attack +25%, Cryo duration -40%"},
            "Soothing Water": {"condition": lambda elements: elements.get("Hydro", 0) >= 2, "effect": "Healing +30%, Pyro duration -40%"},
            "Impetuous Winds": {"condition": lambda elements: elements.get("Anemo", 0) >= 2, "effect": "Stamina -15%, Speed +10%, CD -5%"},
            "High Voltage": {"condition": lambda elements: elements.get("Electro", 0) >= 2, "effect": "Electro-charged reactions generate particles, Hydro duration -40%"},
            "Shattering Ice": {"condition": lambda elements: elements.get("Cryo", 0) >= 2, "effect": "Crit rate +15% vs frozen/Cryo, Electro duration -40%"},
            "Enduring Rock": {"condition": lambda elements: elements.get("Geo", 0) >= 2, "effect": "Shielded: Attack +15%, Interrupt resist +"},
        }

        element_counts = {}
        active_buffs = []

        for character in data["active_characters"]:
            if character:
                character_name = character.split(": ")[1]
                element = character_elements.get(character_name, None)
                if element:
                    element_counts[element] = element_counts.get(element, 0) + 1

        elemental_resonance = {k: v for k, v in element_counts.items()}

        for buff_name, buff_data in party_buffs.items():
            if buff_data["condition"](element_counts):
                active_buffs.append({"name": buff_name, "effect": buff_data["effect"]})

        data["elemental_resonance"] = elemental_resonance
        data["active_buffs"] = active_buffs

        write_json(file_path, data)

    print(f"Player {player_id} update complete.")

def display_party_setup(file_path, file_lock):
    with file_lock:
        data = read_json(file_path)
        print("Party Setup:")
        for character in data["active_characters"]:
            print(character)
        print("-" * 40)

        print("Elemental Resonance:")
        for element, count in data["elemental_resonance"].items():
            print(f"- {element}: {count}")
        print("-" * 40)

        print("Active Buffs:")
        if data["active_buffs"]:
            for buff in data["active_buffs"]:
                print(f"- {buff['name']}: {buff['effect']}")
        else:
            print("No active buffs.")
        print("-" * 40)

def player_actions(file_path, player_id, file_lock, update_semaphore):
    characters = ["Diluc", "Jean", "Xiangling", "Venti", "Fischl", "Xiao", "Beidou", "Furina"]

    print(f"Player {player_id} joining the party...")
    display_party_setup(file_path, file_lock)

    for _ in range(5):
        character = random.choice(characters)
        print(f"Player {player_id} selecting {character}...")

        with update_semaphore: 
            genshin_update_data(file_path, player_id, character, file_lock)

        display_party_setup(file_path, file_lock)
        time.sleep(random.uniform(.1, .5))

    print(f"starting.")

def simulate(file_path):
    file_lock = Lock()
    update_semaphore = Semaphore(2) 
    threads = []

    for i in range(1000):
        for player_id in range(1, 5):
            thread = Thread(target=player_actions, args=(file_path, player_id, file_lock, update_semaphore))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    file_path = "new_party_setup.json"
    simulate(file_path)

