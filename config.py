import yaml
import sys
import os


def config_loader(pathToFile, parameter):
    for i in range(5):
        try:
            config1 = yaml.safe_load(open(pathToFile, encoding="utf8"))
            break
        except FileNotFoundError:
            print("File not Found!")
            if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
                root = "."
            else:
                root = ""
            config_path = os.path.join(".", "_database", "_config")
            if not os.path.exists(config_path):
                print("No worries, we'll create the structure for you.")
                os.makedirs(config_path)
            input(
                "Please place your config file in '{}' and hit enter. {} tries left!".format(
                    config_path, 5 - i
                )
            )
    return config1[parameter]


if sys.platform.startswith("linux"):
    workdir = os.path.dirname(os.path.realpath(__file__))
    path_programm = os.path.join(workdir)

else:
    path_programm = os.path.dirname(sys.argv[0])
    if sys.platform.startswith("darwin"):
        if path_programm is "":
            path_programm = "."

logo_path = os.path.join(
    path_programm, "_database", "_config", "icon", "LaMa_icon_logo.png"
)
