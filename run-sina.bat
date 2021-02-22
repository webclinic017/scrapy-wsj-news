@echo off

:: get currect path
SET currect_path=%~dp0
SET full_path=%currect_path:~0,-1%
:: set env path
SET env_path=%full_path%\venv
:: venv's script
SET venv=%env_path%\Scripts
:: set project path
SET project_path=%full_path%\sina
:: activate venv
SET act=activate
:: run spider
SET run=scrapy crawl sina

cmd /c "cd /d %venv% & %act% & cd /d %project_path% & %run% "
