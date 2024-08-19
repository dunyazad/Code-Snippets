import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import math
import vtk
from VTKApp import VTKApp

if __name__ == "__main__":
    app = VTKApp()

    colors = vtk.vtkNamedColors()

    reader = vtk.vtkSTLReader()
    # reader.SetFileName("C:/Resources/3D/STL/rabbit.stl")
    reader.SetFileName("C:/Resources/3D/STL/maxilla.stl")
    reader.Update()

    polyData = reader.GetOutput()

    numberOfPolys = polyData.GetNumberOfCells()
    lineLength = 0
    for i in range(numberOfPolys):
        cell = polyData.GetCell(i)
        pi0 = cell.GetPointId(0)
        pi1 = cell.GetPointId(1)
        pi2 = cell.GetPointId(2)

        p0 = polyData.GetPoint(pi0)
        p1 = polyData.GetPoint(pi1)
        p2 = polyData.GetPoint(pi2)

        ll0 = math.sqrt(vtk.vtkMath.Distance2BetweenPoints(p0, p1))
        ll1 = math.sqrt(vtk.vtkMath.Distance2BetweenPoints(p1, p2))
        ll2 = math.sqrt(vtk.vtkMath.Distance2BetweenPoints(p2, p0))

        if lineLength < ll0:
            lineLength = ll0
        if lineLength < ll1:
            lineLength = ll1
        if lineLength < ll2:
            lineLength = ll2

    lineLength /= 2

    print(f"Longest Edge length is {lineLength}")

    subdivisionFilter = vtk.vtkAdaptiveSubdivisionFilter()
    subdivisionFilter.SetInputData(polyData)
    subdivisionFilter.SetMaximumEdgeLength(lineLength)
    subdivisionFilter.Update()

    subdividedPolyData = subdivisionFilter.GetOutput()
    bounds = subdividedPolyData.GetBounds()
    xlength = bounds[1] - bounds[0]
    ylength = bounds[3] - bounds[2]
    zlength = bounds[5] - bounds[4]

    xResolution = math.ceil(xlength / lineLength)
    yResolution = math.ceil(ylength / lineLength)
    zResolution = math.ceil(zlength / lineLength)

    structuredGrid = vtk.vtkStructuredGrid()

    # points = subdividedPolyData.GetPoints()
    points = vtk.vtkPoints()
    points.InsertNextPoint(0, 0, -0.5)
    # for i in range(subdividedPolyData.GetNumberOfPoints()):
    #     points.InsertNextPoint(subdividedPolyData.GetPoint(i))

    # structuredGrid.SetDimensions(xResolution, yResolution, zResolution)
    # structuredGrid.SetPoints(points)

    numi, numj, numk = 3, 4, 5

    for k in range(numk):
        for j in range(numj):
            for i in range(numi):
                points.InsertNextPoint(i, j, k)

    structuredGrid.SetDimensions(numi, numj, numk)
    structuredGrid.SetPoints(points)

    # print(f"There are {structuredGrid.GetNumberOfPoints()} points before shrinking.")
    # print(f"There are {structuredGrid.GetNumberOfCells()} cells before shrinking.")

    # shrinkFilter = vtk.vtkShrinkFilter()
    # shrinkFilter.SetInputData(structuredGrid)
    # shrinkFilter.SetShrinkFactor(0.8)
    # shrinkFilter.Update()

    # print(f"There are {shrinkFilter.GetOutput().GetNumberOfPoints()} points after shrinking.")
    # print(f"There are {shrinkFilter.GetOutput().GetNumberOfCells()} cells after shrinking.")

    mapper = vtk.vtkDataSetMapper()
    # mapper.SetInputConnection(shrinkFilter.GetOutputPort())
    mapper.SetInputData(structuredGrid)

    # mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInputData(subdividedPolyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    # actor.GetProperty().SetColor(colors.GetColor3d("MistyRose"))

    app.renderer.AddActor(actor)


    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
