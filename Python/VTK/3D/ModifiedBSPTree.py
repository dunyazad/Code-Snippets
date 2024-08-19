import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import vtk
from VTKApp import VTKApp

if __name__ == "__main__":
    app = VTKApp()

    colors = vtk.vtkNamedColors()

    reader = vtk.vtkSTLReader()
    reader.SetFileName("C:/Resources/3D/STL/rabbit.stl")
    reader.Update()

    modelMapper = vtk.vtkPolyDataMapper()
    modelMapper.SetInputConnection(reader.GetOutputPort())

    modelActor = vtk.vtkActor()
    modelActor.SetMapper(modelMapper)

    modelActor = vtk.vtkActor()
    modelActor.SetMapper(modelMapper)
    modelActor.GetProperty().SetRepresentationToWireframe()
    modelActor.GetProperty().SetColor(colors.GetColor3d("Gold"))



    mbspTree = vtk.vtkModifiedBSPTree()
    mbspTree.SetDataSet(reader.GetOutput())

    lineP0 = [-60, -60, -60 + 50]
    lineP1 = [ 60,  60,  60 + 50]

    intersectPoints = vtk.vtkPoints()
    intersectCells = vtk.vtkIdList()

    tolerance = 1.0e-8
    mbspTree.IntersectWithLine(lineP0, lineP1, tolerance, intersectPoints, intersectCells)

    print(f"NumPoints: {intersectPoints.GetNumberOfPoints()}")

    intersection = [0.0, 0.0, 0.0]
    for i in range(intersectCells.GetNumberOfIds()):
        cellId = intersectCells.GetId(i)
        print(f"\tCellId {i} : {cellId}")


    lineSource = vtk.vtkLineSource()
    lineSource.SetPoint1(lineP0)
    lineSource.SetPoint2(lineP1)

    lineMapper = vtk.vtkPolyDataMapper()
    lineMapper.SetInputConnection(lineSource.GetOutputPort())

    lineActor = vtk.vtkActor()
    lineActor.SetMapper(lineMapper)

    cellSource = vtk.vtkExtractCells()
    cellSource.SetInputConnection(reader.GetOutputPort())
    cellSource.SetCellList(intersectCells)

    cellMapper = vtk.vtkDataSetMapper()
    cellMapper.SetInputConnection(cellSource.GetOutputPort())

    cellActor = vtk.vtkActor()
    cellActor.SetMapper(cellMapper)
    cellActor.GetProperty().SetColor(colors.GetColor3d("Tomato"))

    app.renderer.AddActor(modelActor)
    app.renderer.AddActor(lineActor)
    app.renderer.AddActor(cellActor)
    app.renderer.ResetCamera()
    

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
