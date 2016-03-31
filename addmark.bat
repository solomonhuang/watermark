@echo off

:loop

if "%1"=="" goto continue

watermark -m mark.jpg -t .2 -i %1 

shift
goto loop

:continue
