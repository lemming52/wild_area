from typing import List

WEATHER = [
    "clear",
    "cloudy",
    "rain",
    "thunderstorm",
    "snow",
    "blizzard",
    "sun",
    "sandstorm",
    "fog"
]

REGIONS = [
    "rolling_fields",
    "dappled_grove",
    "watchtower_ruins",
    "east_lake_axewell",
    "west_lake_axewell",
    "axews_eye",
    "south_lake_miloch",
    "north_lake_miloch",
    "giants_seat",
    "motostoke_riverbank",
    "bridge_field",
    "stony_wilderness",
    "giants_cap",
    "giants_mirror",
    "dusty_bowl",
    "hammerlocke_hills",
    "lake_of_outrage"
]

SWORD = False
SHIELD = True

class Habitat():

    def __init__(self, game: bool, region: str, weather: str, encounter: str, environment: str, rate: str) -> None:
        self.environment = environment
        self.game = game
        self.region = region
        self.weather = weather
        self.encounter = encounter
        self.environment = environment
        self.rate = rate

    def __str__(self) -> str:
        return f"{self.region}\t{self.encounter}\t{self.environment}\t{self.rate}"

    def is_available(self, game: bool, region: str, weather: str) -> bool:
        if self.game != game:
            return False
        if self.region != region:
            return False
        return self.weather == weather:


class Pokemon():

    def __init__(self, name: str, number: str) -> None:
        self.name = name
        self.number = number
        self.habitats = []

    def add_habitat(self, habitat: Habitat) -> None:
        self.habitats.append(habitat)

    def is_available(self, game: bool, region: str, weather: str) -> bool:
        for habitat in self.habitats:
            if habitat.is_available(game, region, weather):
                return True
        return False

    def get_habitats(self, game: bool, region: str, weather: str) -> List[Habitat]:
        return [habitat for habitat in self.habitats if habitat.is_available(game, region, weather)]

    def print_habitats(self, game: bool, region: str, weather: str):
        available_habitats = self.get_habitats(game, region, weather)
        if len(available_habitats) > 0:
            print(f"{self.name} [{self.number}]\n")
            for habitat in available_habitats:
                print(habitat)
            print("")

    def print_multiple_habitats(self, game: bool, regions: List[List[str]]):
        available_habitats = []
        for region, weather in regions:
            available_habitats = available_habitats + self.get_habitats(game, region, weather)
        if len(available_habitats) > 0:
            print(f"{self.name}\n")
            for habitat in available_habitats:
                print(habitat)
            print("")





def main() -> None:
    """
    Select Game
    Select Region
    Select Weather
    Load pokemon for region, allow filtering by game and weather
    Load pokemon that are available, along with habitat, level and rate
    """
    all_pokemon = {}
    for region in REGIONS:
        with open(f"data/{region}.txt", "r") as f:
            for line in f:
                line = line.strip("{}")
                components = line.split("|")
                name = components[2]
                if name not in all_pokemon:
                    pokemon = Pokemon(name, components[1])
                    all_pokemon[name] = pokemon
                else:
                    pokemon = all_pokemon[name]

                sword = components[3] == "yes"
                shield = components[4] == "yes"
                encounter = components[5]
                environment = components[6]

                details = components[8:]
                for entry in details:
                    entries = entry.split("=")
                    if len(entries) == 2:
                        if entries[0] in WEATHER:
                            if sword:
                                pokemon.add_habitat(Habitat(SWORD, region, entries[0], encounter, environment, entries[1]))
                            if shield:
                                pokemon.add_habitat(Habitat(SHIELD, region, entries[0], encounter, environment, entries[1]))
                    if len(entries) == 1:
                        for weather in WEATHER:
                            if sword:
                                pokemon.add_habitat(Habitat(SWORD, region, weather, encounter, environment, entry))
                            if shield:
                                pokemon.add_habitat(Habitat(SHIELD, region, weather, encounter, environment, entry))
    regions = [
        ["rolling_fields", "rain"],
        ["dappled_grove", "thunderstorm"],
        ["watchtower_ruins", "snow"],
        ["east_lake_axewell", "fog"],
        ["west_lake_axewell", "snow"],
        ["axews_eye", "fog"],
        ["south_lake_miloch", "cloudy"],
        ["north_lake_miloch", "sandstorm"],
        ["giants_seat", "snow"],
        ["motostoke_riverbank", "rain"],
        ["bridge_field", "clear"],
        ["stony_wilderness", "cloudy"],
        ["giants_cap", "fog"],
        ["giants_mirror", "snow"],
        ["dusty_bowl", "clear"],
        ["hammerlocke_hills", "thunderstorm"],
        ["lake_of_outrage", "snow"]
    ]
    for name, pokemon in all_pokemon.items():
        pokemon.print_multiple_habitats(SHIELD, regions)



if __name__ == "__main__":
    main()