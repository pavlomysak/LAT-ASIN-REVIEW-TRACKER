import streamlit as st
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
import time

# Streamlit App Setup
st.title("Amazon Review Insights")
st.write("What are consumers talking about?? Let's find out!")

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

options = Options()
options.add_argument("--headless")  # Headless mode
options.add_argument("--no-sandbox")  # Disable sandboxing
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
options.add_argument("--disable-gpu")  # Applicable for Windows
options.add_argument("--remote-debugging-port=9222")
options.binary_location = "/usr/bin/chromium"


#@st.cache_resource
#def load_sentiment_analyzer():
#    return pipeline("sentiment-analysis", model='siebert/sentiment-roberta-large-english')

#@st.cache_resource
#def load_summarizer():
#    return pipeline("summarization", model="facebook/bart-large-cnn")

def run_analysis(ASIN):

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
        options=options)

    all_revs = []
    page_number = 1
    
    while True:
        url = f'https://www.amazon.com/product-reviews/{ASIN}/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&pageNumber={page_number}&sortBy=recent'
        driver.get(url)
        
        try:
            reviews = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, '//span[@data-hook="review-body"]//span'))
            )
            
            if not reviews:
                break
            
            for review in reviews:
                all_revs.append(review.text)

            time.sleep(2) 
            
            page_number += 1
        except TimeoutException:
            st.warning(f"Timed out waiting for page {page_number} to load.")
            break

    driver.quit()

    st.write(all_revs)
 
with st.form(key="my_form"):
    asin_value = st.text_input("ASIN", key="ASIN")
    submit_button = st.form_submit_button("Run Analysis")

if submit_button:
    run_analysis(asin_value)