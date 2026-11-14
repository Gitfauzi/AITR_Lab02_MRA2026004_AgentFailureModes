import re

with open(r'C:\Users\Sachin Kumar\.gemini\antigravity\scratch\AITR_Lab02_MRA2026004_AgentFailureModes\paper\main.tex', 'r', encoding='utf-8') as f:
    tex = f.read()

opens  = tex.count(r'\begin{')
closes = tex.count(r'\end{')
lines  = len(tex.splitlines())
figs   = tex.count(r'\begin{figure')
tabs   = tex.count(r'\begin{table')
eqs    = tex.count(r'\begin{equation}')
tikz   = tex.count(r'\begin{tikzpicture}')
hyperref = r'\usepackage{hyperref}' in tex
urlpkg   = r'\usepackage{url}' in tex

print('Total lines    :', lines)
print('Env opens      :', opens)
print('Env closes     :', closes)
print('BALANCED       :', opens == closes)
print('Figures        :', figs)
print('TikZ diagrams  :', tikz)
print('Tables         :', tabs)
print('Equations      :', eqs)
print('hyperref pkg   :', hyperref)
print('url pkg        :', urlpkg)

# Check for the duplicate arrow bug in Fig1
bad_arrow = r'\draw[arrow] (state) -- (plan);'
print('Duplicate arrow removed:', bad_arrow not in tex)

# Check legend moved to lower area
legend_safe = '1.75' in tex and '1.42' in tex
print('Legend in safe zone    :', legend_safe)

# Check Fig2 uses grid layout (not deep tree)
fig2_grid = 'boxstyle' in tex
print('Fig2 grid layout       :', fig2_grid)

# Check Fig3 extended x-axis
fig3_extended = '5.8,0' in tex
print('Fig3 extended x-axis   :', fig3_extended)

# Check url fields in bib
with open(r'C:\Users\Sachin Kumar\.gemini\antigravity\scratch\AITR_Lab02_MRA2026004_AgentFailureModes\paper\references.bib', 'r', encoding='utf-8') as f:
    bib = f.read()
url_count = bib.count('url       =')
bib_entries = len(re.findall(r'@\w+\{', bib))
print('BibTeX entries :', bib_entries)
print('URL fields     :', url_count)
print('All refs have URL:', url_count == bib_entries)
