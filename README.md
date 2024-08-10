# 📸 Insta Influencer Image Analyzer

Welcome to the **Insta Influencer Image Analyzer**! 🚀 This app is your go-to Instagram manager, designed to help you pick the best images and craft perfect captions for your Instagram posts, all powered by cutting-edge AI models.

## 💡 Overview

Ever struggled with selecting the best photo or coming up with a catchy caption? With the Insta Influencer Image Analyzer, those days are over. Just upload your images, and let the AI handle the rest. From picking the top shot to generating a caption that’s sure to engage your audience, this tool does it all!

## 🔧 How It Works

1. **Upload Your Photos**: Start by uploading your images in PNG, JPG, or JPEG format.
2. **AI Image Analysis**: The app uses LLAVA, a large multimodal model, to analyze and describe your images with incredible detail.
3. **Caption Crafting**: Based on the image descriptions, the AI generates a trending, engagement-optimized caption.
4. **AI Agent in Action**: Crew AI coordinates the entire process, ensuring you get the best possible outcome for your Instagram post.
5. **Ready-to-Post**: The app provides a breakdown of all images, the selected winner, and a ready-to-use caption.

## 🚀 The Technology Behind It

- **LLMs (Large Language Models)**: At the heart of this app are powerful LLMs that understand and generate human-like text.
- **LLaMA & LLAVA**: These models work together to process both text and images, making your Instagram posts stand out.
- **AI Agents & Crew AI**: Autonomous AI agents manage the selection and captioning process, ensuring top-notch results.

## 🛠 Installation & Setup

Make sure you have installed ollama and have the models llava and llama3.1 of your choice pulled in your local system

1. **Clone the Repo**:
    ```bash
    git clone https://github.com/dibyendutapadar/insta-influencer-analyzer.git
    ```
2. **Navigate to the Directory**:
    ```bash
    cd insta-influencer-analyzer
    ```
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Set Up Your API Keys**:
   - Add your Groq API key in the `secrets.toml` file.

5. **Run the App**:
    ```bash
    streamlit run <desired app file name>.py
    ```