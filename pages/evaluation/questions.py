import streamlit as st 
from pages.roommate_funcs.display import display_full_profile
from pages.ha_funcs.names import NAMES
from .utilities import gen_globexp_proc, gen_locexp_proc, tebox
from .state import answer_key
from .ordering import question_position
from .summary import render_summary
from .schema import (
    DEMOGRAPHICS_PAGE, DEMOGRAPHIC_LABELS, DEMOGRAPHIC_OPTIONS,
    UNDERSTANDING_CHECK_PAGE, UNDERSTANDING_CHECK_PROMPT, UNDERSTANDING_CHECK_OPTIONS,
)

def demographics():
    st.title("About you")
    st.write("Before the preliminary questions, please tell us a little about yourself.")
    for field, label in DEMOGRAPHIC_LABELS.items():
        with st.container(border=True):
            st.radio(
                label, DEMOGRAPHIC_OPTIONS[field], index=None, horizontal=True,
                key=answer_key(DEMOGRAPHICS_PAGE, field),
            )


def page1():
    # instructions = """
    # In this experiment, we invite you to evaluate an algorithm whose goal is to *explain fair solutions* for the Roommate Matching problem. 
    # In the Roommate Matching problem, individuals need to be paired to share a room according to their preferences over the other individuals.

    # The fairness requirement we consider for a matching is called *rank-envy-freeness* [1], it imposes that no individual A prefers the roommate r(B) of another individual B whereas A ranked r(B) better than what B does in her preferences.

    # We will first introduce you to the concept of rank-envy-freeness with a few examples. Then, we will present to you several instances of the Roommate Matching problem together with a proposed solution, and you will be asked whether you think this solution is \"fair\" and whether our explanations to justify the fairness of this solution convince you.

    
    # [1] Coutance, B., Maddila, P., & Wilczynski, A. (2023, September). Rank-Envy-Freeness in roommate matchings. In 26th European Conference on Artificial Intelligence (ECAI 2023). IOS Press.
    # """
    instructions = """
    In this experiment, we invite you to evaluate an algorithm whose goal is to *explain fair solutions* for the Roommate Matching problem. 
    In this problem, individuals need to be paired to share a room according to their preferences over the other individuals.

    The fairness requirement we consider for a matching is called *rank-envy-freeness* [1], it imposes that no individual A prefers the roommate r(B) of another individual B whereas A ranked r(B) better than what B does in her preferences. A matching is rank-envy-free if no such pair exists. Equal ranks do not create rank-envy.

    We first introduce you to the concept of rank-envy-freeness with a few examples. Then, we will present to you several instances of the Roommate Matching problem that are too contrained to fully satisfy everone, together with an explanation on which constraints are effectively blocking the fairness requirement. You will evaluate whether the explanations help you understand the conclusions and whether you find them convincing.
    
    [1] Coutance, B., Maddila, P., & Wilczynski, A. (2023, September). Rank-Envy-Freeness in roommate matchings. In 26th European Conference on Artificial Intelligence (ECAI 2023). IOS Press.
    """
    instructions
    st.title("Instructions")
    st.markdown(instructions)
def page2():
    instructions = """
    First, we present some examples to make you familiar with the fairness concept of rank-envy-freeness.
    """
    st.title("Preliminary questions")
    st.markdown(instructions)

def page3():
    st.title("Preliminary questions")
    st.subheader("Question 1")
    
    preferences = ((3, 4, 5, 1, 2), (2, 5, 4, 3, 0),(1, 3, 4, 0, 5),(0, 2, 1, 4, 5),(5, 0, 1, 2, 3),(4, 1, 2, 0, 3))
    cols = st.columns([2,1],gap=None)
    with cols[0]:
        st.html(display_full_profile(preferences,matching = {0:1,1:0,  2:3,3:2, 4:5,5:4}))
    with cols[1]:
        with st.container(border=True):
            st.markdown("Is this matching fair in the sense of rank-envy-freeness? ")
            bcols = st.columns(2)
            fair = None 
            with bcols[0]:
                if st.button("Yes"):
                    fair= True 
            with bcols[1]:
                if st.button("No"):
                    fair = False 
            if fair == True:
                st.error("""
                         No, because Paul "legitimately" envies Luc: 

                         Paul prefers the most Ana whereas he is matched with Lea.
                         However, Ana is matched with Luc, who only ranked her as his 4th choice.""")
            if fair == False:
                st.success("""
                           Correct! Paul "legitimately" envies Luc: 
                           
                           Paul prefers the most Ana whereas he is matched with Lea. 
                           However, Ana is matched with Luc, who only ranked her as his 4th choice.""")

