#!/bin/bash
set -u
OUT=FETCHED
rm -rf $OUT; mkdir -p $OUT
declare -A F=(
 [handoff]="https://www.dropbox.com/scl/fi/un2ss48t1hj1qsxs8drja/handoff.md.paper"
 [script]="https://www.dropbox.com/scl/fi/y8yhy234bf84lsagbjgqh/script.md.paper"
 [research]="https://www.dropbox.com/scl/fi/ureb43rdr6nfmqjzqtap4/research.md.paper"
 [beatsheet]="https://www.dropbox.com/scl/fi/en44tihauxjebnu2lahd1/beatsheet.md.paper"
)
for k in "${!F[@]}"; do
  base="${F[$k]}"
  for suf in "?dl=1" "?raw=1" "?dl=0" ""; do
    url="${base}${suf}"
    code=$(curl -sL --max-time 60 -A "Mozilla/5.0" -o "$OUT/$k.try" -w "%{http_code}" "$url")
    sz=$(stat -c%s "$OUT/$k.try" 2>/dev/null || echo 0)
    head -c 60 "$OUT/$k.try" | tr -d '\0' > "$OUT/$k.head"
    echo "$k | $suf | HTTP $code | $sz bytes | $(cat "$OUT/$k.head" | head -1)"
    if [ "$code" = "200" ] && [ "$sz" -gt 300 ]; then
      if ! head -c 200 "$OUT/$k.try" | grep -qi "<!DOCTYPE html"; then
        cp "$OUT/$k.try" "$OUT/$k.md"; echo "   ^ SAVED as $k.md"; break
      fi
    fi
  done
done
echo; echo "=== saved ==="; ls -la $OUT/*.md 2>/dev/null
for f in $OUT/*.md; do echo "----- $f -----"; head -60 "$f"; echo; done
