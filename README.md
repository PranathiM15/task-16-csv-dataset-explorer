# CSV Atlas — Task 16

A small, responsive web application for **loading a CSV dataset with Pandas** and displaying its first and last five records. Built with Python's standard-library HTTP server, Pandas, HTML, CSS, and JavaScript. No Jupyter Notebook, Flask, or database is required.

## Features

- Upload a CSV by file picker or drag and drop.
- Load a public CSV using its direct URL.
- Uses `pandas.read_csv()` to load tabular data.
- Shows the first five records (`DataFrame.head()`) and last five records (`DataFrame.tail()`).
- Shows row count, column count, and total missing values.
- Handles empty files, malformed CSVs, encoding issues, and oversized uploads.
- Responsive custom interface: CSV Atlas.

## Requirements

- Python 3.10 or newer
- Internet connection only for installing Pandas or loading a remote CSV
- Windows PowerShell, Command Prompt, macOS Terminal, or Linux terminal

## Run on Windows PowerShell

1. Extract the ZIP.
2. Open the extracted `task16_csv_dataset_explorer` folder in File Explorer.
3. Click the folder address bar, type `powershell`, and press Enter.
4. Run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

5. Open **http://127.0.0.1:8000** in your browser.
6. Upload any `.csv` file. To stop the server, return to PowerShell and press `Ctrl+C`.

Using `.\.venv\Scripts\python.exe` directly avoids the common PowerShell script execution-policy error that can occur when running `.\.venv\Scripts\Activate.ps1`.

## Run on macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Then visit http://127.0.0.1:8000.

## Quick test dataset

Create a file named `sample_students.csv` in this folder with the following content, then upload it in the app:

```csv
Student,Python,Maths,Attendance
Aarav,88,91,95
Diya,92,89,98
Ishaan,76,84,90
Meera,95,96,99
Kabir,81,78,87
Anaya,89,93,96
Rohan,72,80,85
Sara,97,94,100
```

You should see **8 rows**, **4 columns**, and **0 missing values**. The first five and last five records will appear in separate tables.

## Suggested public dataset sources

Use a direct CSV download URL, not a webpage that merely describes a dataset. Suggested sources include the Iris dataset (CSV copies are available in public repositories), Titanic data, or a student-performance dataset. If a URL fails, download the CSV and upload it locally.

## Project files

- `app.py` — Python web server, CSV upload and Pandas processing
- `requirements.txt` — dependency list
- `README.md` — setup, test instructions, and project documentation
- `.gitignore` — excludes virtual environments and temporary files

## GitHub submission

Create a **Public** repository at https://github.com/new. Suggested repository name: `task-16-csv-dataset-explorer`.

Do not upload `.venv/`. From this project folder, run:

```powershell
git init
git add app.py requirements.txt README.md .gitignore
git commit -m "Build CSV Atlas dataset explorer"
git branch -M main
git remote add origin https://github.com/PranathiM15/task-16-csv-dataset-explorer.git
git push -u origin main
```

If Git says a remote named `origin` already exists, use `git remote -v` to inspect it and correct the URL with:

```powershell
git remote set-url origin https://github.com/PranathiM15/task-16-csv-dataset-explorer.git
```

If GitHub prompts for authentication, finish the browser/device sign-in flow or use Git Credential Manager. Never put a password or access token inside the repository.

## Submission checklist

- [ ] App starts and opens at `http://127.0.0.1:8000`
- [ ] CSV loads successfully
- [ ] First five and last five records are visible
- [ ] README includes setup and project explanation
- [ ] Public GitHub repository contains the project files
- [ ] LinkedIn post is published, as required by the task instructions
- [ ] Submit the public repository URL through the internship portal

## Troubleshooting

**Python command not found:** install Python from https://www.python.org/downloads/ and select “Add Python to PATH”, then reopen the terminal.

**Pandas installation fails:** check your internet connection and try `.\.venv\Scripts\python.exe -m pip install pandas`.

**Port 8000 is busy:** close the other process using it, or change `PORT = 8000` in `app.py` to `PORT = 8001`, then open `http://127.0.0.1:8001`.

**CSV looks incorrect:** ensure the file is comma-separated and has a header row. If using a URL, use the direct raw `.csv` file URL.
