#edges is already an adjacency list where edges[i] is the adjacency list of ith node
def twoColorable(edges):
    #init all node's colors to None
    colors = [None] * len(edges)

    for node, neighbours in enumerate(edges):
        if not colors[node]:
            #init to 0 else just continue onward
            colors[node] = 0

        #set neighbours to the other color
        for neighbour in neighbours:
            # self loop
            if neighbour == node:
                return False

            flippedColor = colors[node] ^ 1

            if not colors[neighbour]:
                #XOR ensures it flips to other color
                colors[neighbour] = flippedColor
            elif colors[neighbour] != flippedColor:
                return False

    return True