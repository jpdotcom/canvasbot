import React from "react";
interface Message{
  from: 'user' | 'assistant';
  text: string;
}
function AIAssistant(){
    const rightArrow=(<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-arrow-right" viewBox="0 0 16 16">
    <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
  </svg>)
  
  const [chatHistory, setChatHistory] = React.useState<Message[]>([]);
  const updateLog = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const input = form.elements[0] as HTMLInputElement;
    const userMessage = input.value.trim();
    if (userMessage) {
      setChatHistory([...chatHistory, { from: 'user', text: userMessage }]);
      input.value = '';
      
     
    }
    console.log(localStorage.getItem("user_id"));
    const response = await fetch('http://localhost:8000/llm/semantic_search/', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: userMessage,
        user_id: localStorage.getItem("user_id"),
      }),
    })

    if (response.ok){
      const data = await response.json();
      //List of assignment ids;
      for (const assignment_id of data){
        const response = await fetch('http://localhost:8000/assignments/' + assignment_id);
        if (response.ok){
          const assignment = await response.json();
          //const assistantMessage = `Assignment: ${assignment.title}\nDescription: ${assignment.description}\nDue Date: ${new Date(assignment.due_date).toLocaleDateString()}`;
          //setChatHistory(prevHistory => [...prevHistory, { from: 'assistant', text: assistantMessage }]);
          const assistantMessage = `Assignment: ${assignment.title} \nDue Date: ${new Date(assignment.due_date).toLocaleDateString()}`;
          setChatHistory(prevHistory => [...prevHistory, { from: 'assistant', text: assistantMessage }]);
        }
      }
      
    }
  };
  return (
    <div
      className="d-flex flex-column border rounded p-3 bg-primary bg-opacity-10"
      style={{ width: "320px" }}
    >
      <h4 className="fw-bold">AI Assistant</h4>
      <div className="d-flex flex-column mt-auto">
        <ul>
          {chatHistory.length === 0 ? (
            <li className="text-muted"></li>
          ) : (
            chatHistory.map((msg, index) => (
              <li key={index} className={msg.from === 'user' ? 'text-end' : 'text-start'}>
                <span className={msg.from === 'user' ? 'bg-primary text-white rounded px-2 py-1' : 'bg-light rounded px-2 py-1'}>
                  {msg.text}
                </span>
              </li>
            ))
          )}
        </ul>
        
        <div className="input-group mt-2">
          <form onSubmit={updateLog}>
          <input
            type="text"
            className="form-control"
            placeholder="Ask me anything..."
           
          />
           <button className="btn btn-outline-primary">
                {rightArrow}
                
          </button>
          </form>

          
         
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
