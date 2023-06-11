import numpy as np
from stl import mesh


def find_free_edges(mesh_data):
    edges = {}
    free_edges = []

    for triangle in mesh_data:
        for i in range(3):
            edge = frozenset([tuple(triangle[i]), tuple(triangle[(i + 1) % 3])])
            if edge in edges:
                edges[edge] += 1
            else:
                edges[edge] = 1

    for edge, count in edges.items():
        if count == 1:
            free_edges.append(edge)

    return free_edges


def create_new_edges(free_edges, fixed_z):
    new_edges = []
    for edge in free_edges:
        v1, v2 = edge
        new_edge = [(v1[0], v1[1], fixed_z), (v2[0], v2[1], fixed_z)]
        new_edges.append(new_edge)
    return new_edges


def create_triangles(free_edges, new_edges):
    triangles = []

    for edge in free_edges:
        v1, v2 = edge
        new_edge = new_edges[free_edges.index(edge)]

        vertex1, vertex2 = v1, v2
        vertex3 = new_edge[0]
        triangle1 = np.array([vertex1, vertex2, vertex3])
        triangles.append(triangle1)

        vertex1, vertex2 = v2, new_edge[1]
        vertex3 = new_edge[0]
        triangle2 = np.array([vertex1, vertex2, vertex3])
        triangles.append(triangle2)

    return triangles


def create_floor(new_edges, fixed_z):
    center_point = np.mean(np.array(new_edges).reshape(-1, 3), axis=0)
    floor_triangles = []

    for edge in new_edges:
        vertex1, vertex2 = edge
        vertex3 = center_point

        triangle = np.array([vertex1, vertex2, vertex3])
        floor_triangles.append(triangle)

    return floor_triangles


def export_stl(triangles, original_mesh, file_name):
    total_triangles = len(triangles)
    output_mesh = mesh.Mesh(np.zeros(total_triangles, dtype=mesh.Mesh.dtype))

    for i, triangle in enumerate(triangles):
        output_mesh.vectors[i] = triangle

    output_mesh.save(file_name)


# Main program
#file_name = input("Enter the name of the STL file: ")
file_name = input("Entrer nom du fichier STL: ")

# Load the original STL file
original_mesh = mesh.Mesh.from_file(file_name)

# Print information about the STL file
num_triangles = len(original_mesh.vectors)
min_z = np.min(original_mesh.vectors[:, :, 2])
max_z = np.max(original_mesh.vectors[:, :, 2])
#print(f"STL file '{file_name}' contains {num_triangles} triangles.")
#print(f"Minimum Z value: {min_z}")
#print(f"Maximum Z value: {max_z}")
print(f"le Fichier STL contiens {num_triangles} triangles.")
print(f"Valeur de Z minimal: {min_z}")
print(f"Valeur de Z maximal: {max_z}")

#fixed_z = float(input("Enter the fixed Z value for new edges and floor: "))
fixed_z = float(input("Entrer la valeur en Z du sole: "))

# Find free edges
free_edges = find_free_edges(original_mesh.vectors)

# Create new edges
new_edges = create_new_edges(free_edges, fixed_z)

# Create triangles for walls
wall_triangles = create_triangles(free_edges, new_edges)

# Create triangles for the floor
floor_triangles = create_floor(new_edges, fixed_z)

# Combine original triangles, wall triangles, and floor triangles
all_triangles = original_mesh.vectors.tolist() + wall_triangles + floor_triangles

# Export the final STL file
output_file_name = "output.stl"
export_stl(all_triangles, original_mesh, output_file_name)

print(f"STL file '{output_file_name}' has been created.")
