import streamlit as st
import base64
import csv
import requests

import pandas as pd

st.set_page_config(page_title="Rank Tracker",page_icon="📈",layout="wide"   )

st.title('Rank Tracker by Yaniss Illoul from Martech with Me')
st.header("Rank Tracker (Serpstack API Edition)")
st.markdown("In order to use this app, you will need a **free Serpstack API** key that allows you to use this interface for 100 free calls a month. You can generate your key by [signing up here](http://serpstack.com?utm_source=FirstPromoter&utm_medium=Affiliate&fpr=martechwithme).")
st.markdown("This interface has been developed by [Yaniss Illoul](https://www.linkedin.com/in/yanissi/) (Feel free to connect!) from [Martech with Me](https://martechwithme.com).")
st.markdown("If you like this project, please consider visiting my website for more Martech tools and tutorials. Don't hesitate to reach out if you have any feature requests or ideas.")

form = st.form(key='rankTrackerForm')

serpstack_key = form.text_input("Input Serpstack API key",value="")



device = form.selectbox('Choose Device (Mobile/Tablet or Desktop)',('desktop','mobile','tablet'))
google_domain = form.text_input('Enter Google Domain (google.fr, google.de, ...)',value='google.com')


keywordQuery = form.text_input('Enter Keyword(s). If multiple, separate with a comma.',value=None)
domainQuery = form.text_input('Enter Domain(s). If multiple, separate with a comma.',value=None)


submit_button = form.form_submit_button(label='Submit')

if submit_button:

    if "," not in keywordQuery and "," not in domainQuery:

        serp_results = requests.get(f"http://api.serpstack.com/search?access_key={serpstack_key}&query={keywordQuery}&device={device}&google_domain={google_domain}&auto_location=1")
        position = "Either not ranking or >18"

        for every in serp_results.json()["organic_results"]:
            if domainQuery in every["domain"]:
                position = every["position"]
            else:
                pass
        
        if position == "Either not ranking or >18":
            output = st.write(f"{domainQuery} is either not ranking or >18 for {keywordQuery}")

        else:
            output = st.write(f"{domainQuery} ranks #{position} for the keyword '{keywordQuery}' on {device} on {google_domain}.")


    elif "," in keywordQuery and "," in domainQuery:

        df = pd.DataFrame()


        keywordQuery = keywordQuery.split(",")

        df['Keywords'] = keywordQuery
        df['Google Domain'] = google_domain
        df['Device'] = device

        domainQuery = domainQuery.split(",")

        progressBar = st.progress(len(domainQuery)*len(keywordQuery))
        progressCount = 0
        progressBar = progressBar.progress(progressCount/(len(domainQuery)*len(keywordQuery)))

        for domain in domainQuery:

            listPosition = []

            for keyword in keywordQuery:

                serp_results = requests.get(f"http://api.serpstack.com/search?access_key={serpstack_key}&query={keyword}&device={device}&google_domain={google_domain}&auto_location=1")
                position = "Either not ranking or >18"

                for result in serp_results.json()["organic_results"]:
                    if domain in result["domain"]:
                        position = result["position"]
                    else:
                        pass

                listPosition.append(str(position))
                print(position)
                print(listPosition)

                progressCount = progressCount + 1
                progressBar = progressBar.progress(progressCount/(len(domainQuery)*len(keywordQuery)))
            
            df[domain] = listPosition
        st.dataframe(df)


    elif "," not in keywordQuery and "," in domainQuery:

        df = pd.DataFrame()

        df['Keywords'] = keywordQuery
        df['Google Domain'] = google_domain
        df['Device'] = device

        domainQuery = domainQuery.split(",")

        progressBar = st.progress(len(domainQuery))
        progressCount = 0

        for domain in domainQuery:

            listPosition = []

            serp_results = requests.get(f"http://api.serpstack.com/search?access_key={serpstack_key}&query={keywordQuery}&device={device}&google_domain={google_domain}&auto_location=1")
            position = "Either not ranking or >18"

            for result in serp_results.json()["organic_results"]:
                if domain in result["domain"]:
                    position = result["position"]
                else:
                    pass

            listPosition.append(str(position))

            progressCount = progressCount + 1
            progressBar = progressBar.progress(progressCount/(len(domainQuery)))
            
            df[domain] = listPosition

        st.dataframe(df)

    elif "," in keywordQuery and "," not in domainQuery:

        df = pd.DataFrame()

        keywordQuery = keywordQuery.split(",")

        df['Keywords'] = keywordQuery
        df['Google Domain'] = google_domain
        df['Device'] = device

        listPosition = []

        progressBar = st.progress(len(keywordQuery))
        progressCount = 0

        for keyword in keywordQuery:

            serp_results = requests.get(f"http://api.serpstack.com/search?access_key={serpstack_key}&query={keyword}&device={device}&google_domain={google_domain}&auto_location=1")
            position = "Either not ranking or >18"

            for result in serp_results.json()["organic_results"]:
                if domainQuery in result["domain"]:
                    position = result["position"]
                else:
                    pass

            listPosition.append(str(position))

            progressCount = progressCount + 1
            progressBar = progressBar.progress(progressCount/(len(keywordQuery)))
        
        df[domainQuery] = listPosition
        st.dataframe(df)

    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown('### **⬇️ Download Output as CSV File **')
    href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as "filename.csv")'
    st.markdown(href, unsafe_allow_html=True)
