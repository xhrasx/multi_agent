import React, { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Send, Bot, Loader2 } from "lucide-react";
import ChatMessage from "./components/ChatMessage";

const WELCOME_MSG = {
  role: "assistant",
  content:
    "👋 你好！我是多智能体协作平台 AI 助手。\n\n" +
    "支持工具：🧮 计算器 | 🌐 翻译 | ☁️ 天气 | 📅 日期 | 🔍 搜索\n\n" +
    '试试输入：「计算 3+5*2」或「翻译你好世界」',
  data: null,
};

const QUICK_QUERIES = [
  "计算 3+5*2",
  "翻译你好世界",
  "北京天气怎么样",
  "今天几号",
  "你是谁",
];

export default function App() {
  const [messages, setMessages] = useState([WELCOME_MSG]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || loading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text, data: null }]);
    setLoading(true);

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: text }), // ← 对应你后端的 QueryRequest
      });
      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.final || "无结果",
          data,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `❌ 请求失败: ${err.message}\n\n请确认后端已启动 (uvicorn app.main:app)`,
          data: null,
        },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-white flex flex-col">
      {/* ====== Header ====== */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-sm px-4 py-3 flex items-center gap-3 shrink-0">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <Bot className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-sm font-semibold tracking-tight">
            Multi-Agent Platform
          </h1>
          <p className="text-xs text-slate-500">ReAct 多智能体协作平台</p>
        </div>
        <div className="ml-auto flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-xs text-slate-500">已连接</span>
        </div>
      </header>

      {/* ====== Messages ====== */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}

        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex gap-3"
          >
            <div className="shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-purple-600 to-indigo-600 flex items-center justify-center">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="bg-slate-800 border border-slate-700 px-4 py-3 rounded-2xl rounded-tl-md flex items-center gap-3">
              <Loader2 className="w-4 h-4 text-indigo-400 animate-spin" />
              <span className="text-sm text-slate-400">Agent 推理中</span>
              <div className="flex gap-1">
                <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full dot-1" />
                <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full dot-2" />
                <span className="w-1.5 h-1.5 bg-indigo-400 rounded-full dot-3" />
              </div>
            </div>
          </motion.div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* ====== Quick Queries ====== */}
      <div className="px-4 pb-2 flex gap-2 flex-wrap">
        {QUICK_QUERIES.map((q) => (
          <button
            key={q}
            onClick={() => setInput(q)}
            className="text-xs bg-slate-800 hover:bg-slate-700 border border-slate-700 
                       text-slate-400 hover:text-slate-200 px-3 py-1.5 rounded-full 
                       transition-colors"
          >
            {q}
          </button>
        ))}
      </div>

      {/* ====== Input Bar ====== */}
      <div className="border-t border-slate-800 bg-slate-900/80 backdrop-blur-sm px-4 py-3 shrink-0">
        <div className="flex items-center gap-2 max-w-3xl mx-auto">
          <input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="输入你的问题..."
            disabled={loading}
            className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 
                       text-sm text-slate-100 placeholder-slate-500 
                       focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 
                       transition-colors disabled:opacity-50"
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-700 
                       disabled:text-slate-500 text-white w-10 h-10 rounded-xl 
                       flex items-center justify-center transition-colors shrink-0"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}