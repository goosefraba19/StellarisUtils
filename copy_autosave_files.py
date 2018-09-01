import re, os, shutil, time
from collections import defaultdict

from src.files import get_settings
from src.model import get_savefile_data



ironsave_timestamps = defaultdict(float)

def copy_new_autosaves(src_folder_path, dest_folder_path):

	if not os.path.exists(dest_folder_path):
		os.mkdir(dest_folder_path)
	
	entries = [e for e in os.scandir(src_folder_path) if e.is_file() and e.name.endswith(".sav")]
	for entry in entries:
		if entry.name == "ironman.sav":

			# try to copy if the last modified timestamp has changed
			previous_timestamp = ironsave_timestamps[entry.path]
			current_timestamp = os.stat(entry.path).st_mtime

			if 1e-6 < abs(previous_timestamp - current_timestamp):
				try_copy_file(
					entry.path,
					os.path.join(dest_folder_path, get_savefile_date(entry.path) + ".sav")
				)
				ironsave_timestamps[entry.path] = current_timestamp

		elif entry.name.startswith("autosave_"):

			try_copy_file(
				entry.path,
				os.path.join(dest_folder_path, entry.name[9:])
			)

def try_copy_file(src_path, dest_path):
	if not os.path.exists(dest_path):
		shutil.copyfile(src_path, dest_path)
		print(dest_path)

def get_savefile_date(path):
	data = get_savefile_data(path)
	match = re.search("date=\"([0-9.]+)\"", data)
	if match:
		return match.group(1)
	else:
		raise Exception("Could not find date in savefile.")


		
def main():

	settings = get_settings()

	src_folder_path = os.path.join(settings["stellaris_folder_path"], "save games")
	dest_folder_path = settings["saves_folder_path"]
	interval = 4

	print("Watching " + src_folder_path)
	print("Copying to " + dest_folder_path)
	print("Checking every " + str(interval) + " seconds")
	print("")
	
	if not os.path.exists(dest_folder_path):
		os.mkdir(dest_folder_path)
		
	while True:
		entries = [e for e in os.scandir(src_folder_path) if e.is_dir()]
		for entry in entries:
			copy_new_autosaves(
				entry.path, 
				os.path.join(dest_folder_path, entry.name)
			)

		time.sleep(interval)
	

	
if __name__=="__main__":
	main()