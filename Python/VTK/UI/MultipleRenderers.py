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

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(reader.GetOutput())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    app.renderer.AddActor(actor)
    app.renderer.ResetCamera()

    app.renderer.SetLayer(0)
    

    foregroundRenderer = vtk.vtkRenderer()
    app.renderWindow.AddRenderer(foregroundRenderer)
    foregroundRenderer.SetViewport(0.75, 0.75, 1, 1)
    foregroundRenderer.SetBackground(vtk.vtkNamedColors().GetColor3d("Gray"))

    foregroundRenderer.AddActor(actor)
    foregroundRenderer.SetLayer(1)

    app.renderWindow.SetNumberOfLayers(2)

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
