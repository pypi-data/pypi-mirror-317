from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI

from mtmai.crews.types import BookOutline


@CrewBase
class OutlineCrew:
    """Book Outline Crew"""

    # agents_config = "config/agents.yaml"
    # tasks_config = "config/tasks.yaml"
    # llm = ChatOpenAI(model="chatgpt-4o-latest")
    llm = ChatOpenAI(model="gpt-4o")

    @agent
    def researcher(self) -> Agent:
        search_tool = SerperDevTool()
        return Agent(
            role="Research Agent",
            goal="""Gather comprehensive information about {topic} that will be used to create an organized and well-structured book outline.
    Here is some additional information about the author's desired goal for the book:\n\n {goal}""",
            backstory="""You're a seasoned researcher, known for gathering the best sources and understanding the key elements of any topic.
    You aim to collect all relevant information so the book outline can be accurate and informative."""
            # config=self.agents_config["researcher"],
            tools=[search_tool],
            llm=self.llm,
            verbose=True,
        )

    @agent
    def outliner(self) -> Agent:
        return Agent(
            role="Book Outlining Agent",
            goal="""Based on the research, generate a book outline about the following topic: {topic}
    The generated outline should include all chapters in sequential order and provide a title and description for each chapter.
    Here is some additional information about the author's desired goal for the book:\n\n {goal}""",
            backstory="""You are a skilled organizer, great at turning scattered information into a structured format.
    Your goal is to create clear, concise chapter outlines with all key topics and subtopics covered.""",
            # config=self.agents_config["outliner"],
            llm=self.llm,
            verbose=True,
        )

    @task
    def research_topic(self) -> Task:
        return Task(
            description="""Research the provided topic of {topic} to gather the most important information that will
    be useful in creating a book outline. Ensure you focus on high-quality, reliable sources.

    Here is some additional information about the author's desired goal for the book:\n\n {goal}""",
            expected_output="A set of key points and important information about {topic} that will be used to create the outline.",
            agent=cls.researcher,
        )

    @task
    def generate_outline(self) -> Task:
        return Task(
            config=self.tasks_config["generate_outline"], output_pydantic=BookOutline
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Book Outline Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
