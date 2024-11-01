import streamlit as st

#multiple select

my_lang = ['python', 'Julia', 'go']

choice = st.selectbox("language", my_lang)
st.write(f'you selected {choice}')

spoken_lang = ['Eng', 'Ger', 'ITL']
my_spoken_lang = st.multiselect("spoken_lang", spoken_lang)
st.write(f'you selected {my_spoken_lang}')

age = st.slider("age", 1, 100)
st.write(age)

color = st.slider("Choose Color", options=['yellow',
                                            'red',
                                            'blue',
                                            'black',
                                            'white'],
                                            value=
                                            ('yellow',
                                            'red',
                                            'blue',
                                            'black',
                                            'white'))