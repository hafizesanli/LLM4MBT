import time
import os.path
import json
from graph_conversions import *
from utility_functions import *

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

    # Automatically detect all vertex names from the model
    all_vertex_names = set(nodes_dict.keys())
    
    def is_vertex(name):
        """Check if item is a vertex (exists in model) or edge"""
        return name in all_vertex_names

    def find_fallback_vertex():
        """Find a suitable fallback vertex for restart"""
        # Priority order for fallback vertices
        fallback_candidates = [
            "start", "v_Start", "Login_v_Start", "DASHBOARD", 
            "q0", "q1", "v_Verify_In_Login_Page"
        ]
        
        for candidate in fallback_candidates:
            if candidate in nodes_dict:
                return nodes_dict[candidate][0], candidate
        
        # If no standard fallback found, use the first vertex in the model
        if nodes_dict:
            first_vertex_name = list(nodes_dict.keys())[0]
            return nodes_dict[first_vertex_name][0], first_vertex_name
        
        return None, None

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
        fallback_id, fallback_name = find_fallback_vertex()
        
        while i < len(test_case):
            item = test_case[i]
            
            # If item is a vertex name and it's the first item, set it as starting point
            if i == 0 and is_vertex(item):
                if item not in nodes_dict:
                    if verbose is True:
                        print(f"Unknown starting node name in test case: {item}")
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
                        if fallback_id:
                            print(f"   → Restarting from {fallback_name}...\n")
                    
                    failed_paths += 1
                    failed_path_details.append(f"Edge '{item}' not found in model")
                    
                    # Restart from fallback vertex
                    if fallback_id:
                        previous_item = fallback_id
                        previous_item_name = fallback_name
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
                        if fallback_id:
                            print(f"   → Restarting from {fallback_name}...\n")
                    
                    failed_paths += 1
                    failed_path_details.append(f"Unknown vertex '{next_item}'")
                    
                    # Restart from fallback vertex
                    if fallback_id:
                        previous_item = fallback_id
                        previous_item_name = fallback_name
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
                        if fallback_id:
                            print(f"   → Restarting from {fallback_name}...\n")
                    
                    failed_paths += 1
                    failed_path_details.append(f"No path: {previous_item_name} -> {next_item} via edge '{item}'")
                    total_paths += 1
                    
                    # Restart from fallback vertex
                    if fallback_id:
                        previous_item = fallback_id
                        previous_item_name = fallback_name
                        i += 2
                        continue
                    else:
                        return False
            else:
                # Handle direct vertex transitions (without explicit edge names)
                if previous_item_name == "":
                    # First vertex in sequence
                    if item not in nodes_dict:
                        if verbose is True:
                            print(f"Unknown node name in test case: {item}")
                        return False
                    previous_item = nodes_dict[item][0]
                    previous_item_name = item
                    i += 1
                else:
                    # Direct vertex-to-vertex transition - find a connecting edge
                    if item not in nodes_dict:
                        if verbose is True:
                            print(f"Unknown vertex name in test case: {item}")
                            print(f"   → Failed path: {previous_item_name} -> {item}")
                            if fallback_id:
                                print(f"   → Restarting from {fallback_name}...\n")
                        
                        failed_paths += 1
                        failed_path_details.append(f"Unknown vertex '{item}'")
                        
                        if fallback_id:
                            previous_item = fallback_id
                            previous_item_name = fallback_name
                            i += 1
                            total_paths += 1
                            continue
                        else:
                            return False
                    
                    # Find any edge connecting previous vertex to current vertex
                    current_items = nodes_dict[item]
                    found_path = False
                    matched_current_item = None
                    used_edge = None
                    
                    for current_item in current_items:
                        for link in model["links"]:
                            if link["source"] == previous_item and link["target"] == current_item:
                                found_path = True
                                matched_current_item = current_item
                                used_edge = link["name"]
                                break
                        if found_path:
                            break
                    
                    if found_path:
                        if verbose is True:
                            print(f"successfully moved from {previous_item_name} -> {item} via edge '{used_edge}'")
                        
                        successful_paths += 1
                        total_paths += 1
                        previous_item = matched_current_item
                        previous_item_name = item
                        i += 1
                    else:
                        if verbose is True:
                            print(f"No direct path found for: {previous_item_name} -> {item}")
                            print(f"   → Failed path: {previous_item_name} -> {item}")
                            if fallback_id:
                                print(f"   → Restarting from {fallback_name}...\n")
                        
                        failed_paths += 1
                        failed_path_details.append(f"No direct path: {previous_item_name} -> {item}")
                        total_paths += 1
                        
                        # Restart from fallback vertex
                        if fallback_id:
                            previous_item = fallback_id
                            previous_item_name = fallback_name
                            i += 1
                            continue
                        else:
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

    # Return both success status and path statistics
    return {
        'all_paths_valid': failed_paths == 0,
        'total_paths': total_paths,
        'successful_paths': successful_paths,
        'failed_paths': failed_paths,
        'success_rate': (successful_paths / total_paths * 100) if total_paths > 0 else 0
    }


