import vtk

class VTKApp:
    def __init__(self) -> None:
        self.onFrameCallbacks = []

        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(0.3, 0.5, 0.7)

        self.renderWindow = vtk.vtkRenderWindow()
        self.renderWindow.SetSize(800, 600)
        self.renderWindow.AddRenderer(self.renderer)

        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.renderWindow)
        self.interactorStyle = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(self.interactorStyle)
        self.interactor.Initialize()

        self.interactor.AddObserver('TimerEvent', self.timerEventCallback)
        self.interactor.CreateRepeatingTimer(16)

        self.framecount = 0

    def timerEventCallback(self, obj, event):
        self.framecount += 1
        for callback in self.onFrameCallbacks:
            callback(obj, event, self.framecount)

    def Run(self):
        self.renderWindow.Render()
        self.interactor.Start()