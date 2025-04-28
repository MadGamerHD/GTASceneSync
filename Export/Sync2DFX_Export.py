import bpy
import re
from bpy.props import StringProperty, EnumProperty
from io import StringIO
from pathlib import Path

# Define Particle Effects as a constant
PARTICLE_EFFECTS = [
    ("prt_blood", "prt_blood", "spark? maybe meant to be a mini red blood splash"),  # 0
    ("prt_boatsplash", "prt_boatsplash", "from a boat splashing in the water. looks like the soap in the car wash"),  # 1
    ("prt_bubble", "prt_bubble", "bubble!"),  # 2
    ("prt_cardebris", "prt_cardebris", "car debris. like when you crash a car"),  # 3
    ("prt_collisionsmoke", "prt_collisionsmoke", "thick white smoke"),  # 4
    ("prt_glass", "prt_glass", "large shard of glass?!"),  # 5
    ("prt_gunshell", "prt_gunshell", "a gun shell"),  # 6
    ("prt_sand", "prt_sand", "sand"),  # 7
    ("prt_sand2", "prt_sand2", "more sand"),  # 8
    ("prt_smokeII_3_expand", "prt_smokeII_3_expand", "weak smoke"),  # 9
    ("prt_smoke_huge", "prt_smoke_huge", "lot's of expanding smoke"),  # 10
    ("prt_spark", "prt_spark", "sparks fly up and then fall down"),  # 11
    ("prt_spark_2", "prt_spark_2", "powerful sparks flying upwards"),  # 12
    ("prt_splash", "prt_splash", "water splash"),  # 13
    ("prt_wake", "prt_wake", "movement in the water"),  # 14
    ("prt_watersplash", "prt_watersplash", "splash of water. like when a car lands in deep water"),  # 15
    ("prt_wheeldirt", "prt_wheeldirt", "puff of dust"),  # 16
    ("boat_prop", "boat_prop", "tiny water splash?"),  # 17
    ("camflash", "camflash", "flash of a camera... cheese!"),  # 18
    ("exhale", "exhale", "exhaled smoke"),  # 19
    ("explosion_fuel_car", "explosion_fuel_car", "a seemingly randomized small explosion"),  # 20
    ("explosion_large", "explosion_large", "huge explosion with debris"),  # 21
    ("explosion_medium", "explosion_medium", "big explosion with debris"),  # 22
    ("explosion_molotov", "explosion_molotov", "molotov cocktail explosion"),  # 23
    ("explosion_small", "explosion_small", "explosion"),  # 24
    ("explosion_tiny", "explosion_tiny", "small explosion"),  # 25
    ("extinguisher", "extinguisher", "fire extinguisher foam"),  # 26
    ("fire", "fire", "fire"),  # 27
    ("fire_bike", "fire_bike", "a bike"),  # 28
    ("fire_car", "fire_car", "fire from the engine of a car"),  # 29
    ("fire_large", "fire_large", "a large fire"),  # 30
    ("fire_med", "fire_med", "a medium sized fire"),  # 31
    ("flamethrower", "flamethrower", "flame being thrown..."),  # 32
    ("gunflash", "gunflash", "flash at the end of a gun being fired"),  # 33
    ("gunsmoke", "gunsmoke", "small smoke from a gun"),  # 34
    ("heli_dust", "heli_dust", "dust particles being blown around by a helicopter's propellers"),  # 35
    ("jetpack", "jetpack", "flame from a jetpack. colour changes between yellow and blue"),  # 36
    ("jetthrust", "jetthrust", "weak blue flame from muffler of car during the use of nitro"),  # 37
    ("molotov_flame", "molotov_flame", "the fire from the rag of a molotov cocktail"),  # 38
    ("nitro", "nitro", "nitro. varying colour/size etc."),  # 39
    ("overheat_car", "overheat_car", "smoke from the hood of a damaged car. varying grey colour"),  # 40
    ("overheat_car_electric", "overheat_car_electric", "similar to the damaged car smoke. has yellow electric sparks"),  # 41
    ("riot_smoke", "riot_smoke", "huge smoke that appears above buildings during the LS Riots"),  # 42
    ("spraycan", "spraycan", "green spray paint from the spray can"),  # 43
    ("tank_fire", "tank_fire", "large blast followed by smoke. like at the end of a tank's turret during fire"),  # 44
    ("teargas", "teargas", "small gas explosion from a gas grenade"),  # 45
    ("teargasAD", "teargasAD", "large spreading gas from a gas grenade"),  # 46
    ("water_hydrant", "water_hydrant", "jet of water as from a fire hydrant. audio included"),  # 47
    ("water_ripples", "water_ripples", "circular ripples in the water"),  # 48
    ("water_speed", "water_speed", "big splash in water"),  # 49
    ("water_splash", "water_splash", "small splash in water"),  # 50
    ("water_splash_big", "water_splash_big", "large splash in water"),  # 51
    ("water_splsh_sml", "water_splsh_sml", "tiny splash in water"),  # 52
    ("water_swim", "water_swim", "swim splash in water"),  # 53
    ("cigarette_smoke", "cigarette_smoke", "smoke from the end of a cigarette"),  # 54
    ("Flame", "Flame", "small fire with crackling sfx"),  # 55
    ("insects", "insects", "tiny flies flying around"),  # 56
    ("smoke30lit", "smoke30lit", "smoke"),  # 57
    ("smoke30m", "smoke30m", "dark smoke"),  # 58
    ("smoke50lit", "smoke50lit", "large smoke"),  # 59
    ("vent", "vent", "thin smoke"),  # 60
    ("vent2", "vent2", "thin smoke"),  # 61
    ("waterfall_end", "waterfall_end", "mist from the bottom of a waterfall"),  # 62
    ("water_fnt_tme", "water_fnt_tme", "upward jet of water from a fountain with sfx"),  # 63
    ("water_fountain", "water_fountain", "upward jet of water from a fountain with sfx"),  # 64
    ("tree_hit_fir", "tree_hit_fir", "small green leaves falling"),  # 65
    ("tree_hit_palm", "tree_hit_palm", "large green leaves falling"),  # 66
    ("blood_heli", "blood_heli", "explosion of blood"),  # 67
    ("carwashspray", "carwashspray", "spray of soap/steam from a car wash"),  # 68
    ("cement", "cement", "cement pouring"),  # 69
    ("cloudfast", "cloudfast", "2 fast forward travelling clouds"),  # 70
    ("coke_puff", "coke_puff", "a puff of cocaina"),  # 71
    ("coke_trail", "coke_trail", "a pouring trail of coke"),  # 72
    ("explosion_barrel", "explosion_barrel", "a wooden explosion"),  # 73
    ("explosion_crate", "explosion_crate", "a wooden explosion"),  # 74
    ("explosion_door", "explosion_door", "smoke and sparks"),  # 75
    ("petrolcan", "petrolcan", "shooting/trickling water/fuel. used as a peeing effect"),  # 76
    ("puke", "puke", "yesterdays dinner"),  # 77
    ("shootlight", "shootlight", "a light being shot out (used for searchlights). sparks and glass"),  # 78
]

