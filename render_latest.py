import json, os, time

from src.model import Model
from src.render import Render

def get_settings():
	with open("settings.json") as fp:
		return json.load(fp)
		
def get_src_path(settings):
	folder_path = os.path.join(settings["json_folder_path"], settings["current"])		
	paths = [os.path.join(folder_path, p) for p in sorted(os.listdir(folder_path), reverse=True)]	
	return paths[0]
	
def get_dest_path(settings):
	folder_path = os.path.join(settings["output_folder_path"], settings["current"])
	
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)
	
	return os.path.join(folder_path, "latest.png")

def main():
	settings = get_settings()

	src_path = get_src_path(settings)
	dest_path = get_dest_path(settings)

	t_start = time.time()
	model = Model.from_jsonzip(src_path)
	t_model = time.time()
	render = Render(model, settings["draw"])
	
	render.regions()
	render.hyperlanes((256,256,256,128), 1)
	render.pops()
	
	render.export(dest_path)
	t_end = time.time()

	t_parse_ms = int(1000*(t_model - t_start))
	t_render_ms = int(1000*(t_end - t_model))
	print("parse: " + str(t_parse_ms))
	print("render: " + str(t_render_ms))
	

if __name__=="__main__":
	main()