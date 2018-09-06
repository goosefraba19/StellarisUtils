import importlib, os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    importlib.import_module("stellaris.render.step." + module[:-3])