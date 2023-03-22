import streamlit as st
from PIL import Image


class Main_page:
    def hello(self):
        st.header('欢迎使用')

    def show_image(self):
        image = Image.open('prothentic.jpg')
        st.image(image)

    # def show_func(self):
    #     st.subheader('请从侧边栏选择功能')


s = Main_page()
s.hello()
s.show_image()
# s.show_func()





