"""RAG Service using OpenAI Agents SDK and Qdrant."""
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from app.config import get_settings


class RAGService:
    """Retrieval Augmented Generation service for textbook Q&A."""
    
    def __init__(self):
        self.settings = get_settings()
        self.openai = OpenAI(api_key=self.settings.openai_api_key)
        
        # Initialize Qdrant client
        if self.settings.qdrant_api_key:
            self.qdrant = QdrantClient(
                url=self.settings.qdrant_url,
                api_key=self.settings.qdrant_api_key
            )
        else:
            self.qdrant = QdrantClient(url=self.settings.qdrant_url)
    
    async def get_embedding(self, text: str) -> list[float]:
        """Get embedding vector for text using OpenAI."""
        response = self.openai.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    async def search_similar(self, query: str, limit: int = 5) -> list[dict]:
        """Search for similar content in vector database."""
        try:
            query_vector = await self.get_embedding(query)
            
            results = self.qdrant.search(
                collection_name=self.settings.qdrant_collection,
                query_vector=query_vector,
                limit=limit
            )
            
            return [
                {
                    "content": hit.payload.get("content", ""),
                    "chapter": hit.payload.get("chapter", ""),
                    "score": hit.score
                }
                for hit in results
            ]
        except Exception:
            # Return empty if collection doesn't exist yet
            return []
    
    async def answer_question(
        self,
        question: str,
        context: str = "",
        user_level: str = "intermediate"
    ) -> dict:
        """Answer a question using RAG."""
        # Search for relevant content
        similar_docs = await self.search_similar(question)
        
        # Build context from retrieved documents
        rag_context = "\n\n".join([
            f"[From {doc['chapter']}]: {doc['content']}"
            for doc in similar_docs
        ])
        
        # Adapt system prompt based on user level
        level_instructions = {
            "beginner": "Use simple language, analogies, and step-by-step explanations.",
            "intermediate": "Balance technical accuracy with clear explanations.",
            "advanced": "Be concise and focus on technical details and edge cases."
        }
        
        system_prompt = f"""You are an expert robotics instructor for the Physical AI textbook.
Answer questions about ROS 2, Gazebo, NVIDIA Isaac, and VLA models.

User Level: {user_level}
{level_instructions.get(user_level, level_instructions['intermediate'])}

Use the following context from the textbook to answer:
{rag_context}

Additional context provided by user:
{context}

If the answer isn't in the context, use your knowledge but mention it's general information."""

        # Generate answer using OpenAI
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return {
            "answer": response.choices[0].message.content,
            "sources": similar_docs[:3] if similar_docs else None,
            "confidence": similar_docs[0]["score"] if similar_docs else 0.5
        }
    
    async def explain_text(self, text: str, user_level: str = "intermediate") -> str:
        """Explain selected text in simpler terms."""
        level_prompts = {
            "beginner": "Explain this like I'm new to programming and robotics:",
            "intermediate": "Explain this concept clearly:",
            "advanced": "Provide a technical deep-dive on:"
        }
        
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful robotics tutor. Explain concepts clearly."
                },
                {
                    "role": "user",
                    "content": f"{level_prompts.get(user_level, level_prompts['intermediate'])}\n\n{text}"
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content

