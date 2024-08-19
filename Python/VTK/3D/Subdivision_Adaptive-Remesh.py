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

    reader = vtk.vtkSTLReader()
    # reader.SetFileName("C:/Resources/3D/STL/rabbit.stl")
    reader.SetFileName("C:/Resources/3D/STL/maxilla.stl")
    reader.Update()

    polyData = reader.GetOutput()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # app.renderer.AddActor(actor)
    app.renderer.ResetCamera()
    
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

    print(f"Longest Edge length is {lineLength}")

    subdivisionFilter = vtk.vtkAdaptiveSubdivisionFilter()
    subdivisionFilter.SetInputData(polyData)
    subdivisionFilter.SetMaximumEdgeLength(lineLength * 1.1)
    subdivisionFilter.Update()

    polyDataNormals = vtk.vtkPolyDataNormals()
    polyDataNormals.SetInputConnection(subdivisionFilter.GetOutputPort())
    polyDataNormals.ComputeCellNormalsOn()
    polyDataNormals.Update()
    
    subdivisionPolyDataMapper = vtk.vtkPolyDataMapper()
    subdivisionPolyDataMapper.SetInputConnection(polyDataNormals.GetOutputPort())

    subdivisionActor = vtk.vtkActor()
    subdivisionActor.SetMapper(subdivisionPolyDataMapper)

    app.renderer.AddActor(subdivisionActor)
    app.renderer.ResetCamera()
    
    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
