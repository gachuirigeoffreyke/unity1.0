import sys
tpl, seed, out = sys.argv[1:4]
t = open(tpl, encoding="utf-8").read()
s = open(seed, encoding="utf-8").read().replace("</", "<\\/")
assert "/*SEED*/null" in t
open(out, "w", encoding="utf-8").write(t.replace("/*SEED*/null", s))
