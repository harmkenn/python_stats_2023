import streamlit as st
import plotly_express as px
from scipy.stats import *
import pandas as pd
import numpy as np
from plotnine import *

def app():
    # title of the app
    st.markdown("Normal Probaility")
    st.sidebar.subheader("Normal Settings")
    norm_choice = st.sidebar.radio("",["z to Probability","Probability to z"])

    if norm_choice == "z to Probability":
        c2,c3,c4 = st.columns(3)
        tp = 0

        with c2:
            lzp = float(st.text_input("Left Z",-1))
        with c3:
            st.markdown("Shade:")
            ls = float(st.checkbox("Left"))
            zpc = float(st.checkbox("Center",1))
            rs = float(st.checkbox("Right"))
        with c4:
            rzp = float(st.text_input("Right Z",1))
           
        g1,g2 = st.columns((1,3))
        
        with g2:
            x = np.arange(-4,4,.01)
            y = norm.pdf(x)
            ndf = pd.DataFrame({"x":x,"y":y})
            fig = px.line(ndf, x = 'x', y = 'y', template= 'simple_white')
            tp = 1
            

            if ls == 0:
                tp = tp - norm.cdf(lzp)
                ndf.loc[(ndf.x <= lzp),'y'] = 0
        
            if zpc == 0:
                tp = tp - (norm.cdf(rzp) - norm.cdf(lzp))
                ndf.loc[(ndf.x >= lzp) & (ndf.x <= rzp),'y'] = 0 
                
            if rs == 0:
                tp = tp - (1 - norm.cdf(rzp))
                ndf.loc[(ndf.x >= rzp),'y'] = 0
            
            fig.add_trace(px.area(ndf, x = 'x', y = 'y', template= 'simple_white').data[0])
                
            st.plotly_chart(fig, use_container_width=True)    
            
            
        with g1:
            st.markdown(f"Total Probability: {tp}")
            
    if norm_choice == "Probability to z":
        c2,c3,c4 = st.columns(3)

        with c2:
            sp = float(st.text_input("Probability", 40))
        with c3:
            st.markdown("Shade:")
            shade = st.radio("Shade:",["Left","Center","Right"])
        
        g1,g2 = st.columns((1,3))
        with g2:
            x = np.arange(-4,4,.1)
            y = norm.pdf(x)
            ndf = pd.DataFrame({"x":x,"y":y})
            normp = ggplot(ndf) + geom_line(aes(x=x,y=y)) + coord_fixed(ratio = 4) 

            if shade == "Left":
                z = norm.ppf(sp/100)
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "steelblue", xlim = (-4,z))
                lz = z
                rz = z
            if shade == "Center":
                z = norm.ppf(((100-sp)/2)/100)
                lz = z 
                rz = -z
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "steelblue", xlim = (lz,rz))
                
            if shade == "Right":
                z = norm.ppf((100-sp)/100)
                lz = z
                rz = z
                normp = normp + stat_function(fun = norm.pdf, geom = "area",fill = "steelblue", xlim = (lz,4))
                
            normp = normp + geom_segment(aes(x = lz, y = 0, xend = lz, yend = norm.pdf(lz)),color="red")
            normp = normp + geom_segment(aes(x = rz, y = 0, xend = rz, yend = norm.pdf(rz)),color="red")
            normp = normp + geom_line(aes(x=x,y=y)) + coord_fixed(ratio = 4) + xlab('z') + ylab('')
            st.pyplot(ggplot.draw(normp))
        with g1:
            st.markdown(f"z-Score: {z}")
            
    # store variables


    