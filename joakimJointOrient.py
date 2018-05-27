#
# Author: Joakim Ö at https://github.com/joakimbo
# Created in May 2018
# Autodesk Maya version: 2018.3
#
# Credit to Micheal Comet at www.comet-cartoons.com
# for his work on cometJointOrient which served as an
# reference for the UI layout.
#

# imports
import pymel.core as pm

# create template for UI
template = pm.uiTemplate('jointOrientTemplate', force = True)
template.define(pm.frameLayout, borderVisible = True, labelVisible = False, marginHeight = 2, marginWidth = 2, width = 455)
template.define(pm.rowLayout, columnWidth5 = [455/5, 455/5, 455/5, 455/5, 455/5])

# create window with template and ui elements
with pm.window(title="joakimJointOrient", sizeable = False) as win:
    with template:
        with pm.columnLayout(rowSpacing = 5):
            with pm.frameLayout():
                pm.text(label = "Show or Hide Local Rotation Axes")
                with pm.rowLayout(numberOfColumns = 2):
                    showAxisBtn = pm.button(label="Show", width = 455/2)
                    hideAxisBtn = pm.button(label="Hide", width = 455/2)
            with pm.frameLayout():
                pm.text(label = "Set or Add values to Joint Orient")
                with pm.columnLayout(rowSpacing = 2):
                    addRotToOrient = pm.button(label="Add Rotate values", width = 455)
                    setRotToOrient = pm.button(label="Set Rotate values", width = 455)
                    pm.separator(width = 455, height = 4, style = 'none')
                    addRotAxisToOrient = pm.button(label="Add Rotate Axis values", width = 455)
                    setRotAxisToOrient = pm.button(label="Set Rotate Axis values", width = 455)
            with pm.frameLayout():
                pm.text(label = "Orient Joints")
                with pm.columnLayout():
                    with pm.rowLayout(numberOfColumns = 5):
                        pm.text(label = 'Aim Axis')
                        aimAxisCollection = pm.radioCollection()
                        pm.radioButton(label = "X", select = 1)
                        pm.radioButton(label = "Y")
                        pm.radioButton(label = "Z")
                        aimAxisIsNegativeBox = pm.checkBox(label = "Is negative")
                    with pm.rowLayout(numberOfColumns = 5):
                        pm.text(label = 'Up Axis')
                        upAxisCollection = pm.radioCollection()
                        pm.radioButton(label = "X")
                        pm.radioButton(label = "Y", select = 1)
                        pm.radioButton(label = "Z")
                        upAxisIsNegativeBox = pm.checkBox(label = "Is negative")
                    with pm.rowLayout(numberOfColumns = 4):
                        worldUpAxisField = pm.floatFieldGrp(label = "World Up Axis",numberOfFields = 3, value1 = 0.00, value2 = 1.00, value3 = 0.00, precision = 2)
                        setWorldUpXBtn = pm.button(label="X")
                        setWorldUpYBtn = pm.button(label="Y")
                        setWorldUpZBtn = pm.button(label="Z")
                    with pm.rowLayout(numberOfColumns = 1):
                        orientJointsBtn = pm.button(label = "Orient Joints", width = 455)
            with pm.frameLayout():
                pm.text(label = "Add or Substract from Joint Orient")
                with pm.columnLayout():
                    with pm.rowLayout(numberOfColumns = 2):
                        floatField = pm.floatFieldGrp(numberOfFields = 3, value1 = 0.00, value2 = 0.00, value3 = 0.00, precision = 2)
                        setTweakValuesToZeroBtn = pm.button(label = "Set to 0")
                    with pm.rowLayout(numberOfColumns = 2):
                        addToJointOrientBtn = pm.button(label="Add", width = 455/2)
                        subtractFromJointOrientBtn = pm.button(label="Subtract", width = 455/2)
    with pm.columnLayout(columnAttach = ('both', 5), columnWidth = 450):
        pm.separator()
        pm.separator(style='none', height = 10)
        pm.text(label = "By Joakim Ö")
        pm.separator(style='none', height = 10)


