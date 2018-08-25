import os, time

from src.files import get_settings, list_jsonzip_paths, get_output_folder_path
from src.model import Model
from src.render import Render

def get_pairs():
	dest_folder_path = os.path.join(get_output_folder_path(), "images")

	if not os.path.exists(dest_folder_path):
		os.makedirs(dest_folder_path)

	for src_path in list_jsonzip_paths():
		name = os.path.splitext(os.path.basename(src_path))[0]
		dest_path = os.path.join(dest_folder_path, name + ".png")
		if not os.path.exists(dest_path):
			yield (name, src_path, dest_path)

def main():
	settings = get_settings()

	pairs = list(get_pairs())

	print("Current game is '" + settings["current"] + "'.")
	print(f"Rendering {len(pairs)} images.")
	print()
		
	for (name, src_path, dest_path) in pairs:						

		t_start = time.time()
		model = Model.from_file(src_path)
		t_model = time.time()
		render = Render(model, settings["render"])
		render.steps()
		render.export(dest_path)
		t_end = time.time()

		t_parse_ms = int(1000*(t_model - t_start))
		t_render_ms = int(1000*(t_end - t_model))
		print(name + " (parse: " + str(t_parse_ms) + ", render: " + str(t_render_ms) + ")")
	

if __name__=="__main__":
	main()