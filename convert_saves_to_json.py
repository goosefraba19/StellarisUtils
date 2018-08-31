import json, os, subprocess, time, zipfile

from src.files import get_settings, get_jsonzip_folder_path, list_savefile_paths
from src.parse import Parser

def get_pairs():
	dest_folder_path = get_jsonzip_folder_path()

	if not os.path.exists(dest_folder_path):
		os.makedirs(dest_folder_path)

	for src_path in list_savefile_paths():
		name = os.path.splitext(os.path.basename(src_path))[0]
		dest_path = os.path.join(dest_folder_path, name + ".zip")

		if not os.path.exists(dest_path):
			yield (name, src_path, dest_path)

def convert_python(src_path, dest_path):
	parser = Parser()

	src_archive = zipfile.ZipFile(src_path)
	with src_archive.open("gamestate") as file:
		data = file.read().decode("utf-8")
		parser.input(data)

	obj = parser.parse()

	dest_archive = zipfile.ZipFile(dest_path, mode="w", compression=zipfile.ZIP_DEFLATED)
	dest_archive.writestr("gamestate.json", json.dumps(obj))
	dest_archive.close()

def convert_dotnet(src_path, dest_path):
	subprocess.run(["dotnet", "convert/Stellaris.Convert.dll", src_path, dest_path], capture_output=True)

def main():
	settings = get_settings()
	
	pairs = list(get_pairs())

	print("Current game is '" + settings["current"] + "'.")
	print(f"Converting {len(pairs)} savefiles.")
	print()

	for (name, src_path, dest_path) in pairs:
		t_start = time.time()

		if settings["convert"] == "python":
			convert_python(src_path, dest_path)
		elif settings["convert"] == "dotnet":
			convert_dotnet(src_path, dest_path)
		else:
			raise Exception("Unrecognized convert setting")

		t_end = time.time()

		ms = int(1000*(t_end - t_start))
		print(f"{name} ({ms})")
	
if __name__=="__main__":
	main()