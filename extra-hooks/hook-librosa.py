from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('librosa')
datas += collect_data_files('pyrender')
hiddenimports=['scipy._lib.messagestream', 'sklearn.tree', 'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree._utils', 'sklearn.utils._weight_vector']