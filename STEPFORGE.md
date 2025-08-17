# StepForge: The Indie Dev Methodology for AI-Driven Pipelines

*By John Daniel Dondlinger*

---

## What is StepForge?
StepForge is a methodology for building, automating, and scaling software pipelines using explicit, step-numbered operations. Inspired by the indie dev spirit, StepForge is about clarity, modularity, and creative control—empowering you to build complex, auditable systems with AI-generated code, one step at a time.

---

## Core Principles

1. **Numerical Order of Operations**
   - Every process, file, and script is assigned a step number (e.g., `1_`, `2_`, `3_`).
   - Step numbers define the flow of data and the sequence of execution.
   
2. **Spelled-Out Order of Operations**
   - Every process, file, and script is assigned a step name using spelled-out numbers (e.g., `one_`, `two_`, `three_`).
   - Step names define the flow of data and the sequence of execution.

3. **Separation of Concerns**
   - Each step does one thing well: prompt generation, API call, summarization, etc.
   - Steps are modular and can be swapped, reordered, or extended.

4. **Manifest & Instructions**
   - A central `INSTRUCTIONS.md` (or manifest) documents the pipeline, step-by-step.
   - Every change to the pipeline updates the manifest.

5. **Traceability**
   - All outputs, logs, and artifacts are tagged with their step number and run ID.
   - Debugging and auditing are easy—just follow the numbers.

6. **Indie Dev Spirit**
   - Embrace experimentation, iteration, and creative solutions.
   - The pipeline is yours to hack, remix, and evolve.

---

## How to Implement StepForge

1. **Start with a Manifest**
   - List each step, its purpose, input, and output.
   - Example:
     
     | Step | Script           | Purpose           | Input(s)           | Output(s)           |
     |------|------------------|-------------------|--------------------|---------------------|
     | 4    | four_promptgen.py| Prompt creation   | User input         | four_prompt.json    |
     | 3    | 3.py             | LLaMA API call    | four_prompt.json   | 3_conversation.json |
     | 5    | five_action.py   | Action planning   | 3_conversation.json| five_action.md      |
     | 6    | tasks.py         | Task automation   | All outputs        | Automated workflows |

2. **Name Everything with Step Numbers**
   - Scripts: `four_promptgen.py`, `3.py`, `five_action.py`, etc.
   - Outputs: `prompt_<uuid>.json`, `output_<uuid>.json`, etc.
   - Logs: `conversation_history_<uuid>.json`, etc.

3. **Keep Steps Modular**
   - Each script should be importable and runnable on its own.
   - Use atomic file writes and robust error handling.
   - Example: `module_common.py` provides shared utilities.

4. **Use Unique Run IDs**
   - For batch or multi-user systems, tag all files with a unique run or prompt ID.
   - Example: `prompt_3286beb8-2ed6-42e7-91d3-fb3ef6d96eab.json`

5. **Update the Manifest with Every Change**
   - Add, remove, or reorder steps? Update `INSTRUCTIONS.md` and `STEPFORGE.md`.
   - Document the reasoning behind each change.

6. **Automate the Pipeline**
   - Use a master script or workflow engine to execute steps in order.
   - Each step checks for its input(s) before running.
   - Example: `tasks.py pipeline` runs the complete workflow.

---

## ResearchForge Implementation

ResearchForge demonstrates StepForge principles in action:

### Step Flow
```
User Input → Step 4 (Prompt Gen) → Step 3 (AI Processing) → Step 5 (Action Plan) → Step 6 (Automation)
```

### Key Features
- **Auditable**: Every step is numbered and tracked
- **Modular**: Steps can be run independently
- **Extensible**: Easy to add new steps (e.g., Step 7: Deploy)
- **Traceable**: UUID tracking for all outputs
- **Automated**: Multiple task runners for different environments

### Windows-Native Implementation
- **Batch files**: Simple, reliable automation
- **PowerShell scripts**: Advanced features and error handling
- **Python tasks**: Cross-platform compatibility
- **NPM scripts**: Familiar interface for Node.js developers

---

## Rules & Best Practices

1. **One Thing Per Step**: Each script should have a single, clear purpose
2. **Fail Fast**: Check inputs and dependencies early
3. **Atomic Operations**: Complete or rollback, no partial states
4. **Unique Identifiers**: Use UUIDs for tracking and debugging
5. **Documentation First**: Update docs with every pipeline change
6. **Testing Integration**: Include tests as part of the pipeline
7. **Error Handling**: Graceful failure with clear error messages

---

## Why StepForge?

### Problems It Solves
- **Black Box AI**: Makes AI pipelines transparent and auditable
- **Debugging Nightmares**: Clear step-by-step execution tracking
- **Monolithic Systems**: Breaks complex workflows into manageable pieces
- **Poor Documentation**: Forces documentation as part of the methodology
- **Difficult Testing**: Each step can be tested independently

### Benefits
- **Clarity**: Anyone can understand the pipeline flow
- **Modularity**: Easy to modify, extend, or replace components
- **Debugging**: Issues can be isolated to specific steps
- **Scaling**: Steps can be distributed across systems
- **Quality**: Built-in testing and validation at each step

---

*StepForge: Forge your pipeline, one step at a time.*

**Created by John Daniel Dondlinger** • **Implemented in ResearchForge**