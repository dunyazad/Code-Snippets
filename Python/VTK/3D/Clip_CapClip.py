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
    backgroundColor = colors.GetColor3d("steel_blue")
    boundaryColor = colors.GetColor3d("banana")
    clipColor = colors.GetColor3d("tomato")

    reader = vtk.vtkSTLReader()
    reader.SetFileName("C:/Resources/3D/STL/rabbit.stl")
    reader.Update()

    polyData = reader.GetOutput()

    plane = vtk.vtkPlane()
    plane.SetOrigin(polyData.GetCenter())
    plane.SetNormal(1.0, -1.0, -1.0)

    clipper = vtk.vtkClipPolyData()
    clipper.SetInputData(polyData)
    clipper.SetClipFunction(plane)
    clipper.SetValue(0)
    clipper.Update()

    polyData = clipper.GetOutput()

    clipMapper = vtk.vtkDataSetMapper()
    clipMapper.SetInputData(polyData)

    clipActor = vtk.vtkActor()
    clipActor.SetMapper(clipMapper)
    clipActor.GetProperty().SetDiffuseColor(clipColor)
    clipActor.GetProperty().SetInterpolationToFlat()
    clipActor.GetProperty().EdgeVisibilityOn()

    # Now extract feature edges
    boundaryEdges = vtk.vtkFeatureEdges()
    boundaryEdges.SetInputData(polyData)
    boundaryEdges.BoundaryEdgesOn()
    boundaryEdges.FeatureEdgesOff()
    boundaryEdges.NonManifoldEdgesOff()
    boundaryEdges.ManifoldEdgesOff()

    boundaryStrips = vtk.vtkStripper()
    boundaryStrips.SetInputConnection(boundaryEdges.GetOutputPort())
    boundaryStrips.Update()

    # Change the polylines into polygons
    boundaryPoly = vtk.vtkPolyData()
    boundaryPoly.SetPoints(boundaryStrips.GetOutput().GetPoints())
    boundaryPoly.SetPolys(boundaryStrips.GetOutput().GetLines())

    boundaryMapper = vtk.vtkPolyDataMapper()
    boundaryMapper.SetInputData(boundaryPoly)

    boundaryActor = vtk.vtkActor()
    boundaryActor.SetMapper(boundaryMapper)
    boundaryActor.GetProperty().SetDiffuseColor(boundaryColor)

    app.renderer.AddActor(clipActor)
    app.renderer.AddActor(boundaryActor)

    app.renderer.SetBackground(backgroundColor)
    app.renderer.ResetCamera()
    app.renderer.GetActiveCamera().Azimuth(30)
    app.renderer.GetActiveCamera().Elevation(30)
    app.renderer.GetActiveCamera().Dolly(1.2)
    app.renderer.ResetCameraClippingRange()

    

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
