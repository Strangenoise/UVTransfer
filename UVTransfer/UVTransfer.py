###############################

# UV Export/Import
# created by Tristan LG
# 4th march 2019

# DESCRIPTION
# exportUVs()
#   Select the mesh with UVs you want to export
#   Duplicate the selected mesh
#   Export it as mesh.fbx in the project/scripts/ directory
#   Delete the duplicate

# importUVs()
#   Select one or more mesh to import the UVs on
#   Import selected fbx file as reference
#   For each selected mesh, polyTransfer the UVs from the imported file to the mesh
#   Delete the reference

# INSTALL
# Put the script in a PYTHONPATH (ex: C:\Users\User\Documents\maya\scripts)

# Create a python shelf button with theses commands to export UVs:
# import UVTransfer
# UVTransfer.exportUVs()

# Create a python shelf button with theses commands to import UVs:
# import UVTransfer
# UVTransfer.importUVs()

# WARNING
# The non-deformer history is deleted on the mesh you import the UVs on, so be carefull

# Report bugs by writing to tristan.legranche@gmail.com
# Script under CC-BY-NC licence
###############################

import maya.cmds as mc
import os


def exportUVs():

    meshes = mc.ls(selection=True)
    currentWorkspace = mc.workspace(fullName = True)

    for mesh in meshes:

        mc.select(mesh, replace=True)
        duplicatedNodes = mc.duplicate(renameChildren=True)

        duplicate = duplicatedNodes[0]
        duplicateChilds = mc.listRelatives(allDescendents=True)

        for item in duplicateChilds:
            if not mc.objectType(item) == 'mesh':
                mc.delete(item)

        mc.select(duplicate, replace=True)

        filePath = os.path.join(currentWorkspace, 'scripts', mesh)

        mc.file(filePath, exportSelected=True, type='FBX export')

        mc.delete(duplicate)


def importUVs():

    meshes = mc.ls(selection=True)
    currentWorkspace = mc.workspace(fullName=True)
    baseDirectory = os.path.join(currentWorkspace, 'scripts')

    if not meshes:
        print 'Select at least one object to import the UVs on'

    else:

        currentFile = mc.fileDialog2(fileMode=1, startingDirectory=baseDirectory)
        reference = mc.file(currentFile[0], reference=True, namespace='UVTransfer')

        referenceNodes = mc.ls('UVTransfer:*')

        for node in referenceNodes:
            if mc.objectType(node) == 'mesh':

                mc.select(node, replace=True)
                transformNode = mc.listRelatives(parent=True)[0]

                for mesh in meshes:
                    try:
                        mc.polyTransfer(mesh, uvSets=True, alternateObject=transformNode)
                        #mc.bakePartialHistory(mesh, prePostDeformers=True)
                    except:
                        print 'Object has not the same topology'

                break

        mc.file(currentFile[0], removeReference=True)
