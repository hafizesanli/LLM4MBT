import time
import os.path
from graph_conversions import *
from utility_functions import *
from tlc_runner import run_tlc_on_model

def check_if_path_exist(links, source, target):
    for link in links:
        if link["source"] == source and link["target"] == target:
            return True

    return False


def apply_test_execution_on_model(test_suite, model, verbose=True):
    # nodes_dict: vertex name -> [vertex IDs] (multiple vertices with same name possible)
    nodes_dict = {}
    for node in model["nodes"]:
        name = node["name"]
        if name not in nodes_dict:
            nodes_dict[name] = []
        nodes_dict[name].append(node["id"])

    # edges_set: all valid edge names
    edges_set = set()
    for link in model["links"]:
        edges_set.add(link["name"])

    start_names = {"v_Start", "start"}

    def is_vertex(name):
        """Check if item is a vertex or edge"""
        return name in start_names or (isinstance(name, str) and (name.startswith("v_") or name.startswith("q")))

    # Statistics for report
    total_paths = 0
    successful_paths = 0
    failed_paths = 0
    failed_path_details = []

    for test_case in test_suite:
        if verbose is True:
            print(f"\n{'='*70}")
            print(f"Test case to apply: {test_case}")
            print(f"{'='*70}")
        
        previous_item = ""
        previous_item_name = ""
        i = 0
        q0_id = None
        
        # Find q0's ID for restart functionality
        if "q0" in nodes_dict:
            q0_id = nodes_dict["q0"][0]
        
        while i < len(test_case):
            item = test_case[i]
            
            # If item is a start marker, set previous_item
            if item in start_names:
                if item not in nodes_dict:
                    if verbose is True:
                        print(f"Unknown node name in test case: {item}")
                    return False
                # Get first ID for start
                previous_item = nodes_dict[item][0]
                previous_item_name = item
                i += 1
                continue
            
            # If item is an edge name (with next being a vertex)
            if not is_vertex(item):
                # Edge validation
                if item not in edges_set:
                    if verbose is True:
                        print(f"Invalid edge name in test case: '{item}' (not found in model)")
                        print(f"   → Failed path: ...{previous_item_name} -> ? via edge '{item}'")
                        print(f"   → Restarting from q0...\n")
                    
                    failed_paths += 1
                    failed_path_details.append(f"Edge '{item}' not found in model")
                    
                    # Restart from q0
                    if q0_id:
                        previous_item = q0_id
                        previous_item_name = "q0"
                        i += 2  # Skip edge and vertex
                        total_paths += 1
                        continue
                    else:
                        return False
                
                # Next element should be a vertex
                if i + 1 >= len(test_case):
                    if verbose is True:
                        print(f"Edge '{item}' has no target vertex")
                    return False
                
                next_item = test_case[i + 1]
                if not is_vertex(next_item):
                    if verbose is True:
                        print(f"After edge '{item}', expected a vertex but got '{next_item}'")
                    return False
                
                if next_item not in nodes_dict:
                    if verbose is True:
                        print(f"Unknown node name in test case: {next_item}")
                        print(f"   → Failed path: ...{previous_item_name} -> {next_item} via edge '{item}'")
                        print(f"   → Restarting from q0...\n")
                    
                    failed_paths += 1
                    failed_path_details.append(f"Unknown vertex '{next_item}'")
                    
                    # Restart from q0
                    if q0_id:
                        previous_item = q0_id
                        previous_item_name = "q0"
                        i += 2
                        total_paths += 1
                        continue
                    else:
                        return False
                
                # Check if we can move to next vertex
                current_items = nodes_dict[next_item]
                found_path = False
                matched_current_item = None
                
                for current_item in current_items:
                    for link in model["links"]:
                        if link["source"] == previous_item and link["target"] == current_item and link["name"] == item:
                            found_path = True
                            matched_current_item = current_item
                            break
                    if found_path:
                        break
                
                if found_path:
                    if verbose is True:
                        print(f"successfully moved from {previous_item_name} -> {next_item} via edge '{item}'")
                    
                    successful_paths += 1
                    total_paths += 1
                    previous_item = matched_current_item
                    previous_item_name = next_item
                    i += 2
                else:
                    if verbose is True:
                        print(f"No path found for: {previous_item_name} -> {next_item} via edge '{item}'")
                        print(f"   → Failed path: {previous_item_name} -> {next_item}")
                        print(f"   → Restarting from q0...\n")
                    
                    failed_paths += 1
                    failed_path_details.append(f"No path: {previous_item_name} -> {next_item} via edge '{item}'")
                    total_paths += 1
                    
                    # Restart from q0
                    if q0_id:
                        previous_item = q0_id
                        previous_item_name = "q0"
                        i += 2
                        continue
                    else:
                        return False
            else:
                # Vertex - should not happen normally since vertices should have edges between them
                if verbose is True:
                    print(f"Unexpected vertex '{item}' without preceding edge")
                return False

    # Print report
    print(f"\n\n{'='*70}")
    print(f"---TEST REPORT---")
    print(f"{'='*70}")
    print(f"Total Paths: {total_paths}")
    print(f"Successful: {successful_paths}")
    print(f"Failed: {failed_paths}")
    
    if total_paths > 0:
        success_percentage = (successful_paths / total_paths) * 100
        failure_percentage = (failed_paths / total_paths) * 100
        print(f"\n Percentages:")
        print(f"   Success Rate: {success_percentage:.2f}%")
        print(f"   Failure Rate: {failure_percentage:.2f}%")
    
    if failed_path_details:
        print(f"\n Failed Paths:")
        for idx, detail in enumerate(failed_path_details, 1):
            print(f"   {idx}. {detail}")
    
    print(f"{'='*70}\n")

    return failed_paths == 0


if __name__ == "__main__":
   ##############################################################################
   ok = run_tlc_on_model("json_models/TLC.txt", "TLC.json", verbose=True)
   print("All passed" if ok else "Some failed")