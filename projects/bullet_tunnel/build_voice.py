# Chips recipe for arnav: the SAME brief on EVERY line (one tone/pitch whole film); blank line between chapters.
import re
BRIEF = '[a friendly explainer, steady energy, one even tone and pitch throughout]'
out, para = [], []
def flush():
    global para
    if para: out.append('\n'.join(para)); para = []
for l in open('03_script.md', encoding='utf8').read().splitlines():
    if l.startswith('##') or l.startswith('[pause]'): flush(); continue
    if l.startswith(('#', '<!--', '     ')) or not l.strip(): continue
    para.append(BRIEF + ' ' + l.split('||')[0].strip())
flush()
text = '\n\n'.join(out)
n = sum(len(p.splitlines()) for p in out)
assert text.count(BRIEF) == n and not re.search(r'\d', text)
open('audio/voice_text_v2.txt', 'w', encoding='utf8').write(text)
print(len(out), 'paragraphs', n, 'lines', len(text), 'chars')
