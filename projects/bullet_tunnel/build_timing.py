import json, re
d = json.load(open('audio/transcript_v3.json', encoding='utf8'))
W = [w for s in d['segments'] for w in s['words']]
# chapters/lines from script
ch, lines = 0, []
for l in open('03_script.md', encoding='utf8').read().splitlines():
    if l.startswith('## '): ch += 1; continue
    if l.startswith(('#', '<!--', '     ', '[pause]')) or not l.strip(): continue
    sp, _, meta = l.partition('||')
    lines.append(dict(ch=ch, text=sp.strip(), meta=meta.strip()))
# chapter first-word starts (from the transcript segments)
CH0 = [0.05, 37.17, 83.44, 130.29, 184.82, 233.9, 275.9]
END = d['segments'][-1]['end']
gaps = sorted((W[i]['end'] + W[i+1]['start']) / 2 for i in range(len(W)-1) if W[i+1]['start'] - W[i]['end'] >= 0.22)
def nw(t):  # expected ASR word count: English number words and hyphens count extra
    return len(re.findall(r'\S+', t.replace('-', ' ')))
for c in range(1, 8):
    L = [x for x in lines if x['ch'] == c]
    t0, t1 = CH0[c-1], (CH0[c] if c < 7 else END)
    Wc = [w for w in W if t0 - 0.05 <= w['start'] < t1 - 0.05]
    m, n = len(Wc), len(L)
    tot = sum(nw(x['text']) for x in L)
    e = [m * nw(x['text']) / tot for x in L]
    gap = [Wc[i+1]['start'] - Wc[i]['end'] for i in range(m-1)]   # gap after word i
    INF = 1e9
    # dp[j][i]: lines 0..j-1 cover words 0..i-1
    dp = [[INF]*(m+1) for _ in range(n+1)]; bk = [[0]*(m+1) for _ in range(n+1)]; dp[0][0] = 0
    for j in range(1, n+1):
        for i in range(j, m+1):
            for p in range(j-1, i):
                if dp[j-1][p] >= INF: continue
                cost = dp[j-1][p] + (i-p-e[j-1])**2 / max(e[j-1], 1) - (12*gap[i-1] if j < n and i-1 < len(gap) else 0)
                if cost < dp[j][i]: dp[j][i] = cost; bk[j][i] = p
    cuts, i = [], m
    for j in range(n, 0, -1):
        p = bk[j][i]; cuts.append((p, i)); i = p
    cuts.reverse()
    for x, (p, i) in zip(L, cuts):
        x['start'] = Wc[p]['start']; x['end'] = Wc[i-1]['end']
for i, x in enumerate(lines): x['n'] = i + 1
json.dump(lines, open('shots.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
for x in lines: print(x['n'], x['ch'], round(x['start'], 1), round(x['end'], 1), round(x['end']-x['start'], 1), x['text'][:40])