def register_particle_property() -> None:
    """Register custom particle properties on bpy.types.Object."""
    bpy.types.Object.particle_name = EnumProperty(
        name="Particle Name",
        description="Select a particle type",
        items=PARTICLE_EFFECTS,
        default="prt_blood",
    )
    bpy.types.Object.particle_names = StringProperty(
        name="Particle Names",
        description="Comma-separated list of particle names",
        default="prt_blood",
    )

class Export2DFXOperator(bpy.types.Operator):
    """Export selected objects to a 2DFX text file."""
    bl_idname = "export_scene.2dfx"
    bl_label = "Export 2DFX"

    filepath: StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({"ERROR"}, "No objects selected")
            return {"CANCELLED"}

        buffer = StringIO()
        buffer.write(f"NumEntries       {len(selected_objects)}\n")

        for i, obj in enumerate(selected_objects, start=1):
            pos = obj.location
            # Retrieve particle names (fallback to "prt_blood" if not set) and split by comma
            particle_names = getattr(obj, "particle_names", "prt_blood").split(",")
            for particle_name in particle_names:
                particle_name = particle_name.strip()
                if not particle_name:
                    continue
                buffer.write(f"######################### {i} #########################\n")
                buffer.write("2dfxType         PARTICLE\n")
                buffer.write(f"Position         {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}\n")
                buffer.write(f"Name             {particle_name}\n")

        # Write output to file with UTF-8 encoding
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write(buffer.getvalue())
        except Exception as e:
            self.report({"ERROR"}, f"Failed to write file: {e}")
            return {"CANCELLED"}

        self.report({"INFO"}, f"Exported to {self.filepath}")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

class Export2DFXMenu(bpy.types.Menu):
    """2DFX Export Menu in File > Export"""
    bl_label = "Export 2DFX"
    bl_idname = "EXPORT_MT_2dfx"

    def draw(self, context):
        layout = self.layout
        layout.operator(Export2DFXOperator.bl_idname, text="2DFX Export (.txt)")

class ParticlePanel(bpy.types.Panel):
    """Panel to Select Particle Type per Object"""
    bl_label = "2DFX Particle Settings"
    bl_idname = "OBJECT_PT_2dfx"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if obj:
            layout.prop(obj, "particle_name")
            layout.prop(obj, "particle_names")

def menu_func_export(self, context):
    self.layout.menu(Export2DFXMenu.bl_idname)

# List of classes for simplified registration
classes = [Export2DFXOperator, Export2DFXMenu, ParticlePanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    register_particle_property()

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    del bpy.types.Object.particle_name
    del bpy.types.Object.particle_names

if __name__ == "__main__":
    register()