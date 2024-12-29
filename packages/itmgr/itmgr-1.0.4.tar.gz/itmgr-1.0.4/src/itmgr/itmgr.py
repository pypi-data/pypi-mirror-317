# type: ignore[import]
# pyright: ignore[import]
# pylint: disable=import-error
# ruff: noqa: F401, E402
# mypy: ignore-errors
# flake8: noqa: F401



import os
import subprocess
import sys
import json
import requests
from packaging import version
import pkg_resources

def add(import_name: str, package_name: str) -> None:
    """
    Adds a mapping between import name and package name to lib.json
    
    Args:
        import_name: The name used in imports (e.g. 'cv2')
        package_name: The actual package name for pip (e.g. 'opencv-python')
    """
    # Get the directory where itmgr.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "lib.json")
    
    # Load existing mappings or create new dict
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            mappings = json.load(f)
    else:
        mappings = {}
    
    # Add both directional mappings
    mappings[import_name] = package_name
    mappings[package_name] = import_name
    
    # Save updated mappings
    with open(json_path, "w") as f:
        json.dump(mappings, f, indent=4)

    print(f"\x1b[38;5;49mLien {import_name} - {package_name} créé !\x1b[0m")


def delete(import_name: str) -> None:
    """
    Deletes a mapping between import name and package name from lib.json

    Args:
        import_name: The name used in imports (e.g. 'cv2')
    """
    # Get the directory where itmgr.py is located
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib.json")

    # Load existing mappings
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            mappings = json.load(f)
    else:
        print(f"\x1b[38;5;196mNo mapping map found in {json_path}.\x1b[0m")

    # Delete both directional mappings
    if import_name in mappings:
        other_import_name = mappings[import_name]
        del mappings[import_name]
        print(f"\x1b[38;5;49mMapping for {import_name} deleted.\x1b[0m")
        if other_import_name in  mappings:
            del mappings[other_import_name]
            print(f"\x1b[38;5;49mMapping for {other_import_name} deleted.\x1b[0m")
        else :
            print(f"\x1b[38;5;196mNo mapping found for {other_import_name}.\x1b[0m")
    else : 
        print(f"\x1b[38;5;196mNo mapping found for {import_name}.\x1b[0m")
    
    # Save updated mappings
    with open(json_path, "w") as f:
        json.dump(mappings, f, indent=4)