def run_test_suite_from_file(test_suite_file, model_file, verbose=True, save_report=False):
    """Run test suite from a txt file on a specific model"""
    if not os.path.exists(test_suite_file):
        print(f"Test suite file not found: {test_suite_file}")
        return False
    
    if not os.path.exists(model_file):
        print(f"Model file not found: {model_file}")
        return False
    
    print(f"\n{'='*80}")
    print(f"RUNNING TEST SUITE: {os.path.basename(test_suite_file)}")
    print(f"ON MODEL: {os.path.basename(model_file)}")
    print(f"{'='*80}")
    
    # Load and parse test suite
    test_suite = parse_test_suite_from_file(test_suite_file)
    if not test_suite:
        print(f"Failed to parse test suite from {test_suite_file}")
        return False, {}
    
    # Convert model to format expected by the test execution function
    model = generate_graph_from_graphwalker_json(os.path.basename(model_file))
    if not model:
        print(f"Failed to convert model from {model_file}")
        return False, {}
    
    # Calculate coverage
    coverage = calculate_coverage(test_suite, model)
    print(f"\n COVERAGE METRICS:")
    print(f"   Edge Coverage: {coverage['edge_coverage']}% ({coverage['covered_edges']}/{coverage['total_edges']})")
    print(f"   Vertex Coverage: {coverage['vertex_coverage']}% ({coverage['covered_vertices']}/{coverage['total_vertices']})")
    
    # Run test execution
    execution_result = apply_test_execution_on_model(test_suite, model, verbose)
    
    # Determine success based on coverage metrics
    # Success criteria: Either achieve high edge coverage OR high vertex coverage
    # - Edge coverage >= 70% OR Vertex coverage >= 85%
    # - This allows tests with good vertex coverage to pass even if some edges are missed
    edge_cov = coverage.get('edge_coverage', 0)
    vertex_cov = coverage.get('vertex_coverage', 0)
    
    success = (edge_cov >= 70.0) or (vertex_cov >= 85.0)
    
    # Add execution details to coverage
    coverage['execution_stats'] = execution_result
    
    # Save report if requested
    if save_report:
        save_single_test_report(test_suite_file, model_file, success, coverage)
    
    return success, coverage


