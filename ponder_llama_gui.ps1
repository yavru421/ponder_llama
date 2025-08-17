# Import necessary assemblies
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Create the main form
$form = New-Object System.Windows.Forms.Form
$form.Text = 'ResearchForge - AI Pipeline GUI'
$form.Size = New-Object System.Drawing.Size(800,700)
$form.StartPosition = 'CenterScreen'
$form.MaximizeBox = $true
$form.MinimizeBox = $true

# Create a TabControl for organizing different functions
$tabControl = New-Object System.Windows.Forms.TabControl
$tabControl.Size = New-Object System.Drawing.Size(780,650)
$tabControl.Location = New-Object System.Drawing.Point(10,10)

# Tab 1: Pipeline Runner
$tabPipeline = New-Object System.Windows.Forms.TabPage
$tabPipeline.Text = 'StepForge Pipeline'

# Pipeline Runner Controls
$labelGoal = New-Object System.Windows.Forms.Label
$labelGoal.Text = 'Goal/Prompt:'
$labelGoal.AutoSize = $true
$labelGoal.Location = New-Object System.Drawing.Point(10,20)

$textBoxGoal = New-Object System.Windows.Forms.TextBox
$textBoxGoal.Multiline = $true
$textBoxGoal.ScrollBars = 'Vertical'
$textBoxGoal.Size = New-Object System.Drawing.Size(740,80)
$textBoxGoal.Location = New-Object System.Drawing.Point(10,45)
$textBoxGoal.Text = 'Research and summarize quantum computing fundamentals'

$labelNegatives = New-Object System.Windows.Forms.Label
$labelNegatives.Text = 'Negatives (what to avoid):'
$labelNegatives.AutoSize = $true
$labelNegatives.Location = New-Object System.Drawing.Point(10,135)

$textBoxNegatives = New-Object System.Windows.Forms.TextBox
$textBoxNegatives.Multiline = $true
$textBoxNegatives.ScrollBars = 'Vertical'
$textBoxNegatives.Size = New-Object System.Drawing.Size(740,60)
$textBoxNegatives.Location = New-Object System.Drawing.Point(10,160)
$textBoxNegatives.Text = 'No opinions, no unverified claims, no print-only scripts'

$labelTools = New-Object System.Windows.Forms.Label
$labelTools.Text = 'Tools/Technologies:'
$labelTools.AutoSize = $true
$labelTools.Location = New-Object System.Drawing.Point(10,230)

$textBoxTools = New-Object System.Windows.Forms.TextBox
$textBoxTools.Size = New-Object System.Drawing.Size(740,25)
$textBoxTools.Location = New-Object System.Drawing.Point(10,255)
$textBoxTools.Text = 'Web search, academic papers, Python, Qiskit'

$labelSearchTerms = New-Object System.Windows.Forms.Label
$labelSearchTerms.Text = 'Search Terms:'
$labelSearchTerms.AutoSize = $true
$labelSearchTerms.Location = New-Object System.Drawing.Point(10,290)

$textBoxSearchTerms = New-Object System.Windows.Forms.TextBox
$textBoxSearchTerms.Size = New-Object System.Drawing.Size(740,25)
$textBoxSearchTerms.Location = New-Object System.Drawing.Point(10,315)
$textBoxSearchTerms.Text = 'quantum computing, qubits, superposition, entanglement'

$labelContextFolder = New-Object System.Windows.Forms.Label
$labelContextFolder.Text = 'Context Folder:'
$labelContextFolder.AutoSize = $true
$labelContextFolder.Location = New-Object System.Drawing.Point(10,350)

$textBoxContextFolder = New-Object System.Windows.Forms.TextBox
$textBoxContextFolder.Size = New-Object System.Drawing.Size(600,25)
$textBoxContextFolder.Location = New-Object System.Drawing.Point(10,375)
$textBoxContextFolder.Text = 'context'

$buttonBrowseContext = New-Object System.Windows.Forms.Button
$buttonBrowseContext.Text = 'Browse'
$buttonBrowseContext.Size = New-Object System.Drawing.Size(80,25)
$buttonBrowseContext.Location = New-Object System.Drawing.Point(620,375)

