#core packages
import streamlit as st

#EDA pkgs
import pandas as pd
import numpy as np

#Utils
import os
import joblib
import hashlib

#Data Vix pkgs
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

#DB
from managed_db import *

#Password
def generate_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def verify_hashes(password, hashed_text):
    if generate_hashes(password) == hashed_text:
        return hashed_text
    return False

feature_names_best = ['age', 'sex', 'steroid', 'antivirals', 'fatigue', 'spiders', 'ascites','varices', 'bilirubin', 'alk_phosphate', 'sgot', 'albumin', 'protime','histology']

gender_dict = {"Miles/Tons (US)":1,"Kilometers/ tonnes (metric)":2}
feature_dict = {"No":1,"Yes":2}
transportmodel_dict = {"Rail":1,"Ship":2, "Air":3, "Truck":4, "Car":5}
carrier_dict = {"DHL":1,"UPS":2, "USPS":3, "Fedex":4}

def get_value(val,my_dict):
	for key,value in my_dict.items():
		if val == key:
			return value

def get_key(val,my_dict):
	for key,value in my_dict.items():
		if val == key:
			return key

def get_fvalue(val):
	feature_dict = {"No":1,"Yes":2}
	for key,value in feature_dict.items():
		if val == key:
			return value

def get_tvalue(val):
	feature_dict = {"Rail":1,"Ship":2, "Air":3, "Truck":4, "Car":5}
	for key,value in transportmodel_dict.items():
		if val == key:
			return value

def get_cvalue(val):
	feature_dict = {"DHL":1,"UPS":2, "USPS":3, "Fedex":4}
	for key,value in carrier_dict.items():
		if val == key:
			return value

# Load ML Models
def load_model(model_file):
	loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
	return loaded_model

prescriptive_message_temp ="""
	<div style="background-color:silver;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<h3 style="text-align:justify;color:black;padding:10px">Options to offset your carbon footprint</h3>
		<ul>
		<li style="text-align:justify;color:black;padding:10px">By not selecting same-day delivery you could reduce your CO2e emissions by an estimated 0.8 tons </li>
		<li style="text-align:justify;color:black;padding:10px">Can use eco-friendly packaging</li>
		<li style="text-align:justify;color:black;padding:10px">Overall Carbon footprint score is euivalent to 1 car off the road for 1 hour</li>
		<li style="text-align:justify;color:black;padding:10px">Overall Carbon footprint score is euivalent to 1 tree planted today</li>
		<li style="text-align:justify;color:black;padding:10px">Use refurbuished items instead of new</li>
		<ul>
	</div>
	"""
# ML Interpretation
import lime
import lime.lime_tabular