def install_and_import(*modules: list[tuple[str, bool | list[str] | str | tuple[str], bool | str]]) -> None:
    """
    Installe et importe des bibliothèques selon les instructions fournies.

    `modules`: Liste de tuples contenant les informations pour chaque bibliothèque.
    
    Chaque tuple doit être de la forme : (nom_installation, mode_importation, alias ou False)

        - nom_installation : nom pour pip install

        - mode_importation : True pour "from module import attr", str ou list[str] ou tuple[str] pour "from module import attr"

        - alias : False pour pas d'alias ou str pour alias avec "as ..."
    """
    
    caller_globals = sys._getframe(1).f_globals
    
    for module_tpl in modules:
        module_name, from_imports, alias = module_tpl
        original_name = module_name
        from_imports = (
            lambda imports: [imports] if (t := type(imports)) == str and t != bool
            else [i for i in imports] if t == tuple and t != bool
            else imports
        )(from_imports)
        module_name = (
            lambda name: get_package_name(name) if not (dots := "." in name) 
            else get_package_name((parts := name.split("."))[0]) + name[len(parts[0]):]
        )(module_name)
        version_name = module_name.split(".")[0]

        try:
            if module_name not in sys.modules:
                try:
                    __import__(module_name)

                except:
                    __import__(original_name)
                    module_name = original_name

            try :
                if not __check_latest_version__(version_name, _code = True)['is_latest']:
                        if (result := input("\x1b[38;5;116mUne mise à jour a été trouvée, souhaitez-vous l'installer ? (y/n) : \x1b[0m")).lower() == 'y':
                            subprocess.check_call([sys.executable, "-m", "pip", "install", version_name, "--upgrade"])
                        else: 
                            print("\x1b[38;5;196mLa mise à jour n'a pas été effectuée.\x1b[0m")
            except:
                    print("\x1b[38;5;196m Une errreur est survenue\x1b[0m")
                    version_name = original_name.split(".")[0]
                    try:
                            if (result := input("\x1b[38;5;116mUn lien a été trouvé, souhaitez-vous réessayer ? (y/n) : \x1b[0m")).lower() == 'y':
                                subprocess.check_call([sys.executable, "-m", "pip", "install", version_name, "--upgrade"])
                            else: 
                                print("\x1b[38;5;196mLa mise à jour n'a pas été effectuée.\x1b[0m")
                    except:
                        print("\x1b[38;5;196m Une errreur est survenue, impossible d'effectuer la mise à jour\x1b[0m")
                        print("\x1b[38;5;196m Veuillez la faire manuellement\x1b[0m")
            
            if (module := sys.modules[module_name]) and (alias_name := (
                original_name.split(".")[-1] if len(original_name.split(".")) > 1 and from_imports == True
                else from_imports if from_imports != True and from_imports != False
                else alias if alias != False else module_name
            )):
                if from_imports == True:
                    caller_globals[alias_name] = module
                elif from_imports != True and from_imports != False:
                    for name in from_imports:
                        caller_globals[name] = getattr(module, name)
                else:
                    raise ValueError("La seconde valeur doit être True ou une liste de noms d'attributs et pas False.")


            
        except ImportError:
            # Tenter l'installation si le module n'existe pas
            print(f"\x1b[38;5;116m{module_name} non trouvé. Installation en cours...\x1b[0m")
            try:
                print(f"\x1b[38;5;116mInstallation de {module_name}...\x1b[0m")
                subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
                print(f"\x1b[38;5;49m{module_name} installé avec succès.\x1b[0m")
            except:
                print(f"\x1b[38;5;116mErreur lors de l'installation de {module_name}.")
                print("Vérifiez le nom du module et réessayez.\x1b[0m")

                path_lib = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib.json")
                if os.path.exists(path_lib):
                    if module_name in (mappings := json.load(open(path_lib))):
                        try:
                            if (result := input("\x1b[38;5;116mUn lien a été trouvé avec le nom du module, souhaitez-vous réessayer avec le nom associé ? (y/n) : \x1b[0m")).lower() == 'y':
                                print(f"\x1b[38;5;116mInstallation de {mappings[module_name]}...\x1b[0m")
                                subprocess.check_call([sys.executable, "-m", "pip", "install", mappings[module_name]])
                                print(f"\x1b[38;5;49m{mappings[module_name]} installé avec succès.\x1b[0m")
                            else:
                                print("\x1b[38;5;160mAnnulé.\x1b[0m")
                        except:
                            print("\x1b[38;5;116mErreur lors de l'installation de {mappings[module_name]}.")
                            print("Installation impossible.")
                            print("Veuillez installer manuellement le module.\x1b[0m")
            
            # Réessayer l'import après installation
            try:
                if module_name not in sys.modules:
                    try:
                        __import__(module_name)
                    except:
                        __import__(original_name)
                        module_name = original_name
                
                if (module := sys.modules[module_name]) and (alias_name := (
                    original_name.split(".")[-1] if len(original_name.split(".")) > 1 and from_imports == True
                    else from_imports if from_imports != True and from_imports != False
                    else module_name
                )):
                    if from_imports == True:
                        caller_globals[alias_name] = module
                    elif from_imports != True and from_imports != False:
                        for name in from_imports:
                            caller_globals[name] = getattr(module, name)
                    else:
                        raise ValueError("\x1b[38;5;116mLa seconde valeur doit être True ou une liste de noms d'attributs et pas False.\x1b[0m")
                    
            except ImportError:
                print(f"\x1b[38;5;116mErreur : échec de l'installation de {module_name}")
        except Exception as e:
            print(f"\x1b[38;5;116mErreur lors de l'importation de {module_name}: {str(e)}")


def get_package_name(import_name: str) -> str:
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib.json")
    return (lambda: mappings[import_name] 
            if import_name in (mappings := json.load(open(json_path))) 
            else import_name)() if os.path.exists(json_path) else import_name

                