# StepForge pipeline buttons
$buttonRunStep4 = New-Object System.Windows.Forms.Button
$buttonRunStep4.Text = 'Step 4: Prompt Gen'
$buttonRunStep4.Size = New-Object System.Drawing.Size(140,35)
$buttonRunStep4.Location = New-Object System.Drawing.Point(10,420)
$buttonRunStep4.BackColor = [System.Drawing.Color]::LightBlue

$buttonRunStep3 = New-Object System.Windows.Forms.Button
$buttonRunStep3.Text = 'Step 3: AI Process'
$buttonRunStep3.Size = New-Object System.Drawing.Size(140,35)
$buttonRunStep3.Location = New-Object System.Drawing.Point(160,420)
$buttonRunStep3.BackColor = [System.Drawing.Color]::LightGreen

$buttonRunStep5 = New-Object System.Windows.Forms.Button
$buttonRunStep5.Text = 'Step 5: Action Plan'
$buttonRunStep5.Size = New-Object System.Drawing.Size(140,35)
$buttonRunStep5.Location = New-Object System.Drawing.Point(310,420)
$buttonRunStep5.BackColor = [System.Drawing.Color]::LightYellow

$buttonRunFullPipeline = New-Object System.Windows.Forms.Button
$buttonRunFullPipeline.Text = 'Run Full Pipeline'
$buttonRunFullPipeline.Size = New-Object System.Drawing.Size(160,35)
$buttonRunFullPipeline.Location = New-Object System.Drawing.Point(460,420)
$buttonRunFullPipeline.BackColor = [System.Drawing.Color]::LightCoral
$buttonRunFullPipeline.Font = New-Object System.Drawing.Font('Microsoft Sans Serif', 9, [System.Drawing.FontStyle]::Bold)

# Output display
$labelOutput = New-Object System.Windows.Forms.Label
$labelOutput.Text = 'Pipeline Output:'
$labelOutput.AutoSize = $true
$labelOutput.Location = New-Object System.Drawing.Point(10,470)

$textBoxOutput = New-Object System.Windows.Forms.TextBox
$textBoxOutput.Multiline = $true
$textBoxOutput.ScrollBars = 'Both'
$textBoxOutput.ReadOnly = $true
$textBoxOutput.Size = New-Object System.Drawing.Size(740,120)
$textBoxOutput.Location = New-Object System.Drawing.Point(10,495)
$textBoxOutput.Font = New-Object System.Drawing.Font('Consolas', 9)

# Add controls to Pipeline tab
$tabPipeline.Controls.Add($labelGoal)
$tabPipeline.Controls.Add($textBoxGoal)
$tabPipeline.Controls.Add($labelNegatives)
$tabPipeline.Controls.Add($textBoxNegatives)
$tabPipeline.Controls.Add($labelTools)
$tabPipeline.Controls.Add($textBoxTools)
$tabPipeline.Controls.Add($labelSearchTerms)
$tabPipeline.Controls.Add($textBoxSearchTerms)
$tabPipeline.Controls.Add($labelContextFolder)
$tabPipeline.Controls.Add($textBoxContextFolder)
$tabPipeline.Controls.Add($buttonBrowseContext)
$tabPipeline.Controls.Add($buttonRunStep4)
$tabPipeline.Controls.Add($buttonRunStep3)
$tabPipeline.Controls.Add($buttonRunStep5)
$tabPipeline.Controls.Add($buttonRunFullPipeline)
$tabPipeline.Controls.Add($labelOutput)
$tabPipeline.Controls.Add($textBoxOutput)

# Tab 2: File Manager
$tabFiles = New-Object System.Windows.Forms.TabPage
$tabFiles.Text = 'File Manager'

# File Manager Controls
$labelFileTypes = New-Object System.Windows.Forms.Label
$labelFileTypes.Text = 'File Categories:'
$labelFileTypes.AutoSize = $true
$labelFileTypes.Location = New-Object System.Drawing.Point(10,20)

$listBoxFileTypes = New-Object System.Windows.Forms.ListBox
$listBoxFileTypes.Size = New-Object System.Drawing.Size(200,150)
$listBoxFileTypes.Location = New-Object System.Drawing.Point(10,45)
$listBoxFileTypes.Items.AddRange(@('Prompts', 'Output', 'Context', 'Python Scripts', 'Tests', 'All Files'))

