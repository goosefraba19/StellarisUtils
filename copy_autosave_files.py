import os, shutil, time

from src.files import get_settings

def copy_new_autosaves(src_folder_path, dest_folder_path):

	if not os.path.exists(dest_folder_path):
		os.mkdir(dest_folder_path)
	
	names = filter(
        lambda p: p.startswith("autosave"),
        os.listdir(src_folder_path)
    )
	
	for name in names:
		src_path = os.path.join(src_folder_path, name)
		dest_path = os.path.join(dest_folder_path, name[9:])

		if not os.path.exists(dest_path):
			shutil.copyfile(src_path, dest_path)
			print(dest_path)
		
def main():

	settings = get_settings()

	src_folder_path = os.path.join(settings["stellaris_folder_path"], "save games")
	dest_folder_path = settings["saves_folder_path"]
	interval = 10

	print("Watching " + src_folder_path)
	print("Copying to " + dest_folder_path)
	print("Checking every " + str(interval) + " seconds")
	print("")
	
	if not os.path.exists(dest_folder_path):
		os.mkdir(dest_folder_path)
		
	folder_pairs = [(os.path.join(src_folder_path, p), os.path.join(dest_folder_path, p)) for p in os.listdir(src_folder_path)]
	
	while True:
		for pair in folder_pairs:
			copy_new_autosaves(*pair)
		time.sleep(interval)
	
	
if __name__=="__main__":
	main()