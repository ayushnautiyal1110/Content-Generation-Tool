import streamlit as st
import newspaper
from newspaper import Article
# from txtai.pipeline import Summary
from PyPDF2 import PdfReader
import requests
import io 
import docx
import spacy
import spacy_streamlit
import en_core_web_sm

# Load the spaCy model
nlp = en_core_web_sm.load()

def generate_summary(text, max_words=100):
    # Process the input text
    doc = nlp(text)

    # Calculate the importance of each sentence based on the sum of its token ranks
    sentence_scores = []
    for sentence in doc.sents:
        score = sum([token.rank for token in sentence])
        sentence_scores.append((sentence, score))

    # Sort sentences by score in descending order
    sentence_scores.sort(key=lambda x: x[1], reverse=True)

    # Generate the summary by selecting the top sentences up to the max_words limit
    summary = []
    word_count = 0
    for sentence, score in sentence_scores:
        if word_count + len(sentence) <= max_words:
            summary.append(sentence.text)
            word_count += len(sentence)
        else:
            break

    return " ".join(summary) 

st.set_page_config(layout="wide")

@st.cache_resource

# @st.cache_data.clear()
# def summary_tex/

# @st.cache_data.clear

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = [p.text for p in doc.paragraphs]
    return '\n'.join(text)
# @st.cache_data.clear

def extract_text_from_pdf(file_path):
    reader=PdfReader(file_path)
    pages=""
    pages=reader.pages[0]
    text=pages.extract_text()
    return text

# @st.cache_data.clear

