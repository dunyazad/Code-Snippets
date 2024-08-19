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
    reader.SetFileName("C:/Resources/3D/STL/Complex.stl")
    reader.Update()

    connected_filter = vtk.vtkConnectivityFilter()
    connected_filter.SetInputConnection(reader.GetOutputPort())
    connected_filter.SetExtractionModeToAllRegions()
    connected_filter.ColorRegionsOn()
    connected_filter.Update()

    num_regions = connected_filter.GetNumberOfExtractedRegions()

    colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1]]

    for region_id in range(num_regions):
        region_extractor = vtk.vtkThreshold()
        region_extractor.SetInputConnection(connected_filter.GetOutputPort())
        region_extractor.ThresholdBetween(region_id, region_id)
        region_extractor.Update()

        # Mapper and actor for the current mesh
        # mapper = vtk.vtkPolyDataMapper()
        # mapper.SetInputConnection(region_extractor.GetOutputPort())

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(region_extractor.GetOutput())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        # actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Set mesh color (red)

        actor.GetProperty().SetColor(colors[region_id])
        print(colors[region_id])

        # Add the actor to the renderer
        app.renderer.AddActor(actor)

    # mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInputData(reader.GetOutput())

    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)

    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)

    # app.renderer.AddActor(actor)
    # app.renderer.ResetCamera()
    

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
