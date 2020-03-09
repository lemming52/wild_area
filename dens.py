import re
from typing import Dict, List, Optional, TextIO

NEST_ID_PATTERN = re.compile(r'Nest ID: (\d+)')
POKEMON_PATTERN = re.compile(r'^[ \t]+(\d{1})-Star ([\w ]+)$')
LEVEL_PATTERN = re.compile(r'^[ \t]+Lv\. (\d+-\d+)$')
RATE_PATTERN = re.compile(r'^[ \t]+(\d{1})-Star Desired: (\d{1,3}%)$')
TR_PATTERN = re.compile(r'^[ \t]+(\d{1,3}%) (TR\d{1,2} .+)$')

SWORD = False
SHIELD = True

class Habitat():

    def __init__(self, game: bool, nest_id: str, nest_count: int, pokemon_stars: str, level: str, stars: int, rate: str) -> None:
        self.game = game
        self.nest_id = nest_id
        self.nest_count = nest_count
        self.pokemon_stars = pokemon_stars
        self.level = level
        self.stars = stars
        self.rate = rate

    def __str__(self) -> str:
        return f"Nest {self.nest_count} [{self.nest_id}]\t({self.pokemon_stars})\t{self.level}\t{self.stars} Stars\t{self.rate}"

    def is_available(self, game: bool, nest_count: Optional[int], nest_id: Optional[str]) -> bool:
        if nest_count and self.nest_count != nest_count:
            return False
        if nest_id and self.nest_id != nest_id:
            return False
        return self.game == game

class Pokemon():

    def __init__(self, name: str) -> None:
        self.name = name
        self.habitats = []

    def add_habitat(self, habitat: Habitat) -> None:
        self.habitats.append(habitat)

    def get_habitats(self, game: bool, nest_counter: Optional[int], nest_id: Optional[str]) -> List[Habitat]:
        return [habitat for habitat in self.habitats if habitat.is_available(game, nest_counter, nest_id)]

    def print_multiple_habitats(self, game: bool, nest_counter: Optional[int], nest_id: Optional[str]) -> None:
        available_habitats = self.get_habitats(game, nest_counter, nest_id)
        if len(available_habitats) > 0:
            print(f"{self.name}\n")
            for habitat in available_habitats:
                print(habitat)
            print("")

def parse_encounters(f: TextIO, all_pokemon: Dict[str, Pokemon], game: bool) -> None:
    stage = "TRs"
    nest = ""
    nest_counter = 0
    pokemon = ""
    pokemon_stars = ""
    level = ""
    for line in f:
            match = None
            if stage == "TRs":
                match = re.match(NEST_ID_PATTERN, line)
                if match:
                    nest = match.group(1)
                    nest_counter += 1
                    continue
                match = re.match(POKEMON_PATTERN, line)
                if match:
                    pokemon_stars = match.group(1)
                    name = match.group(2)
                    if name not in all_pokemon:
                        pokemon = Pokemon(name)
                        all_pokemon[name] = pokemon
                    else:
                        pokemon = all_pokemon[name]
                    stage = "pokemon"
                continue
            elif stage == "pokemon":
                match = re.match(LEVEL_PATTERN, line)
                if match:
                    level = match.group(1)
                    stage = "rates"
                continue
            elif stage == "rates":
                match = re.match(RATE_PATTERN, line)
                if match:
                    stars = match.group(1)
                    rate = match.group(2)
                    pokemon.add_habitat(Habitat(game,
                                                nest,
                                                nest_counter,
                                                pokemon_stars,
                                                level,
                                                stars,
                                                rate))
                    continue
                match = re.match(TR_PATTERN, line)
                if match:
                    stage = "TRs"
                    continue

def main():
    """
    question
    provide game, pokemon
    want dens and rates for those dens
    For each game
        For each nest
            For each pokemon
                Select spawn rate
                Select TRs
    """
    all_pokemon = {}
    with open(f"data/shield_raid_encounters_&_drops.txt", "r") as f:
        parse_encounters(f, all_pokemon, SHIELD)
    with open(f"data/sword_raid_encounters_&_drops.txt", "r") as f:
        parse_encounters(f, all_pokemon, SWORD)

    all_pokemon["Flareon"].print_multiple_habitats(SHIELD, None, None)

    for name, pokemon in all_pokemon.items():
        pokemon.print_multiple_habitats(SHIELD, 33, None)


if __name__ == "__main__":
    main()