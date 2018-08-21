import json, os

from src.model import Model

def get_settings():
    with open("settings.json") as fp:
        return json.load(fp)

def main():
    settings = get_settings()

    all_species = {}

    folder_path = os.path.join(settings["json_folder_path"], settings["current"])    
    for name in os.listdir(folder_path):
        path = os.path.join(folder_path, name)
        print(path)

        model = Model.from_jsonzip(path)

        for species in model.species.values():
            all_species[species.id] = species

    print()

    print("base,id,name")
    bases = [s for s in all_species.values() if s.base == None]
    for base in sorted(bases, key=lambda s: s.id):
        print(f"{base.id},{base.id},{base.name}")

        for child in base.children:
            print(f"{base.id},{child.id},{child.name}")


if __name__=="__main__":
    main()