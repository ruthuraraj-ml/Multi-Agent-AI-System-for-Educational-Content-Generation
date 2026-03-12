from crewai import Crew, Task, Process
from agents import research_agent, image_agent, reviewer_agent, manager_agent


main_task = Task(
    description="""
You are the manager. Follow this protocol STRICTLY. Do not deviate.

The topic is: {topic}

MANDATORY EXECUTION ORDER:

[PHASE 1] → Delegate to Research Agent
- Tool to use: rag_search
- Query: facts about {topic}
- Wait for full output before proceeding

[PHASE 2] → Delegate to Image Agent
- Tool to use: image_generator
- Input: the Research Agent output from Phase 1
- Wait for confirmation that diagram is saved

[PHASE 3] → Delegate to Reviewer Agent
- Input: the Research Agent output from Phase 1
- This is the FINAL step

RULES:
- Reviewer Agent must NEVER run before Research Agent
- Image Agent must NEVER run before Research Agent
- Do not modify the Reviewer Agent output
- Once Reviewer Agent returns output, STOP immediately. Do not verify or follow up.
""",
    expected_output="The exact Reviewer Agent output followed by the diagram filename on a new line. Nothing else.",
)


crew = Crew(
    agents=[research_agent, image_agent, reviewer_agent],
    tasks=[main_task],
    manager_agent=manager_agent,
    process=Process.hierarchical,
    memory=False,
    verbose=True
)