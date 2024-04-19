import open3d as o3d
import numpy as np

# Read the mesh
mesh = o3d.io.read_triangle_mesh("example.STL")
mesh = mesh.compute_vertex_normals()

mesh_center = mesh.get_center()
rotation_matrix_inverse = np.array([[1, 0, 0],
                                    [0, np.cos(-np.pi / 2), -np.sin(-np.pi / 2)],
                                    [0, np.sin(-np.pi / 2), np.cos(-np.pi / 2)]])

mesh.rotate(rotation_matrix_inverse, center=mesh_center)

visualizer = o3d.visualization.Visualizer()
visualizer.create_window(window_name="Rotated Mesh", width=800, height=600)
visualizer.get_render_option().background_color = np.asarray([0, 0, 0])  # Set background to black

# Add the mesh to the scene
visualizer.add_geometry(mesh)

mesh_center = mesh.get_center()
scaling_factor = 0.5
mesh.scale(scaling_factor, center=mesh_center)

rotation_increment = np.pi / 2
i = 1

while True:
    mesh_center = mesh.get_center()

    rotation_matrix_y = np.array([[np.cos(rotation_increment), 0, np.sin(rotation_increment)],
                                   [0, 1, 0],
                                   [-np.sin(rotation_increment), 0, np.cos(rotation_increment)]])
    
    mesh.rotate(rotation_matrix_y, center=mesh_center)

    visualizer.update_geometry(mesh)
    events = visualizer.poll_events()
    if events == False:
        break
    visualizer.update_renderer()
    visualizer.capture_screen_image(f"Image{i}.png")
    i+=1
    if i == 5:
        break

visualizer.destroy_window()  
