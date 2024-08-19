import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import vtk
from VTKApp import VTKApp

# Epsilon = 0.000001
Epsilon = 0.0

# z : 2.8930721664428702

SlicingPlaneZPosition = 2.8930721664428702

def Line2DIntersection(x1, y1, x2, y2, x3, y3, x4, y4):
    if (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4) == 0:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    if t < 0 or t > 1:
        return None
    if u < 0 or u > 1:
        return None
    else:
        return [x1 + t * (x2 - x1), y1 + t * (y2 - y1)]

def Line2DIntersectionOnlyOnLine(x1, y1, x2, y2, x3, y3, x4, y4):
    if (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4) == 0:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    if t <= Epsilon or t >= 1 - Epsilon:
        return None
    if u <= Epsilon or u >= 1 - Epsilon:
        return None
    else:
        return [x1 + t * (x2 - x1), y1 + t * (y2 - y1)]

class ContourCorrector:
    def __init__(self, app, contour) -> None:
        self.app = app
        self.contour = contour

    def Check(self):
        points = self.contour.GetPoints()

        # Iterate all points
        # for i in range(points.GetNumberOfPoints()):
        #     p = points.GetPoint(i)

        # Iterate all lines
        # for i in range(self.contour.GetNumberOfCells()):
        #     line = self.contour.GetCell(i)
        #     pi0 = line.GetPointId(0)
        #     pi1 = line.GetPointId(1)
        #     print(f"{pi0} -> {pi1}      {points.GetPoint(pi0)} => {points.GetPoint(pi1)}")

        intersectionPoints = {}
        for i in range(self.contour.GetNumberOfCells()):
            linei = self.contour.GetCell(i)
            ipi0 = linei.GetPointId(0)
            ipi1 = linei.GetPointId(1)
            ip0 = points.GetPoint(ipi0)
            ip1 = points.GetPoint(ipi1)
            for j in range(i + 1, self.contour.GetNumberOfCells()):
                linej = self.contour.GetCell(j)
                jpi0 = linej.GetPointId(0)
                jpi1 = linej.GetPointId(1)
                jp0 = points.GetPoint(jpi0)
                jp1 = points.GetPoint(jpi1)
            
                intersection = Line2DIntersectionOnlyOnLine(ip0[0], ip0[1], ip1[0], ip1[1], jp0[0], jp0[1], jp1[0], jp1[1])
                if intersection is not None:
                    if i not in intersectionPoints:
                        intersectionPoints[i] = []
                    intersectionPoints[i].append([j, intersection])
                    if j not in intersectionPoints:
                        intersectionPoints[j] = []
                    intersectionPoints[j].append([i, intersection])
            # print(f"{pi0} -> {pi1}      {points.GetPoint(pi0)} => {points.GetPoint(pi1)}")
        return intersectionPoints

    def Correct(self, intersectionPoints):
        created = {}
        pointIndices = {}
        points = self.contour.GetPoints()
        lines = self.contour.GetLines()

        for i in intersectionPoints.keys():
            # print(f'{i} : {intersectionPoints[i]}')
            for j, position in intersectionPoints[i]:
                if (i, j) not in created:
                    index = points.InsertNextPoint(position[0], position[1], SlicingPlaneZPosition)
                    created[(i, j)] = index
                    created[(j, i)] = index

                    if i not in pointIndices:
                        pointIndices[i] = []
                    pointIndices[i].append(index)
                    lineI = self.contour.GetCell(i)
                    ipi0 = lineI.GetPointId(0)
                    ipi1 = lineI.GetPointId(1)
                    pointIndices[i].append(ipi0)
                    pointIndices[i].append(ipi1)

                    if j not in pointIndices:
                        pointIndices[j] = []
                    pointIndices[j].append(index)
                    lineJ = self.contour.GetCell(j)
                    jpi0 = lineJ.GetPointId(0)
                    jpi1 = lineJ.GetPointId(1)
                    pointIndices[j].append(jpi0)
                    pointIndices[j].append(jpi1)

        for k in pointIndices:
            indexList = pointIndices[k]
            toSort = []
            for index in indexList:
                p = self.contour.GetPoint(index)
                toSort.append([p[0], p[1], index])
            sorted_list = sorted(toSort, key=lambda point: (point[0], point[1], point[2]))
            
            for i in range(len(sorted_list) - 1):
                lines.InsertNextCell(2)
                lines.InsertCellPoint(sorted_list[i][2])
                lines.InsertCellPoint(sorted_list[i + 1][2])

        toDelete = set()
        for lineIndex in intersectionPoints.keys():
            if lineIndex not in toDelete:
                toDelete.add(lineIndex)
        
        # for lineIndex in toDelete:
        #     self.contour.DeleteCell(lineIndex)
        # self.contour.RemoveDeletedCells()


        newPoints = vtk.vtkPoints()
        newPoints.DeepCopy(points)

        newLines = vtk.vtkCellArray()
        lines.InitTraversal()
        index = 0
        while True:
            cell = vtk.vtkIdList()
            lines.GetNextCell(cell)
            if cell.GetNumberOfIds() == 0:
                break

            if index in toDelete:
                index += 1
                continue

            index += 1

            newLines.InsertNextCell(2)
            num_ids = cell.GetNumberOfIds()
            for id_index in range(num_ids):
                pi = cell.GetId(id_index)
                newLines.InsertCellPoint(pi)

        self.contour.SetPoints(newPoints)
        self.contour.SetLines(newLines)

