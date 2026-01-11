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
x = sympy.Symbol('x')
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

problems = [
    lambda: generate_aaa(difficulty),
    lambda: generate_aaa(difficulty),
    # lambda: generate_bbb(3, 3)
]

problem2 = [
    lambda: f"$\\left({sympy.latex(problem1)}\\right)'$",
    lambda: f"$\\int \\left({sympy.latex(problem1)}\\right)dx$",
    # lambda: r"$" + f"{sympy.latex(problem1)}" + r"\text{の行列式}$",

]

problem3 = [
    lambda x: f"  \\item $ \\displaystyle {sympy.latex(x)}$ を微分せよ \n"
]

answers = [
    lambda x: x.diff().simplify(),
    lambda x: x.integrate().simplify(),
    # lambda: problem1.det()
]

answers2 = [
    lambda: f"${sympy.latex(answer1)}$",
    lambda: f"${sympy.latex(answer1)}$",
    # lambda: f"${sympy.latex(answer1)}$"
]

answers3 = [
    lambda x: f"  \\item $ \\displaystyle {sympy.latex(x)}$\n"
]

def generate_aaa(depth):
    if depth > 0:
        parts = [
            x ** random.randint(1, 3),
            sympy.S(random.randint(-9, 9)),
            sympy.sqrt(x),
            sympy.sin(x),
            sympy.cos(x),
            sympy.tan(x),
            sympy.exp(x),
            sympy.log(x),
            generate_aaa(depth-1)
        ]
        comb = [
            lambda: generate_aaa(depth-1) * random.choice(parts),
            lambda: generate_aaa(depth-1) + random.choice(parts),
            lambda: generate_aaa(depth-1).subs(x, random.choice(parts)),
            lambda: generate_aaa(depth-1)/random.choice(parts)
        ]
        return random.choice(comb)()
    else:
        return sympy.S(1)

def generate_bbb(i, j):
    return sympy.Matrix([[generate_aaa(difficulty) for b in range(i)] for a in range(j)])

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
                    answer1 = answers[mode](problem1)
                    ax.text(0.5, 0.5, problem2[mode](), fontsize=20, ha='center', va='center')
                    label.config(text=f"Problem{i/2}")
                    start_time = time.time()
                    break
                except Exception as e:
                    print("えらー1: ", e)
        else:
            ax.text(0.5, 0.5, answers2[mode](), fontsize=20, ha='center', va='center')
            label.config(text=f"Answer{(i-1)/2}")
            print(time.time()-start_time)
        canvas.draw()
        i += 1

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
                answs += answers3[mode](answers[mode](prob))
                latex_content += problem3[mode](prob)
                break
            except Exception as e:
                print("えらー", e)
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

# async def chat():
#     client = ollama.AsyncClient()
#     async for part in await client.generate("qwen3-vl:4b-instruct", "この計算を使う文章問題を作成してください。\n\n$y=" + sympy.latex(test2) + "$を微分すると\n$y'=" + sympy.latex(sympy.diff(test2, x)) + "$", stream=True):
#         print(part['response'], end='', flush=True)

# asyncio.run(chat())

