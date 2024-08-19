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



    
    annotated_cube_actor = vtk.vtkAnnotatedCubeActor()
    annotated_cube_actor.SetXPlusFaceText('Right')
    annotated_cube_actor.SetXMinusFaceText('Left')
    annotated_cube_actor.SetYMinusFaceText('Front')
    annotated_cube_actor.SetYPlusFaceText('Rear')
    annotated_cube_actor.SetZMinusFaceText('Bottom')
    annotated_cube_actor.SetZPlusFaceText('Top')
    annotated_cube_actor.GetTextEdgesProperty().SetColor(colors.GetColor3d("Yellow"))
    annotated_cube_actor.GetTextEdgesProperty().SetLineWidth(2)
    annotated_cube_actor.GetCubeProperty().SetColor(colors.GetColor3d("Blue"))
    annotated_cube_actor.SetFaceTextScale(0.17)
    annotated_cube_actor.PickableOn()
    orientationMarker = vtk.vtkOrientationMarkerWidget()
    orientationMarker.SetOrientationMarker(annotated_cube_actor)
    orientationMarker.SetInteractor(app.interactor)
    orientationMarker.EnabledOn()
    orientationMarker.InteractiveOff()
    orientationMarker.SetViewport(0.8, 0.8, 1, 1)

    annotated_cube_actor.PickableOn()



    class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
        def __init__(self, renderWindow, renderer, interactor) -> None:
            super().__init__()

            self.renderWindow = renderWindow
            self.renderer = renderer
            self.interactor = interactor

            self.AddObserver("LeftButtonReleaseEvent", self.left_button_release_event)

        def left_button_release_event(self, obj, event):
            pos = self.interactor.GetEventPosition()
            print(pos)

            picker = vtk.vtkCellPicker()
            # picker.PickFromListOn()
            picker.SetTolerance(0.001)

            # picker.AddPickList(annotated_cube_actor)

            picker.Pick(pos[0], pos[1], 0, self.renderer)
            pickedPosition = picker.GetPickPosition()

            if picker.GetActor() is not None:
                print(f'Pick position is: ({pickedPosition[0]:.6g}, {pickedPosition[1]:.6g}, {pickedPosition[2]:.6g})')

            self.OnLeftButtonUp()

        def on_pick(self, obj, event):
            # Get the picked position
            picker = obj.GetPicker()
            x, y, z = picker.GetPickPosition()

            # Perform actions based on the picked position
            # For example, print the coordinates
            print("Picked position: ({}, {}, {})".format(x, y, z))

    customInteractorStyle = CustomInteractorStyle(app.renderWindow, app.renderer, app.interactor)
    app.interactor.SetInteractorStyle(customInteractorStyle)

    # def onLeftButtonPressEvent(obj, event):
    #     print("LeftButtonPressEvent")

    # app.interactor.AddObserver("LeftButtonPressEvent", onLeftButtonPressEvent)

    picker = vtk.vtkPropPicker()
    app.interactor.SetPicker(picker)

    def on_pick(obj, event):
        # Get the picked position
        picker = obj.GetPicker()
        x, y, z = picker.GetPickPosition()

        # Perform actions based on the picked position
        # For example, print the coordinates
        print("Picked position: ({}, {}, {})".format(x, y, z))

    # Connect the pick event to the callback function
    app.interactor.AddObserver(vtk.vtkCommand.PickEvent, on_pick)




    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
