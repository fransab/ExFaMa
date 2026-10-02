# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 10:31:46 2026

@author: sabatinofr
"""


from pages.roommate_funcs.cnf import FormulaSRP
from pages.roommate_funcs.sequential_al_graph import Seq as Expl
from pages.ha_funcs.tools import gen_local_xp
from pages.roommate_funcs.explain_mus import SAT_Imp_Graph
from pages.roommate_funcs.display import gendic, displayDic
from pages.roommate_funcs.tools import order_agent_expl
from copy import deepcopy as copy

NAMES = ["Luc","Ana","Paul","Lea","Tom","Julie","Max","Laure","Hugo","Alice"]

def convertlatex(latexprof = ""):
    vars = """
    \begin{align*}
        Luc: \quad \blackobj{Lea}  \succ \whiteobj{Tom}  \succ \whiteobj{Julie}  \succ \whiteobj{Ana}  \succ \whiteobj{Paul} \\
        Ana: \quad \whiteobj{Paul}  \succ \whiteobj{Julie}  \succ \whiteobj{Tom}  \succ \whiteobj{Lea}  \succ \whiteobj{Luc} \\
        Paul: \quad \whiteobj{Ana}  \succ \whiteobj{Lea}  \succ \whiteobj{Tom}  \succ \whiteobj{Luc}  \succ \whiteobj{Julie} \\
        Lea: \quad \blackobj{Luc}  \succ \whiteobj{Paul}  \succ \whiteobj{Ana}  \succ \whiteobj{Tom}  \succ \whiteobj{Julie} \\
        Tom: \quad \whiteobj{Julie}  \succ \whiteobj{Luc}  \succ \whiteobj{Ana}  \succ \whiteobj{Paul}  \succ \whiteobj{Lea} \\
        Julie: \quad \whiteobj{Tom}  \succ \whiteobj{Ana}  \succ \whiteobj{Paul}  \succ \whiteobj{Luc}  \succ \whiteobj{Lea} \\
    \end{align*}
    """
    vars = latexprof if latexprof != "" else vars
    val = [[ag for i,ag in enumerate(el.strip().split()) if i%2 == 0] for el in vars.split("\n")]
    val = val[2:-2]
    p = []
    o = {}
    for i,el in enumerate(val):
        prefprof = []
        name = el[0][:-1]
        assert NAMES.index(name) == i 

        prefs = el[1:]
        for pref in prefs:
            pref = pref.split("{")
            _type, name = pref
            name = name[:-1]
            indx = NAMES.index(name)
            prefprof.append( indx )
            print(pref)
            if _type != "\\whiteobj":
                o[i] = indx
        p.append(prefprof)
    return p,o

instance = """
\begin{align*}
    Luc: \quad \blackobj{Julie}  \succ \whiteobj{Lea}  \succ \whiteobj{Paul}  \succ \whiteobj{Ana}  \succ \whiteobj{Tom} \\
    Ana: \quad \whiteobj{Julie}  \succ \whiteobj{Luc}  \succ \whiteobj{Paul}  \succ \blackobj{Tom}  \succ \whiteobj{Lea} \\
    Paul: \quad \blackobj{Lea}  \succ \whiteobj{Julie}  \succ \whiteobj{Ana}  \succ \whiteobj{Tom}  \succ \whiteobj{Luc} \\
    Lea: \quad \blackobj{Paul}  \succ \whiteobj{Tom}  \succ \whiteobj{Luc}  \succ \whiteobj{Julie}  \succ \whiteobj{Ana} \\
    Tom: \quad \whiteobj{Julie}  \succ \whiteobj{Luc}  \succ \whiteobj{Lea}  \succ \whiteobj{Paul}  \succ \blackobj{Ana} \\
    Julie: \quad \blackobj{Luc}  \succ \whiteobj{Paul}  \succ \whiteobj{Lea}  \succ \whiteobj{Ana}  \succ \whiteobj{Tom} \\
