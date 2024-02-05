import streamlit as st
from snowflake.connector import SnowflakeConnection
import pandas as pd
SNOWFLAKE_ACC_DETAILS = {
    "user": "espadaAD",
    "account":'goinzcq-sy58844',
    "password":'espadaAD356@#!23',
    "warehouse":'WORK',
    "database":'EXAMPLE',
    "schema":'TEMP'
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""
    

def app():
    try:
        conn = SnowflakeConnection(**SNOWFLAKE_ACC_DETAILS)
        cursor = conn.cursor()
        st.sidebar.success("Connected the table sucessfully")
    except Exception as e:
        st.error(f"Not able to connect with the Snowflake: {e}")
        raise SystemExit()
    st.sidebar.divider()
    st.sidebar.header(f"Welcome :blue[{st.session_state.username}]" , divider='rainbow')
    # st.sidebar.divider()
    table_name = "new_information"
    functions = ['See the entries' ,'Create an entry', 'Edit the entry']
    with st.sidebar.header("What you want to do today"):
        choosed_option = st.sidebar.selectbox("Choose" , options=functions)

    if choosed_option == 'See the entries':
        select_statement = f"SELECT * FROM {table_name}"
        cursor.execute(select_statement)
        results = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]

        df = pd.DataFrame(results, columns=column_names)
        df = df.reset_index(drop=True)

        st.header(f"The Content of the table {table_name}")
        st.dataframe(df)


    if choosed_option == 'Create an entry':
                ##Input Form
        ID = st.text_input("Enter the unique ID")
        name = st.text_input("Enter your name", placeholder="name")
        age = st.number_input("Enter your Age", placeholder="age", value=0)
        gender = st.selectbox("select your gender" , options=['Male', 'Female'])
        hobbies = st.multiselect("Select your hobbies" , options=['playing outside', 'surfing mobile', 'gathering money'])
        hobbies_str = ','.join(hobbies)

        if st.button("Insert"):
            Insert_statement = f"""
                INSERT INTO {table_name} VALUES ({ID},  '{name}' , {age}, '{gender}', '{hobbies_str}')
            """
            cursor.execute(Insert_statement)
            st.success("The entry has been sucessfully added")

            
    
        
#---------login details-------------

def main():
    if st.session_state.authenticated:
        app()
    else:
        username = st.text_input("Username", placeholder="Please enter your username")
        password = st.text_input("Password", placeholder="Please enter your password")

        # store usename for displaying purpose
        st.session_state.username = username

        #Login Logic
        if st.button("Login"):
            if (username == "admin" and password == "admin"):
                st.session_state.authenticated = True
            else:
                st.error("Please Enter Correct Credentials")



if __name__ == "__main__":
    main(   )