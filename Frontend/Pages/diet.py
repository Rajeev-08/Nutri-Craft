import streamlit as st

st.set_page_config(
    page_title="Diet",
   
)

import streamlit as st
import pandas as pd
from Generate_R import Generator
from random import uniform as rnd
from Find_img.img import get_images_links as find_image
from streamlit_echarts import st_echarts

st.set_page_config(page_title=" Diet Recommendation",layout="wide")


nutritions_values=['Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent']
# Streamlit states initialization
if 'person' not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations=None
    st.session_state.person=None
    st.session_state.weight_loss_option=None
class Person:

    def init(self,age,height,weight,gender,activity,meals_calories_perc,weight_loss):
        self.age=age
        self.height=height
        self.weight=weight
        self.gender=gender
        self.activity=activity
        self.meals_calories_perc=meals_calories_perc
        self.weight_loss=weight_loss
    def calculate_bmi(self,):
        bmi=round(self.weight/((self.height/100)**2),2)
        return bmi

    def display_result(self,):
        bmi=self.calculate_bmi()
        bmi_string=f'{bmi} kg/m²'
        if bmi<18.5:
            category='Underweight'
            color='Red'
        elif 18.5<=bmi<25:
            category='Normal'
            color='Green'
        elif 25<=bmi<30:
            category='Overweight'
            color='Yellow'
        else:
            category='Obesity'    
            color='Red'
        return bmi_string,category,color

    def calculate_bmr(self):
        if self.gender=='Male':
            bmr=10*self.weight+6.25*self.height-5*self.age+5
        else:
            bmr=10*self.weight+6.25*self.height-5*self.age-161
        return bmr

    def calories_calculator(self):
        activites=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
        weights=[1.2,1.375,1.55,1.725,1.9]
        weight = weights[activites.index(self.activity)]
        maintain_calories = self.calculate_bmr()*weight
        return maintain_caloriestitle="<h1 style='text-align: center;'> Diet Recommendation</h1>"
st.markdown(title, unsafe_allow_html=True)
with st.form("recommendation_form"):
    st.write("Modify the values and click the Generate button to use")
    age = st.number_input('Age',min_value=2, max_value=120, step=1)
    height = st.number_input('Height(cm)',min_value=50, max_value=300, step=1)
    weight = st.number_input('Weight(kg)',min_value=10, max_value=300, step=1)
    gender = st.radio('Gender',('Male','Female'))
    activity = st.select_slider('Activity',options=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 
    'Extra active (very active & physical job)'])
    option = st.selectbox('Choose your weight loss plan:',display.plans)
    st.session_state.weight_loss_option=option
    weight_loss=display.weights[display.plans.index(option)]
    number_of_meals=st.slider('Meals per day',min_value=3,max_value=5,step=1,value=3)
    if number_of_meals==3:
        meals_calories_perc={'breakfast':0.35,'lunch':0.40,'dinner':0.25}
    elif number_of_meals==4:
        meals_calories_perc={'breakfast':0.30,'morning snack':0.05,'lunch':0.40,'dinner':0.25}
    else:
        meals_calories_perc={'breakfast':0.30,'morning snack':0.05,'lunch':0.40,'afternoon snack':0.05,'dinner':0.20}
    generated = st.form_submit_button("Generate")
if generated:
    st.session_state.generated=True
    person = Person(age,height,weight,gender,activity,meals_calories_perc,weight_loss)
    with st.container():
        display.display_bmi(person)
    with st.container():
        display.display_calories(person)
    with st.spinner('Generating recommendations...'):     
        recommendations=person.generate_recommendations()
        st.session_state.recommendations=recommendations
        st.session_state.person=person

if st.session_state.generated:
    with st.container():
        display.display_recommendation(st.session_state.person,st.session_state.recommendations)
        st.success('Recommendation Generated Successfully !', icon="✅")
    with st.container():
        display.display_meal_choices(st.session_state.person,st.session_state.recommendations)\"
            