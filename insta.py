import streamlit as st
from langchain_community.llms import Ollama 
import base64
import crewai
from PIL import Image
from langchain_groq import ChatGroq
from langchain.globals import set_verbose
set_verbose(True)

GROQ_API_KEY = st.secrets["groq"]["api_key"]

# Initialize the models
# ----- using local llm ---------
# local_llm = Ollama(model="llama3.1:8b")  # Text-based LLM
# -------------------

# ----- using groq ---------
llm=ChatGroq(temperature=0,
             model_name="llama3-70b-8192",
             api_key=GROQ_API_KEY)
local_llm=llm
# -------------------

local_vision_llm = Ollama(model="llava:latest")  # Multimodel / Vision LLM


def image_encoder(file):
    return base64.b64encode(file.read()).decode('utf-8')

def process_images(uploaded_files):
    images_info_list = [image_encoder(file) for file in uploaded_files]
    images_description = ""


    for n, image in enumerate(images_info_list):
        local_vision_llm_response = local_vision_llm.invoke(input=["Process and Describe the image accurately with minute details of setting, background and objects"], images=[image])
        images_description = images_description.strip() + "\n\n" + f"image{n+1}: " + local_vision_llm_response.replace('\n', ' ')
    
    return images_description

def main():
    st.title("Instagram Influencer Image Analyzer")
    st.write("Upload multiple images to analyze and receive the best caption for Instagram.")

    uploaded_files = st.file_uploader("Choose images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

    if uploaded_files:
        st.write("Uploaded Images:")
        for uploaded_file in uploaded_files:
            img = Image.open(uploaded_file)
            # img_resized = img.resize((300, 300)) 
            st.image(img, caption=uploaded_file.name)


        if st.button("Submit"):
            images_description = ""
            

            def image_encoder(file):
                file.seek(0)  # Reset file pointer to the beginning
                return base64.b64encode(file.read()).decode('utf-8')
            
            print("######## I got image encoded ############")

            images_info_list = [image_encoder(file) for file in uploaded_files]
            
            print("######## I got info list ############")

            for n, image in enumerate(images_info_list):
                local_vision_llm_response = local_vision_llm.invoke(input=["Process and Describe the image accurately with minute details of setting, background and objects"], images=[image])
                print("######## I got local_vision_llm_response ############")
                images_description = images_description.strip() + "\n\n" + f"image{n+1}: " + local_vision_llm_response.replace('\n', ' ')

            print("####################")
            print(images_description)
            print("####################")


            # Instagram Influencer Agent
            Agent = crewai.Agent(
                role="Insta Influencer", 
                goal="""
                From the provided image descriptions,decide which image will get more likes on Instagram and explain why 
                based on the image description.
                Please write a suitable caption that would maximize the chances of likes, traffic conversions based on the image that you choose.
                You can consider the current season, today's date, any particular events of this month, trending hashtags and emojis, 
                to create the perfect caption.
                """,
                backstory="You are a social media influencer that maximizes the chances of likes, traffic conversions of every post.",
                llm=local_llm,
                allow_delegation=False, verbose=True)

            # Task for the Agent
            task = crewai.Task(description="""
                From the provided image descriptions,decide which image will get more likes on Instagram and explain why 
                based on the image description.
                Please write a suitable caption that would maximize the chances of likes, traffic conversions based on the image that you choose.
                You can consider the current season, today's date, any particular events of this month, trending hashtags and emojis, 
                to create the perfect caption.
                                """,
                               agent=Agent,
                               expected_output="""
                               Decription of all the uploaded images descriptions {image_description}, The most suitable picture out of them and a trending caption for the selected picture as an Instagram post. 
                               
                               
                               The  output should be in a markdown format. the output should only contain the markdown format of the response and nothing else.
                               
                               example below
                               
                               ## Uploaded Images Analysis
                               | image number | image short description | image detailed description |

                               ## Selected Image 
                               < the selected image and why it is selected >

                               ## Caption 

                               <the caption>

                               ### Why this caption
                               <explanation of why this caption>


                               """)

            # Crew for Instagram Influencer Agent
            crew = crewai.Crew(agents=[Agent], tasks=[task], verbose=True)
            agent_response = crew.kickoff(inputs={"image_description": images_description})


            st.write("Heres my recommendation", agent_response)


if __name__ == "__main__":
    main()