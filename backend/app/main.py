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
            print("\nGoodbye!")
            break

        try:

            answer, documents = rag_chain(question)

            print("\nNexusRAG:")
            print(answer)

            print("\nSources:")

            seen_sources = set()

            for document in documents:

                source = document.metadata.get(
                    "source",
                    "Unknown"
                )

                page = document.metadata.get(
                    "page",
                    None
                )

                source_name = source.split("\\")[-1]
                source_name = source_name.split("/")[-1]

                source_key = (
                    source_name,
                    page
                )

                if source_key in seen_sources:
                    continue

                seen_sources.add(source_key)

                if page is not None:
                    print(
                        f"  - {source_name}, "
                        f"Page {page + 1}"
                    )
                else:
                    print(
                        f"  - {source_name}"
                    )

            print()

        except Exception as e:

            print("\nError:", e)
            print()


if __name__ == "__main__":
    main()