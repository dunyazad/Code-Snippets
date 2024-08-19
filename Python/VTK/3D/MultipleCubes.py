import os
import sys
import time
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import vtk
from VTKApp import VTKApp

if __name__ == "__main__":
    app = VTKApp()

    cubeSource = vtk.vtkCubeSource()
    cubeSource.SetXLength(1)
    cubeSource.SetYLength(1)
    cubeSource.SetZLength(1)

    cubeMapper = vtk.vtkPolyDataMapper()
    cubeMapper.SetInputConnection(cubeSource.GetOutputPort())

    cubes = vtk.vtkAssembly()

    arr = []

    last = time.time()
    for z in range(1000):
        arry = []
        for y in range(1000):
            arrx = []
            for x in range(1000):
                arrx.append(x)
            arry.append(arrx)
        arr.append(arry)

    now = time.time()
    print(f"delta : {now - last}")

    # def onFrame(obj, event):
    #     pass
    # app.onFrameCallbacks.append(onFrame)

    app.Run()
