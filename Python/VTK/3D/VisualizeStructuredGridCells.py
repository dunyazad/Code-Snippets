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

    structuredGrid = vtk.vtkStructuredGrid()

    points = vtk.vtkPoints()
    numi, numj, numk = 3, 4, 5

    for k in range(numk):
        for j in range(numj):
            for i in range(numi):
                points.InsertNextPoint(i, j, k)

    structuredGrid.SetDimensions(i, j, k)
    structuredGrid.SetPoints(points)

    print(f"There are {structuredGrid.GetNumberOfPoints()} points before shrinking.")
    print(f"There are {structuredGrid.GetNumberOfCells()} cells before shrinking.")

    shrinkFilter = vtk.vtkShrinkFilter()
    shrinkFilter.SetInputData(structuredGrid)
    shrinkFilter.SetShrinkFactor(0.8)
    shrinkFilter.Update()

    print(f"There are {shrinkFilter.GetOutput().GetNumberOfPoints()} points after shrinking.")
    print(f"There are {shrinkFilter.GetOutput().GetNumberOfCells()} cells after shrinking.")

    mapper = vtk.vtkDataSetMapper()
    # mapper.SetInputConnection(shrinkFilter.GetOutputPort())
    mapper.SetInputData(structuredGrid)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("MistyRose"))

    app.renderer.AddActor(actor)


    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
