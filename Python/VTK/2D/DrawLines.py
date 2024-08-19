import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import vtk
from VTKApp import VTKApp

if __name__ == "__main__":
    app = VTKApp()

    points = vtk.vtkPoints()
    points.InsertNextPoint([0, 0, 0])
    points.InsertNextPoint([10, 0, 0])
    points.InsertNextPoint([20, 0, 0])
    points.InsertNextPoint([30, 10, 0])

    polyLine = vtk.vtkPolyLine()
    polyLine.GetPointIds().SetNumberOfIds(points.GetNumberOfPoints())
    for i in range(0, points.GetNumberOfPoints()):
        polyLine.GetPointIds().SetId(i, i)

    cells = vtk.vtkCellArray()
    cells.InsertNextCell(polyLine)
   
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(cells)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 0, 0)
    actor.GetProperty().SetLineWidth(5)
    actor.GetProperty().SetAmbient(1)
    actor.GetProperty().SetDiffuse(0)

    app.renderer.AddActor(actor)
    app.renderer.ResetCamera()
    

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
