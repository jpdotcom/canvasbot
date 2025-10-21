import React from "react";
import LoginPage from "./components/LoginPage";
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import SignupPage from "./components/SignupPage";
import Dashboard from "./components/Dashboard";
import AssignmentView from "./components/AssignmentView";
function App() {
 
  
  const routes =(<BrowserRouter>
      <Routes>
      <Route path="/" element={<LoginPage />}/>
      <Route path="/assignment" element={<AssignmentView/>}/>
      <Route path="/SignUp" element={<SignupPage />} />
      <Route path="/dashboard" element={<Dashboard  />} />
    </Routes>

  </BrowserRouter>

  )
    
  return (<> 
    {routes}

    </>

  );
}

export default App;