$labelFiles = New-Object System.Windows.Forms.Label
$labelFiles.Text = 'Files:'
$labelFiles.AutoSize = $true
$labelFiles.Location = New-Object System.Drawing.Point(230,20)

$listBoxFiles = New-Object System.Windows.Forms.ListBox
$listBoxFiles.Size = New-Object System.Drawing.Size(520,150)
$listBoxFiles.Location = New-Object System.Drawing.Point(230,45)

$buttonOpenFile = New-Object System.Windows.Forms.Button
$buttonOpenFile.Text = 'Open Selected File'
$buttonOpenFile.Size = New-Object System.Drawing.Size(150,30)
$buttonOpenFile.Location = New-Object System.Drawing.Point(10,210)

$buttonOpenFolder = New-Object System.Windows.Forms.Button
$buttonOpenFolder.Text = 'Open Folder'
$buttonOpenFolder.Size = New-Object System.Drawing.Size(150,30)
$buttonOpenFolder.Location = New-Object System.Drawing.Point(170,210)

$buttonRefreshFiles = New-Object System.Windows.Forms.Button
$buttonRefreshFiles.Text = 'Refresh'
$buttonRefreshFiles.Size = New-Object System.Drawing.Size(150,30)
$buttonRefreshFiles.Location = New-Object System.Drawing.Point(330,210)

# File content preview
$labelFileContent = New-Object System.Windows.Forms.Label
$labelFileContent.Text = 'File Preview:'
$labelFileContent.AutoSize = $true
$labelFileContent.Location = New-Object System.Drawing.Point(10,260)

$textBoxFileContent = New-Object System.Windows.Forms.TextBox
$textBoxFileContent.Multiline = $true
$textBoxFileContent.ScrollBars = 'Both'
$textBoxFileContent.ReadOnly = $true
$textBoxFileContent.Size = New-Object System.Drawing.Size(740,320)
$textBoxFileContent.Location = New-Object System.Drawing.Point(10,285)
$textBoxFileContent.Font = New-Object System.Drawing.Font('Consolas', 9)

# Add controls to Files tab
$tabFiles.Controls.Add($labelFileTypes)
$tabFiles.Controls.Add($listBoxFileTypes)
$tabFiles.Controls.Add($labelFiles)
$tabFiles.Controls.Add($listBoxFiles)
$tabFiles.Controls.Add($buttonOpenFile)
$tabFiles.Controls.Add($buttonOpenFolder)
$tabFiles.Controls.Add($buttonRefreshFiles)
$tabFiles.Controls.Add($labelFileContent)
$tabFiles.Controls.Add($textBoxFileContent)

# Tab 3: System Status
$tabStatus = New-Object System.Windows.Forms.TabPage
$tabStatus.Text = 'System Status'

# System Status Controls
$labelSystemInfo = New-Object System.Windows.Forms.Label
$labelSystemInfo.Text = 'System Information:'
$labelSystemInfo.AutoSize = $true
$labelSystemInfo.Location = New-Object System.Drawing.Point(10,20)

$textBoxSystemInfo = New-Object System.Windows.Forms.TextBox
$textBoxSystemInfo.Multiline = $true
$textBoxSystemInfo.ScrollBars = 'Both'
$textBoxSystemInfo.ReadOnly = $true
$textBoxSystemInfo.Size = New-Object System.Drawing.Size(740,200)
$textBoxSystemInfo.Location = New-Object System.Drawing.Point(10,45)
$textBoxSystemInfo.Font = New-Object System.Drawing.Font('Consolas', 9)

$buttonCheckDependencies = New-Object System.Windows.Forms.Button
$buttonCheckDependencies.Text = 'Check Dependencies'
$buttonCheckDependencies.Size = New-Object System.Drawing.Size(150,30)
$buttonCheckDependencies.Location = New-Object System.Drawing.Point(10,260)

$buttonCheckPython = New-Object System.Windows.Forms.Button
$buttonCheckPython.Text = 'Check Python'
$buttonCheckPython.Size = New-Object System.Drawing.Size(150,30)
$buttonCheckPython.Location = New-Object System.Drawing.Point(170,260)

$buttonViewLogs = New-Object System.Windows.Forms.Button
$buttonViewLogs.Text = 'View Latest Output'
$buttonViewLogs.Size = New-Object System.Drawing.Size(150,30)
$buttonViewLogs.Location = New-Object System.Drawing.Point(330,260)

