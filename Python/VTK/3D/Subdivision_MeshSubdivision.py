import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import vtk
from VTKApp import VTKApp

if __name__ == "__main__":
    app = VTKApp()

    app.renderWindow.RemoveRenderer(app.renderer)
    app.renderer = None

    reader = vtk.vtkSTLReader()
    reader.SetFileName("C:/Resources/3D/STL/rabbit.stl")
    reader.Update()

    polyData = reader.GetOutput()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    print(f"Before subdivision\n\tThere are {polyData.GetNumberOfPoints()} points.")
    print(f"\tThere are {polyData.GetNumberOfPolys()} triangles.")

    # app.renderer.AddActor(actor)
    # app.renderer.ResetCamera()
    
    numberOfViewports = 3.0
    app.renderWindow.SetSize(int(200 * numberOfViewports), int(200))
    app.renderWindow.SetWindowName("Subdivisions")

    numberOfSubdivisions = 3
    renderers = []
    colors = ["Gainsboro", "LightGrey", "Silver"]
    for i in range(numberOfSubdivisions):
        subdvisionFilter = None
        if i % 3 == 0:
            subdvisionFilter = vtk.vtkLinearSubdivisionFilter()
            subdvisionFilter.SetNumberOfSubdivisions(numberOfSubdivisions)
            subdvisionFilter.SetInputData(polyData)
            subdvisionFilter.Update()
        elif i % 3 == 1:
            subdvisionFilter = vtk.vtkLoopSubdivisionFilter()
            subdvisionFilter.SetNumberOfSubdivisions(numberOfSubdivisions)
            subdvisionFilter.SetInputData(polyData)
            subdvisionFilter.Update()
        elif i % 3 == 2:
            subdvisionFilter = vtk.vtkButterflySubdivisionFilter()
            subdvisionFilter.SetNumberOfSubdivisions(numberOfSubdivisions)
            subdvisionFilter.SetInputData(polyData)
            subdvisionFilter.Update()
    
        renderer = vtk.vtkRenderer()
        renderer.SetViewport(i / numberOfViewports, 0, (i + 1) / numberOfViewports, 1)
        renderers.append(renderer)

        subdivisionPolyDataMapper = vtk.vtkPolyDataMapper()
        subdivisionPolyDataMapper.SetInputConnection(subdvisionFilter.GetOutputPort())

        subdivisionActor = vtk.vtkActor()
        subdivisionActor.SetMapper(subdivisionPolyDataMapper)
        if i % 3 == 1:
            subdivisionActor.GetProperty().SetColor(vtk.vtkNamedColors().GetColor3d("Yellow"))
        else:
            subdivisionActor.GetProperty().SetColor(vtk.vtkNamedColors().GetColor3d("BurlyWood"))

        renderer.AddActor(subdivisionActor)
        renderer.SetBackground(vtk.vtkNamedColors().GetColor3d(colors[i]))
        renderer.ResetCamera()

        app.renderWindow.AddRenderer(renderer)

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
