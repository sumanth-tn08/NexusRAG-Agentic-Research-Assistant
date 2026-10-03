from app.agent.llm import get_agent_llm


def main():

    llm = get_agent_llm()

    response = llm.invoke(
        "Use calculator tool to Calculate 12 X 1"
    )

    print("Response:")
    print(response)

    print("\nTool calls:")

    print(
        response.tool_calls
    )


if __name__ == "__main__":
    main()