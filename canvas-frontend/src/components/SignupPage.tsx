import React  from "react";
import { useState } from "react";
import { FormEvent } from "react";
function SignupPage(){

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(false);
    const [name, setName] = useState('');
    const [API, setAPI] = useState('')
    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError(false);
    
        try {
            const response = await fetch(`http://localhost:8000/users/`, {
                method: 'POST',
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({
                  email: email,
                  password : password, 
                  name: name, 
                  canvas_token: API 
                  
               
                }),
              });
          if (response.ok) {
            window.location.href = '/dashboard';
          } else {
            setError(true);
          }
        } catch {
          setError(true);
        }
      };
    return     <div className="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div className="card p-4 shadow-sm" style={{ maxWidth: '400px', width: '100%' }}>
      <div className="text-center mb-4">
        <h1 className="h3 mb-2">Canvas Bot</h1>
        <p className="text-muted small">Login to manage your API tokens</p>
      </div>

      <form onSubmit={handleSubmit}>

      <div className="mb-3">
          <label htmlFor="name" className="form-label">Name</label>
          <input
            type="name"
            className="form-control"
            id="name"
            required
            value={name}
            onChange={e => setName(e.target.value)}
          />
        </div>


        <div className="mb-3">
          <label htmlFor="email" className="form-label">Email address</label>
          <input
            type="email"
            className="form-control"
            id="email"
            required
            value={email}
            onChange={e => setEmail(e.target.value)}
          />
        </div>

        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            id="password"
            required
            value={password}
            onChange={e => setPassword(e.target.value)}
          />
        </div>

        <div className="mb-3">
          <label htmlFor="API key" className="form-label">API Key</label>
          <input
            type="password"
            className="form-control"
            id="API"
            required
            value={API}
            onChange={e => setAPI(e.target.value)}
          />
        </div>

       


        <button type="submit" className="btn btn-primary w-100">Login</button>
      </form>


    </div>
  </div>
    
}

export default SignupPage;