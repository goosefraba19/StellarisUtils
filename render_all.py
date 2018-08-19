import json, os, time

from src.model import Model
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
			results.append((name, src, dest))
	
	return results

def main():
	settings = get_settings()
		
	for (name, src_path, dest_path) in get_pairs(settings):						

		t_start = time.time()
		model = Model.from_jsonzip(src_path)
		t_model = time.time()
		render = Render(model, settings["draw"])
		
		render.regions()
		render.hyperlanes((256,256,256,128), 1)
		render.pops()
		render.text((10,10), model.date)
		
		render.export(dest_path)
		t_end = time.time()

		t_parse_ms = int(1000*(t_model - t_start))
		t_render_ms = int(1000*(t_end - t_model))
		print(name + " (parse: " + str(t_parse_ms) + ", render: " + str(t_render_ms) + ")")
	

if __name__=="__main__":
	main()