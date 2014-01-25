from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())

# -*- mode: python -*-
a = Analysis(['..\\Users\\Jeff\\PycharmProjects\\dojo\\main.py'],
             pathex=['C:\\PyInstaller-2.1\\dojo'],
             hiddenimports=[],
             runtime_hooks=None)
for d in a.datas:
    if 'pyconfig.h' in d[0]: 
        a.datas.remove(d)
        break
        
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          Tree('..\\Users\\Jeff\\PycharmProjects\\dojo'),
          a.binaries,
          a.zipfiles,
          a.datas,
          name='dojo.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
