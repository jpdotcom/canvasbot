// components/LoginPage.tsx
import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
interface Props{
    name: string;
    setName: React.Dispatch<React.SetStateAction<string>>;
}
export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const PORT=8000
  const navigate = useNavigate();
  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(false);
    if (isSubmitting) return; // Prevent multiple submissions
    setIsSubmitting(true);
    //print to console to debug 
    console.log("Testing");
    try {
        const response = await fetch(`http://localhost:8000/users/validate`, {
            method: 'POST',
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: email,
              password: password,
           
            }),
          });
        console.log(response.ok);
      if (response.ok) {
       setEmail("")
       setPassword("");
       const userData = await response.json();
       localStorage.setItem("access_token", userData.access_token);
       console.log(userData.access_token)
       localStorage.setItem("name", userData.name);
       localStorage.setItem("user_email", userData.email);
       localStorage.setItem("user_id", userData.id);
       //Sync assignments
        const response1 = await fetch('http://localhost:8000/assignments/sync', {
          method: 'POST',
          headers: {
            "Authorization": `Bearer ${userData.access_token}`,
            "Content-Type": "application/json",
          },
        }); 
        //fetch assignments
        const response2 = await fetch('http://localhost:8000/assignments/all',{
          headers: {
            "Authorization": `Bearer ${userData.access_token}`,
            
          },
        } );
     
        //need local storage for assignments
        const assignments = await response2.json();
      
        localStorage.setItem("assignments", JSON.stringify(assignments));
       


       navigate('/dashboard');
      } else {
        setError(true);
      }
    } catch {
      setError(true);
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center min-vh-100 bg-light">
      <div className="card p-4 shadow-sm" style={{ maxWidth: '400px', width: '100%' }}>
        <div className="text-center mb-4">
          <h1 className="h3 mb-2">Canvas Bot</h1>
          <p className="text-muted small">Login to manage your API tokens</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">Email address</label>
            <input
              type="email"
              className="form-control"
              id="email"
              required
              value = {email}
         
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

         

          {error && (
            <div className="alert alert-danger py-2" role="alert">
              Invalid credentials. Please try again.
            </div>
          )}

          {!isSubmitting && <button type="submit" className="btn btn-primary w-100" disabled={isSubmitting}>Login</button>}
          {isSubmitting && <button type="submit" className="btn btn-primary w-100" disabled={isSubmitting}>Logging in</button>}
        </form>

        <div className="text-center mt-3">
          <a href="#" className="text-primary" onClick={() => {window.location.href="/SignUp"}}>Don't have an account? Sign up</a>
        </div>
      </div>
    </div>
  );
}
