#!/usr/bin/env python3
"""Simple Unicode-aware beat-duration estimate; not a hook scorer or voice aligner.
Usage: python hindi-beat-timer.py script.txt --wpm 150 --json
Keep each beat on its own line. --wpm is a rough editable assumption.
"""
import argparse,json,unicodedata

def words(text):
    out=[]; buf=[]
    for ch in text:
        cat=unicodedata.category(ch)
        if cat[0] in ('L','M','N') or (ch in ("'",'’','-') and buf):
            buf.append(ch)
        elif buf:
            out.append(''.join(buf).strip("'’-"));buf=[]
    if buf:out.append(''.join(buf).strip("'’-"))
    return [x for x in out if x]

def analyze(text,wpm):
    beats=[];elapsed=0.0
    for line in text.splitlines():
        line=line.strip()
        if not line:continue
        count=len(words(line));sec=count*60/wpm
        beats.append({'line':line,'words':count,'start_seconds':round(elapsed,2),'estimated_seconds':round(sec,2)})
        elapsed+=sec
    return {'wpm_assumed':wpm,'total_words':sum(b['words'] for b in beats),'estimated_seconds':round(elapsed,2),'notes':['Rough estimate only; measure real VO before final edit.','The WPM assumption is not calibrated for every speaker or language.'],'beats':beats}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('script');p.add_argument('--wpm',type=float,default=150);p.add_argument('--json',action='store_true');a=p.parse_args()
    if not 40<=a.wpm<=300:p.error('wpm must be between 40 and 300')
    with open(a.script,encoding='utf-8') as f: result=analyze(f.read(),a.wpm)
    if a.json:print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print(f"अनुमान: {result['total_words']} शब्द / {result['estimated_seconds']} सेकंड (assumed {a.wpm:g} WPM)")
        for b in result['beats']: print(f"{b['start_seconds']:>6.2f}s +{b['estimated_seconds']:.2f}s | {b['line']}")
        print('अनुमान मात्र; अंतिम timing वास्तविक रिकॉर्डिंग से मापें।')
if __name__=='__main__':main()
