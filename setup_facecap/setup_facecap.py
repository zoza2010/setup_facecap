from .setup_facecap.dialog import Dialog
from pyfbsdk import *
from pyfbsdk_additions import *
from PySide2 import shiboken2
from PySide2 import QtWidgets


#
# Subclass FBWidgetHolder and override its WidgetCreate function
#
class NativeWidgetHolder(FBWidgetHolder):
    #
    # Override WidgetCreate function to create native widget via PySide2.
    # \param  parentWidget  Memory address of Parent QWidget.
    # \return               Memory address of the child native widget.
    #
    def WidgetCreate(self, pWidgetParent):
        #
        # IN parameter pWidgetparent is the memory address of the parent Qt widget.
        #   here we should PySide2.shiboken2.wrapInstance() function to convert it to PySide2.QtWidget object.
        #   and use it the as the parent for native Qt widgets created via Python.
        #   Similiar approach is available in the sip python module for PyQt
        #
        # Only a single widget is allowed to be the *direct* child of the IN parent widget.
        #
        self.mNativeQtWidget = Dialog(
            shiboken2.wrapInstance(pWidgetParent, QtWidgets.QWidget)
        )

        #
        # return the memory address of the *single direct* child QWidget.
        #
        return shiboken2.getCppPointer(self.mNativeQtWidget)[0]


class NativeQtWidgetTool(FBTool):
    def BuildLayout(self):
        x = FBAddRegionParam(0, FBAttachType.kFBAttachLeft, "")
        y = FBAddRegionParam(0, FBAttachType.kFBAttachTop, "")
        w = FBAddRegionParam(0, FBAttachType.kFBAttachRight, "")
        h = FBAddRegionParam(0, FBAttachType.kFBAttachBottom, "")
        self.AddRegion("main", "main", x, y, w, h)
        self.SetControl("main", self.mNativeWidgetHolder)

    def __init__(self, name):
        FBTool.__init__(self, name)
        self.mNativeWidgetHolder = NativeWidgetHolder()
        self.BuildLayout()
        self.StartSizeX = 600
        self.StartSizeY = 400


gToolName = "SetupFacecapTool"

# Development? - need to recreate each time!!
gDEVELOPMENT = True  # TODO remove

if gDEVELOPMENT:
    FBDestroyToolByName(gToolName)

if gToolName in FBToolList:
    tool = FBToolList[gToolName]
    ShowTool(tool)
else:
    tool = NativeQtWidgetTool(gToolName)
    FBAddTool(tool)
    if gDEVELOPMENT:
        ShowTool(tool)
