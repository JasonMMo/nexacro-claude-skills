#!/bin/bash

# 로컬 자료 검색 스크립트
# ripgrep을 사용한 효율적인 검색

# 사용법: ./search.sh <검색어> [옵션]

if [ $# -eq 0 ]; then
    echo "사용법: $0 <검색어> [옵션]"
    echo ""
    echo "옵션:"
    echo "  -t, --type    파일 타입 지정 (md, js, json 등)"
    echo "  -i, --ignore  대소문자 무시"
    echo "  -l, --files   파일명만 출력"
    echo "  -n, --line    라인 번호 표시"
    echo "  -h, --help    도움말"
    exit 1
fi

SEARCH_WORD="$1"
shift

# 기본 옵션
RG_OPTIONS=""

while [ $# -gt 0 ]; do
    case $1 in
        -t|--type)
            RG_OPTIONS="$RG_OPTIONS --type $2"
            shift 2
            ;;
        -i|--ignore)
            RG_OPTIONS="$RG_OPTIONS -i"
            shift
            ;;
        -l|--files)
            RG_OPTIONS="$RG_OPTIONS -l"
            shift
            ;;
        -n|--line)
            RG_OPTIONS="$RG_OPTIONS -n"
            shift
            ;;
        -h|--help)
            echo "사용법: $0 <검색어> [옵션]"
            echo ""
            echo "옵션:"
            echo "  -t, --type    파일 타입 지정 (md, js, json 등)"
            echo "  -i, --ignore  대소문자 무시"
            echo "  -l, --files   파일명만 출력"
            echo "  -n, --line    라인 번호 표시"
            exit 0
            ;;
        *)
            echo "알 수 없는 옵션: $1"
            exit 1
            ;;
    esac
done

# 검색 실행
echo "검색어: '$SEARCH_WORD'"
echo "옵션: $RG_OPTIONS"
echo "------------------------"

# 현재 디렉토리에서 검색
if [ -z "$RG_OPTIONS" ]; then
    rg "$SEARCH_WORD"
else
    rg "$SEARCH_WORD" $RG_OPTIONS
fi