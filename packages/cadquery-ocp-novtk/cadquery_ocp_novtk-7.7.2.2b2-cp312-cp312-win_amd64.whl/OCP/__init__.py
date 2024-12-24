"""""" # start delvewheel patch
def _delvewheel_patch_1_9_0():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'cadquery_ocp_novtk.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_9_0()
del _delvewheel_patch_1_9_0
# end delvewheel patch

try:
    # Will only work on Windows
    def _vtkmodules():
        import os
        libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'vtkmodules'))
        os.add_dll_directory(libs_dir)
    
    _vtkmodules()
except:
    pass
finally:
    del _vtkmodules

from OCP.OCP import *
from OCP.OCP import __version__
