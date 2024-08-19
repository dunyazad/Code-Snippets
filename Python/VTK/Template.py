import vtk

from VTKApp import VTKApp

if __name__ == "__main__":
    app = VTKApp()

    def onFrame(obj, event, frameCount):
        pass
    app.onFrameCallbacks.append(onFrame)

    app.Run()