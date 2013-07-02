# -*- coding: utf-8 -*-
import bpy
import os

# Todo:
# - fix object name
# - object scale
# - give parameters to openscad

bl_info = {
    "name": "OpenSCAD importer",
    "description": "Imports OpenSCAD (.scad) files.",
    "author": "Maqq",
    "version": (1, 1),
    "blender": (2, 66, 0),
    "location": "File > Import",
    "warning": "", # used for warning icon and text in addons panel
    "category": "Import-Export"
}

# OpenSCAD path
OPENSCAD = "<insert path to openscad here>"

# Temporary stl file
TEMPNAME = "tempexport.stl"

def read_openscad(context, filepath, scale, parameters):
    from io_mesh_stl import stl_utils
    from io_mesh_stl import blender_utils
    
    print(OPENSCAD)
    print(filepath)
    print(parameters)

    # Export stl from OpenSCAD
    old_wd = os.getcwd()
    os.chdir(OPENSCAD)
    os.system("openscad -o %s %s" % (TEMPNAME, filepath))
    
    if os.path.exists(TEMPNAME):
        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')
    
        if bpy.ops.object.select_all.poll():
            bpy.ops.object.select_all(action='DESELECT')
    
        objName = TEMPNAME
        tris, pts = stl_utils.read_stl(TEMPNAME)
        blender_utils.create_and_link_mesh(objName, tris, pts)
        os.remove(TEMPNAME)
    
    os.chdir(old_wd)
    
    return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, PointerProperty, CollectionProperty
from bpy.types import Operator

class ScadSettings(bpy.types.PropertyGroup):
    my_int = bpy.props.IntProperty()
    my_string = bpy.props.StringProperty()

bpy.utils.register_class(ScadSettings)

class OpenSCADImporter(Operator, ImportHelper):
    """Import OpenSCAD files"""
    bl_idname = "import_mesh.scad"
    bl_label = "Import OpenSCAD"

    # ImportHelper mixin class uses this
    filename_ext = ".scad"

    filter_glob = StringProperty(
            default="*.scad",
            options={'HIDDEN'},
            )
    
    scad = StringProperty(name="openscad executable", default=OPENSCAD)
    scale = FloatProperty(name='Scale', default=1.0)
    
    def __init__(self):
        global OPENSCAD
        super(OpenSCADImporter, self).__init__()
        self.scad = OPENSCAD
    
    # Parameters for the scad file
    p1  = StringProperty(name='P1 name')
    p1v = StringProperty(name='P1 value')
    p2  = StringProperty(name='P2 name')
    p2v = StringProperty(name='P2 value')
    p3  = StringProperty(name='P3 name')
    p3v = StringProperty(name='P3 value')
    p4  = StringProperty(name='P4 name')
    p4v = StringProperty(name='P4 value')

    def execute(self, context):
        global OPENSCAD
        OPENSCAD = self.scad
        return read_openscad(context, self.filepath, self.scale, {self.p1:self.p1v, self.p2:self.p2v, self.p3:self.p3v, self.p4:self.p4v})


def menu_func_import(self, context):
    self.layout.operator(OpenSCADImporter.bl_idname, text="OpenSCAD (.scad)")

def register():
    bpy.utils.register_class(OpenSCADImporter)
    bpy.types.INFO_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(OpenSCADImporter)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    pass
    #register()
    # test call
    #bpy.ops.import_test.some_data('INVOKE_DEFAULT')
