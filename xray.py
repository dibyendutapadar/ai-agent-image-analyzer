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



def main():
    st.title("Xray Evaluator")
    st.write("Upload image of Xray")

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
                local_vision_llm_response = local_vision_llm.invoke(input=["""the uploaded image is images of an Xray
                                                                            Process the image and provide an accurate description of which bone is shown and what is the issue in Medical terms"""], 
                                                                    images=[image])
                print("######## I got local_vision_llm_response ############")
                print(local_vision_llm_response)
                images_description = images_description.strip() + "\n\n" + f"image{n+1}: " + local_vision_llm_response.replace('\n', ' ')


            print("####################")
            print(images_description)
            print("####################")



            # Instagram Influencer Agent
            Agent = crewai.Agent(
                role="Radiologist", 
                goal="""
                From the provided description of an xray image, determine what is wrong and prepare a report for the patient
                """,
                backstory="You are an expert Radiologist who is skilled at Determining what is wrong from xray reports and advice solutions",
                llm=local_llm,
                allow_delegation=False, verbose=True)

            # Task for the Agent
            task = crewai.Task(description="""
                                From the provided description of an xray image, determine what is wrong and prepare a report for the patient
                                """,
                               agent=Agent,
                               expected_output=""" You have to provide the description of the Xray Image, a simple explanation and advice
                               output should be in markdown format as below

                               ## Image Description 
                               <Description provided in the image description {image_description}>

                               ## Analysis
                               <which area, bones it is and what is wrong in simple terms so that the patient can understand>

                               ## Procedure 
                               <Procedure of treatment and >

                               ## Advice
                                <advice for the patient on treating the issue>

                               """)

            # Crew for Instagram Influencer Agent
            crew = crewai.Crew(agents=[Agent], tasks=[task], verbose=True)
            agent_response = crew.kickoff(inputs={"image_description": images_description})


            st.write("Heres my recommendation", agent_response)


if __name__ == "__main__":
    main()