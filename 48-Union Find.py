class UnionFind:
    NORMAL = "normal"
    PATH_COMPRESSION = "pathCompression"
    RANK = "rank"

    def __init__(self, mode=NORMAL):
        self.mode = mode # controls if we want to do union find or union find by rank !
        self.parent = dict()
        self.rank = dict()  # basically the height of the tree under it

    def createSet(self, value):
        self.parent[value] = None

        if self.mode == UnionFind.RANK:
            self.rank[value] = 0

    def find(self, value):
        if value not in self.parent:
            return None

        curr = value
        while self.parent[curr] != None:
            curr = self.parent[curr]

        return curr

    def union(self, valueOne, valueTwo):
        parent1 = self.find(valueOne)
        parent2 = self.find(valueTwo)

        if parent1 != parent2:
            if self.mode == UnionFind.NORMAL:
                #normal approach
                # make 2's parent 1
                self.parent[parent2] = parent1
            elif self.mode == UnionFind.PATH_COMPRESSION:
                #use path compression
                #take all of valueTwo's hierarchy and point its parent to parent1
                curr = valueTwo
                while self.parent[curr] != None:
                    temp = curr #to update the current node
                    curr = self.parent[curr] #to traverse up
                    self.parent[temp] = parent1
                #last one
                self.parent[curr] = parent1
            elif self.mode == UnionFind.RANK:
                #union find with rank
                rank1 = self.rank[parent1]
                rank2 = self.rank[parent2]

                if rank1 == rank2:
                    # if ranks are equal then anyone can become child and the parent's rank is increased by one
                    self.parent[parent2] = parent1
                    self.rank[parent1] += 1
                elif rank1 > rank2:
                    #whichever rank is lower that becomes the child and rank doesnt change
                    self.parent[parent2] = parent1
                else:
                    # whichever rank is lower that becomes the child and rank doesnt change
                    self.parent[parent1] = parent2

if __name__ == '__main__':
    #normal
    uf = UnionFind()

    #with path compression
    uf_pc = UnionFind(mode=UnionFind.PATH_COMPRESSION)

    #with rank
    uf_rank = UnionFind(mode=UnionFind.RANK)

    #testing normal
    uf.createSet(0)
    uf.createSet(1)
    uf.find(0)
    uf.find(1)
    uf.union(0,2)
    uf.find(0)
    uf.find(1)
    uf.union(0,1)
    uf.union(1,0)
    uf.find(0)
    uf.find(1)

    #testing path compression
    # uf_pc.createSet(1)
    # uf_pc.createSet(2)
    # uf_pc.createSet(3)
    # uf_pc.createSet(4)
    # uf_pc.createSet(5)
    # uf_pc.find(2)
    # uf_pc.union(2,3)
    # uf_pc.union(4,5)
    # uf_pc.union(5,3)
    # uf_pc.union(1,3)
    # uf_pc.find(2)


    #testing rank
    # uf_rank.createSet(1)
    # uf_rank.createSet(2)
    # uf_rank.createSet(3)
    # uf_rank.createSet(4)
    # uf_rank.createSet(5)
    # uf_rank.find(2)
    # uf_rank.union(2,3)
    # uf_rank.union(4,5)
    # uf_rank.union(5,3)
    # uf_rank.union(1,3)
    # uf_rank.find(2)