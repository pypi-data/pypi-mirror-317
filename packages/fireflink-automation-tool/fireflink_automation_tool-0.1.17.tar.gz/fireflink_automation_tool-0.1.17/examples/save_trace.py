import os
import sys

from langchain_openai import ChatOpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

from fireflink_automation_tool.agent.service import Agent
from fireflink_automation_tool.browser.browser import Browser
from fireflink_automation_tool.browser.context import BrowserContextConfig

llm = ChatOpenAI(model='gpt-4o', temperature=0.0)


async def main():
	browser = Browser()

	async with await browser.new_context(
		config=BrowserContextConfig(trace_path='./tmp/traces/')
	) as context:
		agent = Agent(
			task='Go to hackernews, then go to apple.com and return all titles of open tabs',
			llm=llm,
			browser_context=context,
		)
		await agent.run()

	await browser.close()


asyncio.run(main())
