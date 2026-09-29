"""Diff revised vs final tex (summary of hunks)."""
import difflib

a = open("/repo/paper_master_revised.tex", encoding="utf-8").readlines()
b = open("/repo/paper_master_final.tex", encoding="utf-8").readlines()
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
n = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal":
        n += 1
        print(f"--- {tag} revised[{i1+1}:{i2}] -> final[{j1+1}:{j2}]")
        for line in a[i1:i2][:4]:
            print("  -", line.rstrip()[:95])
        for line in b[j1:j2][:4]:
            print("  +", line.rstrip()[:95])
print("total hunks:", n)