def page4():
    st.title("Preliminary questions")
    st.subheader("Question 2")
    
    preferences = [[3, 4, 5, 1, 2], [2, 5, 4, 3, 0], [1, 3, 4, 0, 5], [0, 2, 1, 4, 5], [5, 0, 1, 2, 3], [4, 1, 2, 0, 3]]
    cols = st.columns([2,1],gap=None)
    with cols[0]:
        st.html(display_full_profile(preferences,matching = {0: 4, 1: 2, 2: 1, 3: 5, 4: 0, 5: 3}))
    with cols[1]:
        with st.container(border=True):
            st.markdown("What about this matching? ")
            bcols = st.columns(2)
            fair = None 
            with bcols[0]:
                if st.button("Yes"):
                    fair= True 
            with bcols[1]:
                if st.button("No"):
                    fair = False 
            if fair == True:
                st.error("Still no! Even though Paul doesn't envy Luc anymore, now Lea envies Tom: Tom is matched with Luc, who Lea prefers to her assigned partner, and he ranks Luc worse than Lea does.")
            if fair == False:
                st.success("Correct! Click on yes for more details")

def page5():
    st.title("Preliminary questions")
    st.subheader("Question 3")
    
    preferences = [[3, 4, 5, 1, 2], [2, 5, 4, 3, 0], [1, 3, 4, 0, 5], [0, 2, 1, 4, 5], [5, 0, 1, 2, 3], [4, 1, 2, 0, 3]]
    cols = st.columns([2,1],gap=None)
    with cols[0]:
        st.html(display_full_profile(preferences,matching = {0: 3, 1: 2, 2: 1, 3: 0, 4: 5, 5: 4}))
    with cols[1]:
        with st.container(border=True):
            st.markdown("What about this one? ")
            bcols = st.columns(2)
            fair = None 
            with bcols[0]:
                if st.button("Yes"):
                    fair= True 
            with bcols[1]:
                if st.button("No"):
                    fair = False 
            if fair == True:
                st.success("Yes! It is easy to see that every agent prefers their partner to any other's.")
            if fair == False:
                st.success("Wrong, this matching is fair. Every agent got their preferred partner so they will always prefer their own to any other agents'. ")

def page6(): # other instance
    st.title("Preliminary questions")
    st.subheader("Question 4")
    preferences = [[2, 4, 3, 1, 5], [2, 0, 4, 5, 3], [5, 0, 1, 3, 4], [4, 2, 1, 0, 5], [2, 0, 3, 5, 1], [2, 0, 1, 4, 3]]
    cols = st.columns([2,1],gap=None)
    with cols[0]:
        st.html(display_full_profile(preferences,matching = {0: 4, 1: 3, 2: 5, 3: 1, 4: 0, 5: 2}))
    with cols[1]:
        with st.container(border=True):
            st.markdown("Is this matching fair? ")
            bcols = st.columns(2)
            fair = None 
            with bcols[0]:
                if st.button("Yes"):
                    fair= True 
            with bcols[1]:
                if st.button("No"):
                    fair = False 
            if fair == True:
                st.error("No, Lea envies Luc: he is matched which Tom, whom she prefers over her current partner. Moreover, she ranks Tom better than Luc does, so she feels like it's unfair. ")
            if fair == False:
                st.success("Correct! Click on Yes for more details")

def page7():
    st.title("Preliminary questions")
    st.subheader("Question 5")
    preferences = [[2, 4, 3, 1, 5], [2, 0, 4, 5, 3], [5, 0, 1, 3, 4], [4, 2, 1, 0, 5], [2, 0, 3, 5, 1], [2, 0, 1, 4, 3]]
    cols = st.columns([2,1],gap=None)
    with cols[0]:
        st.html(display_full_profile(preferences,matching = {0: 1, 1: 0, 2: 5, 3: 4, 4: 3, 5: 2}))
    with cols[1]:
        with st.container(border=True):
            st.markdown("What about this one? ")
            bcols = st.columns(2)
            fair = None 
            with bcols[0]:
                if st.button("Yes"):
                    fair= True 
            with bcols[1]:
                if st.button("No"):
                    fair = False 
            if fair == True:
                text = """ 
                This matching is fair. 

                Luc can't get a better partner than Ana without breaking fairness: even though he prefers Lea, her assigned partner Tom ranks her at the same place as Luc does. So it not justified to assign Luc to Ana instead. He also can't get Paul or Tom, since their assigned partner rank them at the first place, so he doesn't rank them better than they do. 

                Similarly, Ana and Tom can't get a better partner than the one they are assigned to. 

                Paul, Lea and Julie are matched with their preferred partner, so they are not envious of other agents. 
                """
                st.success(text)
            if fair == False:
                st.error("This matching is considered fair. Click on Yes to understand why!")

