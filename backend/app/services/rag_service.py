"""RAG Service using OpenAI Agents SDK and Qdrant.

Integrates with Reusable Intelligence (Skills & Subagents) for enhanced responses.
"""
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from app.config import get_settings
from app.intelligence.skills import SkillContext, RoboticsExplainerSkill
from app.intelligence.subagents import QAAgent


class RAGService:
    """Retrieval Augmented Generation service for textbook Q&A.

    Uses Reusable Intelligence:
    - QAAgent subagent for orchestrating responses
    - RoboticsExplainerSkill for adapting explanations
    """

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

        # Initialize Reusable Intelligence
        self.explainer_skill = RoboticsExplainerSkill()
    
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
        user_level: str = "intermediate",
        programming_languages: list[str] = None,
        robotics_experience: bool = False
    ) -> dict:
        """Answer a question using RAG with Reusable Intelligence.

        Uses:
        - QAAgent subagent for orchestration
        - RoboticsExplainerSkill for level-appropriate explanations
        """
        # Search for relevant content
        similar_docs = await self.search_similar(question)

        # Build context from retrieved documents
        rag_context = "\n\n".join([
            f"[From {doc['chapter']}]: {doc['content']}"
            for doc in similar_docs
        ])

        # Create skill context from user profile
        skill_context = SkillContext(
            user_level=user_level,
            programming_languages=programming_languages or [],
            robotics_experience=robotics_experience
        )

        # Use QAAgent subagent for enhanced prompting
        qa_agent = QAAgent(context=skill_context)

        # Get level-specific adaptation from skill
        level_adaptation = self.explainer_skill.get_level_adaptation(user_level)

        system_prompt = f"""{qa_agent.system_prompt}

## Level Adaptation
{level_adaptation}

## Retrieved Context from Textbook
{rag_context}

## Additional User Context
{context}

If the answer isn't in the context, use your knowledge but mention it's general information.
Always cite sources when using textbook content."""

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
            "confidence": similar_docs[0]["score"] if similar_docs else 0.5,
            "skill_used": "robotics-explainer",
            "subagent_used": "qa-agent"
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

