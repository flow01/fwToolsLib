@echo off
setlocal
setlocal enableDelayedExpansion

for /f "tokens=1,2 delims==" %%a in (config/config.ini) do (
if %%a==hou_version set HOUVERSION=%%b
if %%a==hou_dir set HOUDINIDIR=%%b
if %%a==hou_type set HOUTYPE=%%b
if %%a==plugins_to_load set plugins_to_load=%%b
)

SET "HOUDINI_PATH=%plugins_to_load%;&"

SET "HOUDINIEXE=%HOUDINIDIR%\bin\h%HOUTYPE%.exe"

IF "%HOUTYPE%" == "apprentice" (
	SET "HOUDINIEXE=%HOUDINIDIR%\bin\h%HOUTYPE%.exe"
) ELSE (
	IF "%HOUTYPE%" == "indie" (
		SET "HOUDINIEXE=%HOUDINIDIR%\bin\h%HOUTYPE%.exe"
	) ELSE (
		SET "HOUDINIEXE=%HOUDINIDIR%\bin\houdini%HOUTYPE%.exe"
	)
)

START "" /D "%HOUDINIDIR%\bin" /BELOWNORMAL "%HOUDINIEXE%"