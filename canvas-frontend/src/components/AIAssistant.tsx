import React from "react";

function AIAssistant(){
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
            <i className="bi bi-arrow-right"></i>
                Enter
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