$buttonRunTests = New-Object System.Windows.Forms.Button
$buttonRunTests.Text = 'Run Tests'
$buttonRunTests.Size = New-Object System.Drawing.Size(150,30)
$buttonRunTests.Location = New-Object System.Drawing.Point(490,260)

$labelLatestResults = New-Object System.Windows.Forms.Label
$labelLatestResults.Text = 'Latest Pipeline Results:'
$labelLatestResults.AutoSize = $true
$labelLatestResults.Location = New-Object System.Drawing.Point(10,310)

$textBoxLatestResults = New-Object System.Windows.Forms.TextBox
$textBoxLatestResults.Multiline = $true
$textBoxLatestResults.ScrollBars = 'Both'
$textBoxLatestResults.ReadOnly = $true
$textBoxLatestResults.Size = New-Object System.Drawing.Size(740,270)
$textBoxLatestResults.Location = New-Object System.Drawing.Point(10,335)
$textBoxLatestResults.Font = New-Object System.Drawing.Font('Consolas', 9)

# Add controls to Status tab
$tabStatus.Controls.Add($labelSystemInfo)
$tabStatus.Controls.Add($textBoxSystemInfo)
$tabStatus.Controls.Add($buttonCheckDependencies)
$tabStatus.Controls.Add($buttonCheckPython)
$tabStatus.Controls.Add($buttonViewLogs)
$tabStatus.Controls.Add($buttonRunTests)
$tabStatus.Controls.Add($labelLatestResults)
$tabStatus.Controls.Add($textBoxLatestResults)

# Add tabs to TabControl
$tabControl.TabPages.Add($tabPipeline)
$tabControl.TabPages.Add($tabFiles)
$tabControl.TabPages.Add($tabStatus)

# Add TabControl to form
$form.Controls.Add($tabControl)

# Helper Functions
function Run-PythonScript {
    param([string]$ScriptName, [object]$OutputTextBox)
    try {
        $OutputTextBox.Text += "`n[RUNNING] $ScriptName...`n"
        $OutputTextBox.Refresh()
        
        $process = Start-Process -FilePath "python" -ArgumentList $ScriptName -Wait -PassThru -NoNewWindow -RedirectStandardOutput "temp_output.txt" -RedirectStandardError "temp_error.txt"

        $output = ""
        if (Test-Path "temp_output.txt") {
            $stdOut = Get-Content "temp_output.txt" -Raw
            if ($stdOut) {
                $output += "Output:`n$stdOut`n"
            }
            Remove-Item "temp_output.txt" -ErrorAction SilentlyContinue
        }
        if (Test-Path "temp_error.txt") {
            $error = Get-Content "temp_error.txt" -Raw
            if ($error) {
                $output += "Error:`n$error`n"
            }
            Remove-Item "temp_error.txt" -ErrorAction SilentlyContinue
        }

        if ($process.ExitCode -eq 0) {
            $OutputTextBox.Text += "[SUCCESS] $ScriptName completed`n$output`n"
        } else {
            $OutputTextBox.Text += "[ERROR] $ScriptName failed (Exit Code: $($process.ExitCode))`n$output`n"
        }
        
        $OutputTextBox.SelectionStart = $OutputTextBox.Text.Length
        $OutputTextBox.ScrollToCaret()
        $OutputTextBox.Refresh()
    }
    catch {
        $OutputTextBox.Text += "[EXCEPTION] Error running $ScriptName`: $($_.Exception.Message)`n"
    }
}

function Run-TasksScript {
    param([string]$Task, [object]$OutputTextBox)
    try {
        $OutputTextBox.Text += "`n[RUNNING] python tasks.py $Task...`n"
        $OutputTextBox.Refresh()
        
        $process = Start-Process -FilePath "python" -ArgumentList "tasks.py", $Task -Wait -PassThru -NoNewWindow -RedirectStandardOutput "temp_output.txt" -RedirectStandardError "temp_error.txt"

        $output = ""
        if (Test-Path "temp_output.txt") {
            $stdOut = Get-Content "temp_output.txt" -Raw
            if ($stdOut) {
                $output += "$stdOut`n"
            }
            Remove-Item "temp_output.txt" -ErrorAction SilentlyContinue
        }
        if (Test-Path "temp_error.txt") {
            $error = Get-Content "temp_error.txt" -Raw
            if ($error) {
                $output += "Error: $error`n"
            }
            Remove-Item "temp_error.txt" -ErrorAction SilentlyContinue
        }

        $OutputTextBox.Text += $output
        $OutputTextBox.SelectionStart = $OutputTextBox.Text.Length
        $OutputTextBox.ScrollToCaret()
        $OutputTextBox.Refresh()
    }
    catch {
        $OutputTextBox.Text += "[EXCEPTION] Error running tasks.py $Task`: $($_.Exception.Message)`n"
    }
}

