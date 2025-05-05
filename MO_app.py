import streamlit as st
import regex as re
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

final_data=pd.read_excel("makeover_final_master_data.xlsx")
st.set_page_config(layout='wide')
st.title("Makeover Analysis for Aajol Marathas")
pname = st.selectbox("Select you name..", options = final_data['Name'].unique())
testnum = st.radio(
    "Select the test option",
    ('First test (Jan)', 'Last - 4th test (April)'))
if pname:
  if testnum=='First test (Jan)':
    tempedf = final_data[final_data['Name']==pname][['Name', 'Age', 'Weight - Weight (Kgs)', 'PBF (percentage)', 'BMI (kg/m²)',
        'Waist to Hip Ratio - Score (ratio)', 'Sit & Reach - Distance (cms)',
        'Push Ups - Numbers (reps)', 'Oblique Abs - Numbers (reps)',
        'Iron Man - Time (minutes)', '2.4 Km Run - Time (minutes)']]
    edata = st.data_editor(tempedf)
    # submit_button = st.form_submit("Submit")
  else:
    tempedf = final_data[final_data['Name']==pname][['Name', 'Age','Weight - Your Weight (Kgs)_test4',
       'Percent Body Fat (PBF) - PBF (percentage)_test4',
       'Body Mass Index - BMI (kg/mÂ²)_test4',
       'Waist to Hip Ratio (WH) - Ratio (ratio)_test4',
       'Sit and Reach - Distance (cms)_test4',
       'Push Ups - Numbers (reps)_test4', 'Oblique Abs - Number (reps)_test4',
       'Iron Man - Times (minutes)_test4',
       '2.4 km Run - Time (minutes)_test4']]
    edata = st.data_editor(tempedf)
    # submit_button = st.form_submit("Submit")
#   if submit_button:
# st.dataframe(edata)
for i in edata.columns:
  final_data.loc[final_data['Name']==pname,i]=edata[i].iloc[0]
cats_dict={'Weight - Weight (Kgs)':-1,
 'PBF (percentage)':-1,
 'BMI (kg/m²)':-1,
  'Waist to Hip Ratio - Score (ratio)':-1,
 'Sit & Reach - Distance (cms)':1,
 'Push Ups - Numbers (reps)':1,
 'Oblique Abs - Numbers (reps)':1,
 'Iron Man - Time (minutes)':1,
 '2.4 Km Run - Time (minutes)':-1}

temp_cats=list(cats_dict.keys())
n_columns=['Sr. No.', 'Name', 'Age', 'Gender', 'Height - Length (Cms)',
       'Weight - Weight (Kgs)', 'PBF (percentage)', 'BMI (kg/m²)',
       'Waist to Hip Ratio - Score (ratio)', 'Sit & Reach - Distance (cms)',
       'Push Ups - Numbers (reps)', 'Oblique Abs - Numbers (reps)',
       'Iron Man - Time (minutes)', '2.4 Km Run - Time (minutes)', 'Marathas','Name_test4'] + [i+'_test4' for i in temp_cats]
final_data.columns=n_columns
# cats=[i for i in temp_cats if i not in ['BMI (kg/m²)',
#   'Waist to Hip Ratio - Score (ratio)',
#   'Weight - Weight (Kgs)']]

cats = st.multiselect(
    "Select the categories for analysis!",
    ['Weight - Weight (Kgs)',
 'PBF (percentage)',
 'BMI (kg/m²)',
 'Sit & Reach - Distance (cms)',
 'Push Ups - Numbers (reps)',
 'Oblique Abs - Numbers (reps)',
 'Iron Man - Time (minutes)',
 '2.4 Km Run - Time (minutes)'],
    default=['PBF (percentage)',
 'Sit & Reach - Distance (cms)',
 'Push Ups - Numbers (reps)',
 'Oblique Abs - Numbers (reps)',
 'Iron Man - Time (minutes)',
 '2.4 Km Run - Time (minutes)'],
)
for i in cats:
  final_data[i+'_diff']=final_data.apply(lambda x: float(x[i+'_test4']) - x[i],axis=1)
# TOP 5 IN EACH CATEGORY
# for i in cats:
#   if cats_dict[i]==-1:
#     print("Category", i,"\n\n")
#     temp = final_data[['Name',i+'_diff']].sort_values(by=i+'_diff',ascending=True)
#     print("top5-->", temp.head(5))
#   elif cats_dict[i]==1:
#     print("Category", i,"\n\n")
#     temp = final_data[['Name',i+'_diff']].sort_values(by=i+'_diff',ascending=False)
#     print("top5-->", temp.head(5))

final_data2=final_data.copy(deep=True)
mn=MinMaxScaler()
final_data2[[i+'_normdiff' for i in cats]]=mn.fit_transform(final_data2[[i+"_diff" for i in cats]].abs())
final_data2.drop(['Marathas',
       'Name_test4'],axis=1,inplace=True)
# final_data2.to_excel("master_data_difference.xlsx",index=False)
final_data2['score']=0
for i in cats_dict.keys():
  if i in cats:
    final_data2['score'] = final_data2.apply(lambda x: x[i+'_normdiff']+x['score'] if x[i+'_diff']*cats_dict[i]>0 else x['score']-x[i+'_normdiff'],axis=1)
age_factor = st.text_input("Select Age factor (Default = 1.5, 150% score)", "1.5")
age_factor=float(age_factor)
final_data2['Score_after_age_pt']=final_data2.apply(lambda x: x['score']*age_factor if int(re.findall(r"\d+",x['Age'])[0])>50 else x['score'],axis=1)
final_data2.sort_values('Score_after_age_pt',ascending=False,inplace=True)
final_data2.to_excel("Changed_master_data.xlsx",index=False)

st.divider()
st.write(f"The Approach of the analysis:\n1. Categories considered are {cats}\n2. Differences are calculated for each category. (Last Test number - First test number)\n3. All differences for each category are normalized (0 to 1).\n4. Normalized values are added to create a score (depending on direction of improvment)\n5. Scores are multiplied by age factor for participants with age >50 years")
st.divider()
st.title(":blue[Aajol Marathas leaderboard !] :sunglasses:")
st.dataframe(final_data2[['Name','Age']+[i+'_diff' for i in cats]+['score','Score_after_age_pt']])