def extract_text_from_txt(uploaded_file):
    linestxt = []
    with io.TextIOWrapper(uploaded_file, encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            linestxt.append(line)
    return linestxt
# @st.cache_data.clear

def search(query):
    url = f"https://en.wikipedia.org/wiki/{query}"
    if url:
        article=newspaper.Article(url)
        article.download()
        article.parse()
        article.nlp()
        authors=article.authors
        t=article.title
        st.subheader("Title")
        st.write(''.join(t))
        # t1,t2=st.tabs(["Your Current Text","Your Summarize Text"])
        
        tab1,tab2=st.columns([1,1])
        with tab1:
            st.markdown("Your Current Text")
            st.info(article.text)
        with tab2:
            text1=article.text
            st.markdown("Your Summarize Text")
            st.write(article.summary)
    else:
        st.write("Please Enter the URL don't leave it blank")

# This is the Main Function where user select their choice
# @st.cache_data.clear
def main():
    st.sidebar.header("Main Menu")
    choice = st.sidebar.selectbox("",["Select your Choice","Content Generation using Text","Content Generation using Doc","Content Generation using URL","Content Generation using Search Engine"])

    if choice == "Select your Choice":
       st.title("Welcome To Content Generator")
       st.image("https://tweakyourslides.files.wordpress.com/2013/08/content-development-001.png",width=600)

    elif choice == "Content Generation using Text":
        st.title("Content Generation using Text")
    # https://www.themarcomavenue.com/blog/wp-content/uploads/2020/01/ugc-content-1024x640.png
        st.image("https://i.ytimg.com/vi/Xv2dE5oWMNY/maxresdefault.jpg",width=400)
        txt_input=st.text_area("Enter the Input")
        if txt_input is not None:
         if st.button("Summarize Text"):
             col1,col2=st.columns([1,1])
             with col1:
                  st.markdown("YOUR INPUT TEXT")
                  st.info(txt_input)
             with col2:
                  st.markdown("YOUR SUMMARY RESULT")
                  result=generate_summary(txt_input)
                  st.write(result)
        else:
            st.write("Please Enter Some Input text")

    elif choice == "Content Generation using Doc":
        st.subheader("Content Generation using Documentation")
        st.image("https://nastroyvse.ru/wp-content/uploads/2017/05/konvertaciya-xml-v-pdf-txt-doc.jpg",width=300)
        inp_file=st.file_uploader("Upload Your File",type=["pdf",'txt',"docx"])
    # st.write(inp_file.name)
        if inp_file is not None:
            if st.button("Summarize Document"):
                if inp_file.name.lower().endswith(".pdf"):
                    col1,col2=st.columns([1,1])
                    ext_text=extract_text_from_pdf(inp_file)
                    with col1:
                        st.markdown("YOUR INPUT FILE",)
                
                        st.info(ext_text)
                    with col2:
                        st.markdown("SUMMARY of your FILE")
                        result=generate_summary(ext_text)
                        st.write(result)

                elif inp_file.name.lower().endswith(".docx"):
                    extracted_text = extract_text_from_docx(inp_file)
                    col1,col2=st.columns([1,1])
                    with col1:
                        st.markdown("YOUR INPUT FILE")
                        st.info(extracted_text)
                    with col2:
                        st.markdown("SUMMARY of your FILE")
                        result=generate_summary(extracted_text)
                        st.success(result)
                elif inp_file.name.lower().endswith(".txt"):
                    col1,col2=st.columns([1,1])
                    ext_text=extract_text_from_txt(inp_file)
                    with col1:
                        st.markdown("YOUR INPUT FILE")
                        st.info("".join(ext_text))
                    with col2:
                        st.markdown("SUMMARY of your FILE")
                        result=generate_summary("".join(ext_text))
                        st.write(result)
                        
            else:
                st.write(" ")


    elif choice == "Content Generation using URL":
        st.title("Content Generation using URL")
        st.image("https://i1.wp.com/www.dignited.com/wp-content/uploads/2018/09/url_istock_nicozorn_thumb800.jpg?fit=640%2C360&ssl=1",width=400)
    # url = f"https://en.wikipedia.org/wiki/{query}"
        try: #Checking that Url has something on it or not 
            url1=st.text_input('',placeholder='Paste and Copy URL')
            if st.button("Summarize URL"):
                article=newspaper.Article(url1)
                article.download()
                article.parse()
                article.nlp()
                authors=article.authors
                t=article.title
                st.subheader("Title")
                st.write(''.join(t))
                if not not authors:
                    st.subheader("Author Name")
                    st.write(','.join(authors))
                # article.nlp()
                # st.subheader('Keywords')
                # key=article.keywords
                # st.write(','.join(key))
                # t1,t2=st.tabs(["Your Current Text","Your Summarize Text"])
                
                tab1,tab2=st.columns([1,1])
                with tab1:
                    st.markdown("Your Current Text")
                    st.info(article.text)
                with tab2:
                    text1=article.text
                    st.markdown("Your Summarize Text")
                    st.write(article.summary)
        except Exception as e:
            print(" ")
        
        
    elif choice=="Content Generation using Search Engine":
        st.title(" Content Generation using Search Engine ") 
        st.image("http://blackbirdesolutions.com/files/2013/06/search-marketing.jpg",width=300)
        txt_input=st.text_input("Enter the Keyword to Search")
    # st.write((txt_input))
    
        if st.button("Search"):  
            if txt_input:
                try:
                    # st.info(search(txt_input))
                    st.caption(search(txt_input))
                except Exception as e:
                    
                    st.info("Please Enter the Proper String")
            else:
                st.write("Please Enter the Text Input don't leave it blank")
    # elif choice=="Content Generation using Voice":
    #     st.title("Content Generation using Voice")
    #     st.image("https://www.techpocket.org/wp-content/uploads/2020/02/Best-Speech-to-text.jpg",width=500)
    #     if(st.button("Click to Speak")):
    #         st.write("Recognizing Voice.........")
    #         recognizer = sr.Recognizer()
    #         with sr.Microphone() as source:
    #             # print("Say something:")
    #             audio_data = recognizer.listen(source,timeout=60)
    #         try:
    #             text = recognizer.recognize_google(audio_data)
    #             col1,col2=st.columns([1,1])
    #             with col1:
    #                 st.write("Your Voice Input")
    #                 st.info(text)
    #             with col2:
    #                 st.write("Your Summarize Voice Input")
    #                 st.success(generate_summary(text))    
    #         except sr.UnknownValueError:
    #             st.write("Speech Recognition could not understand audio")
    #         except sr.RequestError as e:
    #             st.write(f"Could not request results from Google Speech Recognition service; {e}")
            

if __name__ == "__main__":
    main()
       
    
