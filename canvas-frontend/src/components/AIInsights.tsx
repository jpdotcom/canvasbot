import React, { useEffect } from "react";
import { useState } from "react";
import { API_URL } from "../config";
function AIInsights(){

  
  const getInsight = async ()=>{
    const response = await fetch(`${API_URL}/llm/get_workload/`+localStorage.getItem("user_id"))
    
    if (response.ok){
      const insight = await response.json();
      return insight
    }

    
  }

  const [insight,setInsights] = useState("");


  useEffect(()=>{
    const fetchInsights=async () =>{
      try{
        const value = await getInsight()
        setInsights(value);
      }
      catch(error){
        console.error("Error fetching: ", error);
        setInsights("Failed To Get Insights");
      }
    }
    fetchInsights();
    
  },[])
  return (
    <div className="border rounded p-3 bg-primary bg-opacity-10">
      <h5 className="fw-bold">AI Insights</h5>
      <p className="text-muted mb-0" style={{ whiteSpace: 'pre-wrap' }}>
        {insight}
      </p>
    </div>
  );
};

export default AIInsights;
