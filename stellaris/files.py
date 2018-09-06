import json, os



_settings = None

def get_settings():
	global _settings
	if _settings == None:
		with open("settings.json") as fp:
			_settings = json.load(fp)
	return _settings



def get_savefile_folder_path(name = None):
	settings = get_settings()

	if name == None:
		name = settings["current"]

	return settings["data"]["saves"].format(name=name)

def list_savefile_paths(name = None):
	folder_path = get_savefile_folder_path(name)
	return [os.path.join(folder_path, p) for p in sorted(os.listdir(folder_path))]



def get_jsonzip_folder_path(name = None):
	settings = get_settings()

	if name == None:
		name = settings["current"]

	return settings["data"]["json"].format(name=name)

def list_jsonzip_paths(name = None):
	folder_path = get_jsonzip_folder_path(name)
	return [os.path.join(folder_path, p) for p in sorted(os.listdir(folder_path))]



def get_output_folder_path(name = None):
	settings = get_settings()

	if name == None:
		name = settings["current"]

	return settings["data"]["output"].format(name=name)
