# libraries
import streamlit as st
import pandas as pd
import joblib
import json
import base64

# Dummy columns
with open('helpers/dummies.json', 'r') as openfile:
    # Reading
    all_categories = json.load(openfile)
inputs = joblib.load(open('helpers/Inputs.h5', 'rb'))
model = joblib.load(open('helpers/model.h5', 'rb'))

# Navigator
nav = st.sidebar.radio("Navigation",["Home","Prediction"])
# Home
if nav == "Home":
    st.markdown("<h1 style='text-align: center;'>Zomato Resturants</h1>", unsafe_allow_html=True)
    st.markdown("""<h3><center>Zomato is an Indian multinational restaurant aggregator and food delivery company founded by <span style="color:#c42626;">Deepinder Goyal</span> and <span style="color:#c42626;">Pankaj Chaddah</span> in <span style="color:#c42626;">2008</span>.</center></h3>
    <h3><center>Our data contain details about restaurants in <span style="color:#c42626;">Bangalore</span> city like (name, location, online_order, cuisines, ...etc).</center></h3>
    <h3><center>Our case is to see if new restaurant will open in this city will <span style="color:#c42626; font-size:50px">success or not</span>.</center></h3>""", unsafe_allow_html=True)
# Prediction
if nav == "Prediction":
    # function for background
    def add_bg_from_local(image_file):
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: 100%;
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    add_bg_from_local('check.jpeg') 
    # header
    st.markdown("<h1 style='text-align:center;'>Check resturant success</h1>", unsafe_allow_html=True)

    # Location
    location = st.selectbox("Location", all_categories['location'])

    # function to return list contain 1 and 0 depend on users select
    def get_multiselect(origin, selected):
        choose_list = [0 for i in range(len(origin))]
        for i in selected:
            index = origin.index(i)
            choose_list[index] = 1
        return choose_list

    # Type
    types = st.multiselect("Type", all_categories['listed_in(type)'])

    # rest_type
    rest_type = st.multiselect("Rest Type", all_categories['rest_type'])
    selected_rest_type = get_multiselect(all_categories['rest_type'], rest_type)

    # cuisines
    cuisines = st.multiselect("Cuisines", all_categories['cuisines'])
    selected_cuisines = get_multiselect(all_categories['cuisines'], cuisines)

    # for approxmat cost
    approx_cost = st.number_input('Approximate cost for one pair', value=0, min_value=0)

    # for online order and book table
    col1, col2, col3 , col4, col5 = st.columns(5)
    online_order = 0
    book_table = 0
    with col2:
        if st.checkbox("Online Order", value=False):
            online_order = 1
    with col4:
        if (st.checkbox("Book Table", value=False)):
            book_table = 1

    # for button
    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #333339;
        color:#ffffff;
    }
    div.stButton > button:hover {
        background-color: darkred;
        color:#ffffff;
        }
    </style>""", unsafe_allow_html=True)
    # buuton
    col1, col2, col3 , col4, col5 = st.columns(5)
    output = False
    with col3:
        if st.button("Predict"):
            output = True
    if output == True:
        for type in types:
            all_data = [online_order, book_table, location, approx_cost] + selected_rest_type + get_multiselect(all_categories['listed_in(type)'], [type]) + selected_cuisines
            prediction = pd.DataFrame(columns=inputs, data=[all_data])
            predict = model.predict(prediction)[0]
            if predict == 1:
                st.markdown(f"<h1 style='text-align:center; font-size:40px; background-color:darkred'>{type} Will succeed 💯</h1>", unsafe_allow_html=True)
                
            else:
                st.markdown("<h1 style='text-align:center; font-size:40px; background-color:#333339'>Unfortunately, Not your place</h1>", unsafe_allow_html=True)