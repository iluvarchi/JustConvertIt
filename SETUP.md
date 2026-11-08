Enter the folder: <br>
`cd JustConvertIt/`

Create the virtual environment: <br>
`python -m venv .venv`

If needed, install this using Ubuntu WSL: <br>
`sudo apt update && sudo apt install -y sed`

Inside the folder, activate the environment: <br>
`source venv/Scripts/activate`

Alternatively, run the virtual environment directly: <br>
`source /d/JustConvertIt/.venv/Scripts/activate`

Install the libraries needed: <br>
`pip install -r requirements.txt`

Run the application in the terminal afterwards: <br>
`python main.py`

Deactivate by simply typing: <br>
`deactivate`