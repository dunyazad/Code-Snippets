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
    # reader.SetFileName("C:/Resources/3D/STL/Composite.stl")
    reader.SetFileName("C:/Resources/3D/STL/Complex.stl")
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

    contourActor = vtk.vtkActor()
    contourActor.GetProperty().SetColor(vtk.vtkNamedColors().GetColor3d('Red'))
    contourActor.GetProperty().SetLineWidth(5)
    contourActor.GetProperty().SetAmbient(1)
    contourActor.GetProperty().SetDiffuse(0)
    contourActor.SetMapper(cutterMapper)

    cutter.Update()


    connectivityFilter = vtk.vtkPolyDataConnectivityFilter()
    connectivityFilter.SetInputData(cutter.GetOutput())
    connectivityFilter.SetExtractionModeToAllRegions()  # Extract the largest connected region
    connectivityFilter.Update()

    numRegions = connectivityFilter.GetNumberOfExtractedRegions()

    connectivityFilter.SetExtractionModeToSpecifiedRegions()
    connectivityFilter.Update()

    namedColors = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.75, 0.5, 0.25], [1.0, 1.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 1.0]]
    for regionId in range(numRegions):
        contourFilter = vtk.vtkPolyDataConnectivityFilter()
        contourFilter.SetExtractionModeToSpecifiedRegions()
        contourFilter.SetInputData(cutter.GetOutput())
        contourFilter.AddSpecifiedRegion(regionId)
        contourFilter.Update()

        regionPolyData = contourFilter.GetOutput()

        triangulator = vtk.vtkContourTriangulator()
        triangulator.SetInputData(regionPolyData)
        triangulator.Update()

        triangulatorMapper = vtk.vtkDataSetMapper()
        triangulatorMapper.SetInputConnection(triangulator.GetOutputPort())
        triangulatorMapper.ScalarVisibilityOff()

        triangulatorActor = vtk.vtkActor()
        triangulatorActor.SetMapper(triangulatorMapper)
        app.renderer.AddActor(triangulatorActor)

        contourMapper = vtk.vtkPolyDataMapper()
        contourMapper.SetInputData(regionPolyData)

        contourActor = vtk.vtkActor()
        contourActor.SetMapper(contourMapper)
        contourActor.GetProperty().SetLineWidth(5)
        contourActor.GetProperty().SetAmbient(1)
        contourActor.GetProperty().SetDiffuse(0)

        index = regionId
        if index >= len(namedColors):
            index = index - len(namedColors)
        contourActor.GetProperty().SetColor(namedColors[index])
        triangulatorActor.GetProperty().SetColor(namedColors[index])
        
        app.renderer.AddActor(contourActor)

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
