import streamlit as st
from sympy import *
import re
init_printing(use_unicode=True)

#Page setup
st.set_page_config(page_title = "Calculator",
                    layout = "wide")

st.title('Math Solver App')

equation_str = st.text_input('Enter equation, use ln instead log:')

pattern = r"(\d+)([a-zA-Z])"

opt = st.sidebar.radio("Choose",["Derivative","Integrate","Simplify","Calculate" ,"Solve"])

submit = st.button('Submit')


#Groups expression into two  
def extract_variables(expr_str):
    pattern = r'\b[A-Za-z]+\b'
    variable_names = set(re.findall(pattern, expr_str))
    return variable_names

#extracts variable from exprerssion
def evaluate_expression(expr_str):
    variable_names = extract_variables(expr_str)
    #st.write(variable_names)
    symbols = [symbols(var) for var in variable_names]
    expr = sympify(expr_str)
    values =  [2] * len(symbols) 
    result = expr.subs(list(zip(symbols, values)))
    return float(result)

if submit:
    equation_str = st.text_area("Corrected Expression:", value= re.sub(pattern, r"\1*\2", equation_str))
    
    try:  #runs selected method from sympy library
        vars = extract_variables(equation_str) 
        keys_list = list(vars)
        if opt == "Derivative" and equation_str!='':
            result = diff(equation_str,keys_list[0])
        if opt == "Solve" and equation_str!='':
            result = solve(equation_str,keys_list[0])
        if opt == "Calculate" and equation_str != '':
            result = evaluate_expression(equation_str)
        if opt == "Simplify" and equation_str!= '':
            x, y, z = symbols('x y z')
            expr = equation_str
            result = simplify(expr)
        if opt == "Integrate" and equation_str!= '':
            x, y, z = symbols('x y z')
            f = equation_str
            result = integrate(f,keys_list)
        st.latex(result)
    except Exception as e: #if error print
        st.error(f"Error: {e}")



