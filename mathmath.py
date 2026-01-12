#!/bin/env python3
import sympy
import random
import time
# import ollama
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import asyncio
import click

# 独立変数
x = sympy.Symbol('x')

# 定数
a = sympy.Symbol('a')
b = sympy.Symbol('b')

# 積分定数
C = sympy.Symbol('C')

i = 0
mode = 0
difficulty = 2

root = tk.Tk()

root.title("MathMath")

label = tk.Label(root, text="Press space key to get started... ")
label.pack()

fig = Figure(figsize=(4, 2))
ax = fig.add_subplot(111)
ax.axis('off')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

# client = ollama.Client()

# model = "qwen3-vl:2b-instruct"

problem_kekka = []

sekibun_kekka = [None] * 2
bibun_kekka = [None] * 2

def sekibun():
    global sekibun_kekka
    sekibun_kekka[1] = genexp3(difficulty)
    sekibun_kekka[0] = sekibun_kekka[1].diff(x)
    return sekibun_kekka[0]

def bibun():
    global bibun_kekka
    bibun_kekka[0] = genexp2(difficulty)
    bibun_kekka[1] = bibun_kekka[0].diff(x)
    return bibun_kekka[0]

# 問題生成
problems = [
    bibun,
    sekibun
    # lambda: generate_bbb(3, 3)
]


problem2 = [
    lambda: f"$\\left({sympy.latex(problem1, fold_func_brackets=True)}\\right)'$",
    lambda: f"$\\int \\left({sympy.latex(problem1, fold_func_brackets=True)}\\right)dx$",
    # lambda: r"$" + f"{sympy.latex(problem1)}" + r"\text{の行列式}$",

]

# 最終的なLaTeXで出力される問題の部分
problem3 = [
    lambda x: f"  \\item $ \\displaystyle y = {sympy.latex(x, fold_func_brackets=True)}$ を微分せよ。 \n",
    lambda x: f"  \\item $ \\displaystyle y = {sympy.latex(x, fold_func_brackets=True)}$ を積分せよ。 \n"
]

# 問題を入れると、答えがでてくる
answers = [
    lambda: bibun_kekka[1].together().trigsimp().simplify().cancel(),
    lambda: sekibun_kekka[1].together().cancel().trigsimp().simplify(),
]

answers2 = [
    lambda: f"${sympy.latex(answer1, fold_func_brackets=True)}$",
    lambda: f"${sympy.latex(answer1, fold_func_brackets=True)}$",
    # lambda: f"${sympy.latex(answer1)}$"
]

# 最終的なLaTeXで出力される答えの部分
answers3 = [
    lambda x: f"  \\item $ \\displaystyle {sympy.latex(x, fold_func_brackets=True)}$\n",
    lambda x: f"  \\item $ \\displaystyle {sympy.latex(x, fold_func_brackets=True)}$\n"
]

def genexp(depth):
    if depth > 0:
        parts = [
            x ** random.randint(1, 3),
            a ** random.randint(1, 3),
            b ** random.randint(1, 3),
            sympy.S(random.randint(-9, 9)),
            sympy.sqrt(x),
            sympy.sin(x),
            sympy.cos(x),
            sympy.tan(x),
            sympy.exp(x),
            sympy.log(x),
            genexp(depth-1)
        ]
        comb = [
            lambda: genexp(depth-1) * random.choice(parts),
            lambda: genexp(depth-1) + random.choice(parts),
            lambda: genexp(depth-1).subs(x, random.choice(parts)),
            lambda: genexp(depth-1)/random.choice(parts)
        ]
        return random.choice(comb)()
    else:
        return sympy.S(1)

def genexp2(depth):
    expression = genexp(depth)
    while expression.has(sympy.oo, sympy.zoo, sympy.nan) or x not in expression.free_symbols or expression in problem_kekka:
        expression = genexp(depth)
    return expression

def genexp3(depth):
    expression = genexp(depth)
    constant, dependent = expression.as_independent(x, as_Add=True)
    expression = dependent + C
    while expression.has(sympy.oo, sympy.zoo, sympy.nan) or x not in expression.free_symbols or expression in problem_kekka:
        expression = genexp(depth)
        constant, dependent = expression.as_independent(x, as_Add=True)
        expression = dependent + C
    return expression
        
def generate_bbb(i, j):
    return sympy.Matrix([[genexp(difficulty) for b in range(i)] for a in range(j)])

def aaaa(event):
    global problem1
    global answer1
    global i
    global start_time

    if event.keysym == "space":
        ax.clear()
        ax.axis('off')
        if i % 2 == 0:
            while True:
                try:
                    problem1 = problems[mode]()
                    answer1 = answers[mode]()

                    ax.text(0.5, 0.5, problem2[mode](), fontsize=20, ha='center', va='center')
                    label.config(text=f"Problem{i/2}")
                    start_time = time.time()
                    break
                except Exception as e:
                    pass
        else:
            ax.text(0.5, 0.5, answers2[mode](), fontsize=20, ha='center', va='center')
            label.config(text=f"Answer{(i-1)/2}")
            print(time.time()-start_time)
        canvas.draw()
        i += 1

# def generateKaisetu(prob, answ):
#     return "\\begin{itembox}{解説}\n" + client.generate("qwen3-vl:4b-instruct", f"以下の問題とその解答のについて参考書風の解説を書け。ただし、数式を書く際にはLaTeXを用いること。\n\n# 問題\n{prob}\n\n# 解答\n{answ}") + "\n\\end{itembox}"

@click.group()
def mathmath():
    pass

@mathmath.command()
@click.argument("mode1", type=int)
@click.argument("difficulty1", type=int)
@click.argument("num_prob", type=int)
def genlatex(mode1=0, difficulty1=2, num_prob=50):
    global mode
    global difficulty

    mode = mode1
    difficulty = difficulty1

    latex_content = r"""
    \documentclass{jlreq}
    \usepackage[utf8]{inputenc}
    \usepackage{amsmath, amssymb}
    \usepackage{ascmac}
    \title{数学問題集D""" + str(difficulty) + "M" + str(mode) + r"""}
    \author{Automatic Math Problem Generating System by Fujita}
    \begin{document}
    \maketitle
    \section{問題}
    \begin{enumerate}
    """
    answs = ""

    for j in range(num_prob):
        while True:
            try:
                prob = problems[mode]()
                prob2 = problem3[mode](prob)

                problem_kekka.append(prob)

                ans = answers[mode]()
                ans2 = answers3[mode](ans)

                # ans2 += generateKaisetu(prob2, ans2)

                answs += ans2
                latex_content += prob2

                break
            except Exception as e:
                pass
                # print(e)
    latex_content += r"""
    \end{enumerate}
    """

    latex_content += r"""
    \section{解答}
    \begin{enumerate}
    """ + answs + r"""
    \end{enumerate}
    \end{document}
    """
    print(latex_content)

@mathmath.command()
@click.argument("mode1", type=int)
@click.argument("difficulty1", type=int)
def interactive(mode1=0, difficulty1=2):
    global mode
    global difficulty

    mode = mode1
    difficulty = difficulty1

    root.bind("<Key>", aaaa)
    root.mainloop()

def main():
    mathmath()

if __name__ == "__main__":
    main()
