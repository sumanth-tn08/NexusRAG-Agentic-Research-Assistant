from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split(file_path: str):
    
    loader = PyMuPDFLoader(file_path)
    
    documents = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
   
    chunks = splitter.split_documents(documents)
   
    return chunks

if __name__ == "__main__":

    chunks = load_and_split(
        "data/documents/OOPS Notes.pdf"
    )

    print("Number of chunks:", len(chunks))

    print("\nFirst chunk:")
    print(chunks[0].page_content)

    print("\nMetadata:")
    print(chunks[0].metadata)