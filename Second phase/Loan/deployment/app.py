# libraries
import streamlit as st
import pandas as pd
import joblib
import json
import base64

inputs = joblib.load(open(r'F:\Fields\Data Sci\Epsilon\ML projects\Epsilon intern\Second phase\Loan\deployment\helpers\Inputs.h5', 'rb'))
model = joblib.load(open(r'F:\Fields\Data Sci\Epsilon\ML projects\Epsilon intern\Second phase\Loan\deployment\helpers\model.h5', 'rb'))



def predict(gender, married, depent, edu, self_employed, app_income, co_app_income, loan_amount, loan_term, credit_history, area):
    all_data = [gender, married, depent, edu, self_employed, app_income, co_app_income, loan_amount, loan_term, credit_history, area]
    prediction = pd.DataFrame(columns=inputs, data=[all_data])
    prediction.to_csv('try.csv', index=False)
    return model.predict(prediction)[0]


def main():
    # header
    st.markdown("<h1 style='text-align:center;'>Loan Status</h1>", unsafe_allow_html=True)
    print('-'*30)
    gender = st.selectbox("Gender", ['Male', 'Female'])
    print('gender = ', gender)
    col1, col2, col3 , col4, col5 = st.columns(5)
    married = 'No'
    if st.checkbox("Married", value=False):
        married = 'Yes'
    depent = st.selectbox("Dependents", [0, 1, 2, 3])
    edu = st.selectbox("Education", ['Graduate', 'Not Graduate'])
    self_employed = 'No'
    if st.checkbox("Self Employed", value=False):
        self_employed = 'Yes'
    app_income = st.slider(label='ApplicantIncome', min_value=100, max_value=50000)
    co_app_income = st.slider(label='CoapplicantIncome', min_value=0, max_value=10000)
    loan_amount = st.slider(label='LoanAmount (K)', min_value=9, max_value=600)
    loan_term = st.selectbox("Loan Amount Term", [36, 60, 84, 120, 180, 240, 300, 360, 480])
    credit_history = 0
    if st.checkbox("Credit History", value=False):
        credit_history = 1
    area = st.selectbox("Area", ['Urban', 'Rural', 'Semiurban'])

    col1, col2, col3 , col4, col5 = st.columns(5)
    output = False
    with col3:
        if st.button("Predict"):
            output = True
    if output:
        pred = predict(gender, married, depent, edu, self_employed, app_income, co_app_income, loan_amount, loan_term, credit_history, area)
        if pred == 1:
            st.markdown(f"<h1 style='text-align:center; font-size:40px; background-color:darkred'>loan will be accepted 💯</h1>", unsafe_allow_html=True)
                
        else:
            st.markdown("<h1 style='text-align:center; font-size:40px; background-color:#333339'>Unfortunately, Not your turn</h1>", unsafe_allow_html=True)
            


if __name__ == '__main__':
    main()
