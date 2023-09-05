import os
from stl import mesh
import numpy as np
import svgwrite

# Corrected function to find unique edges (free edges)
def find_free_edges(triangles):
    edges = set()
    free_edges = set()

    for triangle in triangles:
        for i in range(3):
            edge = (triangle[i], triangle[(i + 1) % 3])  # Ignore edge orientation
            reversed_edge = (edge[1], edge[0])  # Reverse edge to check for uniqueness

            if edge in free_edges or reversed_edge in free_edges:
                free_edges.discard(edge)
                free_edges.discard(reversed_edge)
            else:
                free_edges.add(edge)

    return free_edges

# Function to read an STL file and deconstruct it
def deconstruct_stl(file_name):
    # Read the STL file
    mesh_data = mesh.Mesh.from_file(file_name)

    # Extract unique vertices
    unique_vertices = np.unique(mesh_data.vectors.reshape(-1, 3), axis=0)

    # Create a mapping from vertices to their indices
    vertex_indices = {tuple(vertex): index for index, vertex in enumerate(unique_vertices)}

    # Create a list of triangles using vertex indices
    triangles = []
    for triangle in mesh_data.vectors:
        triangle_indices = [vertex_indices[tuple(vertex)] for vertex in triangle]
        triangles.append(triangle_indices)

    return unique_vertices, triangles

# Function to create an SVG file from free edges
def create_svg_from_edges(file_name, free_edges, vertices):
    dwg = svgwrite.Drawing(file_name, profile='tiny', size=(210, 297))

    # Create a group for all the lines
    lines_group = dwg.add(dwg.g(id='lines_group'))

    for edge in free_edges:
        vertex1 = vertices[edge[0]]
        vertex2 = vertices[edge[1]]
        # Convert vertex values to floats and ignore Z value to make it 2D
        x1, y1 = float(vertex1[0]), float(vertex1[1])
        x2, y2 = float(vertex2[0]), float(vertex2[1])
        # Add the line to the lines group
        lines_group.add(dwg.line(start=(x1, y1), end=(x2, y2), stroke=svgwrite.rgb(0, 0, 0, '%')))

    dwg.save()

# Interactive input from the user
file_name = input("Enter the name of the STL file (including extension): ")

try:
    vertices, triangles = deconstruct_stl(file_name)
    print(f"Unique Vertices: {len(vertices)}")
    print(f"Triangles: {len(triangles)}")

    free_edges = find_free_edges(triangles)
    print(f"Free Edges (Unique Edges in a Single Triangle): {len(free_edges)}")

    # Determine the path and file name for the SVG file
    file_path, file_extension = os.path.splitext(file_name)
    svg_file_name = file_path + "_edges.svg"

    create_svg_from_edges(svg_file_name, free_edges, vertices)
    print(f"SVG file '{svg_file_name}' created with free edges on a single layer/group.")
except Exception as e:
    print(f"Error: {str(e)}")
