# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 00:53:55 2023

@author: iza
"""
#https://docs.google.com/spreadsheets/d/1hr8KiGQ96MeoaOH3MCjgSPHR_MrumXVH/edit#gid=2070559139

import pandas as pd
import numpy as np
import csv
import xlsxwriter
import time
from datetime import timedelta
from datetime import datetime as dt
import plotly.express as px
import streamlit as st
import io

st.title("My School ☀️")
SHEET_ID=st.text_input(label = "Please enter SHEET_ID for Data", value='1hr8KiGQ96MeoaOH3MCjgSPHR_MrumXVH')
SHEET_NAME = 'Data'
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
SHEET_NAME_2 = 'Info'
url_2 = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME_2}'

#@st.cache(suppress_st_warning=True, allow_output_mutation=True)#(persist=True, suppress_st_warning=True)
@st.experimental_memo
def data_import() -> list:
    global df
    global df_raw
    global df_info_raw

    list_clmn=['1_Monday_Gr', '1_Monday_Name', '1_Monday_IN', '1_Monday_OUT', '1_Monday_Abs', \
           '1_Tuesday_Gr', '1_Tuesday_Name', '1_Tuesday_IN', '1_Tuesday_OUT', '1_Tuesday_Abs', \
           '1_Wednesday_Gr', '1_Wednesday_Name', '1_Wednesday_IN', '1_Wednesday_OUT', '1_Wednesday_Abs', \
           '1_Thursday_Gr', '1_Thursday_Name', '1_Thursday_IN', '1_Thursday_OUT', '1_Thursday_Abs', \
           '1_Friday_Gr', '1_Friday_Name', '1_Friday_IN', '1_Friday_OUT', '1_Friday_Abs', \
           '1_Saturday_Gr', '1_Saturday_Name', '1_Saturday_IN', '1_Saturday_OUT', '1_Saturday_Abs', \
           '1_Sunday_Gr', '1_Sunday_Name', '1_Sunday_IN', '1_Sunday_OUT', '1_Sunday_Abs']
    dict_clmn=dict(zip(list_clmn,list_clmn))
    print(dict_clmn)
    
    df = pd.read_csv(url, skip_blank_lines=True)
    df_raw=df
    
    list_columns_row=df.columns
    nr_columns=len(df.columns)
    df=df[list_clmn]
    print(df.head())
    
    
    df_info = pd.read_csv(url_2, skip_blank_lines=True)
    df_info_raw=df_info

    print(df_info.columns)
    #df_info=df_info.dropna(subset=['Name'])
    print(df_info)
    print('df.columns')
    print(df.columns)
    
    #df.to_excel("DF.xlsx")
    #df_info.to_excel("DF_info.xlsx")
    #The more general should rank higher e.g. 1 before 11 and 12/3/4, 2 before 12
    week_dict_keywordincld={
        '1st week':['1_'],
        '10th week':['10_'],
        '11th week':['11_'],
        '2nd week':['2_'],
        '12th week':['12_'],
        '3rd week':['3_'],
        '13th week':['13_'],
        '4th week':['4_'],
        '14th week':['14_'],
        '5th week':['5_'],
        '6th week':['6_'],
        '7th week':['7_'],
        '8th week':['8_'],
        '9th week':['9_']
        }
    #Start Date, End Date for week
    df['Start date']=df['1_Monday_Name']
    df['Start date']=np.where(df['Start date'].isnull(),'-',df['Start date']) 
    df['End Date']=df['1_Sunday_Name']
    df['End Date']=np.where(df['End Date'].isnull(),'-',df['End Date'])
    df['Period']=df['Start date']+'-'+df['End Date']
    df['1_Monday_Abs']=np.where(df['1_Monday_Gr']=='Date:',df['Period'],df['1_Monday_Abs'])
    df['1_Tuesday_Abs']=np.where(df['1_Tuesday_Gr']=='Date:',df['Period'],df['1_Tuesday_Abs'])
    df['1_Wednesday_Abs']=np.where(df['1_Wednesday_Gr']=='Date:',df['Period'],df['1_Wednesday_Abs'])
    df['1_Thursday_Abs']=np.where(df['1_Thursday_Gr']=='Date:',df['Period'],df['1_Thursday_Abs'])
    df['1_Friday_Abs']=np.where(df['1_Friday_Gr']=='Date:',df['Period'],df['1_Friday_Abs'])
    df['1_Saturday_Abs']=np.where(df['1_Saturday_Gr']=='Date:',df['Period'],df['1_Saturday_Abs'])
    df['1_Sunday_Abs']=np.where(df['1_Sunday_Gr']=='Date:',df['Period'],df['1_Sunday_Abs'])
    df=df.drop(columns=['Start date', 'End Date', 'Period'])

    
    #Find no week
    dict_week_index={}
    list_index=[]
    list_week=[]
    whichweek=['1_Monday_Gr']+list(df['1_Monday_Gr'])
    print(whichweek)
    for i in range(1,15):
        weeki=f'{i}_Monday_Gr'
        index=whichweek.index(weeki)
        list_index.append(index)
        list_week.append(i)
    
    dict_week_index=dict(zip(list_week,list_index))
    lastrowindex=df.index[-1]
    lastrowindex=len(df)+1
    print(len(df))
    dict_week_index[15]=lastrowindex 
    print(dict_week_index)
    
    
    #Split df into weeks
    df_pnew = pd.DataFrame()
    for i in range(1,15):
        index_end=(dict_week_index[i+1])-1
        if i==1:
            index_start=0
            new_row =list_clmn
            new_dict_forrow=dict(zip(new_row, new_row))
            df_new_dict_forrow=pd.DataFrame([new_dict_forrow])
            df_i = pd.concat([df_new_dict_forrow,df.iloc[index_start:index_end]]).reset_index(drop=True)
            
        else:
            index_start=(dict_week_index[i])-1
            df_i=df.iloc[index_start:index_end]
            df_i.reset_index(inplace=True)
            df_i=df_i.drop(columns='index')
      
        
        print(df_pnew)
        df_pnew=pd.concat([df_pnew, df_i], axis=1)
        df_pnew.reset_index(inplace=True)
        df_pnew=df_pnew.drop(columns='index')
    
    list_columns=df_pnew.columns
    nr_columns=len(df_pnew.columns)
    
    cols = []  # for tracking duplicates in column names
    new_cols = []
    for col in df_pnew.columns:
        cols.append(col)
        count = cols.count(col)
        
        if count > 1:
            new_cols.append(f'{col}_{count}')
        else:
            new_cols.append(col)
    df_pnew.columns = new_cols 
    for i in range (0, nr_columns):
            df_pnew.rename(columns={df_pnew.columns[i]:i}, inplace=True) 

    #Create new format of df
    
    df_days=pd.DataFrame()
    for i in range(0, nr_columns-5, 5):
    #for i in range(0, 10, 5):
        df_day=df_pnew[[i,i+1,i+2,i+3,i+4]]
        print(df_day)
        
        week_key=df_day[i].iloc[0]
        day_date=df_day[i+1].iloc[1]
        
        day_week=df_day[i].iloc[2]
        period=df_day[i+4].iloc[1]
        

        df_day.rename(columns = {i:'Group', i+1:'Name', i+2:'IN', i+3:'OUT', \
                                 i+4:'Absence'}, inplace = True) 
        df_day=df_day.drop([0,1,2,3,4])   
        if len(week_key)!=0:
            for key, value in week_dict_keywordincld.items():
                for valuei in value:
                    if str(week_key).__contains__(valuei):
                        week_no=key
        
 
        #df_day=df_day.dropna(how=all)
        
        df_day['Week no']=week_no
        df_day['Date']=day_date    
        df_day['Day_of_week']=day_week
        df_day['Teacher (y or n)']=np.nan
        df_day['Factor_price']=np.nan 
        df_day['Price']=np.nan
        df_day['HRS_Scheduled']=np.nan
        df_day['Sum_Scheduled']=np.nan
        df_day['Factor_Present/Absence']=np.nan
        df_day['HRS_Delta']=np.nan
        df_day['Sum_R']=np.nan
        df_day['Note']=np.nan  
        df_day['Period']=period
    
        df_day.reset_index(drop=True, inplace=True)

        df_days=pd.concat([df_days, df_day], axis=0, ignore_index=True)
    
    df_days=df_days[df_days['Name']!='']
    df_days=df_days[['Week no','Date', 'Day_of_week', 'Period', 'Group', 'Name', \
                                'Teacher (y or n)', 'Factor_price', 'Price', \
                                'IN','OUT',  'HRS_Scheduled', 'Sum_Scheduled', \
                                'Absence', 'Factor_Present/Absence', \
                                'HRS_Delta', 'Sum_R', 'Note']]
        
    df_days.reset_index(drop=True, inplace=True)
    
    #Calculate/add values
    df_days['Teacher (y or n)']=df_days['Name'].map(dict(zip(df_info['Name'],df_info['Teacher (y or n)'])))
    df_days['Price']=df_days['Name'].map(dict(zip(df_info['Name'],df_info['Price'])))
    list_teacher=['y', 'yes', 'Y', 'Yes', 'YES', 'T', 't', 'True', 'Teacher', 'teacher', 'TEACHER']
    df_days['Factor_price']=np.where(df_days['Teacher (y or n)'].isin(list_teacher),-1,1 )
    df_days['Price']=np.where((df_days['Price'].isnull()|df_days['Price']==0),0,df_days['Price'] ) 
    list_absent=['y', 'yes', 'Y', 'Yes', 'YES', 'absent', 'Absent', 'ABSENT']
    df_days['Factor_Present/Absence']=np.where(df_days['Absence'].isin(list_absent),-1,1 )
    
    if len(df_days)>0:
        for i in range(0,len(df_days.index)):
            bool_empty_Assumption=df_days['IN'].iloc[i]=='' or df_days['IN'].iloc[i]==0 or pd.isnull(df_days['IN'].iloc[i]) or df_days['OUT'].iloc[i]=='' or df_days['OUT'].iloc[i]==0 or pd.isnull(df_days['OUT'].iloc[i])
            print(i)
            print(bool_empty_Assumption)
            if bool_empty_Assumption==False:
                df_days['HRS_Scheduled'].iloc[i]=((pd.to_datetime(str(df_days['Date'].iloc[i]) + ' ' + str(df_days['OUT'].iloc[i])))-\
                                                   (pd.to_datetime(str(df_days['Date'].iloc[i]) + ' ' + str(df_days['IN'].iloc[i])))).total_seconds() / 60 / 60
            else:
                df_days['HRS_Scheduled'].iloc[i]=0
    
    df_days['Sum_Scheduled']=df_days['HRS_Scheduled']*df_days['Factor_price']*df_days['Price']
    df_days['Sum_Scheduled']=df_days['HRS_Scheduled']*df_days['Factor_price']*df_days['Price']
    df_days['HRS_Delta']=df_days['HRS_Scheduled']*df_days['Factor_Present/Absence']
    df_days['Sum_R']=df_days['Sum_Scheduled']*df_days['Factor_Present/Absence']

    return [df_days.reset_index(drop=True), df_raw, df_info_raw]
    #return df.reset_index(drop=True)

def main():
    global df
    global df_raw
    global df_info_raw
    
    list_df=data_import()
    
    df=list_df[0]
    df.dropna()
    print('test')
    print(df)
    df_data=list_df[1]
    df_info=list_df[2]

    file_container1 = st.expander("<<Data>>")
    shows = df_data
    file_container1.write(shows)
    dict_range={
            '1st week':1,
            '2nd week':2,
            '3rd week':3,
            '4th week':4,
            '5th week':5,
            '6th week':6,
            '7th week':7,
            '8th week':8,
            '9th week':9,
            '10th week':10,
            '11th week':11,
            '12th week':12,
            '13th week':13,
            '14th week':14            
            }
    df['Week_no_int']=df['Week no'].map(dict_range)
    
    
    file_container2 = st.expander("<<Info>>")
    shows2 = df_info
    file_container2.write(shows2)
    
    selection_weeks=st.radio('Time range by', ('Week no', 'Date'), index=0, horizontal=True, label_visibility="visible")
    if selection_weeks=='Week no':
        weeks=list(range(1, 14))
        week_range= st.slider(label="Choose a range", min_value=1, max_value=14, value=(5, 6))
        #st.session_state.week_range[0], st.session_state.week_range[1]

        if (int(week_range[0]) - int(week_range[1])) == 0:
            df_weeksrange=pd.DataFrame()
            st.write('Time range is empty')
        else:
            start_index=week_range[0]-1
            end_index=week_range[1]
            weeks_selected=weeks[start_index:end_index]
            df_filtered_weeks = df[df['Week_no_int'].isin(weeks_selected)]

            st.write(week_range[0])
            st.write(week_range[1])
    
    else:
        dates_list=list(set(df['Period']))
        dict_range=dict(zip(df['Week no'], df['Period']))
        values = len(dates_list)
        format = 'MMM DD, YYYY' 
        start_date=dates_list[0]
        next_date=dates_list[1]
        end_date=dates_list[-1]
        date_range = st.multiselect('Choose a range', dates_list,[start_date])
        st.write(date_range )
        df_filtered_weeks = df[df['Period'].isin(date_range)]

     
    df=df_filtered_weeks    
    list_name=['All']+list(set(df['Name']))
    list_name = [element for element in list_name if str(element) != "nan"]
    selection_name=st.selectbox('Select name:', list_name)
    df.selection_name=selection_name
        
    if selection_name!='All':
        df1=df.loc[df['Name']==selection_name]
    else:
        df1=df[~df['Name'].isnull()]
        
        
        
        
    group_list=['All']+list(set(df['Group']))
    group_list = [element for element in group_list if str(element) != "nan"]
    selection_group=st.selectbox('Select group:', group_list)
    df.selection_group=selection_group
    
    if selection_group!='All':
        df2=df1.loc[df['Group']==selection_group]
    else:
        df2=df1
        
    
    st.subheader('Total')
    sum_r=df2['Sum_R'].sum()#real
    sum_p=df2['Sum_Scheduled'].sum()#assumption
    correction=sum_r-sum_p
    df2['Total delta']=np.nan

    if len(df2) > 0:
        df2['Note']=np.where(df2['Price'].isnull(),"No price",df2['Note'] ) 
        df2['Note']=np.where(df2['Date'].isnull(),"No date",df2['Note'] )
        
        df2['Total delta']=np.nan
        df2.loc[-1,'Total delta']=correction
        df2['Total sum']=np.nan
        df2.loc[-1,'Total sum']=sum_r
        df2['Total scheduled']=np.nan
        df2.loc[-1,'Total scheduled']=sum_p        
        df2['Week_no_int']='Summary: last row of <T>, <U>, <V>'
        st.metric(label='Summary', value=f"${sum_r}", delta=correction, delta_color="normal", help=None)
        st.metric(label='Actual', value=f"${sum_r}", delta=None, delta_color="normal", help=None)
        st.metric(label='Scheduled', value=f"${sum_p}", delta=None, delta_color="normal", help=None)
        
    form = st.form("my_form")    
    

    #================
    group_list=list(set(df_filtered_weeks['Group']))
    sum_list=[]
    for group in group_list:
        df_group=df_filtered_weeks.loc[df_filtered_weeks['Group']==group]
        sum_i=df_group['Sum_R'].sum()
        sum_list.append(sum_i)
    group_count= pd.DataFrame({'Group':group_list,'Sum_R':sum_list})  
    #================
    
    
    st.sidebar.title('Analysis')
    
    
    st.sidebar.subheader(f'With Selection <<{selection_name}>> from <<{selection_group}>> group and the period Generate Output')
    time_str=time.strftime("%Y_%m_%d_%H%M")
    filename="Invoice_"+time_str + '_' + selection_name + '.xlsx' 
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df2.to_excel(writer, sheet_name=selection_name, index=False)
        writer.save()    
        
                
        st.sidebar.download_button(
            label="Download Excel Output",
            data=buffer,
            file_name=filename,
            mime="application/vnd.ms-excel",
            )

        
    st.sidebar.subheader('Show Graph')
    if st.sidebar.checkbox('Histogram for Groups in the time range', False):
        st.markdown('## Sums by Groups')
        fig=px.bar(group_count, x='Group', y='Sum_R', color='Sum_R', height=500)
        st.plotly_chart(fig)
    
    st.sidebar.title('Clear')

    if st.sidebar.button('Clear All'):
        # Clear values from *all* memoized functions:
        st.experimental_memo.clear()
    #================


if __name__=='__main__':

    main()
 
