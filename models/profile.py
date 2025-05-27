import uuid
from typing import List, Dict


class Profile:
    def __init__(
        self,
        name: str,
        title: str = "",
        location: str = "",
        bio: str = "",
        skills: List[str] = None,
        experiences: List[Dict] = None,
        education: List[Dict] = None,
        links: Dict[str, str] = None,
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.title = title
        self.location = location
        self.bio = bio
        self.skills = skills or []
        self.experiences = experiences or []
        self.education = education or []
        self.links = links or {}

        self.posts = []           # List of Post objects
        self.contributions = []   # List of Contribution objects
        self.mentioned_in = []    # Optional: posts where this person was mentioned

    def add_post(self, post):
        self.posts.append(post)

    def add_contribution(self, contribution):
        self.contributions.append(contribution)

    def to_chunks(self) -> List[Dict]:
        """Convert profile data into searchable chunks with metadata."""
        chunks = []
        
        # Basic info chunk
        chunks.append({
            "id": f"{self.id}_basic",
            "object_id": self.id,
            "object_type": "profile",
            "chunk_type": "basic_info",
            "text": f"{self.name} is a {self.title} based in {self.location}. {self.bio}",
            "metadata": {
                "name": self.name,
                "title": self.title,
                "location": self.location
            }
        })

        # Skills chunk
        if self.skills:
            chunks.append({
                "id": f"{self.id}_skills",
                "object_id": self.id,
                "object_type": "profile",
                "chunk_type": "skills",
                "text": f"{self.name}'s skills include: {', '.join(self.skills)}",
                "metadata": {"skills": self.skills}
            })

        # Experience chunks
        for exp in self.experiences:
            chunks.append({
                "id": f"{self.id}_exp_{exp['company']}",
                "object_id": self.id,
                "object_type": "profile",
                "chunk_type": "experience",
                "text": f"From {exp['start']} to {exp['end']}, {self.name} worked as {exp['role']} at {exp['company']}. {exp['description']}",
                "metadata": {
                    "company": exp['company'],
                    "role": exp['role'],
                    "start": exp['start'],
                    "end": exp['end']
                }
            })

        # Education chunks
        for edu in self.education:
            chunks.append({
                "id": f"{self.id}_edu_{edu['school']}",
                "object_id": self.id,
                "object_type": "profile",
                "chunk_type": "education",
                "text": f"{self.name} earned a {edu['degree']} from {edu['school']} in {edu['year']}",
                "metadata": {
                    "school": edu['school'],
                    "degree": edu['degree'],
                    "year": edu['year']
                }
            })

        # Contributions summary
        if self.contributions:
            project_roles = {}
            for contrib in self.contributions:
                if contrib.project.title not in project_roles:
                    project_roles[contrib.project.title] = []
                project_roles[contrib.project.title].append(f"{contrib.role} ({contrib.start}-{contrib.end})")
            
            for project, roles in project_roles.items():
                chunks.append({
                    "id": f"{self.id}_contrib_{project}",
                    "object_id": self.id,
                    "object_type": "profile",
                    "chunk_type": "contributions",
                    "text": f"{self.name} has contributed to {project} as: {', '.join(roles)}",
                    "metadata": {"project": project, "roles": roles}
                })

        return chunks

    def __repr__(self):
        return f"<Profile {self.name}, {self.title} in {self.location}>"