def install(*modules) -> None:
    """
    Installe des bibliothèques Python en utilisant pip.
    -------------------
    - modules : modules à installer.
    """
    for module in modules:
        try:
            print(f"\x1b[38;5;116mInstallation de {module}...\x1b[0m")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print(f"\x1b[38;5;49m{module} installé avec succès.\x1b[0m")
        except:
            print(f"\x1b[38;5;116mErreur lors de l'installation de {module}.")
            print("Vérifiez le nom du module et réessayez.\x1b[0m")

            path_lib = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib.json")
            if os.path.exists(path_lib):
                if module in (mappings := json.load(open(path_lib))):
                    try:
                        if (result := input("\x1b[38;5;80mUn lien a été trouvé avec le nom du module, souhaitez-vous réessayer avec le nom associé ? (y/n) : \x1b[0m")).lower() == 'y':
                            print(f"\x1b[38;5;116mInstallation de {mappings[module]}...\x1b[0m")
                            subprocess.check_call([sys.executable, "-m", "pip", "install", mappings[module]])
                            print(f"\x1b[38;5;49m{mappings[module]} installé avec succès.\x1b[0m")
                        else:
                            print("\x1b[38;5;160mAnnulé.\x1b[0m")
                    except:
                        print("\x1b[38;5;116mErreur lors de l'installation de {mappings[module]}.")
                        print("Installation impossible.")
                        print("Veuillez installer manuellement le module.\x1b[0m")



def importation(*modules : tuple[str, bool | list[str] | str | tuple[str], bool | str]) -> None:
    """
    Importe des bibliothèques Python.
    -------------------
    modules : modules à importer contenant :

        - module : nom du module à importer
        - mode : True pour "import module", str ou list[str] ou tuple[str] pour "from module import attr"
        - alias : False pour pas d'alias ou str pour alias avec "as ..."
    """
    caller_globals = sys._getframe(1).f_globals


    for module_tpl in modules:
        module_name, from_imports, alias = module_tpl
        original_name = module_name
        from_imports = (
            lambda imports: [imports] if (t := type(imports)) == str and t != bool
            else [i for i in imports] if t == tuple and t != bool
            else imports
        )(from_imports)


        module_name = (
            lambda name: get_package_name(name) if not (dots := "." in name) 
            else get_package_name((parts := name.split("."))[0]) + name[len(parts[0]):]
        )(module_name)

        version_name = module_name.split(".")[0]


        try:
            if module_name not in sys.modules:
                try:
                    __import__(module_name)
                except:
                    __import__(original_name)
                    module_name = original_name

                if not __check_latest_version__(version_name, _code = True)['is_latest']:
                    if (result := input("\x1b[38;5;116mUne mise à jour a été trouvée, souhaitez-vous l'installer ? (y/n) : \x1b[0m")).lower() == 'y':
                        subprocess.check_call([sys.executable, "-m", "pip", "install", version_name, "--upgrade"])
                    else: 
                        print("\x1b[38;5;196mLa mise à jour n'a pas été effectuée.\x1b[0m")

            if (module := sys.modules[module_name]) and (alias_name := (
                original_name.split(".")[-1] if len(original_name.split(".")) > 1 and from_imports == True
                else from_imports if from_imports != True and from_imports != False
                else module_name
            )):
                if from_imports == True:
                    caller_globals[alias_name] = module
                elif from_imports != True and from_imports != False:
                    for name in from_imports:
                        caller_globals[name] = getattr(module, name)
                else:
                    raise ValueError("\x1b[38;5;116mLa seconde valeur doit être True ou une liste de noms d'attributs et pas False.\x1b[0m")



        except Exception as e:
            print(f"\x1b[38;5;116mErreur lors de l'importation de {module_name}: {str(e)}")
            print("Vérifiez le nom du module et réessayez.")
            print("Vérifiez si le module est installé.\x1b[0m")
            if (result := input("\x1b[38;5;80mVoulez-vous l'installer ? (y/n) : \x1b[0m")).lower() == 'y':
                install(module_name)
            else:
                print("\x1b[38;5;160mAnnulé.\x1b[0m")


