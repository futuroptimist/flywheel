#!/usr/bin/env python3
"""Build assembly.glb from STL parts using assimp and pygltflib."""
from __future__ import annotations

from pathlib import Path

import assimp_py
from pygltflib import ARRAY_BUFFER
from pygltflib import ELEMENT_ARRAY_BUFFER
from pygltflib import FLOAT
from pygltflib import GLTF2
from pygltflib import SCALAR
from pygltflib import UNSIGNED_INT
from pygltflib import VEC3
from pygltflib import Accessor
from pygltflib import Asset
from pygltflib import Buffer
from pygltflib import BufferView
from pygltflib import Material
from pygltflib import Mesh
from pygltflib import Node
from pygltflib import PbrMetallicRoughness
from pygltflib import Primitive
from pygltflib import Scene

FLAGS = (
    assimp_py.Process_Triangulate
    | assimp_py.Process_GenNormals
    | assimp_py.Process_JoinIdenticalVertices
)

PALETTE = [
    (1.0, 0.3, 0.2, 1.0),
    (0.2, 0.8, 0.4, 1.0),
    (0.2, 0.4, 1.0, 1.0),
    (1.0, 0.8, 0.2, 1.0),
    (0.8, 0.2, 1.0, 1.0),
]

PARTS_DIR = Path("parts")
OUTPUT = Path("assembly.glb")


def _vec_min_max(values: list[float]) -> tuple[list[float], list[float]]:
    xs = values[0::3]
    ys = values[1::3]
    zs = values[2::3]
    return [min(xs), min(ys), min(zs)], [max(xs), max(ys), max(zs)]


def build() -> None:
    parts = sorted(PARTS_DIR.glob("*.stl"))
    if not parts:
        raise SystemExit("No STL files found in ./parts/")

    gltf = GLTF2(asset=Asset(version="2.0"))
    gltf.scenes = [Scene(nodes=list(range(len(parts))))]
    gltf.scene = 0
    gltf.nodes = []
    gltf.meshes = []
    gltf.materials = []
    gltf.bufferViews = []
    gltf.accessors = []
    gltf.buffers = []

    binary = bytearray()

    for idx, part in enumerate(parts):
        scene = assimp_py.import_file(str(part), FLAGS)
        mesh = scene.meshes[0]
        verts = mesh.vertices.tobytes()
        norms = mesh.normals.tobytes() if mesh.normals else b""
        indices = mesh.indices.tobytes()

        v_off = len(binary)
        binary.extend(verts)
        n_off = len(binary)
        binary.extend(norms)
        i_off = len(binary)
        binary.extend(indices)

        gltf.bufferViews.append(
            BufferView(
                buffer=0,
                byteOffset=v_off,
                byteLength=len(verts),
                target=ARRAY_BUFFER,
            )
        )
        pos_bv = len(gltf.bufferViews) - 1

        norm_bv = None
        if norms:
            gltf.bufferViews.append(
                BufferView(
                    buffer=0,
                    byteOffset=n_off,
                    byteLength=len(norms),
                    target=ARRAY_BUFFER,
                )
            )
            norm_bv = len(gltf.bufferViews) - 1

        gltf.bufferViews.append(
            BufferView(
                buffer=0,
                byteOffset=i_off,
                byteLength=len(indices),
                target=ELEMENT_ARRAY_BUFFER,
            )
        )
        idx_bv = len(gltf.bufferViews) - 1

        verts_f = list(memoryview(verts).cast("f"))
        min_v, max_v = _vec_min_max(verts_f)

        gltf.accessors.append(
            Accessor(
                bufferView=pos_bv,
                componentType=FLOAT,
                count=mesh.num_vertices,
                type=VEC3,
                min=min_v,
                max=max_v,
            )
        )
        pos_acc = len(gltf.accessors) - 1

        norm_acc = None
        if norm_bv is not None:
            gltf.accessors.append(
                Accessor(
                    bufferView=norm_bv,
                    componentType=FLOAT,
                    count=mesh.num_vertices,
                    type=VEC3,
                )
            )
            norm_acc = len(gltf.accessors) - 1

        gltf.accessors.append(
            Accessor(
                bufferView=idx_bv,
                componentType=UNSIGNED_INT,
                count=mesh.num_indices,
                type=SCALAR,
            )
        )
        idx_acc = len(gltf.accessors) - 1

        gltf.materials.append(
            Material(
                pbrMetallicRoughness=PbrMetallicRoughness(
                    baseColorFactor=PALETTE[idx % len(PALETTE)]
                )
            )
        )
        mat_idx = len(gltf.materials) - 1

        attrs = {"POSITION": pos_acc}
        if norm_acc is not None:
            attrs["NORMAL"] = norm_acc
        primitive = Primitive(
            attributes=attrs,
            indices=idx_acc,
            material=mat_idx,
        )

        gltf.meshes.append(Mesh(primitives=[primitive]))
        mesh_idx = len(gltf.meshes) - 1

        gltf.nodes.append(Node(mesh=mesh_idx, name=part.stem))

    gltf.buffers.append(Buffer(byteLength=len(binary)))
    gltf.set_binary_blob(binary)
    gltf.save_binary(str(OUTPUT))
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
