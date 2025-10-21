import React from "react";
import "./Message.css";
import { API_URL } from "../config";

interface Message {
  from: 'user' | 'assistant';
  text: string;
}

interface AIAssistantProps {
  assignmentContext?: any;
}

function AIAssistant({ assignmentContext }: AIAssistantProps = {}) {
  const rightArrow = (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-arrow-right" viewBox="0 0 16 16">
      <path fillRule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
    </svg>
  );
  
  const [chatHistory, setChatHistory] = React.useState<Message[]>([]);
  const chatEndRef = React.useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  React.useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

  // Welcome message when assignment context is provided
  React.useEffect(() => {
    if (assignmentContext) {
      const welcomeMessage = `I'm here to help with "${assignmentContext.title}". What would you like to know?`;
      setChatHistory([{ from: 'assistant', text: welcomeMessage }]);
    }
  }, [assignmentContext]);

  const updateLog = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const input = form.elements[0] as HTMLInputElement;
    const userMessage = input.value.trim();
    
    if (!userMessage) return;

    setChatHistory(prev => [...prev, { from: 'user', text: userMessage }]);
    input.value = '';

    if (assignmentContext) {
      console.log(assignmentContext)
      const bundledPrompt = JSON.stringify({
        query: userMessage,
        assignment: assignmentContext
      });

      try {
        const response = await fetch(`${API_URL}/llm/generate_response/`, {
          method: 'POST',
          headers: {
            "Content-Type": "application/json",
          },
          body: bundledPrompt
        });

        if (response.ok) {
          const LLMResponse = await response.json();
          setChatHistory(prevHistory => [...prevHistory, { from: 'assistant', text: LLMResponse }]);
        }
      } catch (error) {
        console.error("Error generating response:", error);
        setChatHistory(prev => [...prev, { 
          from: 'assistant', 
          text: "Sorry, I encountered an error. Please try again." 
        }]);
      }
      return;
    }

    try {
      const response = await fetch(`${API_URL}/llm/semantic_search/`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: userMessage,
          user_id: localStorage.getItem("user_id"),
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const assignment_id = data[0];
        const response2 = await fetch(`${API_URL}/assignments/${assignment_id}`);
        
        if (response2.ok) {
          const assignment = await response2.json();

          const bundledPrompt = JSON.stringify({
            query: userMessage,
            assignment: assignment
          });

          const response3 = await fetch(`${API_URL}/llm/generate_response/`, {
            method: 'POST',
            headers: {
              "Content-Type": "application/json",
            },
            body: bundledPrompt
          });

          if (response3.ok) {
            const LLMResponse = await response3.json();
            setChatHistory(prevHistory => [...prevHistory, { from: 'assistant', text: LLMResponse }]);
          }
        }
      }
    } catch (error) {
      console.error("Error in semantic search:", error);
      setChatHistory(prev => [...prev, { 
        from: 'assistant', 
        text: "Sorry, I couldn't find relevant assignments. Please try rephrasing your question." 
      }]);
    }
  };

  return (
    <div
      className="d-flex flex-column border rounded p-3 bg-primary bg-opacity-10"
      style={{ width: "320px", height: assignmentContext ? "600px" : "400px" }}
    >
      <h4 className="fw-bold">
        AI Assistant
        {assignmentContext && <span className="badge bg-primary ms-2 small">Assignment Mode</span>}
      </h4>
      
      <div className="d-flex flex-column" style={{ flex: 1, overflow: "hidden", minHeight: 0 }}>
        <div style={{ flex: 1, overflowY: "auto", marginBottom: "10px", display: "flex", flexDirection: "column" }}>
          <div style={{ marginTop: "auto" }}>
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {chatHistory.length === 0 ? (
                <li className="text-muted">
                  {assignmentContext 
                    ? "Ask me anything about this assignment..." 
                    : "Ask me about your assignments..."}
                </li>
              ) : (
                chatHistory.map((msg, index) => (
                  <li key={index} style={{ marginBottom: "12px" }}>
                    <div className={`d-flex flex-row align-items-start ${msg.from === 'user' ? 'justify-content-end' : 'justify-content-start'}`}>
                      {msg.from === 'assistant' && (
                        <svg 
                          xmlns="http://www.w3.org/2000/svg" 
                          width="28" 
                          height="28" 
                          fill="currentColor" 
                          className="bi bi-robot me-2 flex-shrink-0" 
                          viewBox="0 0 16 16"
                          style={{ marginTop: "2px" }}
                        >
                          <path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5M3 8.062C3 6.76 4.235 5.765 5.53 5.886a26.6 26.6 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.93.93 0 0 1-.765.935c-.845.147-2.34.346-4.235.346s-3.39-.2-4.235-.346A.93.93 0 0 1 3 9.219zm4.542-.827a.25.25 0 0 0-.217.068l-.92.9a25 25 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25 25 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135"/>
                          <path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2zM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5"/>
                        </svg>
                      )}
                      <div id={msg.from === 'user' ? 'user-message' : 'assistant-message'}>
                        {msg.text}
                      </div>
                      {msg.from === 'user' && (
                        <svg 
                          xmlns="http://www.w3.org/2000/svg" 
                          width="24" 
                          height="24" 
                          fill="currentColor" 
                          className="bi bi-person-circle ms-2 flex-shrink-0" 
                          viewBox="0 0 16 16"
                          style={{ marginTop: "2px" }}
                        >
                          <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0"/>
                          <path fillRule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"/>
                        </svg>
                      )}
                    </div>
                  </li>
                ))
              )}
            </ul>
            <div ref={chatEndRef} />
          </div>
        </div>
        
        <div className="input-group">
          <form onSubmit={updateLog} style={{ display: "flex", gap: "5px", width: "100%" }}>
            <input
              type="text"
              className="form-control"
              placeholder={assignmentContext ? "Ask about this assignment..." : "Ask me anything..."}
            />
            <button className="btn btn-outline-primary" type="submit">
              {rightArrow}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default AIAssistant;