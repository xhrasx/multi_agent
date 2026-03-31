"""FastAPI 部署"""
import os
import app.tools
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.core.agent_base import MultiAgentSystem

app = FastAPI(
    title="Multi-Agent System",
    description="多智能体任务调度与工具调用框架",
    version="1.0.0",
)
agent_system = MultiAgentSystem()

# ========== 静态文件服务 ==========
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")


class QueryRequest(BaseModel):
    query: str


# ========== API 路由（放在前面，优先匹配）==========

@app.post("/chat")
async def chat(request: QueryRequest):
    result = agent_system.run(request.query)
    return result


@app.get("/model")
async def get_model_info():
    return {
        "model": agent_system.reasoner.model,
        "api_url": agent_system.reasoner.url,
    }


@app.post("/ask")
def ask(req: QueryRequest):
    result = agent_system.run(req.query)
    return result


@app.get("/tools")
def list_tools():
    return agent_system.executor.list_tools()


# ========== 前端页面（放在最后）==========

if os.path.exists(STATIC_DIR):
    # 提供 JS/CSS 等静态资源
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

    # 所有其他路径返回 index.html（SPA 路由）
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(STATIC_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "Multi-Agent System Running (前端未构建，请先 npm run build)"}