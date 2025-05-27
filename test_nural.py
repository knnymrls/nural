from models import Profile, Project, Contribution, Post


# 👥 Create profiles
kenny = Profile(name="Kenny Morales", title="Founder", location="Nebraska")
zak = Profile(name="Zak Rab", title="Engineer", location="California")

# 📁 Create a project
signals = Project(
    title="Nural Signals",
    description="A real-time visibility layer to monitor team activity.",
    created_by=kenny,
    status="active"
)

# 🧠 Add contributions (resume-style)
Contribution(
    person=kenny,
    project=signals,
    role="Product Lead",
    start="2023-09",
    end="2024-01",
    description="Led feature planning and rollout strategy for enterprise use."
)

Contribution(
    person=zak,
    project=signals,
    role="ML Engineer",
    start="2023-10",
    end="2024-02",
    description="Built chunked RAG search engine and indexing pipeline."
)

# 📝 Make a post that tags a person and a project
post = Post(
    author=kenny,
    content="Massive progress! Shoutout to @ZakRab for finalizing the search logic in @NuralSignals. The system is live 🎉",
    all_projects=[signals],
    all_profiles=[kenny, zak]
)

# 🔎 Outputs to see everything is linked correctly

print("\n👤 Zak's Contributions:")
for c in zak.contributions:
    print("-", c)

print("\n📁 Project Contributions:")
for c in signals.contributions:
    print("-", c)

print("\n📥 Zak was mentioned in:")
for p in zak.mentioned_in:
    print("-", p)

print("\n📄 Kenny's Posts:")
for p in kenny.posts:
    print("-", p)

print("\n🔗 Projects linked to the post:")
for p in post.linked_projects:
    print("-", p.title)

print("\n👥 People mentioned in the post:")
for p in post.mentioned_people:
    print("-", p.name)