def understanding_check():
    st.title("Preliminary questions")
    st.subheader("Question 6")
    preferences = (
        (5, 4, 1, 2, 3), (0, 3, 2, 4, 5), (5, 4, 3, 1, 0),
        (1, 2, 0, 4, 5), (0, 5, 3, 1, 2), (1, 3, 2, 4, 0),
    )
    matching = {0: 4, 4: 0, 1: 3, 3: 1, 2: 5, 5: 2}
    st.html(display_full_profile(preferences, matching=matching))
    st.write("Julie is dissatisfied with being assigned to their third-choice roommate while all others have seemingly better assignments.")
    # Square checkboxes visually match the PDF. Native radio semantics enforce
    # exactly one selection in the browser, with keyboard support and no rerun.
    # Scope the styling to this group; the Likert radio controls are unaffected.
    st.html("""
        <style>
        .st-key-understanding_check_choices [data-baseweb="radio"] > div:first-child {
            border-radius: 3px;
        }
        .st-key-understanding_check_choices [data-baseweb="radio"] > div:first-child > div {
            border-radius: 2px;
        }
        .st-key-understanding_check_choices [data-baseweb="radio"]:has(input:checked) > div:first-child > div {
            width: 5px !important;
            height: 9px !important;
            background: transparent !important;
            border: solid white;
            border-width: 0 2px 2px 0;
            border-radius: 0;
            transform: translateY(-1px) rotate(45deg);
        }
        </style>
    """)
    with st.container(border=True, key="understanding_check_choices"):
        st.caption("Select one answer.")
        st.radio(
            UNDERSTANDING_CHECK_PROMPT,
            options=tuple(UNDERSTANDING_CHECK_OPTIONS),
            format_func=UNDERSTANDING_CHECK_OPTIONS.__getitem__,
            index=None,
            key=answer_key(UNDERSTANDING_CHECK_PAGE, "answer"),
            width="stretch",
        )


def page8():
    st.title("Preliminary questions")
    prefs = [[4, 1, 3, 2, 5], [0, 5, 4, 2, 3], [4, 3, 0, 1, 5], [0, 4, 5, 1, 2], [3, 1, 0, 5, 2], [1, 0, 4, 3, 2]]
    st.write("Sometimes, preferences are such that no matching exists that satisfies rank-envy-freeness. ")
    st.html(display_full_profile(prefs))
    st.write("At first glance, it seems difficult to understand why this instance have no fair matching. One would have to try every possible matching and check for each of them, that is does not satisfy fairness. To make this easier, we provide an explanation to make it more clear which constraints are responsible for making a fair matching impossible to achieve:")

    st.write("We aim to show that every assignment of this agent to another will eventually violate the fairness constraint, thus making every matching impossible since this agent would have no partner. For this matter, we try individually every possible assignment of this agent to another, and show that it eithers create unfairness, or that another agent can't be matched with agents without generating envy. \n In this case an explanation would be:")

    with st.container(border=True):
        st.write("Luc should be matched with at least one agent. We will show that this is not possible.")
        st.write("- Assume Luc is matched with Ana")
        with st.expander("Why is that not possible ?"):
            st.write("To avoid envy on Luc, Julie must have a partner they prefer over Ana. However, no other agent satisfies that requirement.")
        st.write("- Assume Luc is matched with Paul")
        with st.expander("Why is that not possible ?"):
            st.write("To avoid envy on Paul, Ana must have a partner they prefer over Luc. However, no other agent satisfies that requirement.")
        st.write("- Assume Luc is matched with Lea")
        with st.expander("Why is that not possible ?"):
            st.write("To avoid envy on Luc, Tom must have a partner they prefer over Lea. However, no other agent satisfies that requirement.")
        st.write("- Assume Luc is matched with Tom")
        with st.expander("Why is that not possible ?"):
            st.write("To avoid envy on Tom, Ana must have a partner they prefer over Luc. However, no other agent satisfies that requirement.")
        st.write("- Assume Luc is matched with Julie")
        with st.expander("Why is that not possible ?"):
            st.write("To avoid envy on Julie, Ana must have a partner they prefer over Luc. However, no other agent satisfies that requirement.")


