"use client";

import { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { apiClient } from "@/services/api-client";
import {
  Sparkles,
  Send,
  RefreshCw,
  History,
  ChevronDown,
  ChevronUp,
  Zap,
  Database,
  BarChart3,
  Clock,
  Target,
  Brain,
  Lightbulb,
  AlertTriangle,
  TrendingUp,
  ArrowRight,
  Download,
  User,
  Bot,
} from "lucide-react";

interface Message {
  role: "user" | "ai";
  content: string;
  timestamp: string;
  tools?: string[];
  sources?: any[];
  confidence?: number;
  followups?: string[];
  latency?: number;
}
interface Conversation {
  id: string;
  title: string;
  created_at: string;
}

const SUGGESTED = [
  "What is today's procurement risk?",
  "Why has inventory value changed?",
  "Which suppliers are becoming unreliable?",
  "What inventory should I reorder this week?",
  "What should management prioritize today?",
  "Summarize supplier performance this quarter.",
  "Identify the top 3 business risks right now.",
  "Which warehouses require attention?",
];

export default function ExecutiveCopilot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>(SUGGESTED);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const [expandedMsg, setExpandedMsg] = useState<number | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    apiClient
      .get<{ data: { questions: string[] } }>("/api/v1/ai/executive/suggested-questions")
      .then((r) => {
        if (r.data?.questions) setSuggestions(r.data.questions);
      })
      .catch(() => {});
    apiClient
      .get<{ data: Conversation[] }>("/api/v1/ai/executive/conversations")
      .then((r) => setConversations(r.data || []))
      .catch(() => {});
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async (question: string) => {
    if (!question.trim() || loading) return;
    const userMsg: Message = {
      role: "user",
      content: question,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const r = await apiClient.post<{
        data: {
          answer: string;
          tools_used: string[];
          sources: any[];
          confidence: number;
          latency_ms: number;
          suggested_followups: string[];
        };
      }>("/api/v1/ai/executive/chat", { question });
      const d = r.data;
      const aiMsg: Message = {
        role: "ai",
        content: d.answer || "No response",
        timestamp: new Date().toISOString(),
        tools: d.tools_used,
        sources: d.sources,
        confidence: d.confidence,
        followups: d.suggested_followups,
        latency: d.latency_ms,
      };
      setMessages((prev) => [...prev, aiMsg]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: "AI service is currently unavailable. Please try again.",
          timestamp: new Date().toISOString(),
        },
      ]);
    }
    setLoading(false);
  };

  const exportConversation = () => {
    const text = messages
      .map(
        (m) =>
          `[${m.role.toUpperCase()}] ${new Date(m.timestamp).toLocaleTimeString()}\n${m.content}\n`
      )
      .join("\n");
    const blob = new Blob([text], { type: "text/plain" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "executive-briefing.txt";
    a.click();
  };

  return (
    <div className="flex h-[calc(100vh-6rem)] gap-6">
      {/* Main Chat Area */}
      <div className="flex flex-1 flex-col">
        <div className="mb-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-primary/10 p-2">
              <Sparkles className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h1 className="text-xl font-bold">Executive Copilot</h1>
              <p className="text-xs text-muted-foreground">AI-powered business decision support</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => setShowHistory(!showHistory)}>
              <History className="mr-2 h-3 w-3" /> History
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={exportConversation}
              disabled={messages.length === 0}
            >
              <Download className="mr-2 h-3 w-3" /> Export
            </Button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto space-y-4 pr-2 mb-4">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="rounded-full bg-primary/10 p-6 mb-6">
                <Sparkles className="h-12 w-12 text-primary" />
              </div>
              <h2 className="text-2xl font-bold mb-2">Executive Decision Assistant</h2>
              <p className="text-muted-foreground max-w-md mb-8">
                Ask me anything about your business. I analyze real-time ERP data to provide
                evidence-backed insights.
              </p>
              <div className="flex flex-wrap justify-center gap-2 max-w-xl">
                {suggestions.slice(0, 6).map((q, i) => (
                  <button
                    key={i}
                    onClick={() => sendMessage(q)}
                    className="rounded-full border px-4 py-2 text-sm hover:bg-muted hover:border-primary/50 transition-colors text-left"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-3 ${msg.role === "user" ? "justify-end" : ""}`}>
              {msg.role === "ai" && (
                <div className="rounded-full bg-primary/10 p-1.5 h-fit">
                  <Sparkles className="h-4 w-4 text-primary" />
                </div>
              )}
              <div
                className={`max-w-[80%] ${msg.role === "user" ? "bg-primary text-primary-foreground rounded-2xl rounded-br-md px-4 py-3" : "space-y-3"}`}
              >
                {msg.role === "user" ? (
                  <p className="text-sm">{msg.content}</p>
                ) : (
                  <>
                    <Card className="border-primary/20">
                      <CardContent className="py-4">
                        <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                      </CardContent>
                    </Card>

                    {/* Meta bar */}
                    <div className="flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
                      {msg.confidence && (
                        <span className="flex items-center gap-1 rounded-full bg-muted px-2 py-1">
                          <Target className="h-3 w-3" />
                          {msg.confidence}% confidence
                        </span>
                      )}
                      {msg.latency && (
                        <span className="flex items-center gap-1 rounded-full bg-muted px-2 py-1">
                          <Clock className="h-3 w-3" />
                          {msg.latency}ms
                        </span>
                      )}
                      {msg.tools && msg.tools.length > 0 && (
                        <button
                          onClick={() => setExpandedMsg(expandedMsg === i ? null : i)}
                          className="flex items-center gap-1 rounded-full bg-muted px-2 py-1 hover:bg-muted/80"
                        >
                          <Database className="h-3 w-3" />
                          {msg.tools.length} tools used
                          {expandedMsg === i ? (
                            <ChevronUp className="h-3 w-3" />
                          ) : (
                            <ChevronDown className="h-3 w-3" />
                          )}
                        </button>
                      )}
                    </div>

                    {/* Expanded tools/sources */}
                    {expandedMsg === i && msg.sources && (
                      <Card className="bg-muted/30 border-dashed">
                        <CardContent className="py-3">
                          <p className="text-xs font-medium mb-2">Data Sources Consulted</p>
                          <div className="space-y-1">
                            {msg.sources.map((s: any, j: number) => (
                              <div
                                key={j}
                                className="flex items-center gap-2 text-xs text-muted-foreground"
                              >
                                <Database className="h-3 w-3" />
                                <span>
                                  {s.name}.{s.method}()
                                </span>
                              </div>
                            ))}
                          </div>
                          {msg.tools && (
                            <div className="mt-2 flex flex-wrap gap-1">
                              {msg.tools.map((t: string, j: number) => (
                                <span
                                  key={j}
                                  className="rounded bg-primary/10 px-2 py-0.5 text-xs text-primary"
                                >
                                  {t}
                                </span>
                              ))}
                            </div>
                          )}
                        </CardContent>
                      </Card>
                    )}

                    {/* Follow-ups */}
                    {msg.followups && msg.followups.length > 0 && (
                      <div className="space-y-1">
                        <p className="text-xs font-medium text-muted-foreground">
                          Follow-up questions
                        </p>
                        <div className="flex flex-wrap gap-1">
                          {msg.followups.map((q: string, j: number) => (
                            <button
                              key={j}
                              onClick={() => sendMessage(q)}
                              className="rounded-full border px-3 py-1 text-xs hover:bg-muted hover:border-primary/50 transition-colors text-left"
                            >
                              {q}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </>
                )}
              </div>
              {msg.role === "user" && (
                <div className="rounded-full bg-muted p-1.5 h-fit">
                  <User className="h-4 w-4" />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex gap-3">
              <div className="rounded-full bg-primary/10 p-1.5 h-fit">
                <Sparkles className="h-4 w-4 text-primary animate-pulse" />
              </div>
              <Card className="border-primary/20 max-w-[80%]">
                <CardContent className="py-4">
                  <p className="text-sm text-muted-foreground animate-pulse">
                    Analyzing business data...
                  </p>
                </CardContent>
              </Card>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* Input */}
        <div className="border-t pt-4">
          <div className="flex gap-2">
            <input
              className="flex-1 rounded-full border px-5 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Ask about inventory, procurement, suppliers, or business health..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage(input)}
              disabled={loading}
            />
            <Button
              size="icon"
              className="rounded-full h-12 w-12"
              onClick={() => sendMessage(input)}
              disabled={loading || !input.trim()}
            >
              {loading ? (
                <RefreshCw className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
          <div className="mt-3 flex flex-wrap gap-1.5">
            {suggestions.slice(0, 4).map((q, i) => (
              <button
                key={i}
                onClick={() => sendMessage(q)}
                className="rounded-full border px-3 py-1 text-xs text-muted-foreground hover:bg-muted hover:text-foreground transition-colors"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* History Sidebar */}
      {showHistory && (
        <div className="w-72 border-l pl-4 overflow-y-auto">
          <h3 className="font-semibold text-sm mb-3 flex items-center gap-2">
            <History className="h-4 w-4" /> Recent Conversations
          </h3>
          {conversations.length === 0 ? (
            <p className="text-xs text-muted-foreground">No conversations yet</p>
          ) : (
            <div className="space-y-2">
              {conversations.map((c) => (
                <div
                  key={c.id}
                  className="rounded-lg border p-3 cursor-pointer hover:bg-muted transition-colors"
                >
                  <p className="text-xs font-medium truncate">{c.title}</p>
                  <p className="text-xs text-muted-foreground mt-1">
                    {new Date(c.created_at).toLocaleDateString()}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
