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

    # reader = vtk.vtkSTLReader()
    # reader.SetFileName("C:/Resources/3D/STL/rabbit.stl")
    # reader.Update()

    # polyData = reader.GetOutput()

    # mapper = vtk.vtkPolyDataMapper()
    # mapper.SetInputData(polyData)

    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)

    # actor = vtk.vtkActor()
    # actor.SetMapper(mapper)

    # app.renderer.AddActor(actor)
    # app.renderer.ResetCamera()
    

    sphere_source = vtk.vtkSphereSource()
    sphere_source.SetPhiResolution(20)
    sphere_source.SetThetaResolution(20)
    sphere_source.Update()

    bounds = list(sphere_source.GetOutput().GetBounds())
    for i in range(0, 6, 2):
        dist = bounds[i + 1] - bounds[i]
        bounds[i] = bounds[i] - 0.1 * dist
        bounds[i + 1] = bounds[i + 1] + 0.1 * dist
    voxel_modeller = vtk.vtkVoxelModeller()
    voxel_modeller.SetSampleDimensions(50, 50, 50)
    voxel_modeller.SetModelBounds(bounds)
    voxel_modeller.SetScalarTypeToFloat()
    voxel_modeller.SetMaximumDistance(0.1)

    voxel_modeller.SetInputConnection(sphere_source.GetOutputPort())
    voxel_modeller.Update()
    iso_value = 0.5
    volume = vtk.vtkImageData()
    volume.DeepCopy(voxel_modeller.GetOutput())

    surface = vtk.vtkMarchingCubes()
    surface.SetInputData(volume)
    surface.ComputeNormalsOn()
    surface.SetValue(0, iso_value)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(surface.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('MistyRose'))

    app.renderer.AddActor(actor)

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
