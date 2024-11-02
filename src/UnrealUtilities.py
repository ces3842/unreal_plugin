from unreal import (            #gets unreal and imports a list
    AssetToolsHelpers,          #imports AssetToolsHelpers
    AssetTools,                 #imports AssetTools
    EditorAssetLibrary,         #imports EditorAssetLibrary
    Material,                   #imports Material
    MaterialFactoryNew,         #imports MaterialFactoryNew
    MaterialProperty,           #imports MaterialProperty
    MaterialEditingLibrary,     #imports MaterialEditingLibrary
    MaterialExpressionTextureSampleParameter2D as TexSample2D,      #imports MaterialExpressionTextureSampleParameter2D then nicknames it TexSample2D
    AssetImportTask,            #imports assetImportTask
    FbxImportUI         #imports fbxImportUI
)

import os       #imports the os

class UnealUtility:         #makes a UnrealUtility class
    def __init__(self):     #makes funtion
        self.substanceRootDir = "/game/Substance/"      #sets what "/game/Substance/" is named as
        self.baseMaterialName = "M_SubstanceBase"       #sets what "M_SubstanceBase" is named as
        self.substanceTempDir = "/game/Substance/Temp/"     #sets what "/game/Substance/Temp/" is named as
        self.baseMaterialPath = self.substanceRootDir + self.baseMaterialName       #sets what "self.substanceRootDir + self.baseMaterialName" is named as
        self.baseColorName = "BaseColor"                #sets what "BaseColor" is named as
        self.normalName = "Normal"                      #sets what "Normal" is named as
        self.occRoughnessMetalicName = "OcclusionRoughnessMetalic"      #sets what "OcclusionRoughnessMetalic" is named as

    def FindOrCreateBaseMaterial(self):          #makes funtion
        if EditorAssetLibrary.does_asset_exist(self.baseMaterialPath):      #checks if it has the base material path
            return EditorAssetLibrary.load_asset(self.baseMaterialPath)     #gives the base material path
        
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.baseMaterialName, self.substanceRootDir, Material, MaterialFactoryNew())        #makes base material

        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 0)        #makes the base color and places in the editor of the base Material
        baseColor.set_editor_property("parameter_name", self.baseColorName)                                 #sets the name of the base color
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)      #connets the base color to the base material's base color

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSample2D, -800, 400)         #makes the normal and places in the editor of the base Material
        normal.set_editor_property("parameter_name", self.normalName)                                               #sets the name of the normal
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))       #sets the texture as a normal map
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)                         #connets the map to the base material

        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat,TexSample2D, -800, 800)         #makes the occRoughnessMetalic and places in the editor of the base Material
        occRoughnessMetalic.set_editor_property("parameter_name", self.occRoughnessMetalicName)                             #sets the name of the occRoughnessMetalic
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)   #connets the R value to the ambient occlusion
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS)           #connets the G value to the roughness
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "B", MaterialProperty.MP_METALLIC)            #connets the B value to the metallic

        EditorAssetLibrary.save_asset(baseMat.get_path_name())          #saves the base material
        return baseMat                                                  #gives back the base material
    
    def LoadMeshFromPath(self, meshPath):                               #makes a function for loading the mesh from the path d
        print(f"trying to load mesh from path {meshPath}")
        meshName = os.path.split(meshPath)[-1].replace(".fbx","")       #sets the name of the mesh from the ".fbx" file
        importTask = AssetImportTask()                                  #imports the mesh
        importTask.replace_existing = True                              #replaces the mesh if theres a existing one
        importTask.filename = meshPath                                  #makes the file name the mesh path
        importTask.destination_path = "/game/" + meshName               #makes the destination path the /game/(mesh name)
        importTask.save = True                                          #saves
        importTask.automated = True                                     #automates the import task

        FbxImportOptions = FbxImportUI()                                    #sets the fbx import UI as fbx import options 
        FbxImportOptions.import_mesh = True                                 #imports the mesh
        FbxImportOptions.import_as_skeletal = False                         #doesnt import the skelatal
        FbxImportOptions.import_materials = False                           #doesnt import the fbx's materials
        FbxImportOptions.static_mesh_import_data.combine_meshes = True      #combines the fbx as one mesh

        importTask.options = FbxImportOptions                               #sets the import task as fbx import options

        AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask])    #imports the mesh with the settings
        return importTask.get_objects()[0]                                      #gives back the object
    
    def LoadFromDir(self, fileDir):         #makes function
        for file in os.listdir(fileDir):            #looks though files in the file given
            if ".fbx" in file:                                      #checks if ".fbx" is in the file
                self.LoadMeshFromPath(os.path.join(fileDir, file))  #if it is it loads the file