import json, os, subprocess

def get_settings():
	with open("settings.json") as fp:
		return json.load(fp)
		
def main():
	settings = get_settings()
	
	print("Converting save files for '" + settings["convert"] + "'.")
	
	src_path = os.path.join(settings["saves_folder_path"], settings["current"])
	dest_path = os.path.join(settings["json_folder_path"], settings["current"])
	
	if not os.path.exists(dest_path):
		os.makedirs(dest_path)
	
	subprocess.call([".\\bin\\convert\\convert.exe", src_path, dest_path])
	
	
	
if __name__=="__main__":
	main()