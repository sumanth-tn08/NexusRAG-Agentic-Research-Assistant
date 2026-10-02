from app.rag.rag_chain import get_rag_chain


def main():

    rag_chain = get_rag_chain()

    print("\n================================")
    print("       NexusRAG Assistant")
    print("================================")
    print("Ask questions about your documents.")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        answer, documents = rag_chain(question)

        print("\nNexusRAG:", answer)

        print("\nSources:")

        for i, document in enumerate(documents, start=1):

            page = document.metadata.get(
                "page",
                "unknown"
            )

            print(f"  [{i}] Page {page + 1}")

        print()


if __name__ == "__main__":
    main()