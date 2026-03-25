@echo off
REM Windows용 ripgrep 검색 스크립트

if "%~1"=="" (
    echo 사용법: %~n0 ^<검색어^> [옵션]
    echo.
    echo 옵션:
    echo   -t, --type    파일 타입 지정 (md, js, json 등)
    echo   -i, --ignore  대소문자 무시
    echo   -l, --files   파일명만 출력
    echo   -n, --line    라인 번호 표시
    echo   -h, --help    도움말
    exit /b 1
)

set SEARCH_WORD=%~1
set RG_OPTIONS=

:parse_args
if "%~2"=="" goto :search
if "%~2"=="-t" (
    set RG_OPTIONS=%RG_OPTIONS% --type %~3
    shift
    shift
    goto :parse_args
)
if "%~2"=="-i" (
    set RG_OPTIONS=%RG_OPTIONS% -i
    shift
    goto :parse_args
)
if "%~2"=="-l" (
    set RG_OPTIONS=%RG_OPTIONS% -l
    shift
    goto :parse_args
)
if "%~2"=="-n" (
    set RG_OPTIONS=%RG_OPTIONS% -n
    shift
    goto :parse_args
)
if "%~2"=="-h" (
    echo 사용법: %~n0 ^<검색어^> [옵션]
    echo.
    echo 옵션:
    echo   -t, --type    파일 타입 지정 (md, js, json 등)
    echo   -i, --ignore  대소문자 무시
    echo   -l, --files   파일명만 출력
    echo   -n, --line    라인 번호 표시
    echo   -h, --help    도움말
    exit /b 0
)

echo 알 수 없는 옵션: %~2
exit /b 1

:search
echo 검색어: '%SEARCH_WORD%'
echo 옵션: %RG_OPTIONS%
echo ------------------------

if "%RG_OPTIONS%"=="" (
    rg "%SEARCH_WORD%"
) else (
    rg "%SEARCH_WORD%" %RG_OPTIONS%
)