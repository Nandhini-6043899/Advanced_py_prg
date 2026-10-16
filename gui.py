"""
GUI Calculator using Tkinter.
Supports + - * / %, decimals, sign toggle, clear, backspace and keyboard input.
"""
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:  # headless machine: GUI unavailable, but evaluate() can still be tested
    tk = messagebox = None


class Calculator:
    def __init__(self, root):
        self.root = root
        root.title("Calculator")
        root.resizable(False, False)
        root.configure(bg="#1e1e2e")

        self.expression = ""
        self.display_var = tk.StringVar(value="0")

        tk.Label(root, textvariable=self.display_var, anchor="e", font=("Segoe UI", 26, "bold"),
                 bg="#11111b", fg="#cdd6f4", padx=12, pady=18, width=14).grid(
            row=0, column=0, columnspan=4, sticky="nsew", padx=8, pady=(8, 4))

        buttons = [
            ("C", "AC"), ("DEL", "DEL"), ("%", "%"), ("/", "/"),
            ("7", "7"), ("8", "8"), ("9", "9"), ("*", "*"),
            ("4", "4"), ("5", "5"), ("6", "6"), ("-", "-"),
            ("1", "1"), ("2", "2"), ("3", "3"), ("+", "+"),
            ("+/-", "NEG"), ("0", "0"), (".", "."), ("=", "="),
        ]
        for i, (text, cmd) in enumerate(buttons):
            r, c = divmod(i, 4)
            if text in "/*-+":
                bg = "#fab387"
            elif text == "=":
                bg = "#a6e3a1"
            elif text in ("C", "DEL", "%", "+/-"):
                bg = "#89b4fa"
            else:
                bg = "#313244"
            fg = "#11111b" if bg != "#313244" else "#cdd6f4"
            tk.Button(root, text=text, font=("Segoe UI", 16), width=5, height=2, bg=bg, fg=fg,
                      relief="flat", activebackground="#585b70",
                      command=lambda x=cmd: self.on_press(x)).grid(row=r + 1, column=c, padx=4, pady=4)

        root.bind("<Key>", self.on_key)
        root.bind("<Return>", lambda e: self.on_press("="))
        root.bind("<BackSpace>", lambda e: self.on_press("DEL"))
        root.bind("<Escape>", lambda e: self.on_press("AC"))

    def on_key(self, event):
        if event.char in "0123456789.+-*/%":
            self.on_press(event.char)

    def on_press(self, key):
        if key == "AC":
            self.expression = ""
            self.display_var.set("0")
        elif key == "DEL":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression or "0")
        elif key == "NEG":
            self.toggle_sign()
        elif key == "=":
            self.calculate()
        else:
            self.expression += key
            self.display_var.set(self.expression)

    def toggle_sign(self):
        if self.expression.startswith("-"):
            self.expression = self.expression[1:]
        elif self.expression:
            self.expression = "-" + self.expression
        self.display_var.set(self.expression or "0")

    def calculate(self):
        if not self.expression:
            return
        try:
            result = evaluate(self.expression)
            self.expression = format_number(result)
            self.display_var.set(self.expression)
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero")
            self.on_press("AC")
        except Exception:
            messagebox.showerror("Error", "Invalid expression")
            self.on_press("AC")


def evaluate(expr):
    """Safe arithmetic evaluator (no eval) using a small recursive-descent parser."""
    tokens, i = [], 0
    while i < len(expr):
        ch = expr[i]
        if ch.isdigit() or ch == ".":
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == "."):
                j += 1
            tokens.append(float(expr[i:j]))
            i = j
        elif ch in "+-*/%":
            tokens.append(ch)
            i += 1
        else:
            raise ValueError("bad char")
    pos = [0]

    def peek():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def factor():
        t = peek()
        if t == "-":
            pos[0] += 1
            return -factor()
        if t == "+":
            pos[0] += 1
            return factor()
        if isinstance(t, float):
            pos[0] += 1
            return t
        raise ValueError("syntax")

    def term():
        v = factor()
        while peek() in ("*", "/", "%"):
            op = tokens[pos[0]]
            pos[0] += 1
            r = factor()
            v = v * r if op == "*" else v / r if op == "/" else v % r
        return v

    def expr_():
        v = term()
        while peek() in ("+", "-"):
            op = tokens[pos[0]]
            pos[0] += 1
            r = term()
            v = v + r if op == "+" else v - r
        return v

    result = expr_()
    if pos[0] != len(tokens):
        raise ValueError("syntax")
    return result


def format_number(x):
    return str(int(x)) if x == int(x) else str(round(x, 10))


if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        assert evaluate("2+3*4") == 14
        assert evaluate("10/4") == 2.5
        assert evaluate("-5+2") == -3
        assert evaluate("7%3") == 1
        print("Evaluator tests passed.")
    else:
        root = tk.Tk()
        Calculator(root)
        root.mainloop()
