from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "CONFIDENTIAL",
    options = options,
    version = "1.0",
    description = '4G/us',
    executables = executables
)