def page9():
    st.title("Questionnaire")
    st.write("Now that it is more clear how fairness and explanations work, you will be presented with some instances of Roommate Matching, with explanations if fair matchings don't exist, and will be asked to evaluate the explanations provided, based on your ease of understanding and relevance of the explanation. Feel free to come back any time to the introductory questions if needed.")

def page10():
    prefs = ((1,2,3,4,5),(0,2,3,4,5),(0,3,1,4,5),(0,4,1,2,5),(0,2,1,3,5),(0,2,1,3,4))
    st.title("Questionnaire")
    st.subheader(f"Question {question_position(1)}")
    st.write("The following instance has no matching satisfying rank-envy-freeness.")
    cols = st.columns(2)
    with cols[0]:
        st.html(display_full_profile(prefs))

    with st.container(border=True):
        st.radio("It is clear to me why there is no fair matching.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page10", "understanding"))

def page11():
    prefs = ((1,2,3,4,5),(0,2,3,4,5),(0,3,1,4,5),(0,4,1,2,5),(0,2,1,3,5),(0,2,1,3,4))
    mus = [[4, 5, 6, 10, 14], [-14, 2], [-6, 7], [-2, -1], [-4, 2], [-5], [-14, 1, 3], [-10, 2], [-4, -2], [-10, 1, 3], [-7, 4], [-3]]
    st.title("Questionnaire")
    st.subheader(f"Question {question_position(1)}")
    st.write("The following instance has no matching satisfying rank-envy-freeness.")
    st.write("We now propose an explanation to, hopefully, make it more clear why this instance admits no fair matching.")
    cols = st.columns(2)
    with cols[0]:
        st.html(display_full_profile(prefs))
    
    with cols[1]:
        with st.container(border = True):
            gen_globexp_proc(mus, prefs, key="page11", seed=11)

    with st.container(border=True):
        st.radio("Now, I understand why there is no fair matching.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page11", "understanding"))
        st.radio("From the explanation, I understand why the proposed assignment can be considered fair.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page11", "algorithm_working"))
        st.radio("The explanation is satisfactory.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page11", "satisfaction"))
        st.radio("The explanation has sufficient detail.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page11", "detail"))
        st.radio("The explanation contains irrelevant details.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page11", "completeness"))
        tebox("page11")

def page12():
    prefs = ((1,2,3,4,5),(2,0,3,4,5),(0,1,3,4,5),(4,5,0,1,2),(5,3,0,1,2),(3,4,0,1,2))
    st.title("Questionnaire")
    st.subheader(f"Question {question_position(2)}")
    st.write("The following instance has no matching satisfying rank-envy-freeness.")
    cols = st.columns(2)
    with cols[0]:
        st.html(display_full_profile(prefs))

    with st.container(border=True):
        st.radio("It is clear to me why there is no fair matching.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page12", "understanding"))

def page13():
    prefs = ((1,2,3,4,5),(2,0,3,4,5),(0,1,3,4,5),(4,5,0,1,2),(5,3,0,1,2),(3,4,0,1,2))
    mus = [[7, 8, 9, 10, 15], [-15], [-10], [-8], [-9], [-7]]
    st.title("Questionnaire")
    st.subheader(f"Question {question_position(2)}")
    st.subheader(f"Question {question_position(1)}")
    st.write("The following instance has no matching satisfying rank-envy-freeness.")

    cols = st.columns(2)
    with cols[0]:
        st.html(display_full_profile(prefs))
    
    with cols[1]:
        with st.container(border = True):
            gen_globexp_proc(mus, prefs, key="page13", seed=11)

    with st.container(border=True):
        st.radio("Now, I understand why there is no fair matching.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page13", "understanding"))
        st.radio("From the explanation, I understand why the proposed assignment can be considered fair.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page13", "algorithm_working"))
        st.radio("The explanation is satisfactory.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page13", "satisfaction"))
        st.radio("The explanation has sufficient detail.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page13", "detail"))
        st.radio("The explanation contains irrelevant details.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page13", "completeness"))
        tebox("page13")