\end{align*}
"""
# print('***************')
# print(convertlatex(instance))

def convert(ex):
    ex = ex.split("\n")
    first = ex[:][1]
    ex = ex[3:]
    text = [f"st.write({first})"]
    nbtab = 0 

    for line in ex:
        line = line.strip()
        check = line.split(" ")
        print(check)
        if check[0] == "\\item":    
            line = line.replace("\\item","")
            print("yes")
            if len(check) > 1 and check[1] == "Assume":
                text.append("\t"*nbtab + f"st.write(\"-{line}\")")
            else:
                text.append("\t"*nbtab + f"st.write(\"{line}\")")
        if check[0] == "\\begin{itemize}":
            print("yesitem")
            text.append("\t"*nbtab +"with st.expander(\"Why not?\"):")
            nbtab += 1
        if check[0] == "\\end{itemize}":
            nbtab -= 1
    print("=====================")
    print("====convert expl=====")
    for el in text:
        print(el)
    return True 
    
expl = r""" 
Julie should be matched with at least one agent. We will show that this is not possible.
\begin{itemize}
    \item Assume Julie is matched with Luc 
    \begin{itemize}
        \item To avoid envy on Julie, Tom must have a partner they prefer over Luc. However, no other agent satisfies that requirement.
    \end{itemize}
    \item Assume Julie is matched with Ana.
    \begin{itemize}
        \item To avoid envy on Julie, Lea must have a partner they prefer over Ana, one among: \{Tom\}
        \begin{itemize}
            \item Assume Lea is matched with Tom
            \begin{itemize}
                \item To avoid envy on Tom, Ana must have a partner they prefer over Lea. However, no other agent satisfies that requirement.
            \end{itemize}
        \end{itemize}
    \end{itemize}
    \item Assume Julie is matched with Paul.
    \begin{itemize}
        \item To avoid envy on Paul, Tom must have a partner they prefer over Luc. However, no other agent satisfies that requirement.
    \end{itemize}
    \item Assume Julie is matched with Lea.
    \begin{itemize}
        \item To avoid envy on Lea, Luc must have a partner they prefer over Julie, one among: \{Paul\}.
        \begin{itemize}
            \item Assume Luc is matched with Paul
            \begin{itemize}
                \item To avoid envy on Paul, Tom must have a partner they prefer over Luc. However, no other agent satisfies that requirement.
            \end{itemize}
        \end{itemize}
    \end{itemize}
    \item Assume Julie is matched with Tom.
    \begin{itemize}
        \item To avoid envy on Julie, Paul must have a partner they prefer over Tom. However, no other agent satisfies that requirement.
    \end{itemize}
\end{itemize}
"""
# ex = convert(expl)


from random import randint
import streamlit as st
from .state import answer_key


def gen_globexp_proc(mus, p, *, key="default", seed=None):
    """Render a fixed questionnaire instance with rerun-free Check popovers.

    Use a distinct key per question. The proof is retained across rating changes
    and navigation; changing the profile, MUS, or seed rebuilds it. An explicit
    seed gives the question a reproducible proof; None chooses one per session.
    The supplied profile and MUS are copied, never changed or recomputed.
    """
    profile = tuple(tuple(row) for row in p)
    clauses = tuple(tuple(sorted(clause)) for clause in mus)
    signature = (profile, clauses, seed)
    state_key = f"evaluation_global_explanation:{key}"
    saved = st.session_state.get(state_key)
    if saved is None or saved["signature"] != signature:
        myseed = randint(1000000, 10000000000) if seed is None else seed
        F = FormulaSRP(len(profile), profile, float("inf"), "res")
        s = Expl(SAT_Imp_Graph([list(c) for c in clauses], F), F, seed=myseed)
        s.start()
        text = copy(s.text[1:])
        text[0] += " We will show that this is not possible."
        explanation = gendic(text, F.n, roommate=True)
        order_agent_expl(explanation)
        saved = {"signature": signature, "seed": myseed,
                 "explanation": explanation, "preferences": F.p}
        st.session_state[state_key] = saved

    return displayDic(saved["explanation"], saved["preferences"],
                      detail_mode="popover", roommate=True)


def gen_locexp_proc(p,m,agent,mus, key = "default"):
    F = FormulaSRP(len(p), p, float("inf"), "res")
    F.add_pref(agent, m[agent])
    text = gen_local_xp(F,agent,m[agent],m, mus)

    state_key = f"evaluation_global_explanation:{key}"

    explanation = gendic(text, F.n, roommate = True)
    preferences = F.p

    profile = tuple(tuple(row) for row in p)
    clauses = tuple(tuple(sorted(clause)) for clause in F.cnf)
    signature = (profile, clauses)

    order_agent_expl(explanation)

    saved = {"signature": signature, "explanation": explanation, "preferences": F.p}
    st.session_state[state_key] = saved

    return displayDic(saved["explanation"], saved["preferences"],
                          detail_mode="popover", roommate=True)

def tebox(key, text=None):
    """Render feedback inside the evaluation page's form; navigation saves it."""
    if text is None:
        text = "Please provide short feedback to justify your choices (required)."
    st.caption(text)
    return st.text_area(
        "What did you think of the algorithm’s explanations?",
        placeholder="What was helpful, confusing, or missing?",
        height=180,
        max_chars=5000,
        key=answer_key(key, "feedback", default=""),
    )
