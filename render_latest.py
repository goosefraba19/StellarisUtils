import os, time

from src.files import get_settings, list_jsonzip_paths, get_output_folder_path
from src.model import Model
from src.render import Render

def get_dest_path():
	output_folder_path = get_output_folder_path()
	
	if not os.path.exists(output_folder_path):
		os.makedirs(output_folder_path)
	
	return os.path.join(output_folder_path, "latest.png")

def main():
	settings = get_settings()

	src_path = list_jsonzip_paths()[-1]
	dest_path = get_dest_path()

	t_start = time.time()
	model = Model.from_file(src_path)
	t_model = time.time()
	render = Render(model, settings["render"])
	render.steps()
	render.export(dest_path)
	t_end = time.time()

	t_parse_ms = int(1000*(t_model - t_start))
	t_render_ms = int(1000*(t_end - t_model))
	print("name:   " + model.date)
	print("parse:  " + str(t_parse_ms))
	print("render: " + str(t_render_ms))

if __name__=="__main__":
	main()