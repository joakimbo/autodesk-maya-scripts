#
# Author: Joakim Ö at https://github.com/joakimbo
# Version: 1.0.1
# Created in May 2018
# Autodesk Maya version: 2018.3
#
# Credit to Micheal Comet at www.comet-cartoons.com
# for his work on cometJointOrient which served as an
# reference for the UI layout.
#

# imports
import pymel.core as pm

# define functions
def showHideLocalRotationAxis(val):
    selectedJoints = pm.ls(selection = True, type = 'joint')
    for obj in selectedJoints:
        obj.displayLocalAxis.set(val)

def setRotateToZero(*args):
    selectedJoints = pm.ls(selection = True, type = 'joint')
    for obj in selectedJoints:
        obj.rotate.set(0.0,0.0,0.0)

def setRotateAxisToZero(*args):
    selectedJoints = pm.ls(selection = True, type = 'joint')
    for obj in selectedJoints:
        obj.rotateAxis.set(0.0,0.0,0.0)

def setWorldUpAxis(xyz):
    if xyz == 'X':
        worldUpAxisField.setValue((1.0,0.0,0.0,0.0))
    elif xyz == 'Y':
        worldUpAxisField.setValue((0.0,1.0,0.0,0.0))
    elif xyz == 'Z':
        worldUpAxisField.setValue((0.0,0.0,1.0,0.0))

def aimConstraintParentTowardsChild(parent, children, isLastChild):

    # Set AIM axis
    aimAxisLabel = pm.radioButton(pm.radioCollection(aimAxisCollection, query = True, select = True),query = True, label = True)
    aimAxisIsNegative = pm.checkBox(aimAxisIsNegativeBox, query = True, value = True)
    aimAxisValue = 0
    if aimAxisIsNegative or isLastChild:
        aimAxisValue = -1.0
    else:
        aimAxisValue = 1.0

    aimAxisVector = []
    if aimAxisLabel == 'X':
        aimAxisVector = [aimAxisValue, 0.0, 0.0]
    elif aimAxisLabel == 'Y':
        aimAxisVector = [0.0,aimAxisValue, 0.0]
    elif aimAxisLabel == 'Z':
        aimAxisVector = [0.0, 0.0, aimAxisValue]

    # Set UP axis
    upAxisLabel = pm.radioButton(pm.radioCollection(upAxisCollection, query = True, select = True),query = True, label = True)
    upAxisIsNegative = pm.checkBox(upAxisIsNegativeBox, query = True, value = True)
    upAxisValue = 0
    if upAxisIsNegative:
        upAxisValue = -1.0
    else:
        upAxisValue = 1.0

    upAxisVector = []
    if upAxisLabel == 'X':
        upAxisVector = [upAxisValue, 0.0, 0.0]
    elif upAxisLabel == 'Y':
        upAxisVector = [0.0,upAxisValue, 0.0]
    elif upAxisLabel == 'Z':
        upAxisVector = [0.0, 0.0, upAxisValue]

    # Set WORLD UP axis
    worldUpAxisVector = worldUpAxisField.getValue()

    if isLastChild:
        parent.jointOrient.set([0,0,0])
        aimCon = pm.aimConstraint(children[0], parent, aim = aimAxisVector, u = upAxisVector, wu = worldUpAxisVector)
        pm.aimConstraint(children, parent, edit = True, rm = True)
        parent.jointOrient.set(parent.jointOrient.get()+parent.rotate.get())
        parent.rotate.set(0.0,0.0,0.0)
    else:
        pm.parent(children, world = True)
        parent.jointOrient.set([0,0,0])
        orientChildrenLabel = pm.radioButton(pm.radioCollection(orientChildrenTowardsCollection, query = True, select = True), query = True, label = True)
        if orientChildrenLabel == "Orient Parent towards average of child positions":
            aimCon = pm.aimConstraint(children, parent, aim = aimAxisVector, u = upAxisVector, wu = worldUpAxisVector)
        elif orientChildrenLabel == "Orient Parent towards first child position":
            aimCon = pm.aimConstraint(children[0], parent, aim = aimAxisVector, u = upAxisVector, wu = worldUpAxisVector)
        pm.aimConstraint(children, parent, edit = True, rm = True)
        parent.jointOrient.set(parent.jointOrient.get()+parent.rotate.get())
        parent.rotate.set(0.0,0.0,0.0)
        pm.parent(children, parent)

