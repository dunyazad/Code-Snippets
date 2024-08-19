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

    modelMapper = vtk.vtkPolyDataMapper()
    modelMapper.SetInputConnection(reader.GetOutputPort())

    modelActor = vtk.vtkActor()
    modelActor.SetMapper(modelMapper)
    modelActor.GetProperty().SetInterpolationToFlat()
    modelActor.GetProperty().SetRepresentationToPoints()
    modelActor.GetProperty().SetColor(colors.GetColor3d("Yellow"))

    app.renderer.AddActor(modelActor)

    octree = vtk.vtkOctreePointLocator()
    octree.SetMaximumPointsPerRegion(5)
    octree.SetDataSet(reader.GetOutput())
    octree.BuildLocator()

    octreePolyData = vtk.vtkPolyData()
    octree.GenerateRepresentation(0, octreePolyData)

    octreeMapper = vtk.vtkPolyDataMapper()
    octreeMapper.SetInputData(octreePolyData)

    octreeActor = vtk.vtkActor()
    octreeActor.SetMapper(octreeMapper)
    octreeActor.GetProperty().SetInterpolationToFlat()
    octreeActor.GetProperty().SetRepresentationToWireframe()
    octreeActor.GetProperty().SetColor(colors.GetColor3d("SpringGreen"))

    app.renderer.AddActor(octreeActor)
    app.renderer.ResetCamera()

    sliderRep = vtk.vtkSliderRepresentation2D()
    sliderRep.SetMinimumValue(0)
    sliderRep.SetMaximumValue(octree.GetMaxLevel())
    
    numSteps = 20  # Set the desired number of steps
    stepSize = (sliderRep.GetMaximumValue() - sliderRep.GetMinimumValue()) / numSteps
    sliderRep.SetSliderWidth(0.1 * stepSize)
    
    sliderRep.SetValue(0)
    sliderRep.SetTitleText("Level")
    sliderRep.SetSliderLength(0.075)
    sliderRep.SetSliderWidth(0.05)
    sliderRep.SetEndCapLength(0.05)
    sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep.GetPoint1Coordinate().SetValue(0.2, 0.2)
    sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep.GetPoint2Coordinate().SetValue(0.8, 0.2)
    sliderRep.GetTitleProperty().SetColor(colors.GetColor3d("Beige"))
    sliderRep.GetCapProperty().SetColor(colors.GetColor3d("MistyRose"))
    sliderRep.GetSliderProperty().SetColor(colors.GetColor3d("Red"))
    sliderRep.GetSelectedProperty().SetColor(colors.GetColor3d("Violet"))

    sliderWidget = vtk.vtkSliderWidget()
    sliderWidget.SetInteractor(app.interactor)
    sliderWidget.SetRepresentation(sliderRep)
    sliderWidget.SetAnimationModeToAnimate()
    sliderWidget.EnabledOn()

    class SliderObserver(object):
        def __init__(self, octree, polyData, renderer) -> None:
            self.octree = octree
            self.level = 0
            self.polyData = polyData
            self.renderer = renderer
        
        def __call__(self, caller, event):
            self.level = vtk.vtkMath.Round(caller.GetRepresentation().GetValue())
            self.octree.GenerateRepresentation(self.level, self.polyData)
            self.renderer.Render()
            
    callback = SliderObserver(octree, octreePolyData, app.renderer)
    sliderWidget.AddObserver("InteractionEvent", callback)

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
