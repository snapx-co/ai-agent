from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

from browser_use import Agent, BrowserSession
from dotenv import load_dotenv
load_dotenv()

import asyncio
import os

# llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.1)
# planner_llm = ChatOpenAI(model='gpt-4.1-mini', temperature=0.7)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
planner_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

# llm = ChatOllama(model="deepseek-r1:latest", temperature=0.2)
# planner_llm = ChatOllama(model="deepseek-r1:latest", temperature=0.1)

# Domain-specific sensitive data
sensitive_data = {
    'https://x.com': {'x_username': os.getenv('TWITTER_USER_NAME'), 'x_password': os.getenv('TWITTER_PASSWORD')}
}

# Set browser session with allowed domains that match all domain patterns in sensitive_data
browser_session = BrowserSession(
    executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    user_data_dir=os.path.join(os.path.dirname(__file__), 'chrome_user_data'),
    allowed_domains=[
        'https://x.com'
    ]
)

extend_system_message = ''
# Read the prompt from .agent_prompt file
with open(os.path.join(os.path.dirname(__file__), '.agent_prompt'), 'r', encoding='utf-8') as f:
    extend_system_message = f.read()

if extend_system_message == '':
    print("No prompt file found. Please create a .agent_prompt file.")
    exit(1)

async def main():
    while True:
        try:
            agent = Agent(
                task="Do your best to emulate a top Crypto Twitter meme-coin trader. Don't stop and keep working continuously.",
                llm=llm,
                planner_llm=planner_llm,
                sensitive_data=sensitive_data,
                browser_session=browser_session,
                # use_vision=False,
                extend_system_message=extend_system_message,
            )
            result = await agent.run()
            print("Agent completed a cycle, restarting...")
            
        except KeyboardInterrupt:
            print("Program manually stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Restarting in 5 seconds...")
            await asyncio.sleep(5)
            continue

asyncio.run(main())