def orientJoints(*args):
    selectedJoints = pm.ls(selection = True, type = 'joint')
    allJoints = []
    orientDescendents = pm.checkBox(orientChildrenBox, query = True, value = True)
    for joint in selectedJoints:
        allJoints.append(joint)
        if orientDescendents:
            descendents = pm.listRelatives(joint, allDescendents = True)
            allJoints = allJoints + descendents

    for joint in allJoints:
        allChildren = list(reversed(pm.listRelatives(joint, children = True)))
        if len(allChildren) == 0:
            aimConstraintParentTowardsChild(joint, pm.listRelatives(joint, parent = True), True)
        elif len(allChildren) >= 1:
            aimConstraintParentTowardsChild(joint, allChildren, False)

    pm.select(selectedJoints, r = True)


def setTweakToZero(*args):
    floatField.setValue((0.0,0.0,0.0,0.0))

def addToJointOrient(*args):
    selectedJoints = pm.ls(selection = True, type = 'joint', objectsOnly = True)
    for obj in selectedJoints:
        obj.jointOrient.set(obj.jointOrient.get()+floatField.getValue())

def subFromJointOrient(*args):
    selectedJoints = pm.ls(selection = True, type = 'joint')
    for obj in selectedJoints:
        obj.jointOrient.set(obj.jointOrient.get()-floatField.getValue())

def adjustAimUpAxisOnChange(aimDirStr):
    aimDirLabel = pm.radioButton(pm.radioCollection(aimAxisCollection, query = True, select = True), query = True, label = True)
    upDirLabel = pm.radioButton(pm.radioCollection(upAxisCollection, query = True, select = True), query = True, label = True)
    if aimDirStr == 'aimX' and upDirLabel == 'X':
        pm.radioButton(upAxisYBtn, edit = True, select = True)
    elif aimDirStr == 'aimY' and upDirLabel == 'Y':
        pm.radioButton(upAxisZBtn, edit = True, select = True)
    elif aimDirStr == 'aimZ' and upDirLabel == 'Z':
        pm.radioButton(upAxisXBtn, edit = True, select = True)
    elif aimDirStr == 'upX' and aimDirLabel == 'X':
        pm.radioButton(aimAxisYBtn, edit = True, select = True)
    elif aimDirStr == 'upY' and aimDirLabel == 'Y':
        pm.radioButton(aimAxisZBtn, edit = True, select = True)
    elif aimDirStr == 'upZ' and aimDirLabel == 'Z':
        pm.radioButton(aimAxisXBtn, edit = True, select = True)

# create template for UI
template = pm.uiTemplate('jointOrientTemplate', force = True)
template.define(pm.frameLayout, labelVisible = False, marginHeight = 2, marginWidth = 2, width = 455)
template.define(pm.rowLayout, columnWidth5 = [455/5, 455/5, 455/5, 455/5, 455/5])

