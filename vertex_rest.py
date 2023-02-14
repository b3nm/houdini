import maya.api.OpenMaya as om2
import maya.cmds as cmds
import time
startTime = time.time()

cmds.select(hierarchy=True)

# @dan, this should be the geo of the rig that is being exported...
selectedObjects = cmds.ls(selection=True, long=True, type='mesh')

#set maya to houdini scale
houdiniScale = .01

for mesh in selectedObjects:
    
    selectionList = om2.MSelectionList()
    selectionList.add(mesh)
    dagPath = selectionList.getDagPath(0)
    selMesh = om2.MFnMesh(dagPath)
    
    # get vert list
    vertList = list(set(selMesh.getVertices()[1]))
    lenVertList = len(vertList)
        
    # initial color list
    vertexColorList = []
    
    # add a rest colorset
    colorSetName = "rest"
    if colorSetName not in selMesh.getColorSetNames():
        selMesh.createColorSet("rest", 0)
    
    # set the current color set to the correct one
    selMesh.setCurrentColorSetName(colorSetName)
    
    # get points and positions - multiply for houdini scale in loop
    pointsList = selMesh.getPoints(om2.MSpace.kWorld)
        
    # create color list
    count = 0
    for point in pointsList:
        # assign color
        vertexColorList.append(om2.MColor([pointsList[count][0]*houdiniScale,pointsList[count][1]*houdiniScale,pointsList[count][2]*houdiniScale]))
        count += 1
                
                                
    # sets vert colors
    selMesh.setVertexColors(vertexColorList, vertList)
    
    
    # used for testing - removes all the texture sets on the geo
    # for colorSet in selMesh.getColorSetNames():
    #    selMesh.deleteColorSet(colorSet)
    
   
print(time.time() - startTime)





