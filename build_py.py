import PyInstaller.__main__
PyInstaller.__main__.run([
    '--onefile',
    '--windowed',
    '--name=DragoTurkey',
    '--icon=ressources\\dd_icon.ico',
    '--add-data', 'ressources;ressources',
    '--add-data', 'config.json;.',
    'main.py',
])
