import json, os, shutil, time

def get_settings():
	with open("settings.json") as fp:
		return json.load(fp)

def copy_new_autosaves(src_path, dest_path):

	if not os.path.exists(dest_path):
		os.mkdir(dest_path)
	
	paths = filter(
        lambda p: p.startswith("autosave"),
        os.listdir(src_path)
    )
	
	for path in paths:
		src = os.path.join(src_path, path)
		dest = os.path.join(dest_path, path[9:])

		if not os.path.exists(dest):
			shutil.copyfile(src, dest)
			print(dest)
		
def main():
	settings = get_settings()

	src_folder_path = os.path.join(settings["stellaris_folder_path"], "save games")
	dest_folder_path = settings["saves_folder_path"]
	
	if not os.path.exists(dest_folder_path):
		os.mkdir(dest_folder_path)
		
	pairs = [(os.path.join(src_folder_path, p), os.path.join(dest_folder_path, p)) for p in os.listdir(src_folder_path)]
	
	while True:
		for pair in pairs:
			copy_new_autosaves(*pair)
		time.sleep(60)
	
	
if __name__=="__main__":
	main()