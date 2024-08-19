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

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(reader.GetOutput())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    app.renderer.AddActor(actor)
    app.renderer.ResetCamera()
    

    axes_actor = vtk.vtkAnnotatedCubeActor()
    axes_actor.SetXPlusFaceText('Right')
    axes_actor.SetXMinusFaceText('Left')
    axes_actor.SetYMinusFaceText('Front')
    axes_actor.SetYPlusFaceText('Rear')
    axes_actor.SetZMinusFaceText('Bottom')
    axes_actor.SetZPlusFaceText('Top')
    axes_actor.GetTextEdgesProperty().SetColor(colors.GetColor3d("Yellow"))
    axes_actor.GetTextEdgesProperty().SetLineWidth(2)
    axes_actor.GetCubeProperty().SetColor(colors.GetColor3d("Blue"))
    axes_actor.SetFaceTextScale(0.17)
    axes = vtk.vtkOrientationMarkerWidget()
    axes.SetOrientationMarker(axes_actor)
    axes.SetInteractor(app.interactor)
    axes.EnabledOn()
    axes.InteractiveOn()



    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
