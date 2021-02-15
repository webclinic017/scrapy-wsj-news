@echo off

:: get currect path
SET currect_path=%~dp0
SET full_path=%currect_path:~0,-1%
:: set env path
SET env_path=%full_path%\venv
:: venv's script
SET venv=%env_path%\Scripts
:: set project path
SET project_path=%full_path%\algo
:: activate venv
SET act=activate
:: run spider
SET run=jupyter lab --ip=0.0.0.0 --port=81 --allow-root --NotebookApp.iopub_data_rate_limit=1.0e10

cmd /c "cd /d %venv% & %act% & cd /d %project_path% & %run% "
