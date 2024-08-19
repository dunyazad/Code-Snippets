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

    slideBar = vtk.vtkSliderRepresentation2D()

    slideBar.SetMinimumValue(0.0)
    slideBar.SetMaximumValue(100.0)
    slideBar.SetTitleText("Slider2D")
    slideBar.SetEndCapLength(0.001)
    # slideBar.SetSliderLength(200)
    # slideBar.SetEndCapLength(200)

    slideBar.GetSliderProperty().SetColor(1,0,0)
    slideBar.GetTitleProperty().SetColor(1,0,0)
    slideBar.GetLabelProperty().SetColor(1,0,0)
    slideBar.GetSelectedProperty().SetColor(1,0,0)
    slideBar.GetTubeProperty().SetColor(0,1,0)
    slideBar.GetCapProperty().SetColor(1,1,0)

    slideBar.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
    slideBar.GetPoint1Coordinate().SetValue(750, -50)

    slideBar.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
    slideBar.GetPoint2Coordinate().SetValue(750, 650)

    sliderWidget = vtk.vtkSliderWidget()
    sliderWidget.SetInteractor(app.interactor)
    sliderWidget.SetRepresentation(slideBar)
    sliderWidget.SetAnimationModeToAnimate()
    sliderWidget.EnabledOn()

    def SliderCallback(obj,event):
        value = slideBar.GetValue()
        print(value)
    
    sliderWidget.AddObserver("InteractionEvent", SliderCallback)

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
