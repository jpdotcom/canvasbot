import React from "react";
import { useState } from "react";
import { FormEvent } from "react";
import { Navigate, useNavigate } from "react-router-dom";

interface Props {
  name: string;
  setName: React.Dispatch<React.SetStateAction<string>>;
}

function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);
  const [name, setName] = useState("");
  const [API, setAPI] = useState('');
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const navigate = useNavigate();

  const handleSignup = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(false);
    if (isSubmitting) return; // Prevent multiple submissions
    setIsSubmitting(true);

    try {
      const response = await fetch('http://localhost:8000/users/', {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
          name: name,
          canvas_token: API
        }),
      });

      if (response.ok) {
        const userData = await response.json();
        //Check if user isn't None 
        if (userData != null) {
          const response2 = await fetch('http://localhost:8000/assignments/sync/' + userData.id, {
            method: 'POST',
            headers: {
              "Content-Type": "application/json",
            },
          });
        }
        localStorage.setItem("user_email", userData.email);
        localStorage.setItem("name", userData.name);
        setName(userData.name);
        navigate('/dashboard');
      } else {
        setError(true);
      }
    } catch (error) {
      console.error("Error during signup:", error);
    } finally {
      setIsSubmitting(false); // Re-enable the button after the request completes
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center min-vh-100 bg-light">
      <div className="card p-4 shadow-sm" style={{ maxWidth: '400px', width: '100%' }}>
        <div className="text-center mb-4">
          <h1 className="h3 mb-2">Canvas Bot</h1>
          <p className="text-muted small">Login to manage your API tokens</p>
        </div>

        <form onSubmit={handleSignup}>
  <div className="mb-3">
    <label htmlFor="name" className="form-label">Name</label>
    <input
      type="text"
      className="form-control"
      id="name"
      required
      value={name}
      onChange={(e) => setName(e.target.value)}
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
      onChange={(e) => setEmail(e.target.value)}
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
      onChange={(e) => setPassword(e.target.value)}
    />
  </div>

  <div className="mb-3">
    <label htmlFor="API" className="form-label">API Key</label>
    <input
      type="password"
      className="form-control"
      id="API"
      required
      value={API}
      onChange={(e) => setAPI(e.target.value)}
    />
  </div>

  {/* Display error message if user already exists */}
  {error && (
    <div className="alert alert-danger" role="alert">
      A user with this email already exists. Please try logging in.
    </div>
  )}

  <button
    className="btn btn-primary"
    type="submit"
    disabled={isSubmitting} // Disable the button while submitting
  >
    {isSubmitting ? "Signing Up..." : "Sign Up"}
  </button>
</form>
      </div>
    </div>
  );
}

export default SignupPage;