def page14():
    prefs = ((1,2,3,4,5),(2,0,3,4,5),(0,1,3,4,5),(4,5,0,1,2),(5,3,0,1,2),(3,4,0,1,2))
    m = {0:5,1:2,2:1,3:4,4:3,5:0}

    st.title("Questionnaire")
    st.subheader(f"Question {question_position(3)}")
    st.write("The following instance has a matching satisfying rank-envy-freeness. However Luc feels dissatisfied by their assignment and would like to know why they couldn't have a roommate they prefer to their assigned one.")
    cols = st.columns(2)
    with cols[0]:
        st.html(display_full_profile(prefs, matching = m))

    with st.container(border=True):
        st.radio("It is clear to me why Luc cannot have a preferred roommate.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page14", "understanding"))

def page15():
    prefs = ((1,2,3,4,5),(2,0,3,4,5),(0,1,3,4,5),(4,5,0,1,2),(5,3,0,1,2),(3,4,0,1,2))
    m = {0:5,1:2,2:1,3:4,4:3,5:0}
    mus = [[-7], [-1], [-4], [-2], [1, 2, 4, 7]]
    st.title("Questionnaire")
    st.subheader(f"Question {question_position(3)}")
    st.write("The following instance has a matching satisfying rank-envy-freeness. However Luc feels dissatisfied by their assignment and would like to know why they couldn't have a roommate they prefer to their assigned one.")

    cols = st.columns(2)
    with cols[0]:
        st.html(display_full_profile(prefs, matching = m))
    
    with cols[1]:
        with st.container(border = True):
            gen_locexp_proc(prefs, m, 0, mus, key = "page15")

    with st.container(border=True):
        st.radio("Now, I understand why Luc cannot have a preferred roommate.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page15", "understanding"))
        st.radio("From the explanation, I understand why the proposed assignment can be considered fair.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page15", "algorithm_working"))
        st.radio("The explanation is satisfactory.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page15", "satisfaction"))
        st.radio("The explanation has sufficient detail.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page15", "detail"))
        st.radio("The explanation contains irrelevant details.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page15", "completeness"))
        tebox("page15")

def page16():
    prefs = ((2, 5, 4, 1, 3), (2, 0, 4, 5, 3), (4, 0, 5, 1, 3), (2, 0, 4, 5, 1), (2, 0, 5, 1, 3), (2, 1, 4, 0, 3))
    st.title("Questionnaire")
    st.subheader(f"Question {question_position(4)}")
    st.write("The following instance has no matching satisfying rank-envy-freeness.")
    cols = st.columns(2)
    with cols[0]:
        st.html(display_full_profile(prefs))

    with st.container(border=True):
        st.radio("It is clear to me why there is no fair matching.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page16", "understanding"))

def page17():
    prefs = ((2, 5, 4, 1, 3), (2, 0, 4, 5, 3), (4, 0, 5, 1, 3), (2, 0, 4, 5, 1), (2, 0, 5, 1, 3), (2, 1, 4, 0, 3))
    mus = [[11, 12, 13, 14, 15], [-14, 2], [-11, 3], [-9, -2], [-13, 2], [-15], [-14, 7, 9], [-12, 2], [-13, -2], [-12, 7, 9], [-3, 13], [-7]]
    st.title("Questionnaire")
    st.subheader(f"Question {question_position(4)}")
    st.write("The following instance has no matching satisfying rank-envy-freeness.")

    cols = st.columns(2)
    with cols[0]:
        st.html(display_full_profile(prefs))
    
    with cols[1]:
        with st.container(border = True):
            gen_globexp_proc(mus, prefs, key="page17", seed=11)

    with st.container(border=True):
        st.radio("Now, I understand why there is no fair matching.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page17", "understanding"))
        st.radio("From the explanation, I understand why the proposed assignment can be considered fair.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page17", "algorithm_working"))
        st.radio("The explanation is satisfactory.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page17", "satisfaction"))
        st.radio("The explanation has sufficient detail.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page17", "detail"))
        st.radio("The explanation contains irrelevant details.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page17", "completeness"))
        tebox("page17")

