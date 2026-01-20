import json
import os.path


def generate_graph_from_graphwalker_json(file_name):
    # Load GraphWalker JSON model and convert to internal graph representation
    file_path = os.path.join("json_models", file_name)

    with open(file_path) as f:
        json_data = json.load(f)
        model_data = json_data.get("models")[0]
        # Create internal model structure for graph representation
        model = {
            "directed": False,
            "multigraph": False,
            "graph": {"name": model_data["name"]},
            "nodes": [],
            "links": [],
        }

        # Add all vertices from model to nodes list
        for vertice in model_data["vertices"]:
            vertice_dict = {
                "id": vertice["id"],
                "name": vertice["name"],
                "x": vertice["properties"]["x"],
                "y": vertice["properties"]["y"],
            }
            model["nodes"].append(vertice_dict)

        # Add all edges from model to links list
        for edge in model_data["edges"]:
            edge_dict = {
                "source": edge["sourceVertexId"],
                "target": edge["targetVertexId"],
                "id": edge["id"],
                "name": edge["name"],
            }
            model["links"].append(edge_dict)

        return model
