# -*- mode: python -*-

block_cipher = None


a = Analysis(['launch_pyslvs.py'],
             pathex=['C:\\Users\\ahshoe\\Desktop\\Pyslvs-PyQt5'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='launch_pyslvs',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='icons\\main_big.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='launch_pyslvs')