def page18():
    prefs = ((2, 4, 5, 1, 3), (3, 5, 2, 4, 0), (4, 0, 5, 1, 3), (5, 1, 2, 4, 0), (0, 2, 5, 1, 3), (1, 3, 2, 4, 0))
    st.title("Questionnaire")
    st.subheader(f"Question {question_position(5)}")
    st.write("The following instance has no matching satisfying rank-envy-freeness.")
    cols = st.columns(2)
    with cols[0]:
        st.html(display_full_profile(prefs))

    with st.container(border=True):
        st.radio("It is clear to me why there is no fair matching.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page18", "understanding"))

def page19():
    prefs = ((2, 4, 5, 1, 3), (3, 5, 2, 4, 0), (4, 0, 5, 1, 3), (5, 1, 2, 4, 0), (0, 2, 5, 1, 3), (1, 3, 2, 4, 0))
    mus = [[1, 3, 5, 8, 12], [-5], [-12], [-8], [-1], [-3]]
    st.title("Questionnaire")
    st.subheader(f"Question {question_position(5)}")
    st.write("The following instance has no matching satisfying rank-envy-freeness.")

    cols = st.columns(2)
    with cols[0]:
        st.html(display_full_profile(prefs))
    
    with cols[1]:
        with st.container(border = True):
            gen_globexp_proc(mus, prefs, key="page19", seed=11)

    with st.container(border=True):
        st.radio("Now, I understand why there is no fair matching.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page19", "understanding"))
        st.radio("From the explanation, I understand why the proposed assignment can be considered fair.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page19", "algorithm_working"))
        st.radio("The explanation is satisfactory.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page19", "satisfaction"))
        st.radio("The explanation has sufficient detail.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page19", "detail"))
        st.radio("The explanation contains irrelevant details.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page19", "completeness"))
        tebox("page19")
def page20():
    prefs = ((2, 4, 5, 1, 3), (3, 5, 2, 4, 0), (4, 0, 5, 1, 3), (5, 1, 2, 4, 0), (0, 2, 5, 1, 3), (1, 3, 2, 4, 0))
    m = {2:3, 4:0, 0:4, 5:1, 1:5, 3:2}
    
    st.title("Questionnaire")
    st.subheader(f"Question {question_position(6)}")
    st.write("The following instance has a matching satisfying rank-envy-freeness. However Paul feels dissatisfied by their assignment and would like to know why they couldn't have a roommate they prefer to their assigned one.")
    cols = st.columns(2)
    with cols[0]:
        st.html(display_full_profile(prefs, matching = m))

    with st.container(border=True):
        st.radio("It is clear to me why Paul cannot have a preferred roommate.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page20", "understanding"))

def page21():
    prefs = ((2, 4, 5, 1, 3), (3, 5, 2, 4, 0), (4, 0, 5, 1, 3), (5, 1, 2, 4, 0), (0, 2, 5, 1, 3), (1, 3, 2, 4, 0))
    m = {2:3, 4:0, 0:4, 5:1, 1:5, 3:2}
    mus = [[-3], [-9], [-13], [-2], [2, 3, 9, 13]]
    st.title("Questionnaire")
    st.subheader(f"Question {question_position(6)}")
    st.write("The following instance has a matching satisfying rank-envy-freeness. However Paul feels dissatisfied by their assignment and would like to know why they couldn't have a roommate they prefer to their assigned one.")

    cols = st.columns(2)
    with cols[0]:
        st.html(display_full_profile(prefs, matching = m))
    
    with cols[1]:
        with st.container(border = True):
            gen_locexp_proc(prefs, m, 2, mus = mus, key = "page21")

    with st.container(border=True):
        st.radio("Now, I understand why Paul cannot have a preferred roommate.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page21", "understanding"))
        st.radio("From the explanation, I understand why the proposed assignment can be considered fair.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page21", "algorithm_working"))
        st.radio("The explanation is satisfactory.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page21", "satisfaction"))
        st.radio("The explanation has sufficient detail.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page21", "detail"))
        st.radio("The explanation contains irrelevant details.",options=["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],horizontal=True,index=None,key=answer_key("page21", "completeness"))
        tebox("page21")


def page22():
    st.title("Review your answers")
    st.write("Please review your answers below. Select Previous to make changes, or Finish to complete the evaluation.")
    render_summary(st.session_state["evaluation_answers"])
