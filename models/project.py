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
            "text": f"{self.title} is a project currently marked as '{self.status}'. Description: {self.description}"
        })

        # Contributor summaries
        for i, c in enumerate(self.contributions):
            chunks.append({
                "id": f"{self.id}_contributor_{i}",
                "object_id": self.id,
                "object_type": "project",
                "chunk_type": "contributor",
                "text": f"{c.person.name} worked on {self.title} as a {c.role} from {c.start} to {c.end}. {c.description}"
            })

        return chunks

    def __repr__(self):
        return f"<Project {self.title} ({self.status})>"
