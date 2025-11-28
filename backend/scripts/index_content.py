"""Script to index textbook content into Qdrant vector database."""
import os
import glob
from pathlib import Path
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import hashlib


def get_embedding(client: OpenAI, text: str) -> list[float]:
    """Get embedding vector for text."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def chunk_content(content: str, chunk_size: int = 500) -> list[str]:
    """Split content into chunks for embedding."""
    paragraphs = content.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


def index_textbook():
    """Index all markdown files from the docs folder."""
    # Initialize clients
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    if qdrant_api_key:
        qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    else:
        qdrant = QdrantClient(url=qdrant_url)
    
    collection_name = "textbook_chunks"
    
    # Create collection if not exists
    try:
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
        print(f"Created collection: {collection_name}")
    except Exception as e:
        print(f"Collection exists or error: {e}")
    
    # Find all markdown files
    docs_path = Path(__file__).parent.parent.parent / "docs"
    md_files = glob.glob(str(docs_path / "**/*.md"), recursive=True)
    
    print(f"Found {len(md_files)} markdown files")
    
    points = []
    point_id = 0
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract chapter info from path
        rel_path = Path(md_file).relative_to(docs_path)
        chapter = str(rel_path.parent) if rel_path.parent != Path('.') else "intro"
        
        # Chunk the content
        chunks = chunk_content(content)
        
        for chunk in chunks:
            if len(chunk) < 50:  # Skip very short chunks
                continue
            
            # Generate embedding
            embedding = get_embedding(openai_client, chunk)
            
            # Create point
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "content": chunk,
                    "chapter": chapter,
                    "file": str(rel_path),
                    "hash": hashlib.md5(chunk.encode()).hexdigest()
                }
            )
            points.append(point)
            point_id += 1
            
            print(f"Indexed chunk {point_id} from {rel_path}")
    
    # Upsert all points
    if points:
        qdrant.upsert(collection_name=collection_name, points=points)
        print(f"\n✅ Indexed {len(points)} chunks into Qdrant")
    else:
        print("No content to index")


if __name__ == "__main__":
    index_content()

