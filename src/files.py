import json, os



_settings = None

def get_settings():
	global _settings
	if _settings == None:
		with open("settings.json") as fp:
			_settings = json.load(fp)
	return _settings



def get_savefile_folder_path():
	settings = get_settings()
	return os.path.join(settings["saves_folder_path"], settings["current"])

def list_savefile_paths():
	folder_path = get_savefile_folder_path()
	return [os.path.join(folder_path, p) for p in sorted(os.listdir(folder_path))]



def get_jsonzip_folder_path():
	settings = get_settings()
	return os.path.join(settings["json_folder_path"], settings["current"])

def list_jsonzip_paths():
	folder_path = get_jsonzip_folder_path()
	return [os.path.join(folder_path, p) for p in sorted(os.listdir(folder_path))]



def get_output_folder_path():
	settings = get_settings()
	return os.path.join(settings["output_folder_path"], settings["current"])
