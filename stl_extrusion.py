import os
import threading
import time
import sys
from itertools import cycle
import numpy as np
from stl import mesh
from tqdm import tqdm


def loading_spinner():
    spinner = cycle(['-', '/', '|', '\\'])
    while not loading_spinner.stop_event.is_set():
        sys.stdout.write('\rChargement du STL ' + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 20 + '\r')
    sys.stdout.flush()


def find_free_edges(mesh_data):
    edges = {}
    free_edges = []

    for triangle in tqdm(mesh_data, desc='Recherche des côtés libre'):
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
    for edge in tqdm(free_edges, desc='Création de nouveau côtés'):
        v1, v2 = edge
        new_edge = [(v1[0], v1[1], fixed_z), (v2[0], v2[1], fixed_z)]
        new_edges.append(new_edge)
    return new_edges


def create_triangles(free_edges, new_edges):
    triangles = []

    for edge in tqdm(free_edges, desc='.......Création des mures'):
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
   
    for edge in tqdm(new_edges, desc='.........Creation du sole'):
        vertex1, vertex2 = edge
        vertex3 = center_point

        triangle = np.array([vertex1, vertex2, vertex3])
        floor_triangles.append(triangle)

    return floor_triangles


def export_stl(triangles, original_mesh, input_file_name):
    base_name = os.path.basename(input_file_name)
    output_file_name = os.path.splitext(base_name)[0] + "_extruder.stl"

    total_triangles = len(triangles)
    mesh_data = mesh.Mesh(np.zeros(total_triangles + len(original_mesh.vectors), dtype=mesh.Mesh.dtype))

    for i, triangle in enumerate(triangles):
        mesh_data.vectors[i] = triangle

    for i, triangle in enumerate(original_mesh.vectors):
        offset = total_triangles
        mesh_data.vectors[i + offset] = triangle

    mesh_data.save(output_file_name)

    print(f"\nLe fichier STL '{output_file_name}' a été créer.")



def main():
    while True:
        file_name = input("Entrer le nom du fichier STL: ")

        loading_spinner.stop_event = threading.Event()
        loading_thread = threading.Thread(target=loading_spinner)
        loading_thread.start()

        # Load the STL file
        original_mesh = mesh.Mesh.from_file(file_name)

        loading_spinner.stop_event.set()
        loading_thread.join()

        num_triangles = len(original_mesh.vectors)
        min_z = np.min(original_mesh.vectors[:, :, 2])
        max_z = np.max(original_mesh.vectors[:, :, 2])
        print(f"\nNombre de triangles: {num_triangles}")
        print(f"Valeur Z maximal: {min_z}")
        print(f"Valeur Z minimal: {max_z}")

        fixed_z = float(input("Enter la hauteur en Z du sole: "))

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
        export_stl(all_triangles, original_mesh, file_name)

        # Ask the user if they want to process another file
        choice = input("\nVoulez-vous extruder un autre fichier? (o/n): ")
        if choice.lower() != "o":
            break
        print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")


if __name__ == '__main__':
    main()
