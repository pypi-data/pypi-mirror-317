import os
import sys
from pathlib import Path

from fireflink_automation_tool.agent.views import ActionResult

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from langchain_openai import ChatOpenAI

from fireflink_automation_tool import Agent, Controller
from fireflink_automation_tool.browser.browser import Browser, BrowserConfig
from fireflink_automation_tool.browser.context import BrowserContext

browser = Browser(
	config=BrowserConfig(
		headless=False,
		# NOTE: you need to close your chrome browser - so that this can open your browser in debug mode
		chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	)
)
controller = Controller()


async def main():
	task = f'In docs.google.com write my Papa a quick thank you for everything letter \n - Magnus'
	task += f' and save the document as pdf'
	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(
		task=task,
		llm=model,
		controller=controller,
		browser=browser,
	)

	await agent.run()
	await browser.close()

	input('Press Enter to close...')


if __name__ == '__main__':
	asyncio.run(main())
