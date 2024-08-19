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

    vertex = vtk.vtkVertex()
    vertices = vtk.vtkCellArray()
    for i in range(points.GetNumberOfPoints()):
        vertex.GetPointIds().SetId(0, i)
        vertices.InsertNextCell(vertex)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetVerts(vertices)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1, 0, 0)
    actor.GetProperty().SetPointSize(5)
    actor.GetProperty().SetAmbient(1)
    actor.GetProperty().SetDiffuse(0)

    app.renderer.AddActor(actor)
    app.renderer.ResetCamera()
    

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