def main():
    st.title('Track your Carbon Footprint  ')

    menu = ["Home", "Login", "Signup"]
    submenu = ["Plot","Carbon Calculator", "Enter shipment number"]

    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Home")
        st.text("Reducing carbon footprint from online shopping ")
        st.text("By Shubhi Asthana ")
        st.image("coverphoto.png")

    elif choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = generate_hashes(password)
            result = login_user(username, verify_hashes(password, hashed_pswd))

            st.success("Welcome {}".format(username))
            activity = st.selectbox("Activity",submenu)
            if activity == "Plot":
                st.subheader("Carbon Footprint Data Visualization Plot")
                #df = pd.read_csv("data/clean_hepatitis_dataset.csv")
                df = pd.read_csv("data/carbonfootprint_countries.csv")
                st.dataframe(df)

                #freq_dist plot
                freq_df = pd.read_csv("data/countries_dataset.csv")
                st.bar_chart(freq_df['count'])

                df['Region'].value_counts().plot(kind='bar')


                if st.checkbox("Area Chart"):
                    all_columns = df.columns.to_list()
                    feat_choices = st.multiselect("Choose a Feature", all_columns)
                    new_df = df[feat_choices]
                    st.area_chart(new_df)

            elif activity == "Carbon Calculator":
                st.subheader("Track your shipment's carbon emissions. In just a few simple steps, get the estimated carbon emissions for the entire transportation of your shipment, from vessel to truck")

                age = st.number_input("How many tons do you want to ship?", 1, 80)
                sex = st.radio("What unit of measure applies to your shipment?", tuple(gender_dict.keys()))
                steroid = st.radio("Select one or more Transportation Modes that apply to your shipment", tuple(transportmodel_dict.keys()))

                st.text("Average shipment weights ")
                st.text("Freight tons per railcar : 90 ")
                st.text("Freight tons per truck : 16 ")


                #steroid = st.radio("Select one or more Transportation Modes that apply to your shipment",tuple(transportmodel_dict.keys()))
                #sex = st.radio(" What unit of measure applies to your shipment?", tuple(gender_dict.keys()))
                #age = st.number_input("How many tons do you want to ship?", 1, 100)




                sgot = st.number_input("Average distance travelled by shipment", 1, 100)
                protime = st.number_input("Number of modes of transport", 0.0, 100.0)

                st.text("Lets talk about the details of your shipment! ")
                fatigue = st.radio("Have you selected eco-friendly packaging?", tuple(feature_dict.keys()))
                spiders = st.radio("Will it be same-day delivery?", tuple(feature_dict.keys()))
                ascites = st.selectbox("Is the product refurbished or new?", tuple(feature_dict.keys()))
                varices = st.selectbox("Can the product be recyled?", tuple(feature_dict.keys()))
                bilirubin = st.number_input("If buying retail, what are the number of items chosen", 0.0, 10.0)
                alk_phosphate = st.number_input("Average cost of products", 0.0, 10.0)
                albumin = st.number_input("Average approx weight of packing material used in packaging", 0.0, 10.00)
                histology = st.selectbox("Is the business carbon-neutral?", tuple(feature_dict.keys()))
                antivirals = st.radio("Is the shipment company carbon-neutral?", tuple(feature_dict.keys()))

                feature_list = [age, get_value(sex, gender_dict), get_tvalue(steroid), get_fvalue(antivirals),
                                get_fvalue(fatigue), get_fvalue(spiders), get_fvalue(ascites), get_fvalue(varices),
                                bilirubin, alk_phosphate, sgot, albumin, int(protime), get_fvalue(histology)]
                st.write(len(feature_list))
                st.write(feature_list)
                pretty_result = {"age": age, "sex": sex, "steroid": steroid, "antivirals": antivirals,
                                 "fatigue": fatigue, "spiders": spiders, "ascites": ascites, "varices": varices,
                                 "bilirubin": bilirubin, "alk_phosphate": alk_phosphate, "sgot": sgot,
                                 "albumin": albumin, "protime": protime, "histolog": histology}
                # st.json(pretty_result)
                single_sample = np.array(feature_list).reshape(1, -1)

                # ML
                model_choice = st.selectbox("Select Model", ["LR", "DecisionTree"])
                if st.button("Predict"):
                    if model_choice == "DecisionTree":
                        loaded_model = load_model("models/decision_tree_ClimateHack.pkl")
                        prediction = loaded_model.predict(single_sample)
                        pred_prob = loaded_model.predict_proba(single_sample)
                    else:
                        loaded_model = load_model("models/logistic_regression_ClimateHack.pkl")
                        prediction = loaded_model.predict(single_sample)
                        pred_prob = loaded_model.predict_proba(single_sample)

                    # st.write(prediction)
                    # prediction_label = {"Die":1,"Live":2}
                    # final_result = get_key(prediction,prediction_label)
                    #if prediction == 1:
                    if sex == "Miles/Tons (US)":
                        st.warning("You have significant carbon footprint results")
                        #pred_probability_score = {"Performance Score impact": pred_prob[0][0] * 100, "Overall Performance score": pred_prob[0][1] * 100}
                        if(steroid == 'Car'):
                            pred_probability_score = {"Total estimated CO2e emissions from all selected modes": pred_prob[0][0]*0.7,"Overall Carbon Footprint score": (bilirubin)*1.2  }
                        else:
                            pred_probability_score = {"Total estimated CO2e emissions from all selected modes": pred_prob[0][0]*0.2,"Overall Carbon Footprint score": (bilirubin*0.4 + pred_prob[0][0]) }
                        st.subheader("Prediction Carbon Footprint Score using {}".format(model_choice))
                        st.json(pred_probability_score)
                        st.subheader("What can you do to offset this carbon footprint?")
                        st.markdown(prescriptive_message_temp, unsafe_allow_html=True)

                    else:
                        st.success("You do not have significant carbon footprint results")
                        pred_probability_score = {"Performance Score impact": bilirubin }
                        st.subheader("Prediction Probability Score using {}".format(model_choice))
                        st.json(pred_probability_score)

            elif activity == "Enter shipment number":
                st.subheader("Enter your shipment details")

                shipment = st.radio("What carrier are you using?", tuple(carrier_dict.keys()))

                age = st.number_input("Enter the shipment tracking number", 1, 8000)

                feature_list = [get_cvalue(shipment),  age]
                st.write(len(feature_list))
                st.write(feature_list)
                # st.json(pretty_result)
                single_sample = np.array(feature_list).reshape(1, -1)

                if st.button("Track Carbon Footprint for this shipment"):
                    st.image("DHL.png")
                    st.text('Total estimated CO2e emissions from this shipment : X tons')



    elif choice == "Signup":
        new_username = st.text_input("User name")
        new_password = st.text_input("Password", type='password')

        confirm_password = st.text_input("Confirm Password", type='password')
        if new_password == confirm_password:
            st.success("Password Confirmed")
        else:
            st.warning("Password not the same")

        if st.button("Submit"):
            create_usertable()
            hashed_new_password = generate_hashes(new_password)
            add_userdata(new_username, new_password)
            st.success("You have successfully created a new account")
            st.info("Login to Get Started")


if __name__ == '__main__':
    main()