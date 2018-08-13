import json, os

from src.render import Render

def get_settings():
	with open("settings.json") as fp:
		return json.load(fp)
		
def get_src_path(settings):
	folder_path = os.path.join(settings["json_folder_path"], settings["current"])		
	paths = [os.path.join(folder_path, p) for p in sorted(os.listdir(folder_path), reverse=True)]	
	return paths[0]
	
def get_dest_path(settings):
	folder_path = settings["output_folder_path"]
	
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)
	
	return os.path.join(folder_path, "latest.png")

def main():
	settings = get_settings()
		
	render = Render(get_src_path(settings), settings["draw"])
	
	render.regions()
	render.hyperlanes((256,256,256,128), 1)
	render.pops()
	
	render.export(get_dest_path(settings))
	

if __name__=="__main__":
	main()