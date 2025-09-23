import React from "react";

function Header(){
  return (
    <header className="d-flex justify-content-between align-items-center border-bottom px-4 py-3 bg-white shadow-sm">
      <div className="d-flex align-items-center text-primary gap-2">
        <svg width="32" height="32" fill="currentColor" viewBox="0 0 48 48">
          <path d="M42.4379 44C42.4379 44 36.0744 33.9038 41.1692 24C46.8624 12.9336 42.2078 4 42.2078 4L7.01134 4C7.01134 4 11.6577 12.932 5.96912 23.9969C0.876273 33.9029 7.27094 44 7.27094 44L42.4379 44Z" />
        </svg>
        <h2 className="h5 fw-bold mb-0">Canvas Bot</h2>
      </div>
      <div
        className="rounded-circle"
        style={{
          width: "40px",
          height: "40px",
          backgroundImage:
            "url('https://lh3.googleusercontent.com/aida-public/AB6AXuBwS0VKSsvMyBJF2rTySBXO58hvX0Bfn8Ek3NhY0mQ1JFfEOgWRL6xbSyieKxA11gRfcopqZjsQdF-qsxpJSPCZtqQT_TTixVMotWwlzLzAVwRrejqdYfathMcp1QssekFyBVrUOflFmFHVcAevXWajXxt6NPGEDreIXuvD31wUxU24o6YoOQYznDF7ixUFWsKKuLU9ELRpH-LJvWRZe2LnNXaQkLPTTpwi9ww6WNLrET_o-KDRlgvTQnvjRX6b_-3RcQVGk0osW58')",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      />
    </header>
  );
};

export default Header;
