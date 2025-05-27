import uuid
from datetime import datetime
from typing import List, Dict


class Post:
    def __init__(self, author, content: str, all_projects: List['Project'], all_profiles: List['Profile'], created_at: datetime = None):
        self.id = str(uuid.uuid4())
        self.author = author
        self.content = content
        self.created_at = created_at or datetime.now()
        self.linked_projects = self._detect_projects(content, all_projects)
        self.mentioned_people = self._detect_people(content, all_profiles)

        # Link to author
        self.author.add_post(self)

        # Link to matched projects
        for project in self.linked_projects:
            project.add_post(self)

        # Link to mentioned profiles (optional: add post to their mentions)
        for person in self.mentioned_people:
            if hasattr(person, 'mentioned_in'):
                person.mentioned_in.append(self)

    def _detect_projects(self, content, projects):
        matches = []
        content_normalized = content.lower().replace(" ", "")
        for project in projects:
            if f"@{project.title.lower().replace(' ', '')}" in content_normalized:
                matches.append(project)
        return matches

    def _detect_people(self, content, profiles):
        matches = []
        content_normalized = content.lower().replace(" ", "")
        for profile in profiles:
            if f"@{profile.name.lower().replace(' ', '')}" in content_normalized and profile != self.author:
                matches.append(profile)
        return matches

    def to_chunk(self) -> Dict:
        # Create a more searchable text representation
        text_parts = [
            f"On {self.created_at.strftime('%Y-%m-%d')}, {self.author.name} posted:",
            f"\"{self.content.strip()}\""
        ]
        
        # Add context about mentioned projects and people
        if self.linked_projects:
            text_parts.append(f"This post mentions projects: {', '.join(p.title for p in self.linked_projects)}")
        if self.mentioned_people:
            text_parts.append(f"This post mentions people: {', '.join(p.name for p in self.mentioned_people)}")

        return {
            "id": f"{self.id}_content",
            "object_id": self.id,
            "object_type": "post",
            "chunk_type": "content",
            "text": " ".join(text_parts),
            "metadata": {
                "author": self.author.name,
                "date": self.created_at.strftime('%Y-%m-%d'),
                "projects": [p.title for p in self.linked_projects],
                "mentioned_people": [p.name for p in self.mentioned_people],
                "year": self.created_at.year  # Add year for temporal queries
            }
        }

    def __repr__(self):
        return f"<Post by {self.author.name} on {self.created_at.strftime('%Y-%m-%d')}>"
