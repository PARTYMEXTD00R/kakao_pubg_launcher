import os
def install_module(module):
    os.system(f"pip install {module}")

try:
    import chromedriver_autoinstaller
except:
    install_module("chromedriver_autoinstaller")

chromedriver_autoinstaller.install(True)