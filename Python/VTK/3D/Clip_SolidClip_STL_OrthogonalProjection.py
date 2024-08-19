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

    colors = vtk.vtkNamedColors()

    reader = vtk.vtkSTLReader()
    # reader.SetFileName("C:/Resources/3D/STL/rabbit.stl")
    reader.SetFileName("C:/Resources/3D/STL/Complex.stl")
    # reader.SetFileName("C:/Resources/3D/STL/CubeWIthHoles.stl")
    reader.Update()

    # Define a clipping plane
    clip_plane = vtk.vtkPlane()
    clip_plane.SetNormal(0.0, 0.0, 1.0)
    clip_plane.SetOrigin(0.0, 0.0, 0.0)

    # Clip the source with the plane
    clipper = vtk.vtkClipPolyData()
    clipper.SetInputConnection(reader.GetOutputPort())
    clipper.SetClipFunction(clip_plane)
    # This will give us the polygonal data that is clipped away
    clipper.GenerateClippedOutputOn()

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(clipper.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Black"))
    actor.GetProperty().SetDiffuse(0)
    actor.GetProperty().SetAmbient(1)

    # Create a property to be used for the back faces. Turn off all
    # shading by specifying 0 weights for specular and diffuse. Max the
    # ambient.
    back_faces = vtk.vtkProperty()
    back_faces.SetSpecular(0.0)
    back_faces.SetDiffuse(0.0)
    back_faces.SetAmbient(1.0)
    back_faces.SetAmbientColor(colors.GetColor3d('White'))

    actor.SetBackfaceProperty(back_faces)

    # Here we get the the polygonal data that is clipped away
    clipped_away_mapper = vtk.vtkPolyDataMapper()
    clipped_away_mapper.SetInputData(clipper.GetClippedOutput())
    clipped_away_mapper.ScalarVisibilityOff()

    # Let us display it as a faint object
    clipped_away_actor = vtk.vtkActor()
    clipped_away_actor.SetMapper(clipped_away_mapper)
    clipped_away_actor.GetProperty().SetDiffuseColor(colors.GetColor3d("Silver"))
    clipped_away_actor.GetProperty().SetOpacity(0.1)

    app.renderer.AddActor(actor)
    app.renderer.AddActor(clipped_away_actor)

    app.renderer.SetBackground(0, 0, 0)
    app.renderer.GetActiveCamera().Elevation(180)
    app.renderer.GetActiveCamera().ParallelProjectionOn()


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
    slideBar.GetPoint1Coordinate().SetValue(50, -50)

    slideBar.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
    slideBar.GetPoint2Coordinate().SetValue(50, 650)

    sliderWidget = vtk.vtkSliderWidget()
    sliderWidget.SetInteractor(app.interactor)
    sliderWidget.SetRepresentation(slideBar)
    sliderWidget.SetAnimationModeToAnimate()
    sliderWidget.EnabledOn()

    bounds = actor.GetBounds()
    height = bounds[5] - bounds[4]
    center = (bounds[4] + bounds[5]) * 0.5

    def SliderCallback(obj,event):
        global center, height

        value = slideBar.GetValue()
        z = height * value * 0.01
        print(z)
        clip_plane.SetOrigin(0.0, 0.0, z)
        clip_plane.Modified()

        clipper.Update()
        mapper.Update()
        # app.renderer.ResetCamera()
        app.renderer.Render()
        app.renderWindow.Render()
    
    sliderWidget.AddObserver("InteractionEvent", SliderCallback)

    boxWidget = vtk.vtkBoxWidget()
    boxWidget.SetInteractor(app.interactor)
    boxWidget.SetProp3D(actor)
    boxWidget.SetPlaceFactor(1.25)  # Make the box 1.25x larger than the actor
    boxWidget.PlaceWidget()
    boxWidget.On()

    def boxCallback(obj, event):
        t = vtk.vtkTransform()
        obj.GetTransform(t)
        obj.GetProp3D().SetUserTransform(t)

    boxWidget.AddObserver('InteractionEvent', boxCallback)



    # center = actor.GetCenter()[2]
    # def onFrame(obj, event, framecount):
    #     global center
    #     bounds = actor.GetBounds()
    #     height = bounds[5] - bounds[4]
        
    #     ratio = (framecount % 100) * 0.005
    #     z = height * ratio - center

    #     clip_plane.SetOrigin(0.0, 0.0, z)
    #     clip_plane.Modified()

    #     clipper.Update()
    #     mapper.Update()
    #     # app.renderer.ResetCamera()
    #     app.renderer.Render()
    #     app.renderWindow.Render()


    # app.onFrameCallbacks.append(onFrame)

    app.Run()
