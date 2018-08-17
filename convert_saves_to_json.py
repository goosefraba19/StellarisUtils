import json, os, time, zipfile
from src.parse import Parser

def get_settings():
	with open("settings.json") as fp:
		return json.load(fp)
		
def main():
	settings = get_settings()
	
	print("Current game is '" + settings["current"] + "'.")
	
	src_folder_path = os.path.join(settings["saves_folder_path"], settings["current"])
	dest_folder_path = os.path.join(settings["json_folder_path"], settings["current"])
	
	if not os.path.exists(dest_folder_path):
		os.makedirs(dest_folder_path)

	pairs = []
	for name in os.listdir(src_folder_path):
		src_path = os.path.join(src_folder_path, name)
		dest_path = os.path.join(dest_folder_path, os.path.splitext(name)[0] + ".zip")

		if not os.path.exists(dest_path):
			pairs.append((name, src_path, dest_path))

	print(f"Converting {len(pairs)} savefiles.")
	print()

	for (name, src_path, dest_path) in pairs:
		t_start = time.time()

		parser = Parser()

		src_archive = zipfile.ZipFile(src_path)
		with src_archive.open("gamestate") as file:
			data = file.read().decode("utf-8")
			parser.input(data)

		obj = parser.parse()

		dest_archive = zipfile.ZipFile(dest_path, mode="w", compression=zipfile.ZIP_DEFLATED)
		dest_archive.writestr("gamestate.json", json.dumps(obj))
		dest_archive.close()

		t_end = time.time()

		ms = int(1000*(t_end - t_start))
		print(f"{name} ({ms})")
	
if __name__=="__main__":
	main()