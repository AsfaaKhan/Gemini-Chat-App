from dotenv import load_dotenv
import os
from agents import Agent, AsyncOpenAI,OpenAIChatCompletionsModel, RunConfig, Runner,function_tool
import streamlit as st
import asyncio

load_dotenv()


MODEL_NAME="gemini-2.0-flash"
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
external_client=AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

model=OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=external_client
    )

config=RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
    )
assistant = Agent(
    name="Assistant",
    instructions="Your job is to resolve qurries",
    model=model
    )


async def get_response(user_input):
    result = await Runner.run(assistant,user_input,run_config=config)  
    return result.final_output

# Stremlit
st.set_page_config(page_title="Gemini Search App",page_icon="🧠",layout="centered")

st.title("🧠 Gemini Search App")

user_input = st.text_input(" Enter The question : ")

if st.button("Search"):

    if user_input.strip() == "":
        st.warning("Please enter a question.")

    else:
        with st.spinner("🗯 Thinking..."):
            response = asyncio.run(get_response(user_input))
            st.title("🎊 Your Answer: ")
            st.write(response)

