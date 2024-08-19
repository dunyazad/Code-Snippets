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
    reader.SetFileName("C:/Resources/3D/STL/rabbit.stl")
    reader.Update()

    polyData = reader.GetOutput()

    numberOfPolys = polyData.GetNumberOfCells()
    lineLength = 0
    for i in range(numberOfPolys):
        cell = polyData.GetCell(i)
        pi0 = cell.GetPointId(0)
        pi1 = cell.GetPointId(1)
        pi2 = cell.GetPointId(2)

        p0 = polyData.GetPoint(pi0)
        p1 = polyData.GetPoint(pi1)
        p2 = polyData.GetPoint(pi2)

        ll0 = math.sqrt(vtk.vtkMath.Distance2BetweenPoints(p0, p1))
        ll1 = math.sqrt(vtk.vtkMath.Distance2BetweenPoints(p1, p2))
        ll2 = math.sqrt(vtk.vtkMath.Distance2BetweenPoints(p2, p0))

        if lineLength < ll0:
            lineLength = ll0
        if lineLength < ll1:
            lineLength = ll1
        if lineLength < ll2:
            lineLength = ll2

    print(f"Longest Edge length is {lineLength}")

    subdivisionFilter = vtk.vtkAdaptiveSubdivisionFilter()
    subdivisionFilter.SetInputData(polyData)
    subdivisionFilter.SetMaximumEdgeLength(lineLength)
    subdivisionFilter.Update()

    octree = vtk.vtkOctreePointLocator()
    octree.SetMaximumPointsPerRegion(1)
    octree.SetDataSet(subdivisionFilter.GetOutput())
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
    # octreeActor.GetProperty().SetColor(colors.GetColor3d("White"))

    app.renderer.AddActor(octreeActor)

    modelMapper = vtk.vtkPolyDataMapper()
    modelMapper.SetInputConnection(subdivisionFilter.GetOutputPort())

    modelActor = vtk.vtkActor()
    modelActor.SetMapper(modelMapper)
    modelActor.GetProperty().SetInterpolationToFlat()
    modelActor.GetProperty().SetRepresentationToPoints()
    modelActor.GetProperty().SetPointSize(5)
    modelActor.GetProperty().SetColor(colors.GetColor3d("Yellow"))

    app.renderer.AddActor(modelActor)
    app.renderer.ResetCamera()

    sliderRep = vtk.vtkSliderRepresentation2D()
    sliderRep.SetMinimumValue(0)
    sliderRep.SetMaximumValue(octree.GetMaxLevel())
    
    # numSteps = 20  # Set the desired number of steps
    numSteps = octree.GetMaxLevel()
    stepSize = (sliderRep.GetMaximumValue() - sliderRep.GetMinimumValue()) / numSteps
    sliderRep.SetSliderWidth(0.1 * stepSize)
    
    sliderRep.SetValue(0)
    sliderRep.SetTitleText("Level")
    sliderRep.SetSliderLength(0.075)
    sliderRep.SetSliderWidth(0.05)
    sliderRep.SetEndCapLength(0.05)
    sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep.GetPoint1Coordinate().SetValue(0.2, 0.1)
    sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    sliderRep.GetPoint2Coordinate().SetValue(0.8, 0.1)
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
