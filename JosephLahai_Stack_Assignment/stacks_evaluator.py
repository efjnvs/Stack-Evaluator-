# stacks_evaluator.py
# Simple stack-based expression evaluator

def tokenize(s):
    tokens = []
    num = ""
    for ch in s:
        if ch.isdigit() or ch == '.':
            num += ch
        else:
            if num:
                tokens.append(num); num = ""
            if ch in "+-*/()":
                tokens.append(ch)
    if num:
        tokens.append(num)
    return tokens

def prec(op):
    if op in "+-": return 1
    if op in "*/": return 2
    return 0

def to_postfix(tokens):
    out = []
    st = []
    for t in tokens:
        if t.replace('.', '', 1).isdigit():
            out.append(t)
        elif t == '(':
            st.append(t)
        elif t == ')':
            while st and st[-1] != '(':
                out.append(st.pop())
            if st: st.pop()
        else:
            while st and prec(st[-1]) >= prec(t):
                out.append(st.pop())
            st.append(t)
    while st:
        out.append(st.pop())
    return out

def eval_postfix(tokens):
    st = []
    for t in tokens:
        if t.replace('.', '', 1).isdigit():
            st.append(float(t))
        else:
            b = st.pop(); a = st.pop()
            if t == '+': st.append(a + b)
            elif t == '-': st.append(a - b)
            elif t == '*': st.append(a * b)
            elif t == '/':
                if b == 0:
                    raise ZeroDivisionError("division by zero")
                st.append(a / b)
    res = st.pop()
    if abs(res - round(res)) < 1e-9:
        return int(round(res))
    return res

def process(infile="input.txt", outfile="output.txt", sep="-----"):
    lines = []
    try:
        with open(infile, "r") as f:
            lines = [ln.rstrip("\n") for ln in f]
    except FileNotFoundError:
        print("input.txt not found")
        return

    out_lines = []
    for ln in lines:
        s = ln.strip()
        if s == sep:
            out_lines.append(sep)
        elif s == "":
            out_lines.append("")
        else:
            try:
                toks = tokenize(s)
                pf = to_postfix(toks)
                val = eval_postfix(pf)
                out_lines.append(str(val))
            except Exception as e:
                out_lines.append("ERROR: " + str(e))

    with open(outfile, "w") as f:
        for i, ol in enumerate(out_lines):
            f.write(ol)
            if i != len(out_lines) - 1:
                f.write("\n")
    print("Done — results in", outfile)

if __name__ == "__main__":
    process()
