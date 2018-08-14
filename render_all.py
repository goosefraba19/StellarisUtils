import json, os

from src.render import Render

def get_settings():
	with open("settings.json") as fp:
		return json.load(fp)
		
def get_pairs(settings):
	src_folder_path = os.path.join(settings["json_folder_path"], settings["current"])
	dest_folder_path = os.path.join(settings["output_folder_path"], settings["current"], "images")
	
	if not os.path.exists(dest_folder_path):
		os.makedirs(dest_folder_path)
			
	results = []
	
	for name in sorted(os.listdir(src_folder_path)):
		src = os.path.join(src_folder_path, name)
		dest = os.path.join(dest_folder_path, os.path.splitext(name)[0] + ".png")
		
		if not os.path.exists(dest):
			results.append((src, dest))
	
	return results

def main():
	settings = get_settings()
		
	for (src, dest) in get_pairs(settings):						
		render = Render(src, settings["draw"])
		
		render.regions()
		render.hyperlanes((256,256,256,128), 1)
		render.pops()
		
		render.export(dest)
		print(dest)
	

if __name__=="__main__":
	main()