# LLM4MBT: Large Language Models for Model-Based Testing - Replication Package

This is the replication package for the research paper: **An Empirical Evaluation of Using Large Language Models for Automated Model-Based Test Generation**

## Overview

This package enables researchers to replicate our experiments evaluating how different Large Language Models (LLMs) generate model-based test cases using GraphWalker finite state machine models. The experiments compare coverage effectiveness, test efficiency, and prompt sensitivity across five state-of-the-art LLMs.

---

## Preparation Steps

### Step 1: Install Python 3.13 or Higher

1. Visit the official Python website (https://www.python.org/downloads/)
2. Download the latest Python 3.13+ installer for your operating system
3. Run the installer and follow the installation wizard
4. **Important:** Make sure to check the option "Add Python to PATH" during installation
5. Verify installation by opening a terminal/command prompt and typing:
   ```bash
   python --version
   ```
   You should see Python 3.13.x or higher

### Step 2: Create Python Virtual Environment

After installing Python, create a virtual environment for the project:

1. Open a terminal/command prompt
2. Navigate to the project directory (after cloning, explained in the next section)
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```
5. You should see `(venv)` prefix in your terminal prompt, indicating the virtual environment is active

### Step 3: Install Java Development Kit (JDK) 11 or Higher

GraphWalker requires Java to run.

1. Visit the Oracle JDK download page (https://www.oracle.com/java/technologies/downloads/) or use OpenJDK (https://adoptium.net/)
2. Download and install JDK 11 or higher for your operating system
3. Follow the installation instructions for your platform
4. Verify installation by opening a terminal/command prompt and typing:
   ```bash
   java -version
   ```
   You should see Java version 11 or higher

### Step 4: Install GraphWalker

GraphWalker is the baseline tool we use for model-based testing.

1. Visit the GraphWalker website (https://graphwalker.github.io/)
2. Download the standalone JAR file (graphwalker-cli-4.x.x.jar) from the releases page
3. Place the JAR file in a directory of your choice (e.g., `/usr/local/bin` on macOS/Linux or `C:\GraphWalker` on Windows)
4. Create an alias or add it to your PATH for easier access:
   
   **On macOS/Linux:**
   ```bash
   echo 'alias gw="java -jar /path/to/graphwalker-cli-4.x.x.jar"' >> ~/.zshrc
   source ~/.zshrc
   ```
   
   **On Windows:**
   Add the directory containing the JAR file to your system PATH, or create a batch file `gw.bat`:
   ```batch
   @echo off
   java -jar C:\GraphWalker\graphwalker-cli-4.x.x.jar %*
   ```

5. Verify installation:
   ```bash
   gw --version
   ```

### Step 5: Get Free Access to GitHub Copilot with Multiple LLMs

To replicate our experiments with different LLMs (Claude Opus 4.5, Claude Sonnet 4.5, GPT-5.1, GPT-5.2, Gemini 2.5 Pro), you need access to GitHub Copilot Pro with the education package.

#### 5.1 Activate GitHub Education Pack

1. Visit the GitHub Education page: https://docs.github.com/en/copilot/how-tos/manage-your-account/get-free-access-to-copilot-pro
2. Sign in with your GitHub account
3. Follow the instructions to verify your student or educator status
4. You will need:
   - A valid school/university email address, OR
   - Academic documents proving your affiliation (student ID, enrollment letter, etc.)
5. Once approved, GitHub Copilot Pro will be activated for your account

#### 5.2 Enable Multiple LLM Access in VS Code

1. Install Visual Studio Code from https://code.visualstudio.com/
2. Install the GitHub Copilot extension from the VS Code marketplace
3. Sign in to GitHub Copilot using your GitHub account
4. Once signed in, you can access multiple LLM models through the Copilot chat interface

---

## Cloning the Project

1. Open a terminal/command prompt
2. Navigate to the directory where you want to clone the project
3. Run the following command:
   ```bash
   git clone https://github.com/hafizesanli/LLM4MBT.git
   ```
4. Navigate to the project directory:
   ```bash
   cd LLM4MBT
   ```
5. Create and activate a virtual environment (see Step 2 in Preparation Steps):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # OR
   venv\Scripts\activate  # On Windows
   ```
---

## Project Structure

After cloning, you will see the following important files and directories:

```
LLM4MBT/
├── json_models/                    # GraphWalker FSM models in JSON format
│   ├── TLC.json                    # Traffic Light Controller (simple)
│   ├── Risc-V.json                 # RISC-V CPU (moderate complexity)
│   ├── Parabank.json               # Banking Application (complex)
│   └── Testinium.json              # Test Management Platform (very complex)
├── prompts.json                    # Prompt templates used in experiments
├── QEC-*/                          # Quick Random Edge Coverage results per LLM
├── REC-*/                          # Random Edge Coverage results per LLM
├── VC-*/                           # Vertex Coverage results per LLM
├── graphwalker_test_path_logs_*/   # GraphWalker baseline results
├── comparison_reports/             # Comparison analysis reports
└── test_reports/                   # Individual test execution reports
```

---

## Usage: Replicating Experiments

### Experiment 1: Generate Test Suites with LLMs

This is the core experiment where you use different LLMs to generate test suites.

#### Step 1: Prepare Your GraphWalker Model (Optional - For New Models)

If you want to test with your own GraphWalker model:

1. Create your finite state machine model in JSON format following GraphWalker specifications
2. Place your model file in the `json_models/` folder
3. The model should include vertices (states) and edges (transitions) with proper structure

**Note:** The project already includes four models (TLC, Risc-V, Parabank, Testinium) that you can use directly.

#### Step 2: Open VS Code with the Project

1. Open Visual Studio Code
2. Open the `LLM4MBT` folder: **File → Open Folder** → Select the cloned `LLM4MBT` directory
3. Open the Copilot Chat panel: Press `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Shift+I` (macOS)

#### Step 3: Select Your LLM Model

In the Copilot Chat panel:
1. Click on the model selector (usually shows "GPT-4" or similar)
2. Choose one of the available models:
   - Claude Opus 4.5
   - Claude Sonnet 4.5
   - GPT-5.1
   - GPT-5.2
   - Gemini 2.5 Pro

#### Step 4: Attach Model Files to Chat

1. In the Copilot Chat input area, drag and drop one or more JSON model files from the `json_models/` folder:
   - `TLC.json` (simplest - recommended for first attempt)
   - `Risc-V.json`
   - `Parabank.json`
   - `Testinium.json` (most complex)

#### Step 5: Write Your Prompt

You can either:

**Option A: Copy from prompts.json**
1. Open the `prompts.json` file in VS Code
2. Navigate to the appropriate strategy section (QEC, REC, or VC)
3. Copy a prompt template, for example:
   ```
   You are an expert in Software Testing, specialized in Model-Based Testing, and an expert in the Graphwalker tool. Graphwalker model TLC.json is provided to you. You are tasked with generating graphwalker model-based test cases for this model. You will create a test suite having 100% quick_random edge coverage. Please create the test suite in raw form, as shown in the example below:
   {"currentElementName":"start"} {"currentElementName":"s"} {"currentElementName":"q0"} {"currentElementName":"h"} {"currentElementName":"q8"}
   ```

**Option B: Write Your Own Prompt**

Type directly in the chat input area. Use this template structure:
```
You are an expert in Software Testing, specialized in Model-Based Testing, and an expert in the Graphwalker tool. Graphwalker model [MODEL_NAME].json is provided to you. You are tasked with generating graphwalker model-based test cases for this model and save them in provided txt files. You will create a test suite having 100% [STRATEGY] coverage. Please create the test suite in raw form, as shown in the example below:
{"currentElementName":"start"} {"currentElementName":"s"} {"currentElementName":"q0"} {"currentElementName":"h"} {"currentElementName":"q8"}
```

Replace:
- `[MODEL_NAME]` with: TLC, Risc-V, Parabank, or Testinium
- `[STRATEGY]` with: `quick_random edge`, `random edge`, or `random vertex`

**Important Notes:**
- Always use `quick_random` (with underscore) instead of `quick random` (with space)
- For GPT models, you may need to add: "Don't create a Python script, just give me the test suite in a txt file"

#### Step 6: Prepare Output File and Generate Test Suite

1. **Before writing the prompt**, create a directory and an empty text file for your results:
   - Create a directory for your LLM and strategy (e.g., `QEC-Claude-Opus-4.5/`)
   - Create an empty text file: `[ModelName].txt` (e.g., `TLC.txt`)
   
   Example:
   ```bash
   mkdir QEC-Claude-Opus-4.5
   touch QEC-Claude-Opus-4.5/TLC.txt
   ```

2. **Drag and drop the empty text file** into the Copilot Chat along with your model JSON file:
   - The model JSON file (e.g., `json_models/TLC.json`)
   - The empty output text file (e.g., `QEC-Claude-Opus-4.5/TLC.txt`)

3. **Write and send your prompt** (from Step 5)

4. The LLM will generate the test suite and **automatically write it directly into the text file** you provided

5. After generation, verify the output:
   - Open the text file (e.g., `QEC-Claude-Opus-4.5/TLC.txt`)
   - The content should be a sequence of JSON objects like:
     ```
     {"currentElementName":"v_Start"} {"currentElementName":"e_Init"} {"currentElementName":"v_State1"} ...
     ```

---

### Experiment 2: Analyze Single Test Suite

After generating a test suite with an LLM, you can analyze its coverage and validity using the provided analysis script.

#### Step 1: Generate Baseline with GraphWalker

First, generate a baseline test suite using GraphWalker for comparison:

**Quick Random Edge Coverage:**
```bash
gw offline -m json_models/TLC.json "quick_random(edge_coverage(100))" > graphwalker_test_path_logs_quick/TLC.txt
```

**Random Edge Coverage:**
```bash
gw offline -m json_models/TLC.json "random(edge_coverage(100))" > graphwalker_test_path_logs_edge/TLC.txt
```

**Vertex Coverage:**
```bash
gw offline -m json_models/TLC.json "random(vertex_coverage(100))" > graphwalker_test_path_logs_vertex/TLC.txt
```

Repeat for all models you want to test: TLC, Risc-V, Parabank, Testinium

#### Step 2: Run Single Test Analysis

Use the `--single` flag to analyze a specific test suite. Add `--save-report` flag to save the results to `test_reports/` directory:

```bash
python main.py --single [LLM_DIRECTORY]/[MODEL_NAME].txt json_models/[MODEL_NAME].json --save-report
```

For example:
```bash
python main.py --single QEC-Claude-Opus-4.5/TLC.txt json_models/TLC.json --save-report
```

Or:
```bash
python main.py --single REC-Claude-Sonnet-4.5/Parabank.txt json_models/Parabank.json --save-report
```

This will:
- Analyze the LLM-generated test suite for the specified model
- Calculate vertex and edge coverage
- Count test steps
- Generate a detailed report in `test_reports/` directory (when `--save-report` is used)

**Output:**
The script will create files like:
- `test_reports/REC-GPT-5.2_Testinium.json` - JSON format report
- `test_reports/QEC-Claude-Opus-4.5_TLC.txt` - Readable text report

---

### Experiment 3: Compare Multiple LLM Results

To compare the performance of different LLMs across all models, use the comparison feature.

#### Step 1: Ensure Test Suites are Generated

Make sure you have test suites generated by different LLMs in their respective directories:
- `QEC-Claude-Opus-4.5/`
- `QEC-Claude-Sonnet-4.5/`
- `QEC-GPT-5.1/`
- `QEC-GPT-5.2/`
- `QEC-Gemini-2.5-Pro/`
- etc.

#### Step 2: Run Comparison Analysis

Use the `--compare` flag to compare test suites from different LLM directories:

```bash
python main.py --compare [LLM_DIRECTORY_1]/ [LLM_DIRECTORY_2]/ [LLM_DIRECTORY_3]/ ...
```

For example, to compare two LLM implementations:
```bash
python main.py --compare QEC-Claude-Opus-4.5/ REC-GPT-5.2/
```

Or to compare multiple LLMs:
```bash
python main.py --compare QEC-Claude-Opus-4.5/ QEC-Claude-Sonnet-4.5/ QEC-GPT-5.1/ QEC-GPT-5.2/ QEC-Gemini-2.5-Pro/
```

This will:
- Analyze all test suites in the specified directories
- Compare coverage metrics across different LLMs
- Calculate efficiency metrics (test steps vs. coverage)
- Create comprehensive comparison reports

**Output:**
The script will create:
- `comparison_reports/llm_comparison_YYYYMMDD_HHMMSS.json` - JSON format comparison
- `comparison_reports/llm_comparison_YYYYMMDD_HHMMSS.txt` - Readable comparison report

#### Step 3: Review Comparison Results

Open the generated reports to see:
- **Coverage Comparison**: Vertex and edge coverage for each LLM
- **Efficiency Metrics**: Test steps required by each LLM
- **Performance Rankings**: Which LLMs perform best on which models

---

## Expected Results

When you successfully replicate the experiments, you should observe:

### Coverage Metrics
- **Vertex Coverage**: LLMs achieve ~100% median vertex coverage
- **Edge Coverage**: LLMs achieve ~97.2% median edge coverage
- **GraphWalker Baseline**: 100% coverage but with significantly more test steps

### Test Efficiency
- LLM-generated tests: ~228 median test steps
- GraphWalker Random: ~3166 test steps
- GraphWalker Quick Random: ~420.5 test steps
- **Efficiency Gain**: 13.9× reduction compared to GraphWalker Random

### LLM Performance Variations
- **Claude models**: Most consistent performance across all models
- **GPT models**: Good performance with occasional prompt sensitivity
- **Gemini 2.5 Pro**: High variance, model-specific strengths

---

## Troubleshooting

### Issue: Virtual environment activation fails
**Solution:** 
- On Windows, you may need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Make sure you're in the project directory when creating/activating the virtual environment

### Issue: LLM generates Python code instead of test suite
**Solution:** Add to your prompt: "Don't create a Python script, just give me the test suite directly in the txt file"

### Issue: LLM doesn't understand "quick random"
**Solution:** Use "quick_random" with underscore instead of "quick random" with space

### Issue: GraphWalker command not found
**Solution:** Verify Java installation and GraphWalker JAR file location. Create an alias or add to PATH.

### Issue: main.py script fails to find model files
**Solution:** 
- Ensure you're running the script from the project root directory
- Verify that your model JSON files are in the `json_models/` folder
- Check that test suite files are in the correct LLM-specific directories (e.g., `QEC-Claude-Opus-4.5/`)

### Issue: GitHub Copilot doesn't show multiple LLM options
**Solution:** Ensure you have:
- GitHub Education Pack activated
- GitHub Copilot Pro subscription (free with Education Pack)
- Latest version of VS Code and GitHub Copilot extension