# define functions
def showHideLocalRotationAxis(val):
    selectedJoints = pm.ls(selection = True, type = 'joint')
    for obj in selectedJoints:
        obj.displayLocalAxis.set(val)


def setRotateToJointOrient(*args):
    selectedJoints = pm.ls(selection = True, type = 'joint')
    for obj in selectedJoints:
        print obj.jointOrient.set(obj.rotate.get())
        print obj.rotate.set(0.0,0.0,0.0)

def addRotateToJointOrient(*args):
    selectedJoints = pm.ls(selection = True, type = 'joint')
    for obj in selectedJoints:
        obj.jointOrient.set(obj.jointOrient.get()+obj.rotate.get())
        print obj.rotate.set(0.0,0.0,0.0)

def setRotateAxisToJointOrient(*args):
    selectedJoints = pm.ls(selection = True, type = 'joint')
    for obj in selectedJoints:
        print obj.jointOrient.set(obj.rotateAxis.get())
        print obj.rotate.set(0.0,0.0,0.0)

def addRotateAxisToJointOrient(*args):
    selectedJoints = pm.ls(selection = True, type = 'joint')
    for obj in selectedJoints:
        obj.jointOrient.set(obj.jointOrient.get()+obj.rotateAxis.get())
        print obj.rotate.set(0.0,0.0,0.0)

def setWorldUpAxis(xyz):
    if xyz == 'X':
        worldUpAxisField.setValue((1.0,0.0,0.0,0.0))
    elif xyz == 'Y':
        worldUpAxisField.setValue((0.0,1.0,0.0,0.0))
    elif xyz == 'Z':
        worldUpAxisField.setValue((0.0,0.0,1.0,0.0))

def aimConstraintParentTowardsChild(parent, child, isLastChild):
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
        aimCon = pm.aimConstraint(child, parent, aim = aimAxisVector, u = upAxisVector, wu = worldUpAxisVector)
        pm.delete(aimCon)
    else:
        pm.parent(child, world = True)
        aimCon = pm.aimConstraint(child, parent, aim = aimAxisVector, u = upAxisVector, wu = worldUpAxisVector)
        pm.delete(aimCon)
        print child
        print parent
        pm.parent(child, parent)

def orientJoints(*args):
    parentJoint = pm.ls(selection = True, tail = 1, type = 'joint')
    allJoints = []
    allJoints.append(parentJoint[0])
    if parentJoint:
        allDescendents = list(reversed(pm.listRelatives(parentJoint, allDescendents = True)))
        allJoints = allJoints + allDescendents

        for joint in allJoints:
            allChildren = list(reversed(pm.listRelatives(joint, children = True)))
            if len(allChildren) == 0:
                aimConstraintParentTowardsChild(joint, pm.listRelatives(joint, parent = True)[0], True)
            elif len(allChildren) == 1:
                aimConstraintParentTowardsChild(joint, allChildren[0], False)
            elif len(allChildren) > 1:
                aimConstraintParentTowardsChild(joint, allChildren, False)


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

# Set Callbacks
showAxisBtn.setCommand(pm.Callback(showHideLocalRotationAxis, 1))
hideAxisBtn.setCommand(pm.Callback(showHideLocalRotationAxis, 0))

setRotToOrient.setCommand(pm.Callback(setRotateToJointOrient))
addRotToOrient.setCommand(pm.Callback(addRotateToJointOrient))
setRotAxisToOrient.setCommand(pm.Callback(setRotateAxisToJointOrient))
addRotAxisToOrient.setCommand(pm.Callback(addRotateAxisToJointOrient))

setWorldUpXBtn.setCommand(pm.Callback(setWorldUpAxis, 'X'))
setWorldUpYBtn.setCommand(pm.Callback(setWorldUpAxis, 'Y'))
setWorldUpZBtn.setCommand(pm.Callback(setWorldUpAxis, 'Z'))
orientJointsBtn.setCommand(pm.Callback(orientJoints))

setTweakValuesToZeroBtn.setCommand(setTweakToZero)
addToJointOrientBtn.setCommand(pm.Callback(addToJointOrient))
subtractFromJointOrientBtn.setCommand(pm.Callback(subFromJointOrient))

# show window
win.show()
