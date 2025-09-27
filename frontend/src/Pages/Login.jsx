import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const navigate = useNavigate();

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.(com|me|co\.ke|org|net|edu|gov|mil|int|info|biz|name|pro|aero|coop|museum)$/i;
    return emailRegex.test(email);
  };

  const validatePassword = (password) => {
  const validatePassword = (password) => {
    if (password.length > 10) {
      return "Password must not exceed 10 characters";
    }

    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);

    if (!hasUppercase) {
      return "Password must include at least one uppercase letter";
    }
    if (!hasLowercase) {
      return "Password must include at least one lowercase letter";
    }
    if (!hasNumber && !hasSpecialChar) {
      return "Password must include at least one number or special character";
    }

    return "";
  };

  const handleEmailChange = (e) => {
    const value = e.target.value;
    setEmail(value);

    if (value && !validateEmail(value)) {
      setEmailError("Email must be in format 'example@domain.com' with valid domain (.com, .me, .co.ke, etc.)");
    } else {
      setEmailError("");
    }
  };

  const handlePasswordChange = (e) => {
    const value = e.target.value;
    setPassword(value);

    if (value) {
      const passwordValidationError = validatePassword(value);
      setPasswordError(passwordValidationError);
    } else {
      setPasswordError("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!validateEmail(email)) {
      setError("Please enter a valid email address");
      return;
    }

    const passwordValidationError = validatePassword(password);
    if (passwordValidationError) {
      setError(passwordValidationError);
      return;
    }

    try {
      const response = await fetch("http:
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

      
      if (!data.id) {
        throw new Error("Login response missing user ID");
      }

     
      localStorage.setItem("user", JSON.stringify(data));

      
      navigate("/plans");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <h1>Sign In</h1>
          <p>Enter your credentials to access your WiFi plans</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="input-group">
            <input
              type="email"
              placeholder="Enter your email (e.g., user@example.com)"
              value={email}
              onChange={handleEmailChange}
              required
              className={emailError ? "input-error" : ""}
            />
            {emailError && <p className="validation-error">{emailError}</p>}
          </div>

          <div className="input-group">
            <input
              type="password"
              placeholder="Enter your password (max 10 chars, A-z, 0-9 or special)"
              value={password}
              onChange={handlePasswordChange}
              required
              maxLength="10"
              className={passwordError ? "input-error" : ""}
            />
            {passwordError && <p className="validation-error">{passwordError}</p>}
          </div>

          {error && <p className="error">{error}</p>}

          <button
            type="submit"
            disabled={emailError || passwordError || !email || !password}
            className={emailError || passwordError || !email || !password ? "button-disabled" : ""}
          >
            Login
          </button>
        </form>

        <p className="auth-footer">
          Don’t have an account?{" "}
          <a href="/signup" className="auth-link">
            Sign up here
          </a>
        </p>
      </div>
    </div>
  );
}

export default Login;
