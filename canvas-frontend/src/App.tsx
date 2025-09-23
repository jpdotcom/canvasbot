import React from "react";
import LoginPage from "./components/LoginPage";
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import SignupPage from "./components/SignupPage";
import Dashboard from "./components/Dashboard";
function App() {
  const routes =(<BrowserRouter>
      <Routes>
      <Route path="/SignUp" element={<SignupPage />} />
      <Route path="dashboard" element={<Dashboard/>} />
    </Routes>

  </BrowserRouter>

  )
    
  return (<> 
    {routes}
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <LoginPage />
    </div>
    </>

  );
}

export default App;
