import uuid
from typing import List


class Project:
    def __init__(self, title, description="", created_by=None, status="active"):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.status = status  # "active", "paused", "complete"
        self.created_by = created_by
        self.contributions: List['Contribution'] = []
        self.linked_posts: List['Post'] = []

    def add_contribution(self, contribution):
        self.contributions.append(contribution)

    def add_post(self, post):
        self.linked_posts.append(post)

    def to_chunks(self) -> List[dict]:
        """Break the project into text chunks for embedding and retrieval."""
        chunks = []

        # Basic project info
        chunks.append({
            "id": f"{self.id}_overview",
            "object_id": self.id,
            "object_type": "project",
            "chunk_type": "overview",
            "text": f"Project Overview: {self.title} is a project currently marked as '{self.status}'. Description: {self.description}"
        })

        # Group current and past contributors
        current_contributors = []
        past_contributors = []
        
        for c in self.contributions:
            if c.end.lower() == "present":
                current_contributors.append(c)
            else:
                past_contributors.append(c)

        # Create a chunk for current team
        if current_contributors:
            # Create a more distinctive current team chunk
            current_team_text = f"Current Team for {self.title}: "
            current_team_text += " | ".join(
                f"{c.person.name} (Role: {c.role}, Focus: {c.description})"
                for c in current_contributors
            )
            chunks.append({
                "id": f"{self.id}_current_team",
                "object_id": self.id,
                "object_type": "project",
                "chunk_type": "current_team",
                "text": current_team_text,
                "metadata": {
                    "project": self.title,
                    "current_contributors": [
                        {
                            "name": c.person.name,
                            "role": c.role,
                            "description": c.description
                        }
                        for c in current_contributors
                    ]
                }
            })

        # Create chunks for individual contributors (both current and past)
        for i, c in enumerate(self.contributions):
            status = "currently" if c.end.lower() == "present" else f"from {c.start} to {c.end}"
            chunks.append({
                "id": f"{self.id}_contributor_{i}",
                "object_id": self.id,
                "object_type": "project",
                "chunk_type": "contributor",
                "text": f"Contributor: {c.person.name} {status} works on {self.title} as a {c.role}. {c.description}",
                "metadata": {
                    "name": c.person.name,
                    "role": c.role,
                    "status": status,
                    "description": c.description
                }
            })

        return chunks

    def __repr__(self):
        return f"<Project {self.title} ({self.status})>"
