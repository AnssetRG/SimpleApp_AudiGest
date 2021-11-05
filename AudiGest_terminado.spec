# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

print("DISPATH: ", DISTPATH)
print("HOMEPATH: ", HOMEPATH)
print("SPEC: ", SPEC)
print("workpath: ", workpath)

print("CURRENT WORK DIRECTORY: ", os.getcwd())


a = Analysis(['AudiGest_terminado.pyw'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[(os.path.join(HOMEPATH,'librosa'),'librosa'), (os.path.join(HOMEPATH,'pyrender'), 'pyrender')],
             hiddenimports=['scipy._lib.messagestream', 'sklearn.tree', 'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree._utils', 'sklearn.utils._weight_vector', 'sklearn.neighbors._typedefs', 'sklearn.neighbors._quad_tree'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='AudiGest',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
