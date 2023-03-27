import numpy as np
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering

if __name__ == "__main__":
    app = gui.Application.instance
    app.initialize()

    vis = o3d.visualization.O3DVisualizer("Frames", 1024, 768)
    vis.show_settings = True

    # vis.add_geometry('geometry', geometry)

    vis.reset_camera_to_default()
    app.add_window(vis)
    app.run()
