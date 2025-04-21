import time
from collections import deque


class Solver:
    def DFS(cell, N, CELLS):
        startTime = time.time()
        start = (cell.row, cell.column)
        explored = [start]
        frontier = [start]

        dfsPath = {}

        while len(frontier) > 0:
            currCell = frontier.pop()
            if currCell == (N - 1, N - 1):
                break

            for d in "ESNW":
                if d in CELLS[currCell[0]][currCell[1]].openWalls:
                    if d == 'E':
                        childCell = (currCell[0], currCell[1] + 1)
                    elif d == 'S':
                        childCell = (currCell[0] + 1, currCell[1])
                    elif d == 'N':
                        childCell = (currCell[0] - 1, currCell[1])
                    elif d == 'W':
                        childCell = (currCell[0], currCell[1] - 1)
                    if childCell in explored:
                        continue

                    explored.append(childCell)
                    frontier.append(childCell)

                    dfsPath[childCell] = currCell
        endTime = time.time()
        print("DFS solve time in milliseconds: ", endTime - startTime)
        fwdPath = {}
        pathCell = dfsPath[N - 1, N - 1]
        while pathCell != start:
            fwdPath[dfsPath[pathCell]] = pathCell
            pathCell = dfsPath[pathCell]
        return dfsPath,fwdPath

    def BFS(cell, N, CELLS):
        startTime = time.time()
        frontier = deque()
        start = (cell.row, cell.column)
        frontier.append(start)
        bfsPath = {}
        visited = {start}
        while len(frontier) > 0:
            currCell = frontier.popleft()
            if currCell == (N - 1, N - 1):
                break
            for d in "ESNW":
                if d in CELLS[currCell[0]][currCell[1]].openWalls:
                    if d == 'W' and (currCell[0], currCell[1] - 1) not in visited:
                        nextCell = (currCell[0], currCell[1] - 1)
                        bfsPath[nextCell] = currCell
                        frontier.append(nextCell)
                        visited.add(nextCell)
                    if d == 'S' and (currCell[0] + 1, currCell[1]) not in visited:
                        nextCell = (currCell[0] + 1, currCell[1])
                        bfsPath[nextCell] = currCell
                        frontier.append(nextCell)
                        visited.add(nextCell)
                    if d == 'E' and (currCell[0], currCell[1] + 1) not in visited:
                        nextCell = (currCell[0], currCell[1] + 1)
                        bfsPath[nextCell] = currCell
                        frontier.append(nextCell)
                        visited.add(nextCell)
                    if d == 'N' and (currCell[0] - 1, currCell[1]) not in visited:
                        nextCell = (currCell[0] - 1, currCell[1])
                        bfsPath[nextCell] = currCell
                        frontier.append(nextCell)
                        visited.add(nextCell)
        endTime = time.time()
        print("BFS solve time in milliseconds: ", endTime - startTime)
        fwdPath = {}
        pathCell = bfsPath[N - 1, N - 1]
        while pathCell != start:
            fwdPath[bfsPath[pathCell]] = pathCell
            pathCell = bfsPath[pathCell]
        return bfsPath, fwdPath

    def Dijkstra(cell, N, CELLS):
        startTime=time.time()
        count = 0
        unvisited = {}
        for i in range(0, N):
            for j in range(0, N):
                unvisited[(i,j)] = float('inf')
        unvisited[(cell.row, cell.column)] = 0
        visited = {}
        dijkstraPath = {}

        endCell = CELLS[N - 1][N - 1]
        end = (endCell.row, endCell.column)
        start = (cell.row, cell.column)
        while unvisited:
            currCell = min(unvisited,key=unvisited.get)
            visited[currCell] = unvisited[currCell]
            count+=1

            if currCell == end:
                break
            for d in "ESNW":
                if d in CELLS[currCell[0]][currCell[1]].openWalls:
                    if d == 'E':
                        childCell = (currCell[0], currCell[1] + 1)
                    elif d == 'S':
                        childCell = (currCell[0] + 1, currCell[1])
                    elif d == 'N':
                        childCell = (currCell[0] - 1, currCell[1])
                    elif d == 'W':
                        childCell = (currCell[0], currCell[1] - 1)
                    if childCell in visited:
                        continue
                    tempDist = unvisited[currCell]+1

                    if tempDist < unvisited[childCell]:
                        unvisited[childCell] = tempDist
                        dijkstraPath[childCell] = currCell
            unvisited.pop(currCell)

        endTime = time.time()
        print("Dijkstra solve time in milliseconds: ", endTime-startTime)
        print("Dijkstra path length: ",count)
        fwdPath = {}
        pathCell = dijkstraPath[N-1, N-1]
        while pathCell != start:
            fwdPath[dijkstraPath[pathCell]] = pathCell
            pathCell = dijkstraPath[pathCell]

        return dijkstraPath, fwdPath