def parse_test_suite_from_file(file_path):
    """Parse test suite from txt file in the format you created"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Parse the JSON-like format: {"currentElementName":"vertex_name"}
        import re
        pattern = r'\{"currentElementName":"([^"]+)"\}'
        matches = re.findall(pattern, content)
        
        if not matches:
            print(f"No valid test steps found in {file_path}")
            return None
        
        # Return as a single test case (list of vertex names)
        return [matches]
        
    except Exception as e:
        print(f"Error parsing test suite file {file_path}: {e}")
        return None


def run_all_test_suites_in_directory(directory_path="graphwalker_test_path_logs", model_directory="json_models", verbose=False):
    """Run all test suites from an LLM output directory
    
    Args:
        directory_path: Directory containing test suite files (e.g., 'Claude-Haiku-4.5/')
        model_directory: Directory containing JSON models (e.g., 'json_models/')
        verbose: Whether to show detailed test execution logs
        
    Returns:
        Dictionary with results for each test suite including coverage metrics
    """
    # Get the directory where main.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Convert to absolute path if relative path provided
    if not os.path.isabs(directory_path):
        directory_path = os.path.join(script_dir, directory_path)
    
    # Remove trailing slash if present
    directory_path = directory_path.rstrip('/')
    
    if not os.path.exists(directory_path):
        print(f"Test suite directory not found: {directory_path}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Script directory: {script_dir}")
        return {}
    
    # Convert model_directory to absolute path if relative
    if not os.path.isabs(model_directory):
        model_directory = os.path.join(script_dir, model_directory)
    
    if not os.path.exists(model_directory):
        print(f"Model directory not found: {model_directory}")
        return {}
    
    # Find all test suite files
    test_files = []
    for file in os.listdir(directory_path):
        if file.endswith('.txt'):
            test_files.append(file)
    
    if not test_files:
        print(f"No test suite files found in {directory_path}")
        return {}
    
    print(f"\n{'='*80}")
    print(f"TESTING LLM OUTPUT FROM: {os.path.basename(directory_path)}")
    print(f"{'='*80}")
    
    results = {}
    
    for test_file in sorted(test_files):
        # Direct match: TLC.txt -> TLC.json, Parabank.txt -> Parabank.json
        model_name = test_file.replace(".txt", ".json")
        
        test_file_path = os.path.join(directory_path, test_file)
        model_file_path = os.path.join(model_directory, model_name)
        
        # Check if model file exists
        if not os.path.exists(model_file_path):
            print(f"\n!!!  Warning: No matching model found for {test_file}")
            results[test_file] = {'success': False, 'error': 'Model not found', 'coverage': {}}
            continue
        
        try:
            success, coverage = run_test_suite_from_file(test_file_path, model_file_path, verbose)
            results[test_file] = {
                'success': success,
                'coverage': coverage
            }
        except Exception as e:
            print(f"\n❌ Error running {test_file}: {e}")
            results[test_file] = {'success': False, 'error': str(e), 'coverage': {}}
    
    return results


def compare_llm_outputs(llm_directories, model_directory="json_models", verbose=False, save_report=True):
    """Compare multiple LLM outputs and generate comparison report
    
    Args:
        llm_directories: List of directories containing LLM outputs (e.g., ['Claude-Haiku-4.5/', 'GPT-4/'])
        model_directory: Directory containing JSON models
        verbose: Whether to show detailed logs
        save_report: Whether to save the report to files (JSON and TXT)
        
    Returns:
        Comparison report with coverage and accuracy for each LLM
    """
    print(f"\n{'#'*80}")
    print(f"# COMPARING MULTIPLE LLM OUTPUTS")
    print(f"{'#'*80}")
    
    comparison_results = {}
    
    # Run tests for each LLM directory
    for llm_dir in llm_directories:
        if not os.path.exists(llm_dir):
            print(f"\n!!!  Warning: Directory not found: {llm_dir}")
            continue
        
        llm_name = os.path.basename(llm_dir.rstrip('/'))
        print(f"\n Processing: {llm_name}")
        results = run_all_test_suites_in_directory(llm_dir, model_directory, verbose)
        comparison_results[llm_name] = results
    
    # Generate comparison report
    print_comparison_report(comparison_results)
    
    # Save reports to files
    if save_report and comparison_results:
        save_comparison_reports(comparison_results)
    
    return comparison_results


def print_comparison_report(comparison_results):
    """Print a comprehensive comparison report across all LLMs"""
    print(f"\n{'#'*80}")
    print(f"# LLM COMPARISON REPORT")
    print(f"{'#'*80}\n")
    
    if not comparison_results:
        print("No results to compare.")
        return
    
    # Collect all unique test files
    all_test_files = set()
    for llm_results in comparison_results.values():
        all_test_files.update(llm_results.keys())
    
    # Print summary for each LLM
    print("=" * 80)
    print("OVERALL PERFORMANCE BY LLM")
    print("=" * 80)
    
    for llm_name, results in comparison_results.items():
        if not results:
            print(f"\n❌ {llm_name}: No test results")
            continue
        
        # Calculate overall metrics
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get('success', False))
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Calculate average coverage
        edge_coverages = [r['coverage']['edge_coverage'] for r in results.values() 
                         if 'coverage' in r and 'edge_coverage' in r['coverage']]
        vertex_coverages = [r['coverage']['vertex_coverage'] for r in results.values() 
                           if 'coverage' in r and 'vertex_coverage' in r['coverage']]
        
        avg_edge_coverage = sum(edge_coverages) / len(edge_coverages) if edge_coverages else 0
        avg_vertex_coverage = sum(vertex_coverages) / len(vertex_coverages) if vertex_coverages else 0
        
        print(f"\n {llm_name}")
        print(f"   ✅ Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
        print(f"   Avg Edge Coverage: {avg_edge_coverage:.1f}%")
        print(f"   Avg Vertex Coverage: {avg_vertex_coverage:.1f}%")
    
    # Detailed comparison per test file
    print(f"\n{'=' * 80}")
    print("DETAILED COMPARISON BY TEST FILE")
    print(f"{'=' * 80}\n")
    
    for test_file in sorted(all_test_files):
        print(f"\n {test_file}")
        print(f"{'─' * 80}")
        
        for llm_name in sorted(comparison_results.keys()):
            result = comparison_results[llm_name].get(test_file)
            
            if not result:
                print(f"   {llm_name:30} → !!!  No result")
                continue
            
            if 'error' in result:
                print(f"   {llm_name:30} → ❌ Error: {result['error']}")
                continue
            
            success = result.get('success', False)
            coverage = result.get('coverage', {})
            
            edge_cov = coverage.get('edge_coverage', 0)
            vertex_cov = coverage.get('vertex_coverage', 0)
            
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"   {llm_name:30} → {status} | Edge: {edge_cov:5.1f}% | Vertex: {vertex_cov:5.1f}%")
    
    print(f"\n{'=' * 80}\n")


def save_comparison_reports(comparison_results, output_dir="comparison_reports"):
    """Save comparison results to JSON and TXT files
    
    Args:
        comparison_results: Dictionary with LLM comparison results
        output_dir: Directory to save the reports
    """
    import datetime
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate timestamp for filenames
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Calculate summary statistics for JSON
    summary_stats = {}
    for llm_name, results in comparison_results.items():
        if not results:
            continue
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get('success', False))
        
        edge_coverages = [r['coverage']['edge_coverage'] for r in results.values() 
                         if 'coverage' in r and 'edge_coverage' in r['coverage']]
        vertex_coverages = [r['coverage']['vertex_coverage'] for r in results.values() 
                           if 'coverage' in r and 'vertex_coverage' in r['coverage']]
        
        summary_stats[llm_name] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'avg_edge_coverage': sum(edge_coverages) / len(edge_coverages) if edge_coverages else 0,
            'avg_vertex_coverage': sum(vertex_coverages) / len(vertex_coverages) if vertex_coverages else 0
        }
    
    # Save JSON report
    json_filename = os.path.join(output_dir, f"llm_comparison_{timestamp}.json")
    json_report = {
        'timestamp': timestamp,
        'summary': summary_stats,
        'detailed_results': comparison_results
    }
    
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=2, ensure_ascii=False)
    
    print(f"\n JSON report saved: {json_filename}")
    
    # Save TXT report (human-readable)
    txt_filename = os.path.join(output_dir, f"llm_comparison_{timestamp}.txt")
    
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("LLM COMPARISON REPORT\n")
        f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        # Overall performance
        f.write("="*80 + "\n")
        f.write("OVERALL PERFORMANCE BY LLM\n")
        f.write("="*80 + "\n\n")
        
        for llm_name, stats in summary_stats.items():
            f.write(f" {llm_name}\n")
            f.write(f"   ✅ Success Rate: {stats['success_rate']:.1f}% ")
            f.write(f"({stats['passed_tests']}/{stats['total_tests']})\n")
            f.write(f"   Avg Edge Coverage: {stats['avg_edge_coverage']:.1f}%\n")
            f.write(f"   Avg Vertex Coverage: {stats['avg_vertex_coverage']:.1f}%\n\n")
        
        # Detailed comparison per test file
        f.write("="*80 + "\n")
        f.write("DETAILED COMPARISON BY TEST FILE\n")
        f.write("="*80 + "\n\n")
        
        # Collect all unique test files
        all_test_files = set()
        for llm_results in comparison_results.values():
            all_test_files.update(llm_results.keys())
        
        for test_file in sorted(all_test_files):
            f.write(f"\n {test_file}\n")
            f.write("-"*80 + "\n")
            
            for llm_name in sorted(comparison_results.keys()):
                result = comparison_results[llm_name].get(test_file)
                
                if not result:
                    f.write(f"   {llm_name:30} → !!!  No result\n")
                    continue
                
                if 'error' in result:
                    f.write(f"   {llm_name:30} → ❌ Error: {result['error']}\n")
                    continue
                
                success = result.get('success', False)
                coverage = result.get('coverage', {})
                
                edge_cov = coverage.get('edge_coverage', 0)
                vertex_cov = coverage.get('vertex_coverage', 0)
                
                status = "✅ PASS" if success else "❌ FAIL"
                f.write(f"   {llm_name:30} → {status} | ")
                f.write(f"Edge: {edge_cov:5.1f}% | Vertex: {vertex_cov:5.1f}%\n")
        
        f.write("\n" + "="*80 + "\n")
    
    print(f"TXT report saved: {txt_filename}")


def save_single_test_report(test_file, model_file, success, coverage, output_dir="test_reports"):
    """Save single test results to JSON and TXT files
    
    Args:
        test_file: Path to the test file
        model_file: Path to the model file
        success: Whether the test passed
        coverage: Coverage metrics dictionary
        output_dir: Directory to save the reports
    """
    import datetime
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate timestamp for filenames
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    test_name = os.path.basename(test_file).replace('.txt', '')
    
    # Save JSON report
    json_filename = os.path.join(output_dir, f"{test_name}_{timestamp}.json")
    json_report = {
        'timestamp': timestamp,
        'test_file': test_file,
        'model_file': model_file,
        'success': success,
        'coverage': coverage
    }
    
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(json_report, f, indent=2, ensure_ascii=False)
    
    print(f"\n JSON report saved: {json_filename}")
    
    # Save TXT report
    txt_filename = os.path.join(output_dir, f"{test_name}_{timestamp}.txt")
    
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("TEST EXECUTION REPORT\n")
        f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Test File: {test_file}\n")
        f.write(f"Model File: {model_file}\n")
        f.write(f"Status: {'✅ PASSED' if success else '❌ FAILED'}\n\n")
        
        f.write("="*80 + "\n")
        f.write("COVERAGE METRICS\n")
        f.write("="*80 + "\n\n")
        
        if coverage:
            f.write(f"Edge Coverage: {coverage.get('edge_coverage', 0):.1f}% ")
            f.write(f"({coverage.get('covered_edges', 0)}/{coverage.get('total_edges', 0)})\n")
            f.write(f"Vertex Coverage: {coverage.get('vertex_coverage', 0):.1f}% ")
            f.write(f"({coverage.get('covered_vertices', 0)}/{coverage.get('total_vertices', 0)})\n")
            
            if 'covered_edge_names' in coverage:
                f.write(f"\nCovered Edges: {', '.join(coverage['covered_edge_names'])}\n")
            if 'uncovered_edge_names' in coverage:
                f.write(f"Uncovered Edges: {', '.join(coverage['uncovered_edge_names'])}\n")
        else:
            f.write("No coverage data available\n")
        
        f.write("\n" + "="*80 + "\n")
    
    print(f"TXT report saved: {txt_filename}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            # Run all test suites in a single LLM directory
            llm_dir = sys.argv[2] if len(sys.argv) > 2 else "graphwalker_test_path_logs"
            print(f"Running all test suites from {llm_dir}...")
            results = run_all_test_suites_in_directory(llm_dir, "json_models", verbose=True)
            
            # Print summary
            passed = sum(1 for r in results.values() if r.get('success', False))
            total = len(results)
            print(f"\n{'='*80}")
            print(f"SUMMARY: {passed}/{total} tests passed")
            print(f"{'='*80}")
        
        elif sys.argv[1] == "--compare":
            # Compare multiple LLM outputs
            if len(sys.argv) < 3:
                print("Usage: python main.py --compare <llm_dir1> <llm_dir2> [llm_dir3] ...")
                print("Example: python main.py --compare Claude-Haiku-4.5/ GPT-4/ Gemini-Pro/")
                sys.exit(1)
            
            llm_dirs = sys.argv[2:]
            print(f"Comparing {len(llm_dirs)} LLM outputs...")
            compare_llm_outputs(llm_dirs, "json_models", verbose=False, save_report=True)
        
        elif sys.argv[1] == "--single":
            # Run single test suite with optional save-report flag
            if len(sys.argv) < 4:
                print("Usage: python main.py --single test_file.txt model.json [--save-report]")
                sys.exit(1)
            
            test_file = sys.argv[2]
            model_file = sys.argv[3]
            save_report = "--save-report" in sys.argv
            
            success, coverage = run_test_suite_from_file(test_file, model_file, verbose=True, save_report=save_report)
            print("\n✅ Test passed!" if success else "\n❌ Test failed!")
        
        else:
            print("Usage:")
            print("  python main.py --all [llm_dir]                          # Run all test suites from one LLM directory")
            print("  python main.py --compare <dir1> <dir2> [dir3]...        # Compare multiple LLM outputs (auto-saves reports)")
            print("  python main.py --single test.txt model.json [--save-report]  # Run single test suite")
            print("\nExamples:")
            print("  python main.py --all Claude-Haiku-4.5/")
            print("  python main.py --compare Claude-Haiku-4.5/ GPT-4/ Gemini-Pro/")
            print("  python main.py --single test.txt model.json --save-report")
    
    else:
        # Default: Run all test suites from graphwalker_test_path_logs
        print("Running all test suites from graphwalker_test_path_logs...")
        results = run_all_test_suites_in_directory("graphwalker_test_path_logs", "json_models", verbose=True)
        
        passed = sum(1 for r in results.values() if r.get('success', False))
        total = len(results)
        print(f"\n{'='*80}")
        print(f"SUMMARY: {passed}/{total} tests passed")
        print(f"{'='*80}")