if __name__ == "__main__":
    project = Project("default", "data")

    app = gui.Application.instance
    app.initialize()

    vis = o3d.visualization.O3DVisualizer("Frames", 2048, 1536)
    vis.show_settings = True

    axes = o3d.geometry.LineSet()
    axes.points = o3d.utility.Vector3dVector([[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0], [0, 0, -1], [0, 0, 1]])
    axes.lines = o3d.utility.Vector2iVector([[0, 1], [2, 3], [4, 5]])
    axes.colors = o3d.utility.Vector3dVector([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    vis.add_geometry("axes", axes)


    toDraw = DrawFrameLines(project.frames)
    cnt = 0
    for geometry in toDraw:
        vis.add_geometry(str(cnt), geometry)
        vis.show_geometry(str(cnt), False)
        vis.show_geometry(str(cnt), True)
        cnt += 1


    vis.reset_camera_to_default()
    app.add_window(vis)
    app.run()
