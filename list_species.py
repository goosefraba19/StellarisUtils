from src.files import list_jsonzip_paths
from src.model import Model

def main():
    all_species = {}

    for path in list_jsonzip_paths():
        model = Model.from_jsonzip(path)
        print(model.date)
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