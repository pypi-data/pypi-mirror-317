import streamlit as st
import smtplib
import pyttsx3

#'''------------> add bg image function <--------------'''
def bg_image(url):
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)
   
#---------function passing url--------
#a='https://w0.peakpx.com/wallpaper/314/578/HD-wallpaper-dark-bg-bg-wp-abstract-dark.jpg'
#bg_image(a)

#'''------------> header remove function <--------------'''

def header_hide():
    hide="""
    <style>
    #mainmenu {visiblity:hidden}
    header{visibility:hidden;}
    </style>
    """
    st.markdown(hide,unsafe_allow_html=True)
#---------hide header menu------------
#header_hide()

#---------------> check box into button <-----------------

def checkbox_into_button():
    st.markdown("""
    <style>
    /* Hide the actual checkbox */
    div[data-testid="stCheckbox"] > label > div:first-child {
        display: none;
    }

    /* Style the label (which is now acting like a button) */
    div[data-testid="stCheckbox"] > label {
        background-color: blue; /* Green background */
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition-duration: 0.4s;
    }

    /* Hover effect */
    div[data-testid="stCheckbox"] > label:hover {
        background-color: white;
        color: black;
        border: 2px solid blue;
    }
    </style>
    """, unsafe_allow_html=True)


#checkbox_into_button()-----Note: if you call the fuction entire page of the code in check box is change , if want to avoid the problem to splite the separate module
#st.checkbox("main")



#----------------> side bar bg image <-------------------------

def sidebar_bg_image(ur):
     st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("{ur}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


#st.sidebar.header("Sidebar")
#sidebar_bg_image('https://cdn.vectorstock.com/i/1000v/27/12/black-crystal-blue-vector-1702712.jpg')


#-------------->sending mail<-------------------
def mail(sender_email,receiver_email,subject_fun,body_fun,password):
    email_sender =sender_email
    email_receiver = receiver_email
    subject = subject_fun
    body = body_fun

        
    text=f"subject:{subject}\n\n{body}"

    server=smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()

    server.login(email_sender,password)

    server.sendmail(email_sender,email_receiver,text)
    server.quit()
    
#---------------------->text to speech<---------------

def text_to_speech(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
#user_input=input("Enter a speech sentence: ")
#text_to_speech(user_input)