function Get-FilesByCategory {
    param([string]$Category)
    $files = @()
    switch ($Category) {
        'Prompts' { $files = Get-ChildItem -Path "prompts" -Filter "*.json" -ErrorAction SilentlyContinue }
        'Output' { $files = Get-ChildItem -Path "output" -Filter "*.*" -ErrorAction SilentlyContinue }
        'Context' { $files = Get-ChildItem -Path "context" -Filter "*.*" -ErrorAction SilentlyContinue }
        'Python Scripts' { $files = Get-ChildItem -Path "." -Filter "*.py" -ErrorAction SilentlyContinue }
        'Tests' { $files = Get-ChildItem -Path "tests" -Filter "*.py" -ErrorAction SilentlyContinue }
        'All Files' { $files = Get-ChildItem -Path "." -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -notlike "__pycache__*" -and $_.Name -notlike "*.pyc" } }
    }
    return $files
}

function Load-FileContent {
    param([string]$FilePath)
    try {
        if (Test-Path $FilePath) {
            $content = Get-Content $FilePath -Raw -Encoding UTF8
            if ($content.Length -gt 5000) {
                return $content.Substring(0, 5000) + "`n`n... (file truncated, showing first 5000 characters)"
            }
            return $content
        }
        return "File not found or cannot be read."
    }
    catch {
        return "Error reading file: $($_.Exception.Message)"
    }
}

# Event Handlers

# Browse Context Folder
$buttonBrowseContext.Add_Click({
    $folderDialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderDialog.Description = "Select Context Folder"
    $folderDialog.SelectedPath = (Get-Location).Path
    if ($folderDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $textBoxContextFolder.Text = $folderDialog.SelectedPath
    }
})

# StepForge Pipeline Step Runners
$buttonRunStep4.Add_Click({
    $textBoxOutput.Text = "[STEPFORGE] Starting Step 4: Prompt Generation`n"
    Run-PythonScript "four_promptgen.py" $textBoxOutput
})

$buttonRunStep3.Add_Click({
    $textBoxOutput.Text += "`n[STEPFORGE] Starting Step 3: AI Processing`n"
    Run-PythonScript "3.py" $textBoxOutput
})

$buttonRunStep5.Add_Click({
    $textBoxOutput.Text += "`n[STEPFORGE] Starting Step 5: Action Plan Generation`n"
    Run-PythonScript "five_action.py" $textBoxOutput
})

$buttonRunFullPipeline.Add_Click({
    if ([string]::IsNullOrWhiteSpace($textBoxGoal.Text)) {
        [System.Windows.Forms.MessageBox]::Show("Please enter a goal/prompt before running the pipeline.", "Missing Input", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Warning)
        return
    }

    $textBoxOutput.Text = "[STEPFORGE] Starting Full Pipeline`n"
    $textBoxOutput.Text += "Goal: $($textBoxGoal.Text)`n"
    $textBoxOutput.Text += "========================================`n"

    # Run StepForge pipeline in correct order
    Run-PythonScript "four_promptgen.py" $textBoxOutput
    Start-Sleep -Seconds 2
    Run-PythonScript "3.py" $textBoxOutput
    Start-Sleep -Seconds 2
    Run-PythonScript "five_action.py" $textBoxOutput
    
    $textBoxOutput.Text += "`n[STEPFORGE] Pipeline completed! Check output/ folder for results.`n"
})

# File Manager Events
$listBoxFileTypes.Add_SelectedIndexChanged({
    if ($listBoxFileTypes.SelectedItem) {
        $files = Get-FilesByCategory $listBoxFileTypes.SelectedItem
        $listBoxFiles.Items.Clear()
        foreach ($file in $files) {
            $listBoxFiles.Items.Add($file.Name)
        }
    }
})

