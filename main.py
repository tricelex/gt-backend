import asyncio
from contextlib import asynccontextmanager
from typing import List, Dict, Any, AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.DataSEOAgent.tools.data_mcp import dataforseo_server
from app.agency import agency
from app.schema import ChatResponse, ChatHistory, ChatRequest
from app.settings import settings

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan."""
    # Try to connect to the MCP server, but don't fail if it's unavailable
    await dataforseo_server.connect()
    yield
    await dataforseo_server.cleanup()


app = FastAPI(
    title="Genta AI Agent",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chat history storage
chat_histories: Dict[str, List[Dict[str, Any]]] = {}


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker"""
    return {"status": "healthy", "message": "Genta AI Agent is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for interacting with the AI agent"""
    try:
        if not agency:
            raise HTTPException(status_code=500, detail="Agency not available")

        # Get or create chat history for user
        if request.user_id not in chat_histories:
            chat_histories[request.user_id] = []

        # Add user message to history
        chat_histories[request.user_id].append({
            "role": "user",
            "content": request.message,
            "timestamp": asyncio.get_event_loop().time()
        })

        # Use agency.get_completion method to get response
        print(f"Processing message from user {request.user_id}: {request.message}")
        response = agency.get_completion(
            message=request.message,
            verbose=False
        )

        # Add agent response to history
        chat_histories[request.user_id].append({
            "role": "assistant",
            "content": response,
            "timestamp": asyncio.get_event_loop().time()
        })

        # Extract tools used from response (if available)
        tools_used = []
        # Note: tools_used information might be available in the response object
        # depending on the agency implementation

        return ChatResponse(
            reply=response,
            agent_name="DataSEOAgent",
            tools_used=tools_used
        )

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/chat/history/{user_id}", response_model=ChatHistory)
async def get_chat_history(user_id: str):
    """Get chat history for a specific user"""
    if user_id not in chat_histories:
        return ChatHistory(user_id=user_id, messages=[])

    return ChatHistory(
        user_id=user_id,
        messages=chat_histories[user_id]
    )


@app.delete("/chat/history/{user_id}")
async def clear_chat_history(user_id: str):
    """Clear chat history for a specific user"""
    if user_id in chat_histories:
        del chat_histories[user_id]
    return {"message": "Chat history cleared"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
