import json, os
from src.model import Model
from src.statistics import GalaxyCounts, CountryCounts, SpeciesCounts

def get_settings():
	with open("settings.json") as fp:
		return json.load(fp)

def main():
	settings = get_settings()

	folder_path = os.path.join(settings["json_folder_path"], settings["current"])    

	stats = [
		GalaxyCounts()
	]

	json_paths = [os.path.join(folder_path, p) for p in os.listdir(folder_path)]
	for path in sorted(json_paths):
		print(path)
		model = Model.from_jsonzip(path)
		for stat in stats:
			stat.step(model)

	for stat in stats:
		stat.export(settings)

if __name__=="__main__":
	main()