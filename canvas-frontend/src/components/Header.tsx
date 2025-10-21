// components/Header.tsx
import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Header() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();
  
  // Get user info from localStorage
  const userName = localStorage.getItem("name") || "User";
  const userEmail = localStorage.getItem("user_email") || "";
  
  // Get initials for profile picture
  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = () => {
    // Clear all localStorage data
    localStorage.removeItem("access_token");
    localStorage.removeItem("name");
    localStorage.removeItem("user_email");
    localStorage.removeItem("user_id");
    localStorage.removeItem("assignments");
    
    // Redirect to login page
    navigate('/');
  };
  const goHome = () => {
    navigate('/dashboard')
  }
  return (
    <header className="bg-white shadow-sm">
      <div className="container-fluid">
        <div className="d-flex align-items-center justify-content-between py-3 px-4">
          <div className="d-flex align-items-center gap-3" onClick={goHome} style={{cursor:'pointer'}}>
            <h1 className="h4 mb-0 fw-bold text-primary">Canvas Bot</h1>
          </div>

          {/* Profile Dropdown */}
          <div className="position-relative" ref={dropdownRef}>
            <button
              className="btn btn-link p-0 border-0"
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              style={{ textDecoration: 'none' }}
              aria-label="User menu"
            >
              <div
                className="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center"
                style={{
                  width: '40px',
                  height: '40px',
                  fontSize: '16px',
                  fontWeight: '600',
                  cursor: 'pointer'
                }}
              >
                {getInitials(userName)}
              </div>
            </button>

            {/* Dropdown Menu */}
            {isDropdownOpen && (
              <div
                className="position-absolute end-0 mt-2 bg-white rounded shadow"
                style={{
                  minWidth: '220px',
                  zIndex: 1000,
                  border: '1px solid #dee2e6'
                }}
              >
                {/* User Info Section */}
                <div className="p-3 border-bottom">
                  <div className="fw-semibold text-dark">{userName}</div>
                  <div className="text-muted small">{userEmail}</div>
                </div>

                {/* Logout Button */}
                <div className="p-2">
                  <button
                    className="btn btn-link text-danger w-100 text-start text-decoration-none d-flex align-items-center gap-2"
                    onClick={handleLogout}
                  >
                    <svg 
                      xmlns="http://www.w3.org/2000/svg" 
                      width="16" 
                      height="16" 
                      fill="currentColor" 
                      viewBox="0 0 16 16"
                    >
                      <path fillRule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0v2z"/>
                      <path fillRule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3z"/>
                    </svg>
                    Logout
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}