from src.files import get_settings, list_jsonzip_paths
from src.model import Model
from src.statistics import GalaxyCounts, CountryCounts, SpeciesCounts

def main():
	stats = [
		GalaxyCounts(),		
		CountryCounts("0", "country_gekkota"),
		CountryCounts("1", "country_devils"),
		SpeciesCounts(["914a42131321444cfdb5a4e768c1ca0c"], "species_gekkota", include_children=True),
		SpeciesCounts(["6d1e40b260b879b009cce7bf2f42fda5"], "species_gnome", include_children=True),
		SpeciesCounts(["8d9c2b498082675d7cc7025630263176"], "species_prossnakan", include_children=True),
		SpeciesCounts(["c19c2f352dbb54b80ef8ca465898c965"], "species_fafossan", include_children=True),
		SpeciesCounts(["d96ca9ad300d225d02f52f7a4a753059"], "species_belmacossa", include_children=True),
		SpeciesCounts(["966875c49a50703e480bd7d5543c0809"], "species_hahnmur", include_children=True)
	]

	for path in list_jsonzip_paths():
		model = Model.from_jsonzip(path)
		print(model.date)
		for stat in stats:
			stat.step(model)

	for stat in stats:
		stat.export()

if __name__=="__main__":
	main()