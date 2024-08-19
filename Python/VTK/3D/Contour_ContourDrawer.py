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
    reader.SetFileName("C:/Resources/3D/STL/Composite.stl")
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
    slicingPlane.SetOrigin(0, 0, 0)
    slicingPlane.SetNormal(0, 0, 1)

    cutter = vtk.vtkCutter()
    cutter.SetInputData(reader.GetOutput())
    cutter.SetCutFunction(slicingPlane)
    cutter.Update()

    cutterMapper = vtk.vtkPolyDataMapper()
    cutterMapper.SetInputConnection(cutter.GetOutputPort())

    triangulator = vtk.vtkContourTriangulator()
    triangulator.SetInputConnection(cutter.GetOutputPort())
    triangulator.Update()

    triangulatorMapper = vtk.vtkDataSetMapper()
    triangulatorMapper.SetInputConnection(triangulator.GetOutputPort())
    triangulatorMapper.ScalarVisibilityOff()

    triangulatorActor = vtk.vtkActor()
    triangulatorActor.SetMapper(triangulatorMapper)
    app.renderer.AddActor(triangulatorActor)

    contourMapper = vtk.vtkPolyDataMapper()
    contourMapper.SetInputConnection(cutter.GetOutputPort())

    contourActor = vtk.vtkActor()
    contourActor.SetMapper(contourMapper)
    contourActor.GetProperty().SetColor(1, 0, 0)
    contourActor.GetProperty().SetLineWidth(5)
    contourActor.GetProperty().SetAmbient(1)
    contourActor.GetProperty().SetDiffuse(0)

    app.renderer.AddActor(contourActor)

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
