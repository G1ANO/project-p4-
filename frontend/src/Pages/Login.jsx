import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error("Invalid email or password");
        } else {
          throw new Error("Login failed. Please try again.");
        }
      }

      const data = await response.json();
      localStorage.setItem("user", JSON.stringify(data));

      // Redirect to the user-specific dashboard
      navigate(`/dashboard/${data.id}`);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="home-login">
      <header className="home-header">
        <h1>Welcome to SubTrackr</h1>
        <p>
          Your one-stop solution for managing subscriptions. Manage your
          subscriptions in one place. Track your active bundles, never miss a
          renewal, and stay in control of your spending.
        </p>
        <ul>
          <li>Sign up for an account</li>
          <li>Browse and subscribe to plans</li>
          <li>Manage and track your subscriptions</li>
        </ul>
        <p>Get started today! 🥳</p>
      </header>

      <div className="auth-box">
        <h2>Login</h2>
        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {error && <p className="error">{error}</p>}

          <button type="submit">Login</button>
        </form>
      </div>

      <footer className="home-footer">
        <p>
          Don’t have an account? <a href="/signup">Sign up here</a>
        </p>

        <p>Contacts</p>
        <p>Email: support@subtrackr.com</p>
        <p>Phone: +2547012345678</p>
        <p>Address: 123 Subscription St, Suite 100, Cityville, Country</p>
        <p>&copy; 2024 SubTrackr. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default Login;
