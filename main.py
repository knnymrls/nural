import openai
from config import OPENAI_API_KEY
from data.sample_data import get_sample_employees
from utils.formatter import profile_to_string
from utils.embedding import rank_profiles, get_embedding
from utils.embedding_cache import get_or_create_embeddings, save_embeddings

openai.api_key = OPENAI_API_KEY

def chat_mode(profile_texts, profile_embeddings):
    """Run the persistent-memory chat interface for employee Q&A."""
    chat_history = [
        {
            "role": "system",
            "content": (
                "You are Nexus, an intelligent internal knowledge assistant that understands employee skills, experience, and project history. "
                "You can answer any type of question about employees by analyzing their profiles, including:\n"
                "- Location-based queries (e.g., 'who works in SF?', 'employees near Tokyo')\n"
                "- Team/role queries (e.g., 'who are the engineers?', 'show me the marketing team')\n"
                "- Skill-based queries (e.g., 'who knows Python?', 'people with cloud experience')\n"
                "- Project-based queries (e.g., 'recent projects', 'AI initiatives')\n"
                "- Language queries (e.g., 'who speaks Spanish?', 'multilingual employees')\n"
                "- Experience queries (e.g., 'senior engineers', 'people with startup experience')\n"
                "- Impact queries (e.g., 'projects with highest impact', 'revenue growth initiatives')\n"
                "Analyze the entire dataset to find relevant information and provide comprehensive answers. If you don't know something or don't get what the user is asking ask for a follow up question until you understand the question. And end with a short follow up question."
                "Be direct, human, and include specific details from the profiles when relevant."
            )
        }
    ]

    print("\n💬 Nexus is online. Ask about employees. Type 'q' to quit.\n")

    while True:
        user_input = input("🧠 Ask a question: ").strip()
        if user_input.lower() == 'q':
            print("👋 Goodbye!")
            break

        # Retrieve top 3 profile texts
        top_indices = rank_profiles(user_input, profile_texts, profile_embeddings)
        top_profiles = [profile_texts[i] for i in top_indices[:5]]

        # Append user query with relevant profiles to memory
        chat_history.append({
            "role": "user",
            "content": f"{user_input}\n\nRelevant employee profiles:\n\n" + "\n\n".join(top_profiles)
        })

        # Ask OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_history,
            temperature=0.7  # Add some creativity in how it analyzes and presents the data
        )

        reply = response.choices[0].message.content.strip()
        print(f"\n🔍 Answer:\n{reply}\n")
        chat_history.append({"role": "assistant", "content": reply})

def regenerate_embeddings(profile_texts):
    """Force regeneration of embeddings."""
    print("🔄 Regenerating embeddings...")
    embeddings = [get_embedding(text) for text in profile_texts]
    save_embeddings(profile_texts, embeddings)
    return profile_texts, embeddings

def main():
    employees = get_sample_employees()
    profile_texts = [profile_to_string(p) for p in employees]

    # Get initial embeddings from cache or create new ones if needed
    profile_texts, profile_embeddings = get_or_create_embeddings(profile_texts)

    while True:
        print("\n📋 Menu:")
        print("1. Chat about employees")
        print("2. Regenerate embeddings")
        print("3. Quit")

        choice = input("\nSelect an option (1-3): ").strip()

        if choice == "1":
            chat_mode(profile_texts, profile_embeddings)
        elif choice == "2":
            profile_texts, profile_embeddings = regenerate_embeddings(profile_texts)
            print("✅ Embeddings regenerated successfully!")
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
