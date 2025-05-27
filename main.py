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
    
    # # Debug: Print retrieved chunks with more detail
    # print("\n🔍 Retrieved chunks:")
    # for chunk in top_chunks:
    #     print(f"- Type: {chunk['object_type']}, Chunk: {chunk['chunk_type']}")
    #     print(f"  Text: {chunk['text']}")
    #     if 'metadata' in chunk:
    #         print(f"  Metadata: {chunk['metadata']}")
    
    # Group chunks by type for better context organization
    project_chunks = []
    profile_chunks = []
    other_chunks = []
    
    for chunk in top_chunks:
        if chunk["object_type"] == "project":
            project_chunks.append(chunk)
        elif chunk["object_type"] == "profile":
            profile_chunks.append(chunk)
        else:
            other_chunks.append(chunk)
    
    # Build structured context
    context_parts = []
    
    if project_chunks:
        context_parts.append("Project Information:")
        for chunk in project_chunks:
            context_parts.append(f"- {chunk['text']}")
    
    if profile_chunks:
        context_parts.append("\nProfile Information:")
        for chunk in profile_chunks:
            context_parts.append(f"- {chunk['text']}")
    
    if other_chunks:
        context_parts.append("\nOther Information:")
        for chunk in other_chunks:
            context_parts.append(f"- {chunk['text']}")
    
    context = "\n".join(context_parts)
    
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


def regenerate_chunks(store: ChunkStore, cache_file: str = "data/chunks.json") -> ChunkStore:
    """Regenerate and save chunks from sample data."""
    print("🔄 Regenerating chunks from sample data...")
    
    # Remove existing cache file to force regeneration
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print("🗑️ Removed existing cache file")
    
    # Create new store
    store = ChunkStore()
    
    # Get fresh sample data
    profiles = get_sample_data()
    
    # Debug: Print chunk creation
    print("\n📦 Creating chunks:")
    
    # First, create project chunks to ensure they exist
    projects = {}
    for profile in profiles:
        for contrib in profile.contributions:
            if contrib.project.title not in projects:
                projects[contrib.project.title] = contrib.project
                print(f"\nCreating chunks for project: {contrib.project.title}")
                project_chunks = contrib.project.to_chunks()
                for chunk in project_chunks:
                    print(f"- Type: {chunk['object_type']}, Chunk: {chunk['chunk_type']}")
                    print(f"  Text: {chunk['text']}")
                store.bulk_add(project_chunks)
    
    # Then add profile and post chunks
    for profile in profiles:
        print(f"\nCreating chunks for profile: {profile.name}")
        profile_chunks = profile.to_chunks()
        for chunk in profile_chunks:
            print(f"- Type: {chunk['object_type']}, Chunk: {chunk['chunk_type']}")
            print(f"  Text: {chunk['text']}")
        store.bulk_add(profile_chunks)
        
        for post in profile.posts:
            post_chunk = post.to_chunk()
            print(f"\nPost by {post.author.name}")
            print(f"- Type: {post_chunk['object_type']}, Chunk: {post_chunk['chunk_type']}")
            print(f"  Text: {post_chunk['text']}")
            store.add_chunk(post_chunk)
    
    # Save to file
    store.save(cache_file)
    print(f"\n✅ Successfully regenerated {store.count()} chunks")
    
    # Debug: Verify current team chunks
    print("\n🔍 Verifying current team chunks:")
    for chunk in store.chunks:
        if chunk["chunk_type"] == "current_team":
            print(f"- Project: {chunk['metadata']['project']}")
            print(f"  Text: {chunk['text']}")
    
    return store


def build_chunk_store(cache_file="data/chunks.json", force_regenerate=False) -> ChunkStore:
    # Ensure data directory exists
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    
    # If force_regenerate is True or cache doesn't exist, regenerate
    if force_regenerate or not os.path.exists(cache_file):
        return regenerate_chunks(ChunkStore(), cache_file)
    
    # Otherwise load from cache
    store = ChunkStore()
    store.load(cache_file)
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
            store = build_chunk_store(force_regenerate=True)
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")


if __name__ == "__main__":
    main()
