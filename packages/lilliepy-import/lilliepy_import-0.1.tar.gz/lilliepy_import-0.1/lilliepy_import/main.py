from pathlib import Path
import os
import importlib.util

route = None

def Importer(component_folder):
    """
    Sets the global route variable to the specified component folder.
    """
    global route
    route = Path(os.path.join(os.getcwd(), component_folder))
    if not route.is_dir():
        raise ValueError(f"The specified component folder '{route}' does not exist or is not a directory.")

def _import(file, component):
    """
    Dynamically imports a module by file name and component name from the global route.
    """
    if route is None:
        raise ValueError("The route has not been set. Call 'Importer' first to set the component folder.")

    module_path = os.path.join(route, file)
    if not os.path.isfile(module_path):
        raise FileNotFoundError(f"The file '{module_path}' does not exist.")

    spec = importlib.util.spec_from_file_location(component, module_path)
    if spec is None:
        raise ImportError(f"Cannot create a spec for '{module_path}'.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  
    return getattr(module, component, None)  
