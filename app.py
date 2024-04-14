import streamlit as st
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth,db
import google.generativeai as genai
import pyttsx3
import plotly.express as px
import pandas as pd
import sys
sys.path.insert(1,r"C:\Users\LENOVO T480\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\streamlit_option_menu")
from streamlit_option_menu import option_menu
from plotly.graph_objs import Pie

if not firebase_admin._apps:
    cred=credentials.Certificate('abhiram-866b9-firebase-adminsdk-nsy1t-30ce645102.json')
    firebase_admin.initialize_app(cred,{
       'databaseURL':'https://abhiram-866b9-default-rtdb.firebaseio.com/' 
    })

load_dotenv()

@st.cache_resource
def get_session_state():
    return {"is_authenticated": False}

def login_page():
    st.title("Welcome to :blue[MindMate]")
    choice=st.selectbox('Login/Signup', ['Login', 'Sign Up'])

    if choice=='Login':
        email=st.text_input('Email Address')
        password=st.text_input('Password',type='password')
        if st.button("Login"):
            user=login(email, password) 
            if user:
                if isinstance(user, firebase_admin.auth.UserRecord):
                    user_id=user.uid
                else:
                    user_id=getattr(user,"uid",None)

                if user_id:
                    st.session_state.user={"uid": user_id}
                    session_state["is_authenticated"]=True
                    st.success("Login successful!")
                else:
                    st.error("User ID not found in user object. Please contact support.")
            else:
                st.error("Login failed. Please check your credentials.")



    elif choice=='Sign Up':
        email=st.text_input('Email Address')
        password=st.text_input('Password', type='password')
        username=st.text_input("Enter your unique Username")
        if st.button('Sign Up'):
            user=signup(email, password, username)
            if user:
                st.success("Hi and Welcome"+username)
            else:
                st.error("Account sign up failed")


ref=db.reference('/')


def login(email, password):
    try:
        user=auth.get_user_by_email(email)
        st.session_state.user=user
        return user
    except firebase_admin.auth.UserNotFoundError:
        st.error("User not found. Please check your credentials.")
        return None
    except Exception as e:
        st.error(f"An error occurred during login: {e}")
        return None

def signup(email, password, username):
  try:
    user=auth.create_user(email=email, password=password)
    st.success("Account Created Successfully!")
    st.balloons()

    user_ref=ref.child("users").push()
    user_ref.set({
        "email": email,
        "handle": username,
        "ID": user.uid
    })

    return user
  except Exception as e:
    st.error(f"An error occurred during signup: {e}")
    return None


def chat_section():
    st.title("Let's Talk")
    prompt=st.text_input("Tell me what's happening")

    API_KEY=os.environ.get("GOOGLE_API_KEY")
    genai.configure(api_key=API_KEY)

    model=genai.GenerativeModel("gemini-pro")

    engine=pyttsx3.init()
    voices=engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id) 
    engine.setProperty('rate',200)

    if st.button("Enter", key='chat_button'):
        response=model.generate_content(prompt)
        st.write("")
        st.header(":blue[Response]")
        
        st.markdown(response.text)
        engine.say(response.text)
        engine.runAndWait()
        return


def write_journal_entry(mood, content, user):
    try:
        if not user:
            print("Error: User not logged in!")
            return False

        if not user.get("uid"):
            print("Error: User ID not found in user object.")
            return False

        user_id=user.get("uid")

        user_ref=ref.child("users").child(user_id)
        timestamp=user_ref.push().key
        journal_ref=user_ref.child("journals").child(timestamp)

        journal_ref.set({
            "mood": mood,
            "content": content
        })

        return True
    except Exception as e:
        print(f"An error occurred during journal entry submission: {e}")
        return False


if "user" not in st.session_state:
    st.session_state.user=None

def journal_page():
    st.title("Journal")
    st.header("How are you feeling today?")
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    mood=st.radio("Mood:", options=['Positive', 'Negative', 'Neutral'],)
    content=st.text_area("Write your journal entry:", key="entry_content")
    
    if st.button("Submit Entry"):
        if st.session_state.user: 
            write_journal_entry(mood, content, st.session_state.user)
            st.success("Entry saved successfully!")
        else:
            return 
    
def dashboard():
    st.title("Dashboard")

    try:
        
        if st.session_state.get("user"):
            user_id=st.session_state.user.get("uid")
            if not user_id:
                st.error("User ID not found in session state. Please log in again.")
                return 

            user_ref=ref.child("users").child(user_id)
            journals_ref=user_ref.child("journals")

            journals_data=journals_ref.get() 

            if journals_data:
                journals=list(journals_data.values())  # Convert dictionary values to a list
                
                sentiment_counts={"Positive": 0, "Negative": 0, "Neutral": 0}

                for journal in journals:
                    mood=journal.get("mood")
                    sentiment_counts[mood] += 1

                #DataFrame from sentiment counts for column graph
                df_sentiments=pd.DataFrame(sentiment_counts.items(), columns=["Sentiment", "Count"])

                #column graph
                st.subheader("Number of Positive, Negative, and Neutral Entries (Column Graph)")
                fig_column=px.bar(df_sentiments, x="Sentiment", y="Count", color="Sentiment",
                                     template="plotly_dark", title="Number of Positive, Negative, and Neutral Entries")
                st.plotly_chart(fig_column, use_container_width=True) 

                #Nightingale chart
                st.subheader("Distribution of Journal Sentiments (Nightingale Chart)")
                fig_nightingale=px.bar_polar(df_sentiments, r="Count", theta="Sentiment", color="Sentiment",
                                                template="plotly_dark", title="Distribution of Journal Sentiments")
                st.plotly_chart(fig_nightingale, use_container_width=True)

                #jornals
                st.subheader("Your journals:")
                st.write(journals)
                
                return
            else:
                st.info("You don't have any journal entries yet. Why not write one?")
        else:
            st.error("Please log in to view your journals.")
        
    except Exception as e:
        print(f"An error occurred while retrieving journals: {e}")
        st.error("There was a problem loading your journals. Please try again later.")


def get_date_from_timestamp(timestamp):
  return f"Date extracted from timestamp: {timestamp[:10]}"

def main():
    global session_state
    session_state=get_session_state()
    
    if not session_state["is_authenticated"]:
        login_page()
    else:
        st.title(":blue[MindMate]")
        selected=option_menu(
            menu_title="", 
            options=["Journal", "dashboard", "chatbot"],
            orientation="horizontal",
            icons=["calendar-minus", "bar-chart", "chat-dots"],
        )
        if selected == "Journal":
            journal_page()
        elif selected == "dashboard":
            dashboard()
        elif selected == "chatbot":
            chat_section()

if __name__ == "__main__":
    main()
