import os
import openai
from config import OPENAI_API_KEY
from utils.chunkstore import ChunkStore
from utils.chat_memory import ChatMemory
from data.sample_data import get_sample_data

openai.api_key = OPENAI_API_KEY


def ask_nural(question: str, store: ChunkStore, memory: ChatMemory) -> str:
    # Get relevant context from the knowledge base
    top_chunks = store.query(question, top_k=5)
    context = "\n".join(f"- {c['text']}" for c in top_chunks)
    
    # Get conversation history
    history = memory.get_history()
    
    # Create the prompt with context
    prompt = f"""Context from knowledge base:
{context}

User Question: {question}"""

    history.append({"role": "user", "content": prompt})

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        temperature=0.7
    )
    answer = response.choices[0].message.content.strip()
    
    # Add this interaction to memory
    memory.add_interaction(context, question, answer)
    
    return answer


def chat_mode(store: ChunkStore):
    print("\n💬 Nural is online. Ask about employees. Type 'q' to quit, 'clear' to reset conversation.\n")
    memory = ChatMemory()

    while True:
        user_input = input("🧠 Ask a question: ").strip()
        if user_input.lower() == 'q':
            print("👋 Goodbye!")
            break
        elif user_input.lower() == 'clear':
            memory.clear()
            print("🧹 Conversation history cleared.")
            continue

        reply = ask_nural(user_input, store, memory)
        print(f"\n🔍 Answer:\n{reply}\n")


def build_chunk_store(cache_file="data/chunks.json") -> ChunkStore:
    # Ensure data directory exists
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    
    store = ChunkStore()

    # Load from disk if available
    if os.path.exists(cache_file):
        store.load(cache_file)
        return store

    # Otherwise, build from scratch
    profiles = get_sample_data()

    for p in profiles:
        store.bulk_add(p.to_chunks())
        for post in p.posts:
            store.add_chunk(post.to_chunk())
        for contrib in p.contributions:
            store.bulk_add(contrib.project.to_chunks())

    store.save(cache_file)
    print(f"✅ Embedded and saved {store.count()} chunks to {cache_file}")
    return store


def main():
    store = build_chunk_store()

    while True:
        print("\n📋 Menu:")
        print("1. Chat with Nural")
        print("2. Reload and regenerate chunks")
        print("3. Quit")

        choice = input("\nSelect an option (1-3): ").strip()

        if choice == "1":
            chat_mode(store)
        elif choice == "2":
            store = build_chunk_store()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")


if __name__ == "__main__":
    main()
