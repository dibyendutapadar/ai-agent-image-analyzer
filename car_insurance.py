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
    st.title("Car Damage Evaluator")
    st.write("Upload images of the damage from multiple angles")

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
                local_vision_llm_response = local_vision_llm.invoke(input=["""the uploaded images are of a car damage
                                                                            Process the image and provide an accurate description of what type of car, where is the damage and how extensive is the damage"""], 
                                                                    images=[image])
                print("######## I got local_vision_llm_response ############")
                print(local_vision_llm_response)
                images_description = images_description.strip() + "\n\n" + f"image{n+1}: " + local_vision_llm_response.replace('\n', ' ')


            print("####################")
            print(images_description)
            print("####################")



            # Instagram Influencer Agent
            Agent = crewai.Agent(
                role="Car Mechanic", 
                goal="""
                From the provided description of an car damage, analyse the damage and provide step by step repair procedure, and parts required
                """,
                backstory="a car mechanic expert in body shop denting, painting and accidental repairs",
                llm=local_llm,
                allow_delegation=False, verbose=True)

            # Task for the Agent
            task = crewai.Task(description="""
                                From the provided description of an car damage, analyse the damage and provide step by step repair procedure, and parts required
                                """,
                               agent=Agent,
                               expected_output=""" You have to provide the Analysis of the damage by collating the information in the provided description of the damage {image_description}, repair procedure and parts required

                               ## Damage Analysis
                               < Damage Analysis>

                               ## Repair Procedure
                               <step by step repair procedure>

                               ## Parts Required 
                               <Parts required and a tentative price of the part for this kind of a car in India>

                               """)

            # Crew for Instagram Influencer Agent
            crew = crewai.Crew(agents=[Agent], tasks=[task], verbose=True)
            agent_response = crew.kickoff(inputs={"image_description": images_description})


            st.write("Heres my recommendation", agent_response)


if __name__ == "__main__":
    main()