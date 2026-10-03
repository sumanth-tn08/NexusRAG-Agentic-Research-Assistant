from langchain_core.messages import HumanMessage

from app.agent.graph import graph


def main():

    print("\n================================")
    print("       NexusRAG Agent")
    print("================================")
    print("Ask questions or perform calculations.")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=question
                    )
                ]
            }
        )

        final_message = result["messages"][-1]

        print("\nNexusRAG:")
        print(final_message.content)
        print()


if __name__ == "__main__":
    main()