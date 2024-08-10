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

local_vision_llm = Ollama(model="llava:34b")  # Multimodel / Vision LLM


# def image_encoder(file):
#     return base64.b64encode(file.read()).decode('utf-8')

# def process_images(uploaded_files):
#     images_info_list = [image_encoder(file) for file in uploaded_files]
#     images_description = ""


#     for n, image in enumerate(images_info_list):
#         local_vision_llm_response = local_vision_llm.invoke(input=["the uploaded images are images of answer sheet. Process and extract the handwritten texts including the question and answers"], images=[image])
#         images_description = images_description.strip() + "\n\n" + f"image{n+1}: " + local_vision_llm_response.replace('\n', ' ')
    
#     return images_description

def main():
    st.title("Answer sheet Evaluator")
    st.write("Upload images of handwritten answer sheet for evaluation")

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
                local_vision_llm_response = local_vision_llm.invoke(input=["""the uploaded images are images of answer sheets. 
                                                                           on the sheets There are printed questions with alloted marks
                                                                           every question is followed by hand written answer by the student
                                                                            Process the image and extract the texts including the questions, alloted marks and the corresponding answers"""], 
                                                                    images=[image])
                print("######## I got local_vision_llm_response ############")
                images_description = images_description.strip() + "\n\n" + f"image{n+1}: " + local_vision_llm_response.replace('\n', ' ')


            print("####################")
            print(images_description)
            print("####################")



            # Instagram Influencer Agent
            Agent = crewai.Agent(
                role="Answer sheet evaluator", 
                goal="""
                From the provided transcript of a hand written answer script determine the questions, alloted marks and answers to each of the questions that the student has written
                explain how well a answer is written what could have been done better
                explain how much marks in percentage should be given to the student for each answer to each question
                """,
                backstory="You are a teacher with extensive knowledge who evaluates answer sheets with logic and precision",
                llm=local_llm,
                allow_delegation=False, verbose=True)

            # Task for the Agent
            task = crewai.Task(description="""
               From the provided transcript of a hand written answer script determine the questions, alloted marks and answers to each of the questions that the student has written
                explain how well a answer is written what could have been done better
                explain how much marks in should be given to the student for each answer to each question
                                """,
                               agent=Agent,
                               expected_output="""
                               Analyse the image description {image_description}, and provide the question and answer written by the student along with 
                               how well the answer is written, what could be done better
                               marks in percentage, explanation of the marks
                               
                               
                               The  output should be in a markdown format. the output should only contain the markdown format of the response and nothing else.
                                 ## Assessment
                               
                               Next for each question repeat the below in this format

                                # Question
                                <the question>
                                # written Answer
                                <the answer>
                               
                               ## Answer analysis 
                               < how well the answer is written, what could be done better >

                               ## Marks 
                                < Mark to be given for this answer, and why>


                               """)
            

            # Crew for Instagram Influencer Agent
            crew = crewai.Crew(agents=[Agent], tasks=[task], verbose=True)
            agent_response = crew.kickoff(inputs={"image_description": images_description})


            st.write("Heres my recommendation", agent_response)


if __name__ == "__main__":
    main()