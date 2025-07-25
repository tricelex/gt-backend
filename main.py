import asyncio
from contextlib import asynccontextmanager
from typing import List, Dict, Any, AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.DataSEOAgent.tools.data_mcp import dataforseo_server
from app.agency import agency
from app.schema import ChatResponse, ChatRequest

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan."""
    await dataforseo_server.connect()
    yield
    await dataforseo_server.cleanup()


app = FastAPI(
    title="Genta AI Agent",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.router.lifespan_context = lifespan

chat_histories: Dict[str, List[Dict[str, Any]]] = {}


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
        response_obj = await agency.get_response(
            message=request.message,
            verbose=False
        )
        response_text = getattr(response_obj, "final_output", str(response_obj))

        # Add agent response to history
        chat_histories[request.user_id].append({
            "role": "assistant",
            "content": response_text,
            "timestamp": asyncio.get_event_loop().time()
        })

        tools_used = []

        return ChatResponse(
            reply=response_text,
            agent_name="DataSEOAgent",
            tools_used=tools_used
        )

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
