import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.chunkstore import ChunkStore
from data.sample_data import get_sample_data


def regenerate_chunks(cache_file="chunks.json"):
    """Regenerate and save chunks from sample data."""
    print("🔄 Regenerating chunks from sample data...")
    
    # Create new store
    store = ChunkStore()
    
    # Get fresh sample data
    profiles = get_sample_data()
    
    # Add all chunks
    for profile in profiles:
        store.bulk_add(profile.to_chunks())
        for post in profile.posts:
            store.add_chunk(post.to_chunk())
        for contrib in profile.contributions:
            store.bulk_add(contrib.project.to_chunks())
    
    # Save to file
    store.save(cache_file)
    print(f"✅ Successfully regenerated {store.count()} chunks")


if __name__ == "__main__":
    regenerate_chunks() 