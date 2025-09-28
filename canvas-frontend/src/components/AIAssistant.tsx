import React from "react";

function AIAssistant(){
    const rightArrow=(<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-arrow-right" viewBox="0 0 16 16">
    <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
  </svg>)
  return (
    <div
      className="d-flex flex-column border rounded p-3 bg-primary bg-opacity-10"
      style={{ width: "320px" }}
    >
      <h4 className="fw-bold">AI Assistant</h4>
      <div className="d-flex flex-column mt-auto">
        <div className="align-self-end bg-primary text-white p-2 rounded mb-2">
          Can you summarize the main points for the Case Study Analysis?
        </div>
        <div className="align-self-start bg-light p-2 rounded mb-2">
          <small className="text-dark">
            Certainly. The main points are to identify key ethical dilemmas,
            analyze stakeholder perspectives, and propose a solution based on
            ethical frameworks.
          </small>
        </div>
        <div className="input-group mt-2">
          <input
            type="text"
            className="form-control"
            placeholder="Ask me anything..."
          />
          <button className="btn btn-outline-primary">
                {rightArrow}
                
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
