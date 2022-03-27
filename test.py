import streamlit as st
import streamlit.components.v1 as components
from iteru.map import *
import base64
m = Map()

st.components.v1.html(m.save('test.html'), width=600,
                      height=600, scrolling=True)
