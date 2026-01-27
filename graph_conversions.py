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
            # Check if properties exist, use default values if not
            if "properties" in vertice:
                x_coord = vertice["properties"]["x"]
                y_coord = vertice["properties"]["y"]
            else:
                # Default coordinates for vertices without properties
                x_coord = 0.0
                y_coord = 0.0
                
            vertice_dict = {
                "id": vertice["id"],
                "name": vertice["name"],
                "x": x_coord,
                "y": y_coord,
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


def calculate_coverage(test_suite, model):
    """
    Calculate edge and vertex coverage achieved by test suite
    Returns dict with coverage metrics
    """
    if not test_suite or not model:
        return {"edge_coverage": 0, "vertex_coverage": 0, "covered_edges": 0, "total_edges": 0, "covered_vertices": 0, "total_vertices": 0}
    
    # Get all edges and vertices from model
    all_edges = set()
    for link in model["links"]:
        # Create unique edge identifier: source_id->edge_name->target_id
        edge_id = f"{link['source']}->{link['name']}->{link['target']}"
        all_edges.add(edge_id)
    
    all_vertices = set()
    for node in model["nodes"]:
        all_vertices.add(node["id"])
    
    # Track covered edges and vertices
    covered_edges = set()
    covered_vertices = set()
    
    # Build vertex name to ID mapping
    vertex_name_to_ids = {}
    for node in model["nodes"]:
        name = node["name"]
        if name not in vertex_name_to_ids:
            vertex_name_to_ids[name] = []
        vertex_name_to_ids[name].append(node["id"])
    
    # Process each test case in the suite
    for test_case in test_suite:
        previous_vertex_id = None
        previous_vertex_name = None
        
        for i, item in enumerate(test_case):
            # Check if this is a vertex
            if item in vertex_name_to_ids:
                # Mark vertex as covered
                vertex_ids = vertex_name_to_ids[item]
                for vid in vertex_ids:
                    covered_vertices.add(vid)
                
                # If we have a previous vertex, find the connecting edge
                if previous_vertex_id is not None and i > 0:
                    # Look for edge between previous and current vertex
                    for current_vid in vertex_ids:
                        for link in model["links"]:
                            if link["source"] == previous_vertex_id and link["target"] == current_vid:
                                edge_id = f"{link['source']}->{link['name']}->{link['target']}"
                                covered_edges.add(edge_id)
                                break
                
                # Update for next iteration
                if vertex_ids:
                    previous_vertex_id = vertex_ids[0]
                    previous_vertex_name = item
            else:
                # This might be an edge name
                # Next item should be a vertex
                if i + 1 < len(test_case):
                    next_item = test_case[i + 1]
                    if next_item in vertex_name_to_ids and previous_vertex_id is not None:
                        # Find edge with this name connecting vertices
                        for target_vid in vertex_name_to_ids[next_item]:
                            for link in model["links"]:
                                if (link["source"] == previous_vertex_id and 
                                    link["target"] == target_vid and 
                                    link["name"] == item):
                                    edge_id = f"{link['source']}->{link['name']}->{link['target']}"
                                    covered_edges.add(edge_id)
                                    break
    
    # Calculate percentages
    edge_coverage = (len(covered_edges) / len(all_edges) * 100) if all_edges else 0
    vertex_coverage = (len(covered_vertices) / len(all_vertices) * 100) if all_vertices else 0
    
    return {
        "edge_coverage": round(edge_coverage, 2),
        "vertex_coverage": round(vertex_coverage, 2),
        "covered_edges": len(covered_edges),
        "total_edges": len(all_edges),
        "covered_vertices": len(covered_vertices),
        "total_vertices": len(all_vertices)
    }


def calculate_model_statistics(model):
    """
    Calculate basic statistics about the model
    """
    num_vertices = len(model["nodes"])
    num_edges = len(model["links"])
    
    # Calculate branching factor
    vertex_branching = {}
    for node in model["nodes"]:
        vertex_branching[node["id"]] = 0
    
    for link in model["links"]:
        source_id = link["source"]
        if source_id in vertex_branching:
            vertex_branching[source_id] += 1
    
    branching_factors = list(vertex_branching.values())
    avg_branching = sum(branching_factors) / len(branching_factors) if branching_factors else 0
    max_branching = max(branching_factors) if branching_factors else 0
    
    return {
        "vertices": num_vertices,
        "edges": num_edges,
        "avg_branching_factor": round(avg_branching, 2),
        "max_branching_factor": max_branching
    }