def uninstall(*modules) -> None:
    """
    Désinstalle des bibliothèques Python.
    -------------------
    - modules : modules à désinstaller.
    """
    for module in modules:
        original_module_name = module
        module = get_package_name(module)
        try:
            try:
                __import__(module)
            except ImportError:
                module = original_module_name
                __import__(original_module_name)
                
            # If module exists, try to uninstall it
            print(f"\x1b[38;5;116mDésinstallation de {module}...\x1b[0m")
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", module])
            print(f"\x1b[38;5;49m{module} désinstallé avec succès.\x1b[0m")
            
        except ImportError:
            print(f"\x1b[38;5;116mLe module {module} n'est pas installé ou le nom spécifié est incorrect.\x1b[0m")
            
        except subprocess.CalledProcessError:
            print(f"\x1b[38;5;116mErreur lors de la désinstallation de {module}.")
            print("Veuillez désinstaller manuellement le module.\x1b[0m")


def remove_module(*modules) -> None:
    """
    Enlève des bibliothèques Python dans le programme actuel.
    -------------------
    modules : tuple du module à enlever sous la forme :

        - nom_module : nom du module

        - mode_importation : True pour "from module import attr", str ou list[str] ou tuple[str] pour "from module import attr"

        - alias : False pour pas d'alias ou str pour alias avec "as ..."
    """
    
    caller_globals = sys._getframe(1).f_globals
    
    for module_tpl in modules:
        module_name, from_imports, alias = module_tpl
        original_name = module_name
        from_imports = (
            lambda imports: [imports] if (t := type(imports)) == str and t != bool
            else [i for i in imports] if t == tuple and t != bool
            else imports
        )(from_imports)

    
        module_name = (
            lambda name: get_package_name(name) if not (dots := "." in name) 
            else get_package_name((parts := name.split("."))[0]) + name[len(parts[0]):]
        )(module_name)

    
        try:
            if module_name not in sys.modules:
                __import__(module_name)   
            
            module = sys.modules[module_name]

            if (alias_name := (
                original_name.split(".")[-1] if len(original_name.split(".")) > 1 and from_imports == True
                else from_imports if from_imports != True and from_imports != False
                else original_name
            )):
                if from_imports == True:
                    del caller_globals[alias_name]
                elif from_imports != True and from_imports != False:
                    for name in from_imports:
                        del caller_globals[name]
                else:
                    raise ValueError("x1b[38;5;116mLa seconde valeur doit être True ou une liste de noms d'attributs et pas False.\x1b[0m")

            print(f"\x1b[38;5;49m{module} enlevé avec succès.\x1b[0m")

        except Exception as e:
            print(f"\x1b[38;5;116mErreur : {module} n'est pas installé et ne peut pas être enlevé. \n{e}\x1b[0m")
            if (result := input("\x1b[38;5;80mVoulez-vous l'installer ? (y/n) : \x1b[0m")).lower() == 'y':
                install(module)
            else:
                print("\x1b[38;5;160mAnnulé.\x1b[0m")


