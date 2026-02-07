# LLM4MBT - LLM for Model-Based Testing

A comprehensive framework for testing and comparing Large Language Models (LLMs) on generating GraphWalker model-based test cases with different coverage strategies. This project evaluates how well different LLMs can generate test suites that achieve edge coverage, vertex coverage, or both, for finite state machine models.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Models](#models)
- [Usage](#usage)
  - [Running Single Test Suite](#running-single-test-suite)
  - [Running All Tests from One LLM](#running-all-tests-from-one-llm)
  - [Comparing Multiple LLMs](#comparing-multiple-llms)
- [Test Suite Format](#test-suite-format)
- [Output Reports](#output-reports)
- [Scripts Reference](#scripts-reference)
- [Examples](#examples)

---

## Overview

This project provides tools to:

1. **Generate** GraphWalker model-based test suites using LLMs with different coverage strategies
2. **Execute** test suites against finite state machine models
3. **Validate** test paths and transitions with intelligent fallback recovery
4. **Calculate** edge and vertex coverage metrics
5. **Compare** performance across different LLMs and coverage strategies
6. **Generate** comprehensive reports (JSON and TXT formats)

### Key Features

- Support for multiple GraphWalker models (TLC, Parabank, Testinium, Risc-V)
- Three coverage strategies: Quick Random Edge Coverage (QEC), Random Edge Coverage (REC), and Vertex Coverage (VC)
- Flexible success criteria: Pass with either ≥70% edge coverage OR ≥85% vertex coverage
- Automatic test execution with path validation and restart capability
- Coverage analysis (edge and vertex coverage)
- Multi-LLM and multi-strategy comparison capabilities
- Detailed error reporting and failure recovery
- Both readable (TXT) and (JSON) reports
- Automatic path resolution relative to script location

---

## Project Structure

```
LLM4MBT/
├── main.py                          # Main test execution and comparison engine
├── graph_conversions.py             # JSON model parsing and graph conversion
├── utility_functions.py             # Helper functions for array comparison
├── prompts.json                     # LLM prompts used for test generation
│
├── json_models/                     # GraphWalker JSON models
│   ├── TLC.json                     
│   ├── Parabank.json
│   ├── Risc-V.json                
│   └── Testinium.json               
│
├── graphwalker_test_path_logs_edge/ # Reference edge coverage test suites
│   ├── TLC.txt
│   ├── Parabank.txt
│   ├── Risc-V.txt
│   └── Testinium.txt
│
├── graphwalker_test_path_logs_quick/ # Reference quick random edge coverage test suites
│   ├── TLC.txt
│   ├── Parabank.txt
│   ├── Risc-V.txt
│   └── Testinium.txt
│
├── graphwalker_test_path_logs_vertex/ # Reference vertex coverage test suites
│   ├── TLC.txt
│   ├── Parabank.txt
│   ├── Risc-V.txt
│   └── Testinium.txt
│
├── QEC-{LLM-Name}/                  # Quick Random Edge Coverage (100%) test suites
│   ├── QEC-Claude-Opus-4.5/
│   ├── QEC-Claude-Sonnet-4.5/
│   ├── QEC-GPT-5.1/
│   ├── QEC-GPT-5.2/
│   └── QEC-Gemini-2.5-Pro/
│       ├── TLC.txt
│       ├── Parabank.txt
│       ├── Risc-V.txt
│       └── Testinium.txt
│
├── REC-{LLM-Name}/                  # Random Edge Coverage (100%) test suites
│   ├── REC-Claude-Opus-4.5/
│   ├── REC-Claude-Sonnet-4.5/
│   ├── REC-GPT-5.1/
│   ├── REC-GPT-5.2/
│   └── REC-Gemini-2.5-Pro/
│       ├── TLC.txt
│       ├── Parabank.txt
│       ├── Risc-V.txt
│       └── Testinium.txt
│
├── VC-{LLM-Name}/                   # Vertex Coverage (100%) test suites
│   ├── VC-Claude-Opus-4.5/
│   ├── VC-Claude-Sonnet-4.5/
│   ├── VC-GPT-5.1/
│   ├── VC-GPT-5.2/
│   └── VC-Gemini-2.5-Pro/
│       ├── TLC.txt
│       ├── Parabank.txt
│       ├── Risc-V.txt
│       └── Testinium.txt
│
├── test_reports/                    # Individual test execution reports
│   ├── REC-GPT-5.1_TLC.json
│   ├── REC-GPT-5.1_TLC.txt
│   ├── QEC-Claude-Opus-4.5_Parabank.json
│   └── QEC-Claude-Opus-4.5_Parabank.txt
│
└── comparison_reports/              # Multi-LLM comparison reports
    ├── llm_comparison_20260202_150133.json
    └── llm_comparison_20260202_150133.txt
```

---

## Installation

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Setup

```bash
# Clone the repository
git clone https://github.com/hafizesanli/LLM4MBT.git
cd LLM4MBT

# The project is ready to use - no pip install needed
```

---

## Models

### 1. TLC

- **Vertices**: 10 (start, q0-q8)
- **Edges**: 18 (labeled a-s)
- **Complexity**: Simple finite state machine
- **Use Case**: Basic model for testing fundamental graph traversal

### 2. Risc-V

- **Vertices**: 16
- **Edges**: 36
- **Complexity**: Moderate finite state machine
- **Use Case**: Moderately simple model for testing fundamental graph traversal

### 3. Parabank

- **Vertices**: 75
- **Edges**: 144
- **Modules**: Login, Register, AccountOverview, AccountActivity, FindTransactions, BillPay, TransferFunds, RequestLoan, UpdateContactInfo, OpenNewAccount
- **Complexity**: Complex multi-module application
- **Use Case**: Real-world banking workflow simulation

### 4. Testinium

- **Vertices**: 129
- **Edges**: 259
- **Modules**: Login, Dashboard, Reports, Projects, Scenarios, Suites
- **Complexity**: Large-scale enterprise application
- **Use Case**: Comprehensive test platform with multiple workflows

---

## Usage

### Running Single Test Suite

Test a single LLM-generated test suite against a specific model:

```bash
# Basic usage - Quick Random Edge Coverage
python main.py --single QEC-Claude-Opus-4.5/TLC.txt json_models/TLC.json

# Test Random Edge Coverage with report saving
python main.py --single REC-Claude-Sonnet-4.5/Parabank.txt json_models/Parabank.json --save-report

# Test Vertex Coverage
python main.py --single VC-Gemini-2.5-Pro/Testinium.txt json_models/Testinium.json --save-report
```

**Output:**

- Detailed test execution logs
- Coverage metrics (edge and vertex coverage)
- Success/failure status
- Optional: Saves JSON and TXT reports to `test_reports/`

### Running All Tests from One LLM

Execute all test suites from a single LLM directory:

```bash
# Run all tests from reference edge coverage logs
python main.py --all graphwalker_test_path_logs_edge

# Run all tests from reference vertex coverage logs
python main.py --all graphwalker_test_path_logs_vertex

# Run all tests from Quick Random Edge Coverage - Claude Opus 4.5
python main.py --all QEC-Claude-Opus-4.5/

# Run all tests from Random Edge Coverage - GPT 5.2
python main.py --all REC-GPT-5.2/

# Run all tests from Vertex Coverage - Gemini 2.5 Pro
python main.py --all VC-Gemini-2.5-Pro/
```

**Output:**

```
================================================================================
TESTING LLM OUTPUT FROM: QEC-Claude-Opus-4.5
================================================================================

Running Test: TLC.txt on Model: TLC.json
Edge Coverage: 100.0% (18/18)
Vertex Coverage: 100.0% (10/10)
✅ Test PASSED

Running Test: Parabank.txt on Model: Parabank.json
Edge Coverage: 100.0% (144/144)
Vertex Coverage: 100.0% (75/75)
✅ Test PASSED

Running Test: Testinium.txt on Model: Testinium.json
Edge Coverage: 100.0% (258/258)
Vertex Coverage: 100.0% (129/129)
✅ Test PASSED

================================================================================
SUMMARY: 3/3 tests passed
================================================================================
```

### Comparing Multiple LLMs

Compare performance across multiple LLM outputs with automatic report generation:

```bash
# Compare 2 LLMs with different coverage strategies
python main.py --compare QEC-Claude-Opus-4.5/ REC-GPT-5.2/

# Compare 3 LLMs including vertex coverage
python main.py --compare QEC-Claude-Opus-4.5/ REC-GPT-5.2/ VC-Gemini-2.5-Pro/

# Compare with reference edge coverage
python main.py --compare graphwalker_test_path_logs_edge/ QEC-Claude-Opus-4.5/ REC-GPT-5.2/

# Compare same LLM with different coverage strategies
python main.py --compare QEC-Claude-Opus-4.5/ REC-Claude-Opus-4.5/ VC-Claude-Opus-4.5/
```

**Output:**

- Comprehensive comparison report printed to console
- Automatically saves to `comparison_reports/`:
  - `llm_comparison_YYYYMMDD_HHMMSS.json` 
  - `llm_comparison_YYYYMMDD_HHMMSS.txt` 

**Sample Comparison Report:**

```
================================================================================
LLM COMPARISON REPORT
Generated: 2026-02-02 15:01:33
================================================================================

================================================================================
OVERALL PERFORMANCE BY LLM
================================================================================

QEC-Claude-Opus-4.5 (Quick Random Edge Coverage)
   Success Rate: 100.0% (3/3)
   Avg Edge Coverage: 100.0%
   Avg Vertex Coverage: 100.0%

REC-GPT-5.2 (Random Edge Coverage)
   Success Rate: 100.0% (3/3)
   Avg Edge Coverage: 98.5%
   Avg Vertex Coverage: 97.3%

VC-Gemini-2.5-Pro (Vertex Coverage)
   Success Rate: 100.0% (3/3)
   Avg Edge Coverage: 75.2%
   Avg Vertex Coverage: 95.8%

================================================================================
DETAILED COMPARISON BY TEST FILE
================================================================================

📄 Parabank.txt
--------------------------------------------------------------------------------
   QEC-Claude-Opus-4.5           → ✅ PASS | Edge: 100.0% | Vertex: 100.0%
   REC-GPT-5.2                   → ✅ PASS | Edge:  98.6% | Vertex:  98.7%
   VC-Gemini-2.5-Pro             → ✅ PASS | Edge:  72.9% | Vertex:  92.0%

📄 TLC.txt
--------------------------------------------------------------------------------
   QEC-Claude-Opus-4.5           → ✅ PASS | Edge: 100.0% | Vertex: 100.0%
   REC-GPT-5.2                   → ✅ PASS | Edge: 100.0% | Vertex: 100.0%
   VC-Gemini-2.5-Pro             → ✅ PASS | Edge:  50.0% | Vertex: 100.0%

📄 Testinium.txt
--------------------------------------------------------------------------------
   QEC-Claude-Opus-4.5           → ✅ PASS | Edge: 100.0% | Vertex: 100.0%
   REC-GPT-5.2                   → ✅ PASS | Edge:  96.9% | Vertex:  93.0%
   VC-Gemini-2.5-Pro             → ✅ PASS | Edge:  80.2% | Vertex:  99.2%
```

---

## Test Suite Format

Test suites must be in **raw format** with space-separated JSON objects:

```json
{"currentElementName":"start"} {"currentElementName":"a"} {"currentElementName":"q0"} {"currentElementName":"b"} {"currentElementName":"q1"}
```

### Format Rules:

1. Each element is a JSON object with `"currentElementName"` field
2. Objects are separated by single spaces
3. Elements include both **vertices** (states) and **edges** (transitions)
4. The sequence must follow valid paths in the model

### Example Test Suite (TLC.txt):

```json
{"currentElementName":"start"} {"currentElementName":"s"} {"currentElementName":"q0"} {"currentElementName":"h"} {"currentElementName":"q8"} {"currentElementName":"r"} {"currentElementName":"q7"} {"currentElementName":"p"} {"currentElementName":"q6"}
```

### Identifying Vertices vs Edges:

- **TLC Model**: Vertices start with `q` or are `start` (e.g., `start`, `q0`, `q1`, ..., `q8`); edges are single letters (e.g., `a`, `b`, `c`)
- **Parabank Model**: Vertices have `_v_` prefix (e.g., `Login_v_Start`); edges have `_e_` prefix (e.g., `Login_e_goto_login`)
- **Testinium Model**: Vertices start with `v_` (e.g., `v_Start`, `v_Verify_In_Login_Page`); edges start with `e_` (e.g., `e_click_login`)

---

## Output Reports

### Individual Test Reports

Generated when using `--save-report` flag or `--single` command:

**Location:** `test_reports/`

**Files:**

- `{LLM_Directory}_{ModelName}.json` - Structured data for programmatic access
- `{LLM_Directory}_{ModelName}.txt` - Readable report

**Example filenames:**
- `REC-GPT-5.1_TLC.json` - Test report for GPT-5.1 with REC strategy on TLC model
- `QEC-Claude-Opus-4.5_Parabank.txt` - Test report for Claude Opus with QEC strategy on Parabank model

**Contents:**

```
================================================================================
TEST EXECUTION REPORT
Generated: 2026-01-27 00:56:33
================================================================================

Test File: graphwalker_test_path_logs/TLC.txt
Model File: json_models/TLC.json
Status: ✅ PASSED

================================================================================
COVERAGE METRICS
================================================================================

Edge Coverage: 83.3% (15/18)
Vertex Coverage: 90.0% (9/10)

Covered Edges: a, b, c, d, e, f, g, i, k, l, m, n, o
Uncovered Edges: h, j, p, r, s
```

### Comparison Reports

Automatically generated when using `--compare` command:

**Location:** `comparison_reports/`

**Files:**

- `llm_comparison_{Timestamp}.json` - Structured comparison data
- `llm_comparison_{Timestamp}.txt` - Readable comparison

**JSON Structure:**

```json
{
  "timestamp": "20260127_010056",
  "summary": {
    "Claude-Opus-4.5": {
      "total_tests": 3,
      "passed_tests": 3,
      "failed_tests": 0,
      "success_rate": 100.0,
      "avg_edge_coverage": 99.5,
      "avg_vertex_coverage": 100.0
    }
  },
  "detailed_results": {
    "Claude-Opus-4.5": {
      "TLC.txt": {
        "success": true,
        "coverage": {
          "edge_coverage": 100.0,
          "vertex_coverage": 100.0
        }
      }
    }
  }
}
```

---

## Scripts Reference

### `main.py`

**Main test execution and comparison engine**

**Key Functions:**

| Function                                                                        | Description                                        |
| ------------------------------------------------------------------------------- | -------------------------------------------------- |
| `apply_test_execution_on_model(test_suite, model, verbose)`                     | Execute test suite on a model with path validation |
| `run_test_suite_from_file(test_suite_file, model_file, verbose, save_report)`   | Run a single test file against a model             |
| `run_all_test_suites_in_directory(directory_path, model_directory, verbose)`    | Run all test suites from one LLM directory         |
| `compare_llm_outputs(llm_directories, model_directory, verbose, save_report)`   | Compare multiple LLM outputs                       |
| `parse_test_suite_from_file(file_path)`                                         | Parse test suite from raw format                   |
| `save_single_test_report(test_file, model_file, success, coverage, output_dir)` | Save individual test report                        |
| `save_comparison_reports(comparison_results, output_dir)`                       | Save comparison reports                            |

**Command Line Interface:**

```bash
# Default behavior (runs graphwalker_test_path_logs)
python main.py

# Run all tests from specific directory
python main.py --all <directory>

# Compare multiple LLM outputs
python main.py --compare <dir1> <dir2> [dir3] ...

# Run single test with optional report
python main.py --single <test.txt> <model.json> [--save-report]
```

### `graph_conversions.py`

**JSON model parsing and graph conversion utilities**

**Key Functions:**

| Function                                          | Description                                               |
| ------------------------------------------------- | --------------------------------------------------------- |
| `generate_graph_from_graphwalker_json(file_name)` | Convert GraphWalker JSON to internal graph representation |
| `calculate_coverage(test_suite, model)`           | Calculate edge and vertex coverage metrics                |

**Usage:**

```python
from graph_conversions import generate_graph_from_graphwalker_json, calculate_coverage

# Load model
model = generate_graph_from_graphwalker_json("TLC.json")

# Calculate coverage
coverage = calculate_coverage(test_suite, model)
print(f"Edge Coverage: {coverage['edge_coverage']}%")
```

### `utility_functions.py`

**Helper utility functions**

**Key Functions:**

| Function                                  | Description                                         |
| ----------------------------------------- | --------------------------------------------------- |
| `are_arrays_equal(arr1, arr2)`            | Compare two arrays for equality (order-independent) |
| `get_key_from_value_in_dict(value, dict)` | Reverse dictionary lookup                           |

---

## Examples

### Example 1: Test a New LLM Output

```bash
# 1. Create directories for your LLM with different coverage strategies
mkdir QEC-Claude-Sonnet-4.0/
mkdir REC-GPT-5/
mkdir VC-Gemini-3-Pro/

# 2. Generate test suites using your LLM
# QEC: Generate with quick_random(edge_coverage(100))
# REC: Generate with random(edge_coverage(100))
# VC: Generate with random(vertex_coverage(100))

# 3. Run tests for each strategy
python main.py --all QEC-Claude-Sonnet-4.0/
python main.py --all REC-GPT-5/
python main.py --all VC-Gemini-3-Pro/

# 4. Compare all strategies
python main.py --compare QEC-Claude-Sonnet-4.0/ REC-GPT-5/ VC-Gemini-3-Pro/
```

### Example 2: Debug a Failing Test

```bash
# Run with verbose output
python main.py --single REC-GPT-5.2/TLC.txt json_models/TLC.json

# Example output showing failure:
# ❌ Failed: No path found for: q0 -> q2 via edge 'x'
#    → Failed path: q0 -> q2
#    → Restarting from start...

# If test still passes despite errors, it means coverage threshold was met:
# Edge Coverage: 72.5% (13/18) - Below 70% threshold
# Vertex Coverage: 90.0% (9/10) - Above 85% threshold
# Result: ✅ PASS (Vertex coverage criterion met)
```

### Example 3: Analyze Coverage

```python
from graph_conversions import generate_graph_from_graphwalker_json, calculate_coverage
from main import parse_test_suite_from_file

# Load model and test suite
model = generate_graph_from_graphwalker_json("TLC.json")
test_suite = parse_test_suite_from_file("QEC-Claude-Opus-4.5/TLC.txt")

# Calculate coverage
coverage = calculate_coverage(test_suite, model)

print(f"Edge Coverage: {coverage['edge_coverage']}%")
print(f"Vertex Coverage: {coverage['vertex_coverage']}%")
print(f"Covered Edges: {coverage['covered_edges']}/{coverage['total_edges']}")
print(f"Covered Vertices: {coverage['covered_vertices']}/{coverage['total_vertices']}")

# Check if test would pass
edge_cov = coverage['edge_coverage']
vertex_cov = coverage['vertex_coverage']
passes = (edge_cov >= 70.0) or (vertex_cov >= 85.0)
print(f"Test Result: {'✅ PASS' if passes else '❌ FAIL'}")
```

### Example 4: Batch Testing

```bash
# Test all coverage strategies for all LLMs
for strategy in QEC REC VC; do
    for llm in Claude-Opus-4.5 Claude-Sonnet-4.5 GPT-5.1 GPT-5.2 Gemini-2.5-Pro; do
        echo "Testing $strategy-$llm..."
        python main.py --all $strategy-$llm/
    done
done

# Compare all Quick Random Edge Coverage implementations
python main.py --compare QEC-Claude-Opus-4.5/ QEC-Claude-Sonnet-4.5/ QEC-GPT-5.1/ QEC-GPT-5.2/ QEC-Gemini-2.5-Pro/

# Compare different strategies for the same LLM
python main.py --compare QEC-GPT-5.1/ REC-Gemini-2.5-Pro/ VC-Claude-Sonnet-4.5/
```

---

## How It Works

### Test Execution Flow

1. **Parse Test Suite**: Extract element names from raw format
2. **Load Model**: Convert GraphWalker JSON to internal graph representation
3. **Validate Paths**: Check each transition (vertex → edge → vertex)
4. **Track Coverage**: Record which edges and vertices were visited
5. **Calculate Metrics**: Compute edge and vertex coverage percentages
6. **Generate Report**: Create detailed execution and coverage reports

### Path Validation Logic

```
For each element in test suite:
  1. If element is a vertex:
     - Check if vertex exists in model
     - Find connecting edge from previous vertex

  2. If element is an edge:
     - Check if edge exists in model
     - Verify next element is a target vertex
     - Validate transition: source → edge → target

  3. If path is invalid:
     - Log failure
     - Restart from fallback vertex (start, v_Start, etc.)
     - Continue execution
```

### Coverage Calculation

- **Edge Coverage**: `(covered_edges / total_edges) × 100%`
- **Vertex Coverage**: `(covered_vertices / total_vertices) × 100%`

**Goal**: Achieve 100% edge coverage (all transitions in the model are exercised)

---

## Best Practices

### For LLM Test Generation

1. **Start from the model's start vertex** (e.g., `start`, `v_Start`, `Login_v_Start`)
2. **Use exact vertex and edge names** from the JSON model
3. **Follow the format strictly**: `{"currentElementName":"name"}` with single spaces
4. **Aim for 100% edge coverage**: Ensure all edges are traversed at least once
5. **Use random path algorithm**: Vary the paths to increase robustness

### For Testing

1. **Always start with single test**: `python main.py --single ...` to debug issues
2. **Use verbose mode**: Add `verbose=True` to see detailed execution logs
3. **Check reference first**: Compare with `graphwalker_test_path_logs/` outputs
4. **Save reports**: Use `--save-report` flag for documentation

### For Comparison

1. **Include reference**: Always compare with `graphwalker_test_path_logs_edge/`, `graphwalker_test_path_logs_quick/` or `graphwalker_test_path_logs_vertex/`
2. **Test all models**: Ensure each LLM directory has TLC.txt, Parabank.txt, and Testinium.txt
3. **Analyze coverage**: Focus on both edge and vertex coverage metrics
4. **Compare strategies**: Test the same LLM with different coverage strategies (QEC, REC, VC)
5. **Review failures**: Check the detailed comparison report for specific issues
6. **Understand thresholds**: Remember that tests pass with either ≥70% edge OR ≥85% vertex coverage

---

## Performance Metrics

### Success Criteria

Tests are considered successful if they meet **either** of the following criteria:

- **Edge Coverage ≥ 70%** - Ensures most state transitions are covered
- **Vertex Coverage ≥ 85%** - Ensures most states are visited

This flexible approach recognizes that:
- **Edge Coverage** tests (QEC, REC) focus on transition completeness
- **Vertex Coverage** tests (VC) focus on state exploration
- Both approaches are valuable for comprehensive testing

### Coverage Targets

| Metric          | Target | Good | Acceptable | Pass Threshold |
| --------------- | ------ | ---- | ---------- | -------------- |
| Edge Coverage   | 100%   | ≥95% | ≥85%       | ≥70%           |
| Vertex Coverage | 100%   | ≥95% | ≥90%       | ≥85%           |

### Test Suite Types

| Type | Full Name                    | Primary Goal      | Coverage Focus      |
| ---- | ---------------------------- | ----------------- | ------------------- |
| QEC  | Quick Random Edge Coverage   | 100% Edge         | All transitions     |
| REC  | Random Edge Coverage         | 100% Edge         | All transitions     |
| VC   | Vertex Coverage              | Maximum Vertices  | All states          |

### Common Issues

| Issue               | Cause                                  | Solution                               |
| ------------------- | -------------------------------------- | -------------------------------------- |
| Low edge coverage   | Missing edges in test suite            | Ensure all edges in model are included |
| Invalid transitions | Wrong edge names or non-existent paths | Verify edge names match model exactly  |
| Parse errors        | Incorrect format                       | Check JSON format and spacing          |
| Unknown vertices    | Typos or wrong names                   | Use exact vertex names from model      |

---

## Contributing

To add a new LLM to the comparison:

1. Create directories for each coverage strategy:
   ```bash
   mkdir QEC-Your-LLM-Name/
   mkdir REC-Your-LLM-Name/
   mkdir VC-Your-LLM-Name/
   ```

2. Generate test suites for all three models with each strategy:
   - **QEC**: Use `quick_random(edge_coverage(100))` algorithm
   - **REC**: Use `random(edge_coverage(100))` algorithm  
   - **VC**: Use `random(vertex_coverage(100))` algorithm

3. Save in raw format with exact naming: `TLC.txt`, `Parabank.txt`, `Testinium.txt`

4. Run comprehensive comparison:
   ```bash
   python main.py --compare graphwalker_test_path_logs_edge/ QEC-Your-LLM-Name/ REC-Your-LLM-Name/ VC-Your-LLM-Name/
   ```

---

## License

This project is part of the LLM4MBT research initiative by Hafize Sanlı.

---

## Contact

For questions or issues, please contact with me or open an issue on GitHub.

---

## Acknowledgments

- GraphWalker for model-based testing framework concepts
- Various LLM providers (Claude, GPT, Gemini) for test generation capabilities

---

**Happy Testing!! :) **
