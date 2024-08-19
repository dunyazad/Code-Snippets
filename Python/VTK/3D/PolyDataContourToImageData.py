import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import vtk
from VTKApp import VTKApp

if __name__ == "__main__":
    app = VTKApp()

    reader = vtk.vtkSTLReader()
    reader.SetFileName("C:/Resources/3D/STL/rabbit.stl")
    reader.Update()

    polyData = reader.GetOutput()

    polyDataCutter = vtk.vtkCutter()
    polyDataCutter.SetInput(polyData)
    cutPlane = vtk.vtkPlane()
    cutPlane.SetOrigin(polyData.GetCenter())
    cutPlane.SetNormal(0, 0, 1)
    polyDataCutter.SetCutFunction(cutPlane)

    stripper = vtk.vtkStripper()
    stripper.SetInputConnection(polyDataCutter.GetOutputPort())  # valid circle
    stripper.Update()

    circle = stripper.GetOutput()





    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    app.renderer.AddActor(actor)
    app.renderer.ResetCamera()
    

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
