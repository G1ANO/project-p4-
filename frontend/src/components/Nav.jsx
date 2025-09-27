import { Link, useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";

export default function Nav() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const checkUser = () => {
      const savedUser = localStorage.getItem("user");
      if (savedUser) {
        setUser(JSON.parse(savedUser));
      } else {
        setUser(null);
      }
    };

    
    checkUser();

    
    const handleLogout = () => {
      setUser(null);
    };

    window.addEventListener('userLogout', handleLogout);

    return () => {
      window.removeEventListener('userLogout', handleLogout);
    };
  }, [location]);

  return (
    <nav className="nav">
      <div className="nav-content">
        {user ? (
          <>
            <div className="nav-user">
              <span className="username">{user.name}</span>
            </div>
            <div className="nav-links">
              <Link to="/plans" className="nav-btn">Plans</Link>
              <Link to="/subscriptions" className="nav-btn">Subscriptions</Link>
            </div>
          </>
        ) : (
          <>
            <h1 className="nav-logo">WiFi Portal</h1>
            <div className="nav-links">
              <Link to="/login" className="nav-btn">Login</Link>
              <Link to="/signup" className="nav-btn">Sign Up</Link>
            </div>
          </>
        )}
      </div>
    </nav>
  );
}
