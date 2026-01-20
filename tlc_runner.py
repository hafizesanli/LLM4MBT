import re
import os

from graph_conversions import generate_graph_from_graphwalker_json

def load_tlc_test_suite(tlc_path, remove_duplicates=False):
    # Read entire file and extract "currentElementName" values
    elems = []
    with open(tlc_path, "r", encoding="utf-8") as f:
        content = f.read()
        # Find all matches
        matches = re.findall(r'"currentElementName"\s*:\s*"([^"]+)"', content)
        elems.extend(matches)

    # Create test case with vertices and edges together
    # Vertex: 'start' or starting with q (q0, q1, q2, ..., q8 etc)
    # Edge: all other elements
    
    # 'start' must be present
    if "start" not in elems:
        raise ValueError("'start' not found in TLC file. Please check GraphWalker output.")

    # Test cases: start a new test when we see 'start'
    test_suite = []
    current_test = None
    
    for elem in elems:
        if elem == "start":
            # Start new test
            if current_test is not None:
                if remove_duplicates:
                    if current_test not in test_suite:
                        test_suite.append(current_test.copy())
                else:
                    test_suite.append(current_test.copy())
            current_test = [elem]
        else:
            # Add all elements after start (vertices and edges)
            if current_test is not None:
                current_test.append(elem)

    # Add final test
    if current_test is not None:
        if remove_duplicates:
            if current_test not in test_suite:
                test_suite.append(current_test.copy())
        else:
            test_suite.append(current_test.copy())

    return test_suite

def run_tlc_on_model(tlc_path, model_json_name, verbose=True, remove_duplicates=False):
    if not os.path.exists(tlc_path):
        raise FileNotFoundError(f"{tlc_path} bulunamadı.")
    model = generate_graph_from_graphwalker_json(model_json_name)
    test_suite = load_tlc_test_suite(tlc_path, remove_duplicates=remove_duplicates)

    from main import apply_test_execution_on_model
    return apply_test_execution_on_model(test_suite, model, verbose)