# create window with template and ui elements
with pm.window(title="joakimJointOrient 1.0.1", sizeable = False) as win:
    with template:
        with pm.columnLayout(rowSpacing = 5):
            with pm.frameLayout():
                pm.text(label = "Show or Hide Local Rotation Axes")
                with pm.rowLayout(numberOfColumns = 2):
                    showAxisBtn = pm.button(label='Show', width = 455/2)
                    hideAxisBtn = pm.button(label='Hide', width = 455/2)
            with pm.frameLayout():
                pm.separator(width = 450)
                pm.text(label = "Set Rotate and/or Rotate Axis to 0")
                with pm.columnLayout(rowSpacing = 2):
                    addRotToOrient = pm.button(label="Set rotate to 0", width = 455)
                    pm.separator(width = 455, height = 4, style = 'none')
                    addRotAxisToOrient = pm.button(label="Set Rotate Axis to 0", width = 455)
            with pm.frameLayout():
                pm.separator(width = 450)
                pm.text(label = "Orient Joints")
                with pm.columnLayout():
                    with pm.rowLayout(numberOfColumns = 5):
                        pm.text(label = "Aim Axis")
                        aimAxisCollection = pm.radioCollection()
                        aimAxisXBtn = pm.radioButton(label = 'X', select = 1)
                        aimAxisYBtn = pm.radioButton(label = 'Y')
                        aimAxisZBtn = pm.radioButton(label = 'Z')
                        aimAxisIsNegativeBox = pm.checkBox(label = "Is negative")
                    with pm.rowLayout(numberOfColumns = 5):
                        pm.text(label = "Up Axis")
                        upAxisCollection = pm.radioCollection()
                        upAxisXBtn = pm.radioButton(label = 'X')
                        upAxisYBtn = pm.radioButton(label = 'Y', select = 1)
                        upAxisZBtn = pm.radioButton(label = 'Z')
                        upAxisIsNegativeBox = pm.checkBox(label = "Is negative")
                    with pm.rowLayout(numberOfColumns = 4):
                        worldUpAxisField = pm.floatFieldGrp(label = "World Up Axis",numberOfFields = 3, value1 = 0.00, value2 = 1.00, value3 = 0.00, precision = 2)
                        setWorldUpXBtn = pm.button(label='X')
                        setWorldUpYBtn = pm.button(label='Y')
                        setWorldUpZBtn = pm.button(label='Z')
                    with pm.columnLayout(columnWidth = 455, columnAttach = ('both', 5)):
                        orientChildrenBox = pm.checkBox(label = "Orient children of selected joints", value = True)
                        pm.text(label = "If joint has several children", height = 20, align = 'left')
                        orientChildrenTowardsCollection = pm.radioCollection()
                        pm.radioButton(label = "Orient Parent towards average of child positions", select = 1)
                        pm.radioButton(label = "Orient Parent towards first child position")
                    with pm.rowLayout(numberOfColumns = 1):
                        orientJointsBtn = pm.button(label = "Orient Joints", width = 455)

            with pm.frameLayout():
                pm.separator(width = 450)
                pm.text(label = "Add or Substract from Joint Orient")
                with pm.columnLayout():
                    with pm.rowLayout(numberOfColumns = 2):
                        floatField = pm.floatFieldGrp(numberOfFields = 3, value1 = 0.00, value2 = 0.00, value3 = 0.00, precision = 2)
                        setTweakValuesToZeroBtn = pm.button(label = "Set to 0")
                    with pm.rowLayout(numberOfColumns = 2):
                        addToJointOrientBtn = pm.button(label='Add', width = 455/2)
                        subtractFromJointOrientBtn = pm.button(label='Subtract', width = 455/2)
    with pm.columnLayout():
        pm.separator(width = 455)
        pm.separator(style='none', height = 10)
        pm.text(label = "By Joakim Ö", width = 455)
        pm.separator(style='none', height = 10)

# Set Callbacks
showAxisBtn.setCommand(pm.Callback(showHideLocalRotationAxis, 1))
hideAxisBtn.setCommand(pm.Callback(showHideLocalRotationAxis, 0))

addRotToOrient.setCommand(pm.Callback(setRotateToZero))
addRotAxisToOrient.setCommand(pm.Callback(setRotateAxisToZero))

aimAxisXBtn.onCommand(pm.Callback(adjustAimUpAxisOnChange,'aimX'))
aimAxisYBtn.onCommand(pm.Callback(adjustAimUpAxisOnChange,'aimY'))
aimAxisZBtn.onCommand(pm.Callback(adjustAimUpAxisOnChange,'aimZ'))
upAxisXBtn.onCommand(pm.Callback(adjustAimUpAxisOnChange,'upX'))
upAxisYBtn.onCommand(pm.Callback(adjustAimUpAxisOnChange,'upY'))
upAxisZBtn.onCommand(pm.Callback(adjustAimUpAxisOnChange,'upZ'))

setWorldUpXBtn.setCommand(pm.Callback(setWorldUpAxis, 'X'))
setWorldUpYBtn.setCommand(pm.Callback(setWorldUpAxis, 'Y'))
setWorldUpZBtn.setCommand(pm.Callback(setWorldUpAxis, 'Z'))
orientJointsBtn.setCommand(pm.Callback(orientJoints))

setTweakValuesToZeroBtn.setCommand(setTweakToZero)
addToJointOrientBtn.setCommand(pm.Callback(addToJointOrient))
subtractFromJointOrientBtn.setCommand(pm.Callback(subFromJointOrient))

# show window
win.show()
