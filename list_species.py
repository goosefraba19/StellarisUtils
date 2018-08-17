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
            if species.id not in all_species:
                all_species[species.id] = species

    print()

    parents = [s for s in all_species.values() if s.parent == None]
    for parent in sorted(parents, key=lambda s: int(s.id)):
        print(f"{parent.id}: {parent.name}")

        children = [s for s in all_species.values() if s.parent != None and s.parent.id == parent.id]
        for child in sorted(children, key=lambda s: int(s.id)):
            print(f"  {child.id}: {child.name}")


if __name__=="__main__":
    main()