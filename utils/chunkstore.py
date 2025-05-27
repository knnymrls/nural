import openai
import numpy as np
import json
import os
from typing import List, Dict

from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY


def get_embedding(text: str) -> np.ndarray:
    """Get the OpenAI embedding for a given string."""
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class ChunkStore:
    def __init__(self):
        self.chunks: List[Dict] = []

    def add_chunk(self, chunk: Dict):
        """Embed a single chunk and add it to the store."""
        if "embedding" not in chunk:
            chunk["embedding"] = get_embedding(chunk["text"])
        self.chunks.append(chunk)

    def bulk_add(self, chunks: List[Dict]):
        """Embed and add multiple chunks to the store."""
        for chunk in chunks:
            self.add_chunk(chunk)

    def query(self, question: str, top_k=5) -> List[Dict]:
        """
        Find the top-k most relevant chunks for a user query, with special handling for team queries.
        
        The method uses semantic search (embeddings) to find relevant chunks, but has special logic
        for queries about project teams. For example, "Who is working on NuralChat right now?" will
        prioritize current team information.
        
        Args:
            question: The user's question
            top_k: Maximum number of chunks to return (default: 5)
            
        Returns:
            List of relevant chunks, each containing:
            - text: The chunk's content
            - object_type: Type of object (project, profile, post)
            - chunk_type: Type of information (overview, current_team, contributor, etc.)
            - metadata: Additional context about the chunk
        """
        # Get semantic embedding for the question
        query_embedding = get_embedding(question)
        
        # Calculate similarity scores for all chunks
        # Each chunk is paired with its cosine similarity to the query
        scored_chunks = [
            (chunk, cosine_similarity(query_embedding, chunk["embedding"]))
            for chunk in self.chunks
        ]
        
        # Sort chunks by similarity score (highest first)
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        
        # Define keywords to detect different types of queries
        # Team queries ask about people/contributors
        team_keywords = ["who", "working", "team", "member", "contributor", "people", "current", "now"]
        # Project queries mention work or projects in general
        project_keywords = ["project", "work", "on", "right", "now", "currently", "both"]
        
        # Check if this is a query about a project team
        is_team_query = any(word in question.lower() for word in team_keywords)
        is_project_query = any(word in question.lower() for word in project_keywords)
        
        # Special handling for team queries about specific projects
        if is_team_query and is_project_query:
            # Get all unique, canonical project names from the entire chunk store
            all_known_project_names = set()
            for chunk_item in self.chunks:
                if chunk_item.get("object_type") == "project" and \
                   "metadata" in chunk_item and \
                   "project" in chunk_item["metadata"]:
                    all_known_project_names.add(chunk_item["metadata"]["project"])

            # Identify project names explicitly mentioned in the question
            project_names = set()
            question_lower = question.lower()
            if all_known_project_names: # Only proceed if we know some project names
                for known_name in all_known_project_names:
                    if known_name.lower() in question_lower:
                        project_names.add(known_name) # Add the canonical name

            # If direct extraction from query yields no projects (or few, for non-specific queries),
            # fall back to/augment with the semantic search method.
            if not project_names or not ("both" in question_lower or "and" in question_lower or len(project_names) > 1):
                # Use a temporary set for semantic additions to avoid modifying project_names if it was already populated by direct match for a specific multi-project query
                semantic_project_names = set()
                for chunk, _ in scored_chunks[:20]:
                    if chunk.get("object_type") == "project":
                        if "metadata" in chunk and "project" in chunk["metadata"]:
                            # Ensure the project name from metadata is one of the known canonical names
                            if chunk["metadata"]["project"] in all_known_project_names:
                                semantic_project_names.add(chunk["metadata"]["project"])
                        elif chunk.get("chunk_type") == "overview": # If no metadata.project, try parsing overview
                            text = chunk["text"].lower()
                            if " is a project" in text:
                                parsed_name_lower = text.split(" is a project")[0].strip()
                                for canonical_name in all_known_project_names:
                                    if canonical_name.lower() == parsed_name_lower:
                                        semantic_project_names.add(canonical_name)
                                        break
                if not project_names: # If direct search found nothing
                    project_names = semantic_project_names
                else: # If direct search found some, augment them (e.g. for vague queries that named one project)
                    project_names.update(semantic_project_names)
            
            # For multi-project queries (e.g., "Who works on both X and Y?")
            is_multi_project = len(project_names) > 1 or "both" in question.lower() or "and" in question.lower()
            
            if is_multi_project:
                # First, collect all current team chunks for the relevant projects
                project_teams = {}
                for chunk in self.chunks:  # Look through ALL chunks, not just scored ones
                    if (chunk["chunk_type"] == "current_team" and 
                        "metadata" in chunk and 
                        chunk["metadata"].get("project") in project_names):
                        project = chunk["metadata"]["project"]
                        if project not in project_teams:
                            project_teams[project] = chunk
                
                # If we don't have team chunks for all projects, try to find them in scored chunks
                if len(project_teams) < len(project_names):
                    for chunk, _ in scored_chunks:
                        if (chunk["chunk_type"] == "current_team" and 
                            "metadata" in chunk and 
                            chunk["metadata"].get("project") in project_names and
                            chunk["metadata"]["project"] not in project_teams):
                            project = chunk["metadata"]["project"]
                            project_teams[project] = chunk
                
                # Find people who work on multiple projects
                person_projects = {}  # Map person name to dict of project -> role
                
                # Process each project's team chunk
                for project, team_chunk in project_teams.items():
                    # Extract team members from the text if metadata is not available
                    if "metadata" not in team_chunk or "current_contributors" not in team_chunk["metadata"]:
                        # Parse the text format: "Name (Role: X, Focus: Y)"
                        text = team_chunk["text"]
                        if "Current Team for" in text:
                            members_text = text.split("Current Team for " + project + ": ")[1]
                            for member_info in members_text.split(" | "):
                                if "(" in member_info and ")" in member_info:
                                    name = member_info.split(" (")[0].strip()
                                    role_info = member_info.split("(")[1].split(")")[0]
                                    role = role_info.split(", Focus:")[0].replace("Role: ", "").strip()
                                    description = role_info.split(", Focus:")[1].strip() if ", Focus:" in role_info else ""
                                    
                                    if name not in person_projects:
                                        person_projects[name] = {}
                                    person_projects[name][project] = {
                                        "role": role,
                                        "description": description
                                    }
                    else:
                        # Use metadata if available
                        for contributor in team_chunk["metadata"]["current_contributors"]:
                            name = contributor["name"]
                            if name not in person_projects:
                                person_projects[name] = {}
                            person_projects[name][project] = {
                                "role": contributor["role"],
                                "description": contributor["description"]
                            }
                
                # Find people who work on all relevant projects
                multi_project_people = {
                    name: projects 
                    for name, projects in person_projects.items() 
                    if len(projects) > 1
                }
                
                if multi_project_people:
                    # Create a special chunk for people working on multiple projects
                    result = [{
                        "text": "People working on multiple projects:\n" + 
                               "\n".join(
                                   f"{name}:\n" + 
                                   "\n".join(
                                       f"- {project}: {info['role']} ({info['description']})"
                                       for project, info in projects.items()
                                   )
                                   for name, projects in multi_project_people.items()
                               ),
                        "object_type": "project",
                        "chunk_type": "multi_project_team",
                        "metadata": {
                            "people": list(multi_project_people.keys()),
                            "projects": list(project_names),
                            "roles": {
                                name: {
                                    project: info["role"]
                                    for project, info in projects.items()
                                }
                                for name, projects in multi_project_people.items()
                            }
                        }
                    }]
                    
                    # Add individual contributor chunks for these people
                    for chunk, _ in scored_chunks:
                        if (chunk["chunk_type"] == "contributor" and 
                            "metadata" in chunk and 
                            chunk["metadata"].get("name") in multi_project_people):
                            result.append(chunk)
                            if len(result) >= top_k:
                                break
                    
                    return result[:top_k]
                
                # If no multi-project people found, return team chunks for all projects
                result = []
                for project, team_chunk in project_teams.items():
                    result.append(team_chunk)
                    if len(result) >= top_k:
                        break
                return result[:top_k]
            
            # For single project queries, use the original organization logic
            organized_chunks = {
                project: {
                    "current_team": None,  # Only one current team chunk per project
                    "overview": None,      # Only one overview chunk per project
                    "contributors": {},    # Multiple contributor chunks possible
                    "posts": []            # Multiple posts possible
                }
                for project in project_names
            }
            
            # Process chunks and organize them
            for chunk, score in scored_chunks:
                if "metadata" not in chunk:
                    continue
                    
                project = chunk["metadata"].get("project")
                if not project or project not in project_names:
                    continue
                
                chunk_type = chunk["chunk_type"]
                
                # Store chunks based on their type
                if chunk_type == "current_team" and not organized_chunks[project]["current_team"]:
                    organized_chunks[project]["current_team"] = chunk
                elif chunk_type == "overview" and not organized_chunks[project]["overview"]:
                    organized_chunks[project]["overview"] = chunk
                elif chunk_type == "contributor":
                    person = chunk["metadata"].get("name")
                    if person and person not in organized_chunks[project]["contributors"]:
                        organized_chunks[project]["contributors"][person] = chunk
                elif chunk_type == "content" and chunk["object_type"] == "post":
                    organized_chunks[project]["posts"].append(chunk)
            
            # Build the final result list
            result = []
            
            # Add current team chunks for all relevant projects
            for project in project_names:
                if organized_chunks[project]["current_team"]:
                    result.append(organized_chunks[project]["current_team"])
                if organized_chunks[project]["overview"]:
                    result.append(organized_chunks[project]["overview"])
            
            # Add contributor chunks if we still need more
            if len(result) < top_k:
                for project in project_names:
                    for contributor in organized_chunks[project]["contributors"].values():
                        if contributor not in result:
                            result.append(contributor)
                            if len(result) >= top_k:
                                break
                    if len(result) >= top_k:
                        break
            
            # Add relevant posts if we still need more
            if len(result) < top_k:
                for project in project_names:
                    for post in organized_chunks[project]["posts"]:
                        if post not in result:
                            result.append(post)
                            if len(result) >= top_k:
                                break
                    if len(result) >= top_k:
                        break
            
            return result[:top_k]
        
        # For non-team queries, return unique chunks based on object_id and chunk_type
        # This prevents duplicate information while maintaining diversity
        seen = set()
        unique_chunks = []
        for chunk, _ in scored_chunks:
            key = (chunk["object_id"], chunk["chunk_type"])
            if key not in seen:
                seen.add(key)
                unique_chunks.append(chunk)
                if len(unique_chunks) >= top_k:
                    break
        
        return unique_chunks

    def exists(self, text: str) -> bool:
        """Check if a chunk with this exact text is already stored."""
        return any(c["text"] == text for c in self.chunks)

    def count(self) -> int:
        return len(self.chunks)

    def clear(self):
        """Reset the store (remove all chunks)."""
        self.chunks = []

    def save(self, filepath: str):
        """Save all chunks (with embeddings) to a JSON file."""
        serializable = [
            {
                k: (v.tolist() if k == "embedding" else v)
                for k, v in chunk.items()
            }
            for chunk in self.chunks
        ]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2)
        print(f"💾 Saved {len(self.chunks)} chunks to {filepath}")

    def load(self, filepath: str):
        """Load chunks and embeddings from a JSON file."""
        if not os.path.exists(filepath):
            print(f"⚠️ File not found: {filepath}")
            return

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.chunks = [
            {
                **chunk,
                "embedding": np.array(chunk["embedding"])
            }
            for chunk in data
        ]
        print(f"📂 Loaded {len(self.chunks)} chunks from {filepath}")
