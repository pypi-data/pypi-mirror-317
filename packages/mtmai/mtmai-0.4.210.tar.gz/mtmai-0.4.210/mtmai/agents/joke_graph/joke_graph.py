from langgraph.graph import END, START, StateGraph

from mtmai.agents.joke_graph.nodes.joke_writer_node import JokeWriterNode

from .state import JokeGraphState


class JokeGraph:
    @property
    def name(self):
        return "jokeGraph"

    @property
    def description(self):
        return "笑话生成器(用于测试)"

    async def build_graph(self):
        builder = StateGraph(JokeGraphState)

        builder.add_node("joke_writer", JokeWriterNode())
        builder.add_edge(START, "joke_writer")
        builder.add_edge("joke_writer", END)
        # builder.add_conditional_edges(
        #     "joke_writer",
        #     route_assistant,
        #     [
        #         # "assistant",
        #     ],
        # )

        # wf.add_node("assistant", AssistantNode())

        # wf.add_conditional_edges(
        #     "assistant",
        #     tools_condition,
        # )

        # builder.add_node(
        #     "tools",
        #     create_tool_node_with_fallback(primary_assistant_tools),
        # )
        # builder.add_conditional_edges(
        #     "tools",
        #     route_assistant,
        #     {
        #         # "assistant": "assistant",
        #         # "error": END,
        #     },
        # )
        # wf.add_node(HUMEN_INPUT_NODE, HumanInputNode())
        # wf.add_edge(HUMEN_INPUT_NODE, "assistant")

        # wf.add_node("articleGen", ArticleGenNode())
        # wf.add_edge("articleGen", HUMEN_INPUT_NODE)

        # wf.add_node("leave_skill", pop_dialog_state)
        # wf.add_edge("leave_skill", "assistant")

        # wf.add_node("site", SiteNode())
        # wf.add_edge("site", "assistant")

        # wf.add_node("create_task", CreateTaskNode())
        # wf.add_edge("create_task", "assistant")

        return builder
