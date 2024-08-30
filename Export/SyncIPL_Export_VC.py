import bpy
import re

def clean_name(name):
    """Remove numeric suffixes from the model name."""
    return re.sub(r'\.\d+$', '', name)

class ExportAsIPLVC(bpy.types.Operator):
    """Export Selected Objects as IPL with VC Format"""
    bl_idname = "export_scene.ipl_vc"
    bl_label = "Export Selected as IPL (GTA VC)"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    model_id: bpy.props.IntProperty(name="Starting Model ID", default=4794)
    apply_default_rotation: bpy.props.BoolProperty(name="Apply Default Rotation", default=False)
    default_rotation: bpy.props.FloatVectorProperty(name="Default Rotation (Euler)", subtype="EULER", default=(0.0, 0.0, 0.0))

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "model_id")
        layout.prop(self, "apply_default_rotation")
        if self.apply_default_rotation:
            layout.prop(self, "default_rotation")

    def execute(self, context):
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'WARNING'}, "No mesh objects selected for export.")
            return {'CANCELLED'}
        
        # Ensure the file has the .ipl extension
        if not self.filepath.lower().endswith(".ipl"):
            self.filepath += ".ipl"
        
        with open(self.filepath, 'w') as file:
            file.write("inst\n")
            
            for obj in selected_objects:
                loc = obj.location
                
                # Use default rotation if specified
                if self.apply_default_rotation:
                    rot = self.default_rotation
                else:
                    rot = obj.rotation_euler
                
                # Clean the name to remove any numeric suffixes
                model_name = clean_name(obj.name) if obj.name else "Unnamed"
                
                # Prepare position values
                pos_x = round(loc.x, 6)
                pos_y = round(loc.y, 6)
                pos_z = round(loc.z, 6)
                
                # Hardcode the output
                rot_x = 1
                rot_y = 1
                rot_z = 1
                scale_x = 0
                scale_y = 0
                scale_z = 0
                rot_w = 1
                
                # Write the line in VC format
                line = f"{self.model_id}, {model_name}, 0, {pos_x:.6f}, {pos_y:.6f}, {pos_z:.6f}, {rot_x}, {rot_y}, {rot_z}, {scale_x}, {scale_y}, {scale_z}, {rot_w}\n"
                file.write(line)
                
                # Increment model ID for the next object
                self.model_id += 1
            
            file.write("end\n")

        self.report({'INFO'}, "Export complete as IPL (VC)!")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Registering the operator
def register():
    bpy.utils.register_class(ExportAsIPLVC)

def unregister():
    bpy.utils.unregister_class(ExportAsIPLVC)

if __name__ == "__main__":
    register()