if __name__ == "__main__":
    app = VTKApp()

    reader = vtk.vtkSTLReader()
    reader.SetFileName("C:/Resources/3D/STL/Maxilla.stl")
    # reader.SetFileName("C:/Resources/3D/STL/Composite.stl")
    # reader.SetFileName("C:/Resources/3D/STL/Complex.stl")
    # reader.SetFileName("C:/Resources/3D/STL/Support.stl")
    # reader.SetFileName("C:/Resources/3D/STL/Complex_Merged.stl")
    reader.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(reader.GetOutput())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # app.renderer.AddActor(actor)
    # app.renderer.ResetCamera()
    
    slicingPlane = vtk.vtkPlane()
    slicingPlane.SetOrigin(0, 0, SlicingPlaneZPosition)
    # slicingPlane.SetOrigin(0, 0, 0)
    slicingPlane.SetNormal(0, 0, 1)

    cutter = vtk.vtkCutter()
    cutter.SetInputData(reader.GetOutput())
    cutter.SetCutFunction(slicingPlane)
    cutter.Update()

    contourData = cutter.GetOutput()

    contourCorrector = ContourCorrector(app, contourData)
    intersectionPoints = contourCorrector.Check()
    contourCorrector.Correct(intersectionPoints)

    cutterMapper = vtk.vtkPolyDataMapper()
    cutterMapper.SetInputConnection(cutter.GetOutputPort())

    triangulator = vtk.vtkContourTriangulator()
    triangulator.SetInputData(contourData)
    triangulator.Update()

    triangulatorMapper = vtk.vtkDataSetMapper()
    triangulatorMapper.SetInputConnection(triangulator.GetOutputPort())
    triangulatorMapper.ScalarVisibilityOff()

    triangulatorActor = vtk.vtkActor()
    triangulatorActor.SetMapper(triangulatorMapper)
    app.renderer.AddActor(triangulatorActor)

    contourMapper = vtk.vtkPolyDataMapper()
    contourMapper.SetInputData(contourData)

    contourActor = vtk.vtkActor()
    contourActor.SetMapper(contourMapper)
    contourActor.GetProperty().SetColor(1, 1, 1)
    contourActor.GetProperty().SetLineWidth(2)
    contourActor.GetProperty().SetAmbient(1)
    contourActor.GetProperty().SetDiffuse(0)

    app.renderer.AddActor(contourActor)

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
