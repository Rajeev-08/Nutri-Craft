import streamlit as st
import pandas as pd
from Generate_Recommendations import Generator
from ImageFinder.ImageFinder import get_images_links as find_image
from streamlit_echarts import st_echarts

# Configure Page
st.set_page_config(page_title="Custom Food Recommendation", page_icon="🍽", layout="wide")

# Define Nutrition Parameters
nutrition_values = [
    "Calories", "FatContent", "SaturatedFatContent", "CholesterolContent",
    "SodiumContent", "CarbohydrateContent", "FiberContent", "SugarContent", "ProteinContent"
]

# Session State
if "generated" not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations = None

# Recommendation Class
class Recommendation:
    def init(self, nutrition_list, nb_recommendations, ingredient_txt):
        self.nutrition_list = nutrition_list
        self.nb_recommendations = nb_recommendations
        self.ingredient_txt = ingredient_txt

    def generate(self):
        params = {"n_neighbors": self.nb_recommendations, "return_distance": False}
        ingredients = self.ingredient_txt.split(";")
        generator = Generator(self.nutrition_list, ingredients, params)
        recommendations = generator.generate()
        recommendations = recommendations.json().get("output", [])

        # Add image links
        for recipe in recommendations:
            recipe["image_link"] = find_image(recipe["Name"])
        return recommendations

# Display Class
class Display:
    def init(self):
        self.nutrition_values = nutrition_values

    def display_recommendation(self, recommendations):
        st.subheader("🍲 Recommended Recipes")

        if not recommendations:
            st.warning("No recipes found for the selected ingredients.", icon="⚠️")
            return

        num_cols = 3  # Number of columns per row
        cols = st.columns(num_cols)

        for idx, recipe in enumerate(recommendations):
            with cols[idx % num_cols]:
                st.image(recipe["image_link"], use_column_width=True)
                st.write(f"{recipe['Name']}")

                with st.expander("View Details"):
                    st.write("### 🥗 Ingredients")
                    for ingredient in recipe["RecipeIngredientParts"]:
                        st.markdown(f"- {ingredient}")

                    st.write("### 👨‍🍳 Instructions")
                    for instruction in recipe["RecipeInstructions"]:
                        st.markdown(f"- {instruction}")

                    st.write("### 🥄 Nutrition Facts (g)")
                    nutritions_df = pd.DataFrame({key: [recipe[key]] for key in self.nutrition_values})
                    st.dataframe(nutritions_df, use_container_width=True)

    def display_overview(self, recommendations):
        if not recommendations:
            return

        st.subheader("📊 Nutrition Overview")

        # Recipe selection
        selected_recipe_name = st.selectbox("Select a recipe:", [recipe["Name"] for recipe in recommendations])
        selected_recipe = next(recipe for recipe in recommendations if recipe["Name"] == selected_recipe_name)

        # Pie Chart Data
        options = {
            "title": {"text": "Nutrition Breakdown", "subtext": selected_recipe_name, "left": "center"},
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "vertical", "left": "left"},
            "series": [
                {
                    "name": "Nutrition values",
                    "type": "pie",
                    "radius": "50%",
                    "data": [{"value": selected_recipe[nutrition], "name": nutrition} for nutrition in self.nutrition_values],
                    "emphasis": {"itemStyle": {"shadowBlur": 10, "shadowOffsetX": 0, "shadowColor": "rgba(0, 0, 0, 0.5)"}},
                }
            ],
        }
        st_echarts(options=options, height="500px")
        st.caption("Click on legend items to show/hide specific nutrition values.")

# UI Header
st.markdown("<h1 style='text-align: center;'>🍽 Custom Food Recommendation</h1>", unsafe_allow_html=True)
display = Display()

# Sidebar Inputs
with st.sidebar:
    st.header("⚙️ Customize Your Preferences")
    Calories = st.slider("Calories", 0, 2000, 500)
    FatContent = st.slider("FatContent", 0, 100, 50)
    SaturatedFatContent = st.slider("SaturatedFatContent", 0, 13, 0)
    CholesterolContent = st.slider("CholesterolContent", 0, 300, 0)
    SodiumContent = st.slider("SodiumContent", 0, 2300, 400)
    CarbohydrateContent = st.slider("CarbohydrateContent", 0, 325, 100)
    FiberContent = st.slider("FiberContent", 0, 50, 10)
    SugarContent = st.slider("SugarContent", 0, 40, 10)
    ProteinContent = st.slider("ProteinContent", 0, 40, 10)

    nutritions_values_list = [
        Calories, FatContent, SaturatedFatContent, CholesterolContent,
        SodiumContent, CarbohydrateContent, FiberContent, SugarContent, ProteinContent
    ]

    st.subheader("Optional Filters")
    nb_recommendations = st.slider("Number of recommendations", 5, 20, step=5)
    ingredient_txt = st.text_input("Ingredients (separated by ';')", placeholder="E.g., Milk;Eggs;Chicken")

    generate_btn = st.button("🔍 Generate Recommendations")

# Generate Recommendations
if generate_btn:
    with st.spinner("Generating recommendations..."):
        recommendation = Recommendation(nutritions_values_list, nb_recommendations, ingredient_txt)
        recommendations = recommendation.generate()
        st.session_state.recommendations = recommendations
        st.session_state.generated = True

# Display Results in Tabs
if st.session_state.generated:
    tab1, tab2 = st.tabs(["📌 Recommendations", "📊 Nutrition Overview"])

    with tab1:
        display.display_recommendation(st.session_state.recommendations)

    with tab2:
        display.display_overview(st.session_state.recommendations)