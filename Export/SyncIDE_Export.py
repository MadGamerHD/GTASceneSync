import bpy
import re

def clean_name(name):
    """Remove numeric suffixes from the model name."""
    return re.sub(r'\.\d+$', '', name)

class ExportAsIDE(bpy.types.Operator):
    """Export Selected Objects as IDE with Incremental Model IDs"""
    bl_idname = "export_scene.ide"
    bl_label = "Export Selected as IDE"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    model_id: bpy.props.IntProperty(name="Starting Model ID", default=19388)
    render_distance: bpy.props.FloatProperty(name="Render Distance", default=299, min=0, max=1200)
    
    flag_options = [
        ("0", "Default", ""),
        ("1", "Render_Wet_Effects", ""),
        ("2", "TOBJ_Night_Flag", ""),
        ("16", "TOBJ_Day_Flag", ""),
        ("4", "Alpha_Transparency_1", ""),
        ("8", "Alpha_Transparency_2", ""),
        ("32", "Interior_Object", ""),
        ("64", "Disable_Shadow_Culling", ""),
        ("128", "Exclude_Surface_From_Culling", ""),
        ("256", "Disable_Draw_Distance", ""),
        ("512", "Breakable_Window_1", ""),
        ("1024", "Breakable_Window_2", ""),
    ]
    
    selected_flag: bpy.props.EnumProperty(name="Object Flag", items=flag_options, default="0")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "model_id")
        layout.prop(self, "render_distance")
        layout.prop(self, "selected_flag")

    def execute(self, context):
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'WARNING'}, "No mesh objects selected for export.")
            return {'CANCELLED'}
        
        # Ensure the file has the .ide extension
        if not self.filepath.lower().endswith(".ide"):
            self.filepath += ".ide"
        
        unique_names = {}
        current_id = self.model_id
        
        for obj in selected_objects:
            base_name = clean_name(obj.name)
            if base_name not in unique_names:
                unique_names[base_name] = current_id
                current_id += 1
        
        with open(self.filepath, 'w') as file:
            file.write("objs\n")
            
            for name, obj_id in unique_names.items():
                line = f"{obj_id}, {name}, generic, {self.render_distance}, {self.selected_flag}\n"
                file.write(line)
            
            file.write("end\n")

        self.report({'INFO'}, "Export complete as IDE!")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
