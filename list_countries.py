from src.files import list_jsonzip_paths
from src.model import Model

def main():
    countries = {}

    for path in list_jsonzip_paths():
        model = Model.from_jsonzip(path)
        print(model.date)
        for country in model.countries.values():
            countries[country.id] = country

    print()

    print("id,name")
    for c in countries.values():
        print(f"{c.id},{c.name}")

if __name__=="__main__":
    main()