from models import Profile, Project, Post, Contribution
from datetime import datetime


def get_sample_data():
    # --- Create profiles ---
    kenny = Profile(
        name="Kenny Morales",
        title="Product Manager",
        location="Lincoln, Nebraska",
        bio="Kenny is a builder and visionary. He focuses on early-stage product strategy and team velocity.",
        skills=["Product Strategy", "User Research", "Leadership", "AI Product Development"],
        experiences=[
            {
                "company": "Nural",
                "role": "Founder",
                "start": "2023-01",
                "end": "2024-05",
                "description": "Launched Nural from idea to working prototype with AI-assisted querying."
            },
            {
                "company": "Nural",
                "role": "Product Lead",
                "start": "2024-01",
                "end": "present",
                "description": "Leading product strategy for AI-powered chatbot platform."
            }
        ],
        education=[
            {
                "school": "University of Nebraska",
                "degree": "BS Computer Science",
                "year": "2020"
            }
        ]
    )

    zak = Profile(
        name="Zak Rab",
        title="Machine Learning Engineer",
        location="Lincoln, Nebraska",
        bio="Zak loves working on LLMs, search infrastructure, and backend systems. Expert in building scalable AI solutions.",
        skills=["Python", "LLMs", "Vector Search", "RAG", "FastAPI", "MLOps", "Docker", "Chatbot Development"],
        experiences=[
            {
                "company": "Nural",
                "role": "ML Engineer",
                "start": "2023-02",
                "end": "2024-05",
                "description": "Built chunking pipeline and retrieval system using OpenAI embeddings."
            },
            {
                "company": "Nural",
                "role": "Senior ML Engineer",
                "start": "2024-01",
                "end": "present",
                "description": "Leading ML infrastructure for conversational AI and chatbot systems."
            }
        ],
        education=[
            {
                "school": "Stanford University",
                "degree": "MS Computer Science",
                "year": "2022"
            }
        ]
    )

    # New profiles
    sophia = Profile(
        name="Sophia Chen",
        title="Senior UX Designer",
        location="San Francisco, California",
        bio="Passionate about creating intuitive and beautiful user experiences. Specializes in AI product design and user research.",
        skills=["UI/UX Design", "Figma", "User Research", "Design Systems", "AI/ML Product Design"],
        experiences=[
            {
                "company": "Nural",
                "role": "Senior UX Designer",
                "start": "2023-06",
                "end": "present",
                "description": "Leading design for NuralChat and Signals platforms, focusing on AI-human interaction patterns."
            },
            {
                "company": "Google",
                "role": "UX Designer",
                "start": "2020-06",
                "end": "2023-05",
                "description": "Designed user experiences for Google Cloud AI products."
            }
        ],
        education=[
            {
                "school": "Rhode Island School of Design",
                "degree": "BFA Interaction Design",
                "year": "2020"
            }
        ]
    )

    marcus = Profile(
        name="Marcus Johnson",
        title="Growth Marketing Manager",
        location="Austin, Texas",
        bio="Data-driven marketer with a passion for scaling early-stage startups. Expert in growth hacking and content strategy.",
        skills=["Growth Marketing", "Content Strategy", "SEO", "Social Media", "Analytics", "A/B Testing"],
        experiences=[
            {
                "company": "Nural",
                "role": "Growth Marketing Manager",
                "start": "2023-09",
                "end": "present",
                "description": "Leading marketing strategy and growth initiatives for Nural's products."
            },
            {
                "company": "HubSpot",
                "role": "Marketing Specialist",
                "start": "2021-03",
                "end": "2023-08",
                "description": "Managed content marketing and social media campaigns."
            }
        ],
        education=[
            {
                "school": "University of Texas",
                "degree": "BS Marketing",
                "year": "2021"
            }
        ]
    )

    aisha = Profile(
        name="Aisha Patel",
        title="Product Design Intern",
        location="Remote",
        bio="Aspiring product designer with a focus on AI and user experience. Currently learning the ropes of startup design.",
        skills=["UI Design", "Figma", "User Research", "Prototyping", "Design Thinking"],
        experiences=[
            {
                "company": "Nural",
                "role": "Product Design Intern",
                "start": "2024-01",
                "end": "present",
                "description": "Assisting with user research and design iterations for NuralChat."
            }
        ],
        education=[
            {
                "school": "University of Michigan",
                "degree": "BS Interaction Design",
                "year": "Expected 2025"
            }
        ]
    )

    # Additional profiles
    rachel = Profile(
        name="Rachel Kim",
        title="Data Scientist",
        location="Seattle, Washington",
        bio="Data scientist passionate about using AI to understand user behavior and improve product experiences. Expert in NLP and behavioral analytics.",
        skills=["Python", "Data Analysis", "NLP", "Machine Learning", "A/B Testing", "SQL", "TensorFlow"],
        experiences=[
            {
                "company": "Nural",
                "role": "Senior Data Scientist",
                "start": "2023-08",
                "end": "present",
                "description": "Leading analytics and ML initiatives to improve NuralChat's understanding of user interactions."
            },
            {
                "company": "Amazon",
                "role": "Data Scientist",
                "start": "2021-01",
                "end": "2023-07",
                "description": "Developed ML models for customer behavior prediction and recommendation systems."
            }
        ],
        education=[
            {
                "school": "University of Washington",
                "degree": "MS Data Science",
                "year": "2021"
            }
        ]
    )

    james = Profile(
        name="James Wilson",
        title="Frontend Engineer",
        location="Remote",
        bio="Frontend specialist focused on building beautiful, performant web applications. Passionate about React and modern web technologies.",
        skills=["React", "TypeScript", "Next.js", "Tailwind CSS", "Web Performance", "UI Development"],
        experiences=[
            {
                "company": "Nural",
                "role": "Senior Frontend Engineer",
                "start": "2023-10",
                "end": "present",
                "description": "Leading frontend development for NuralChat's web interface and component library."
            },
            {
                "company": "Stripe",
                "role": "Frontend Engineer",
                "start": "2020-06",
                "end": "2023-09",
                "description": "Built and maintained Stripe's dashboard interface and payment components."
            }
        ],
        education=[
            {
                "school": "Georgia Tech",
                "degree": "BS Computer Science",
                "year": "2020"
            }
        ]
    )

    maria = Profile(
        name="Maria Rodriguez",
        title="Customer Success Manager",
        location="Miami, Florida",
        bio="Customer success expert with a focus on AI products. Dedicated to helping teams maximize the value of Nural's solutions.",
        skills=["Customer Success", "Product Training", "Account Management", "Customer Onboarding", "Technical Support"],
        experiences=[
            {
                "company": "Nural",
                "role": "Customer Success Manager",
                "start": "2023-11",
                "end": "present",
                "description": "Managing enterprise customer relationships and driving adoption of NuralChat."
            },
            {
                "company": "Salesforce",
                "role": "Customer Success Specialist",
                "start": "2021-03",
                "end": "2023-10",
                "description": "Led customer onboarding and success programs for enterprise clients."
            }
        ],
        education=[
            {
                "school": "University of Miami",
                "degree": "BS Business Administration",
                "year": "2021"
            }
        ]
    )

    # Additional profiles
    david = Profile(
        name="David Park",
        title="Backend Engineer",
        location="New York, New York",
        bio="Backend specialist focused on scalable systems and API design. Expert in distributed systems and cloud architecture.",
        skills=["Go", "Python", "Kubernetes", "AWS", "Microservices", "API Design", "System Architecture"],
        experiences=[
            {
                "company": "Nural",
                "role": "Senior Backend Engineer",
                "start": "2023-12",
                "end": "present",
                "description": "Leading backend architecture and scaling initiatives for Nural's platforms."
            },
            {
                "company": "Twitter",
                "role": "Backend Engineer",
                "start": "2020-08",
                "end": "2023-11",
                "description": "Worked on Twitter's API infrastructure and real-time messaging systems."
            }
        ],
        education=[
            {
                "school": "Columbia University",
                "degree": "MS Computer Science",
                "year": "2020"
            }
        ]
    )

    priya = Profile(
        name="Priya Sharma",
        title="Product Marketing Manager",
        location="Boston, Massachusetts",
        bio="Product marketing expert with a focus on AI products. Passionate about storytelling and market positioning.",
        skills=["Product Marketing", "Go-to-Market Strategy", "Content Strategy", "Market Research", "Product Positioning"],
        experiences=[
            {
                "company": "Nural",
                "role": "Product Marketing Manager",
                "start": "2024-01",
                "end": "present",
                "description": "Leading product marketing strategy and go-to-market initiatives."
            },
            {
                "company": "Microsoft",
                "role": "Product Marketing Specialist",
                "start": "2021-06",
                "end": "2023-12",
                "description": "Led marketing for Microsoft's AI and cloud products."
            }
        ],
        education=[
            {
                "school": "MIT",
                "degree": "MBA",
                "year": "2021"
            }
        ]
    )

    emma = Profile(
        name="Emma Thompson",
        title="UX Researcher",
        location="Portland, Oregon",
        bio="UX researcher focused on understanding how teams interact with AI tools. Expert in qualitative research and user behavior analysis.",
        skills=["User Research", "Qualitative Analysis", "Usability Testing", "Behavioral Psychology", "Research Methods"],
        experiences=[
            {
                "company": "Nural",
                "role": "Senior UX Researcher",
                "start": "2023-11",
                "end": "present",
                "description": "Leading user research initiatives to improve AI-human interaction in Nural's products."
            },
            {
                "company": "Adobe",
                "role": "UX Researcher",
                "start": "2021-01",
                "end": "2023-10",
                "description": "Conducted research for Adobe's creative cloud products."
            }
        ],
        education=[
            {
                "school": "University of Oregon",
                "degree": "PhD Human-Computer Interaction",
                "year": "2021"
            }
        ]
    )

    # --- Create projects ---
    signals = Project(
        title="Nural Signals",
        description="Nural Signals provides real-time visibility into what your teammates are working on.",
        created_by=kenny,
        status="active"
    )

    nuralchat = Project(
        title="NuralChat",
        description="AI-powered chatbot platform that helps teams communicate and collaborate more effectively using natural language.",
        created_by=kenny,
        status="active"
    )

    brand = Project(
        title="Nural Brand Refresh",
        description="Revitalizing Nural's brand identity and visual language to better reflect our AI-first approach.",
        created_by=sophia,
        status="active"
    )

    analytics = Project(
        title="Nural Analytics",
        description="Advanced analytics platform for understanding team communication patterns and improving collaboration through AI insights.",
        created_by=rachel,
        status="active"
    )

    platform = Project(
        title="Nural Platform",
        description="Core platform infrastructure for scaling Nural's services and enabling enterprise-grade reliability.",
        created_by=david,
        status="active"
    )

    # --- Create contributions ---
    # Existing contributions
    Contribution(
        person=kenny,
        project=signals,
        role="Product Lead",
        start="2023-01",
        end="2023-04",
        description="Designed the MVP and helped recruit internal testers."
    )

    Contribution(
        person=zak,
        project=signals,
        role="ML Engineer",
        start="2023-02",
        end="2023-04",
        description="Built and deployed the search engine using RAG and OpenAI APIs."
    )

    Contribution(
        person=kenny,
        project=nuralchat,
        role="Product Lead",
        start="2024-01",
        end="present",
        description="Leading product strategy and user experience for the chatbot platform."
    )

    Contribution(
        person=zak,
        project=nuralchat,
        role="Senior ML Engineer",
        start="2024-01",
        end="present",
        description="Building and scaling the conversational AI infrastructure and fine-tuning LLMs for better chat interactions."
    )

    # New contributions
    Contribution(
        person=sophia,
        project=nuralchat,
        role="Lead Designer",
        start="2023-06",
        end="present",
        description="Designing the user interface and interaction patterns for NuralChat."
    )

    Contribution(
        person=sophia,
        project=brand,
        role="Design Lead",
        start="2024-01",
        end="present",
        description="Leading the complete brand refresh initiative."
    )

    Contribution(
        person=marcus,
        project=nuralchat,
        role="Growth Lead",
        start="2023-09",
        end="present",
        description="Developing and executing growth strategies for NuralChat."
    )

    Contribution(
        person=aisha,
        project=nuralchat,
        role="Design Intern",
        start="2024-01",
        end="present",
        description="Supporting the design team with user research and interface iterations."
    )

    # Additional contributions
    Contribution(
        person=rachel,
        project=nuralchat,
        role="Data Science Lead",
        start="2023-08",
        end="present",
        description="Developing ML models to improve chat understanding and user experience."
    )

    Contribution(
        person=rachel,
        project=analytics,
        role="Project Lead",
        start="2024-01",
        end="present",
        description="Building analytics platform to provide insights into team communication patterns."
    )

    Contribution(
        person=james,
        project=nuralchat,
        role="Frontend Lead",
        start="2023-10",
        end="present",
        description="Leading the development of NuralChat's web interface and component system."
    )

    Contribution(
        person=james,
        project=brand,
        role="Frontend Engineer",
        start="2024-01",
        end="present",
        description="Implementing the new brand design system across web applications."
    )

    Contribution(
        person=maria,
        project=nuralchat,
        role="Customer Success Lead",
        start="2023-11",
        end="present",
        description="Managing enterprise customer relationships and driving product adoption."
    )

    Contribution(
        person=maria,
        project=signals,
        role="Customer Success Manager",
        start="2023-11",
        end="present",
        description="Helping teams implement and optimize their use of Nural Signals."
    )

    # Additional contributions
    Contribution(
        person=david,
        project=platform,
        role="Technical Lead",
        start="2023-12",
        end="present",
        description="Leading the development of Nural's core platform infrastructure."
    )

    Contribution(
        person=david,
        project=nuralchat,
        role="Backend Lead",
        start="2023-12",
        end="present",
        description="Architecting and scaling the backend systems for NuralChat."
    )

    Contribution(
        person=priya,
        project=nuralchat,
        role="Product Marketing Lead",
        start="2024-01",
        end="present",
        description="Developing go-to-market strategy and product positioning for NuralChat."
    )

    Contribution(
        person=priya,
        project=brand,
        role="Marketing Lead",
        start="2024-01",
        end="present",
        description="Leading marketing strategy for the brand refresh initiative."
    )

    Contribution(
        person=emma,
        project=nuralchat,
        role="Research Lead",
        start="2023-11",
        end="present",
        description="Leading user research to improve AI-human interaction in NuralChat."
    )

    Contribution(
        person=emma,
        project=signals,
        role="UX Researcher",
        start="2023-11",
        end="present",
        description="Conducting research to optimize team visibility features."
    )

    # --- Create posts ---
    # Existing posts
    Post(
        author=kenny,
        content="Wrapped up first user test for @Nural Signals today. Huge props to @Zak Rab for handling the search logic 🙌",
        all_projects=[signals],
        all_profiles=[kenny, zak],
        created_at=datetime(2024, 1, 15)
    )

    Post(
        author=zak,
        content="Embedded 100+ chunks using OpenAI. Search on @Nural Signals now returns real results. Let's go!",
        all_projects=[signals],
        all_profiles=[kenny, zak],
        created_at=datetime(2024, 1, 20)
    )

    # New posts
    Post(
        author=sophia,
        content="Just wrapped up user testing for the new @NuralChat interface. The feedback on the AI interaction patterns has been incredible! @Aisha Patel did an amazing job helping with the research.",
        all_projects=[nuralchat],
        all_profiles=[sophia, aisha],
        created_at=datetime(2024, 2, 5)
    )

    Post(
        author=marcus,
        content="Our latest growth experiment for @NuralChat shows 40% higher engagement with the new onboarding flow. The AI-powered tutorials are really resonating with users!",
        all_projects=[nuralchat],
        all_profiles=[marcus],
        created_at=datetime(2024, 2, 10)
    )

    Post(
        author=aisha,
        content="First week at @Nural complete! Learning so much about AI product design from @Sophia Chen. The user research insights are fascinating!",
        all_projects=[nuralchat],
        all_profiles=[aisha, sophia],
        created_at=datetime(2024, 1, 8)
    )

    Post(
        author=sophia,
        content="Excited to kick off the @Nural Brand Refresh project! We're reimagining our visual identity to better reflect our AI-first approach. Stay tuned for updates!",
        all_projects=[brand],
        all_profiles=[sophia],
        created_at=datetime(2024, 2, 20)
    )

    # Additional posts
    Post(
        author=rachel,
        content="Excited to share that our new sentiment analysis model for @NuralChat is showing 92% accuracy in understanding user intent! This will help make conversations more natural and effective.",
        all_projects=[nuralchat],
        all_profiles=[rachel],
        created_at=datetime(2024, 2, 25)
    )

    Post(
        author=james,
        content="Just shipped a major performance update to @NuralChat's web interface. Page load times are down 60% and the new component library is making development much faster!",
        all_projects=[nuralchat],
        all_profiles=[james],
        created_at=datetime(2024, 2, 28)
    )

    Post(
        author=maria,
        content="Thrilled to announce that @NuralChat has been adopted by 5 new enterprise teams this month! The onboarding process we developed with @Sophia Chen is really resonating with customers.",
        all_projects=[nuralchat],
        all_profiles=[maria, sophia],
        created_at=datetime(2024, 3, 1)
    )

    Post(
        author=rachel,
        content="Kicking off the @Nural Analytics project today! We're building a powerful platform to help teams understand their communication patterns and improve collaboration. Looking forward to working with @Zak Rab on the ML infrastructure!",
        all_projects=[analytics],
        all_profiles=[rachel, zak],
        created_at=datetime(2024, 3, 5)
    )

    Post(
        author=james,
        content="Working with @Sophia Chen on implementing the new brand system across our web apps. The new design language is looking amazing!",
        all_projects=[brand],
        all_profiles=[james, sophia],
        created_at=datetime(2024, 3, 8)
    )

    Post(
        author=maria,
        content="Hosted our first customer workshop for @Nural Signals today. Great feedback from the team at Acme Corp on how they're using it to improve cross-team visibility!",
        all_projects=[signals],
        all_profiles=[maria],
        created_at=datetime(2024, 3, 10)
    )

    # Additional posts
    Post(
        author=david,
        content="Just completed the migration of @NuralChat's backend to our new microservices architecture. The system is now handling 10x the load with better reliability!",
        all_projects=[nuralchat, platform],
        all_profiles=[david],
        created_at=datetime(2024, 3, 12)
    )

    Post(
        author=priya,
        content="Excited to share our new positioning for @NuralChat: 'The AI-powered communication platform that makes teams smarter, not just faster.' Working with @Marcus Johnson on the launch campaign!",
        all_projects=[nuralchat],
        all_profiles=[priya, marcus],
        created_at=datetime(2024, 3, 15)
    )

    Post(
        author=emma,
        content="Fascinating insights from our latest research on AI-human collaboration! Teams using @NuralChat report 40% better communication clarity. Full report coming soon!",
        all_projects=[nuralchat],
        all_profiles=[emma],
        created_at=datetime(2024, 3, 18)
    )

    Post(
        author=david,
        content="Kicking off the @Nural Platform project today! Building the foundation for enterprise-scale reliability. Looking forward to working with @Zak Rab on the ML infrastructure integration!",
        all_projects=[platform],
        all_profiles=[david, zak],
        created_at=datetime(2024, 3, 20)
    )

    Post(
        author=priya,
        content="Working with @Sophia Chen and @Emma Thompson on our new brand story. The research insights are helping us craft a compelling narrative about AI-human collaboration!",
        all_projects=[brand],
        all_profiles=[priya, sophia, emma],
        created_at=datetime(2024, 3, 22)
    )

    Post(
        author=emma,
        content="Just wrapped up user interviews for @Nural Signals. Teams love the visibility features, but we've identified some opportunities to make the interface more intuitive. @Sophia Chen, let's discuss!",
        all_projects=[signals],
        all_profiles=[emma, sophia],
        created_at=datetime(2024, 3, 25)
    )

    # Return as list
    return [kenny, zak, sophia, marcus, aisha, rachel, james, maria, david, priya, emma]
