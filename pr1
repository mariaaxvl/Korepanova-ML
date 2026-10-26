# Практика 1
## Задание 1
```
localhost:~# grep -oE '^[^:]+' /etc/passwd | sort

```
## Задание 2
```
localhost:~# cd /etc

localhost:/etc# awk '{print $2, $1}' protocols | sort -nr | head -n 5

localhost:/etc# cd ~
```
## Задание 3
```
localhost:~# nano banner

text="$1"
length=${#text}
line=$(printf '%*s' "$length" ''| tr ' ' '-')
echo "+-${line}-+"
echo "| ${text} |"
echo "+-${line}-+"

localhost:~# chmod +x banner
localhost:~# ./banner "Hello from RTU MIREA!"
```
## Задание 4
```
localhost:~# nano find_ids

filename="$1"
grep -oE '[a-zA-Z_][a-zA-Z0-9_]*' "$filename" | sort -u | xargs

localhost:~# chmod +x find_ids
localhost:~# ./find_ids hello.c
```
## Задание 5
```
localhost:~# nano reg

name="$1"
chmod +x "$name"
cp "$name" /usr/local/bin/

localhost:~# chmod +x reg
localhost:~# ./reg banner
localhost:~# banner "Работает!"
```
## Задание 6
```
localhost:~# nano check_comment

dir="$1"
for f in "$dir"/*.c "$dir"/*.js "$dir"/*.py; do
    [ -f "$f" ] || continue
    first_line=$(head -n 1 "$f")
    case "$f" in
        *.py)
            echo "$first_line" | grep -q '^[[:space:]]*#' && echo "$f: есть комментарий" || echo "$f: нет комментария"
            ;;
        *)
            echo "$first_line" | grep -qE '^[[:space:]]*(//|/\*)' && echo "$f: есть комментарий" || echo "$f: нет комментария"
            ;;
    esac
done

localhost:~# chmod +x check_comment
localhost:~# ./check_comment .
```

## Задание 7
```
localhost:~# nano find_dups

#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <path>"
    exit 1
fi

path="$1"

if [ ! -d "$path" ]; then
    echo "Ошибка: $path - не директория"
    exit 1
fi

find "$path" -type f -exec md5sum {} + | sort | awk '
{
    hash = $1
    $1 = ""
    sub(/^ /, "")
    files[hash] = files[hash] $0 "\n"
    count[hash]++
}
END {
    for (h in count) {
        if (count[h] > 1) {
            printf "Группа дубликатов (хэш %s):\n", h
            printf "%s", files[h]
            print ""
        }
    }
}'

localhost:~# chmod +x find_dups
localhost:~# ./find_dups .

```

## Задание 8
```
localhost:~# nano archive_ext

ext="$1"
tar -cf "archive_${ext}.tar" ./*."$ext"

localhost:~# chmod +x archive_ext
localhost:~# ./archive_ext txt

```

## Задание 9
```
localhost:~# nano spaces2tabs

infile="$1"
outfile="$2"
sed 's/    /\t/g' "$infile" > "$outfile"

localhost:~# chmod +x spaces2tabs
localhost:~# ./spaces2tabs in.txt out.txt

```

## Задание 10
```
localhost:~# nano find_empty

# ищем пустые .txt файлы в каталоге
dir="${1:-.}"
find "$dir" -maxdepth 1 -type f -empty -name "*.txt"

localhost:~# chmod +x find_empty
localhost:~# ./find_empty .

```
