import re, os, shutil, time
from collections import defaultdict

from stellaris.files import get_settings, get_savefile_folder_path
from stellaris.model import get_savefile_data

INTERVAL = 4 # seconds


ironsave_timestamps = defaultdict(float)

def copy_new_autosaves(src_folder_path, dest_folder_path):
	
	entries = [e for e in os.scandir(src_folder_path) if e.is_file() and e.name.endswith(".sav")]
	for entry in entries:
		if entry.name == "ironman.sav":

			# try to copy if the last modified timestamp has changed
			previous_timestamp = ironsave_timestamps[entry.path]
			current_timestamp = os.stat(entry.path).st_mtime

			if 1e-6 < abs(previous_timestamp - current_timestamp):
				try_copy_file(
					entry.path,
					dest_folder_path,
					get_savefile_date(entry.path) + ".sav"
				)
				ironsave_timestamps[entry.path] = current_timestamp

		elif entry.name.startswith("autosave_"):

			try_copy_file(
				entry.path,
				dest_folder_path,
				entry.name[9:]
			)



def try_copy_file(src_path, dest_folder_path, dest_name):

	if not os.path.exists(dest_folder_path):
		os.makedirs(dest_folder_path)

	dest_path = os.path.join(dest_folder_path, dest_name)

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

	print("Watching " + src_folder_path)
	print("Checking every " + str(INTERVAL) + " seconds")
	print("")
	
	while True:
		entries = [e for e in os.scandir(src_folder_path) if e.is_dir()]
		for entry in entries:
			copy_new_autosaves(
				entry.path, 
				get_savefile_folder_path(entry.name)
			)

		time.sleep(INTERVAL)
	

	
if __name__=="__main__":
	main()