def __check_latest_version__(package_name : str, returning : tuple[bool, bool] = (False, False), _code : bool = False) -> dict:
    """
    _Fonction.code_
    """
    if not _code:  
        try:
            current_version = pkg_resources.get_distribution(package_name).version
            
            response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
            latest_version = response.json()["info"]["version"]
            
            is_latest = version.parse(current_version) >= version.parse(latest_version)

            if returning[0]:

                if not returning[1]:
                    return {"package": package_name, "current_version": current_version, "latest_version": latest_version, "is_latest": is_latest}
                else:
                    print(f"\x1b[38;5;49m{package_name} version actuelle: {current_version}")
                    print(f"Dernière version disponible: {latest_version}")
                    print(f"À jour: {is_latest}\x1b[0m")
            
            else: 

                if returning[1]:
                    if (result := input("\x1b[38;5;116mUne mise à jour a été trouvée, souhaitez-vous l'installer ? (y/n) : \x1b[0m")).lower() == 'y':
                        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--upgrade"])
                    else: 
                        print("\x1b[38;5;196mLa mise à jour n'a pas été effectuée.\x1b[0m")
                    
                    return {"package": package_name, "current_version": current_version, "latest_version": latest_version, "is_latest": is_latest}
                    
                if not is_latest:
                    if (result := input("\x1b[38;5;116mUne mise à jour a été trouvée, souhaitez-vous l'installer ? (y/n) : \x1b[0m")).lower() == 'y':
                        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--upgrade"])
                    else: 
                        print("\x1b[38;5;196mLa mise à jour n'a pas été effectuée.\x1b[0m")
        except:
            print(f"\x1b[38;5;116mErreur lors de la recheche de mise à jour de {package_name}.")
            print("Vérifiez le nom du module et réessayez.\x1b[0m")

            path_lib = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib.json")
            if os.path.exists(path_lib):
                if package_name in (mappings := json.load(open(path_lib))):
                    try:
                        if (result := input("\x1b[38;5;116mUn lien a été trouvé avec le nom du module, souhaitez-vous réessayer avec le nom associé ? (y/n) : \x1b[0m")).lower() == 'y':
                            current_version = pkg_resources.get_distribution(mappings[package_name]).version
                            
                            response = requests.get(f"https://pypi.org/pypi/{mappings[package_name]}/json")
                            latest_version = response.json()["info"]["version"]
                            
                            is_latest = version.parse(current_version) >= version.parse(latest_version)
                            
                            if returning[0]:

                                if not returning[1]:
                                    return {"package": package_name, "current_version": current_version, "latest_version": latest_version, "is_latest": is_latest}
                                else:
                                    print(f"\x1b[38;5;49m{package_name} version actuelle: {current_version}")
                                    print(f"Dernière version disponible: {latest_version}")
                                    print(f"À jour: {is_latest}\x1b[0m")
                            
                            else: 

                                if returning[1]:
                                    if (result := input("\x1b[38;5;116mUne mise à jour a été trouvée, souhaitez-vous l'installer ? (y/n) : \x1b[0m")).lower() == 'y':
                                        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--upgrade"])
                                    else: 
                                        print("\x1b[38;5;196mLa mise à jour n'a pas été effectuée.\x1b[0m")
                                    
                                    return {"package": package_name, "current_version": current_version, "latest_version": latest_version, "is_latest": is_latest}
                                    
                                if not is_latest:
                                    if (result := input("\x1b[38;5;116mUne mise à jour a été trouvée, souhaitez-vous l'installer ? (y/n) : \x1b[0m")).lower() == 'y':
                                        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--upgrade"])
                                    else: 
                                        print("\x1b[38;5;196mLa mise à jour n'a pas été effectuée.\x1b[0m")
                    except:
                        print(f"\x1b[38;5;116mErreur lors de la recherche de mise à jour de {mappings[package_name]}.")
                        print("Recheche impossible.")
                        print("Veuillez rechercher la version manuellement du module.\x1b[0m")
    
    elif _code:
        current_version = pkg_resources.get_distribution(package_name).version
        
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        latest_version = response.json()["info"]["version"]
        
        is_latest = version.parse(current_version) >= version.parse(latest_version)
        
        return {
            "package": package_name,
            "current_version": current_version,
            "latest_version": latest_version,
            "is_latest": is_latest
        }



def check_latest_version(package_name : str, returning : tuple[bool, bool] = (False, False)) -> dict:
    """
    Vérifie si la version actuelle d'un package est la plus récente.
    -------------------
    - package_name : nom du package à vérifier.
    - returning : si la fonction doit retourner les informations ou non en print ou en "return"
        - (False, False) : ne retourne rien et installe si besoin
        - (True, False) : retourne les informations (return)
        - (True, True) : retourne les informations (print)
        - (False, True) : retourne les informations (return) et installe si besoin
    """
    return __check_latest_version__(package_name, returning)


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "add":
        add(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3 and sys.argv[1] == "del":
        delete(sys.argv[2])
    else:
        print("\x1b[38;5;196mWrong usage.\x1b[0m")
        print("\x1b[38;5;116mUsage: python itmgr.py add <import_name> <package_name>")
        print("Usage: python itmgr.py del <import_name> (according to the mapping in lib.json or the mapping you added with add)\x1b[0m")

if __name__ == "__main__":
    main()