$listBoxFiles.Add_SelectedIndexChanged({
    if ($listBoxFiles.SelectedItem -and $listBoxFileTypes.SelectedItem) {
        $files = Get-FilesByCategory $listBoxFileTypes.SelectedItem
        $selectedFile = $files | Where-Object { $_.Name -eq $listBoxFiles.SelectedItem }
        if ($selectedFile) {
            $content = Load-FileContent $selectedFile.FullName
            $textBoxFileContent.Text = $content
        }
    }
})

$buttonOpenFile.Add_Click({
    if ($listBoxFiles.SelectedItem -and $listBoxFileTypes.SelectedItem) {
        $files = Get-FilesByCategory $listBoxFileTypes.SelectedItem
        $selectedFile = $files | Where-Object { $_.Name -eq $listBoxFiles.SelectedItem }
        if ($selectedFile) {
            Start-Process -FilePath "notepad.exe" -ArgumentList $selectedFile.FullName
        }
    }
})

$buttonOpenFolder.Add_Click({
    if ($listBoxFileTypes.SelectedItem) {
        $folderPath = switch ($listBoxFileTypes.SelectedItem) {
            'Prompts' { "prompts" }
            'Output' { "output" }
            'Context' { "context" }
            'Tests' { "tests" }
            default { "." }
        }
        if (Test-Path $folderPath) {
            Start-Process -FilePath "explorer.exe" -ArgumentList (Resolve-Path $folderPath).Path
        } else {
            Start-Process -FilePath "explorer.exe" -ArgumentList (Get-Location).Path
        }
    }
})

$buttonRefreshFiles.Add_Click({
    if ($listBoxFileTypes.SelectedItem) {
        $files = Get-FilesByCategory $listBoxFileTypes.SelectedItem
        $listBoxFiles.Items.Clear()
        foreach ($file in $files) {
            $listBoxFiles.Items.Add($file.Name)
        }
    }
})

# System Status Events
$buttonCheckDependencies.Add_Click({
    $textBoxSystemInfo.Text = "Checking dependencies...`n"
    try {
        $pipList = & pip list 2>&1
        $textBoxSystemInfo.Text = "Installed Python packages:`n$pipList"
    }
    catch {
        $textBoxSystemInfo.Text = "Error checking dependencies: $($_.Exception.Message)"
    }
})

$buttonCheckPython.Add_Click({
    $textBoxSystemInfo.Text = "Checking Python installation...`n"
    try {
        $pythonVersion = & python --version 2>&1
        $pythonPath = & python -c "import sys; print(sys.executable)" 2>&1
        $pipVersion = & pip --version 2>&1
        $textBoxSystemInfo.Text = "Python Version: $pythonVersion`nPython Path: $pythonPath`nPip Version: $pipVersion"
    }
    catch {
        $textBoxSystemInfo.Text = "Error checking Python: $($_.Exception.Message)"
    }
})

$buttonViewLogs.Add_Click({
    $latestOutput = ""
    if (Test-Path "output") {
        $latestFile = Get-ChildItem -Path "output" -Filter "*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($latestFile) {
            $latestOutput = Load-FileContent $latestFile.FullName
        }
    }
    $textBoxLatestResults.Text = if ($latestOutput) { $latestOutput } else { "No recent output files found." }
})

$buttonRunTests.Add_Click({
    $textBoxLatestResults.Text = "Running tests...`n"
    Run-TasksScript "test" $textBoxLatestResults
})

# Initialize system status on startup
$textBoxSystemInfo.Text = "🔬 ResearchForge - AI Pipeline System`nWorkspace: $(Get-Location)`nStepForge Methodology Active`nInitialized: $(Get-Date)`n`nReady to run AI-powered research pipelines!"

# Initialize file manager
$listBoxFileTypes.SelectedIndex = 0

# Set initial output text
$textBoxOutput.Text = "🔬 ResearchForge StepForge Pipeline Ready`n`nWelcome to the AI-powered research pipeline!`n`nSteps:`n4. Prompt Generation (four_promptgen.py)`n3. AI Processing (3.py)`n5. Action Plan (five_action.py)`n`nClick 'Run Full Pipeline' to execute all steps.`n"

# Show the form
$form.ShowDialog() | Out-Null