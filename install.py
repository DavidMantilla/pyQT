import PyInstaller.__main__

PyInstaller.__main__.run([
    'src/login.py',
    '--onefile',
    '--windowed'
])