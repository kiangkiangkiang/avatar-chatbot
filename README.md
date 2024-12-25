# Avatar Chatbot

## Overview

Welcome to the Avatar Chatbot project! This project aims to create an engaging and interactive chatbot that users can interact with using an avatar interface. The Avatar Chatbot enhances user experience by adding a visual and dynamic component to traditional text-based chatbots.

![Avatar Chatbot Overview](path_to_your_image.png)  

**Toy Demonstration**

To see a demonstration of the Avatar Chatbot in action, please refer to the video below:

![Avatar Chatbot Demo](path_to_your_video.mp4)

## Quickstart

Avatar Chatbot is implemented with complete frontend and backend separation, allowing users to independently develop components they are interested in while maintaining minimal dependencies. 

This means that users do not need to install large additional packages such as **Gradio**, **Streamlit**, **Chainlit**, or **Langchain**. Users can expand according to their own needs.

### Prerequisites

#### API Key

The only requirement for Avatar Chatbot is an OpenAI API Key (Only for Text Generation and Text to Speech). Users simply need to place their API Key in the environment variables (`.env` file) to successfully run the project.

- OPENAI_API_KEY

#### Dev. Environment

- Python 3.10
- Ubuntu 20.04
  
#### Note

Currently, Huggingface Models are not supported, but users can independently extend the related model inference modules!

### Clone Project

```sh
git clone https://github.com/kiangkiangkiang/avatar-chatbot.git
cd avatar-chatbot
```

### Launch Frontend Services

To get started with the frontend of the Avatar Chatbot, please follow these steps:

```sh
cd frontend
yarn
yarn dev
```

Now, you have started the frontend service. You can directly visit `http://localhost:5173` to check the current status. 

(Conversation is not possible at the moment because the backend has not been started yet.)

Any changes needed for the UI can be fully referenced from the contents inside the `./frontend` directory. For changes related to the avatar, you can refer to the #Customize-Avatar section.

### Backend

### Optional

#### Lip-Sync Package

#### Customize Avatar

1. **Clone the Repository**  
   Clone this repository to your local machine using the command:
   ```bash
   git clone https://github.com/yourusername/avatar-chatbot.git

Install Dependencies

Navigate into the project directory and install the necessary dependencies:

bash
cd avatar-chatbot
npm install
Run the Application

Start the chatbot application with the following command:

bash
npm start
Access the Chatbot

Open your web browser and go to http://localhost:3000 to interact with the Avatar Chatbot.

Reference
wget https://github.com/DanielSWolf/rhubarb-lip-sync/releases/download/v1.13.0/Rhubarb-Lip-Sync-1.13.0-Linux.zip

unzip

把整個資料夾移動到 bin 內（起後端服務的）

