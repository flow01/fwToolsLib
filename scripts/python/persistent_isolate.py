import hou

def addAncestors(node, ancestors):
    parent = node.parent()
    children = list(parent.children())
    children.remove(node)
    ancestors += children
    if node.parent() != hou.node("/obj"):
        ancestors += addAncestors(parent, ancestors)
    return list(set(ancestors))

def getUnselected(selectedNodes):
    unselNodesList = []

    selNode = selectedNodes[0]
    gatheredNodes = addAncestors(selNode, [])

    for uNode in gatheredNodes:
        if uNode not in selectedNodes:
            try:
                if uNode.isDisplayFlagSet() == True:
                    unselNodesList.append(uNode)
            except:
                pass
    return unselNodesList

def toggleIsolation():
    #### toggle isolation mode
    #### get isolation-node if exists or Null:
    isonode = hou.node('/obj/FW_ISOLATIONDATA')
    if not isonode:
        #### NON-Isolated Mode: Gather selected Nodes - find unselected (but visible), store their paths in a list and hide them...
        selectedNodes = list(hou.selectedNodes())
        if not selectedNodes:
            hou.ui.displayMessage("Nothing to isolate")
            return
        unselectedNodes = getUnselected(selectedNodes)

        #### Create the Isolation-Node and add the gathered Paths as UserDateString
        isonode = hou.node('/obj').createNode('null','FW_ISOLATIONDATA')
        isonode.hide(True)
        for i in unselectedNodes:
            try:
                i.setDisplayFlag(False)
            except:
                continue
        isonode.setUserData('isolist', ",".join([x.path() for x in unselectedNodes]))

    else:
        #### ISOLATION-MODE:
        isoObjects = isonode.userData('isolist')
        for n in isoObjects.split(','):
            try:
                hou.node(n).setDisplayFlag(True)
            except:
                continue
        isonode.destroy()
