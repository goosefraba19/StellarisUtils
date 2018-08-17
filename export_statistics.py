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
		GalaxyCounts(),		
		CountryCounts("0", "country_gekkota"),
		CountryCounts("1", "country_devils"),
		SpeciesCounts(["0", "88", "116"], "species_gekkota"),
		SpeciesCounts(["1", "62", "66", "78", "90" ,"115", "120"], "species_gnome"),
		SpeciesCounts(["2", "93", "95", "96"], "species_prossnakan"),
		SpeciesCounts(["4", "79", "83", "86", "87", "89", "97", "100", "104", "105", "107", "109", "118"], "species_fafossan"),
		SpeciesCounts(["21", "113", "117"], "species_belmacossa"),
		SpeciesCounts(["3", "129"], "species_hahnmur")
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