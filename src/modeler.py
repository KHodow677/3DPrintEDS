import open3d as o3d
import numpy as np

class Modeler:
    def __init__(self, mesh_file):
        self.mesh = o3d.io.read_triangle_mesh(mesh_file)
        self.mesh.compute_vertex_normals()
        self.visualizer = o3d.visualization.Visualizer()
        self.rotation_increment = np.pi / 2
        self.scaling_factor = 0.5

    def rotate_mesh(self, rotation_matrix, center=None):
        if center is None:
            center = self.mesh.get_center()
        self.mesh.rotate(rotation_matrix, center=center)

    def scale_mesh(self, scaling_factor, center=None):
        if center is None:
            center = self.mesh.get_center()
        self.mesh.scale(scaling_factor, center=center)

    def create_window(self):
        self.visualizer.create_window(window_name="Rotated Mesh", width=800, height=600, visible=False)
        self.visualizer.get_render_option().background_color = np.asarray([0, 0, 0]) 
        self.visualizer.get_render_option().ambient_intensity = 0.2

    def add_geometry(self):
        self.visualizer.add_geometry(self.mesh)

    def update_and_capture(self, num_images):
        i = 1
        while True:
            self.rotate_mesh_y()
            self.visualizer.update_geometry(self.mesh)
            events = self.visualizer.poll_events()
            if not events or i == num_images:
                break
            self.visualizer.update_renderer()
            self.visualizer.capture_screen_image(f"Image{i}.png")
            i += 1

    def rotate_mesh_y(self):
        mesh_center = self.mesh.get_center()
        rotation_matrix_y = np.array([[np.cos(self.rotation_increment), 0, np.sin(self.rotation_increment)],
                                      [0, 1, 0],
                                      [-np.sin(self.rotation_increment), 0, np.cos(self.rotation_increment)]])
        self.rotate_mesh(rotation_matrix_y, center=mesh_center)

    def run(self):
        self.create_window()
        self.add_geometry()
        self.scale_mesh(self.scaling_factor)
        self.update_and_capture(5)
        self.visualizer.destroy_window()

# Example usage:
if __name__ == "__main__":
    modeler = Modeler("example.STL")
    modeler.run()
