import tkinter.filedialog       #imports filedialog
from unreal import ToolMenus, ToolMenuContext, ToolMenuEntryScript, uclass, ufunction       #imports unreal's toolMenus
import sys              #imports the sys
import os           #imports os
import importlib        #imports importlib
import tkinter          #imports tkinter

srcDir = os.path.dirname(os.path.abspath(__file__))     #gets the path of the source code
if srcDir not in sys.path:                              #checks if the path of the source is not in the system path
    sys.path.append(srcDir)                             #adds the path in the system

import UnrealUtilities                              #imports unreal's utilities
importlib.reload(UnrealUtilities)                   #reloads unreal's utilities

@uclass()                                               #makes unreal class
class LoadFromDirEntryScript(ToolMenuEntryScript):      #makes a class for loading from directory
    @ufunction(override=True)                           #makes a unreal Function that also overrides another function
    def execute(self, context):                               #makes a execute function
        window = tkinter.Tk()                                 #makes the window
        window.withdraw()                                     #hides the window
        fileDir = tkinter.filedialog.askdirectory()           #asks for the file directory
        window.destroy()                                      #deletes the window
        UnrealUtilities.UnealUtility().LoadFromDir(fileDir)   #loads the file from the directory

@uclass()                                                       #makes unreal class
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):        #makes a class for Buliding a Base Material
    @ufunction(override=True)                                   #makes a unreal Function that also overrides another function
    def execute(self, context: ToolMenuContext) -> None:        #makes a function that returns nothing
        UnrealUtilities.UnealUtility().FindOrCreateBaseMaterial()       #runs the FindOrCreateBaseMaterial function in unreal utilities

class UnrealSubstancePlugin:                    #makes unreal substance plugin class
    def __init__(self):                         #makes funtion
        self.subMenuName="SubstancePlugin"      #names the sub menu to SubstancePlugin
        self.subMenuLabel="Substance Plugin"    #names the sub menu's label to SubstancePlugin
        self.InitUI()                           #does InitUI function

    def InitUI(self):
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")                                                #finds the level editor main menu
        self.subMenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", "SubstancePlugin", "Stubstance Plugin")        #adds in a sub menu for the substance plugin
        self.AddEntryScript("BuildBaseMaterail", "Build Base Material", BuildBaseMaterialEntryScript())             #adds build base Material button to the sub menu
        self.AddEntryScript("LoadFromDir", "Load From Directory", LoadFromDirEntryScript())                         #adds load from directory button to the sub menu
        ToolMenus.get().refresh_all_widgets()                                                                       #refreshs the widgets

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript):                             #makes add entry script funtion
        script.init_entry(self.subMenu.menu_name, self.subMenu.menu_name, "", name, label)          #initializes the entry of the script
        script.register_menu_entry()                                                                #adds the script button to the menu

UnrealSubstancePlugin()                                                         #runs the unreal substance plugin