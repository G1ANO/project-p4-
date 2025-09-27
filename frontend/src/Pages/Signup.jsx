import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

export default function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [confirmError, setConfirmError] = useState("");
  const navigate = useNavigate();

  
  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.(com|me|co\.ke|org|net|edu|gov|mil|int|info|biz|name|pro|aero|coop|museum)$/i;
    return emailRegex.test(email);
  };

  
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

    
    if (confirm && value !== confirm) {
      setConfirmError("Passwords do not match");
    } else if (confirm) {
      setConfirmError("");
    }
  };

  const handleConfirmChange = (e) => {
    const value = e.target.value;
    setConfirm(value);

    if (value && password !== value) {
      setConfirmError("Passwords do not match");
    } else {
      setConfirmError("");
    }
  };

  
  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) navigate("/plans");
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!username || !email || !password || !confirm) {
      setError("Please fill out all required fields.");
      return;
    }

    
    if (!validateEmail(email)) {
      setError("Please enter a valid email address");
      return;
    }

    
    const passwordValidationError = validatePassword(password);
    if (passwordValidationError) {
      setError(passwordValidationError);
      return;
    }

    if (password !== confirm) {
      setError("Passwords do not match.");
      return;
    }

    try {
      const res = await axios.post("http:
        name: username,
        email,
        password,
      });
      
      localStorage.setItem("user", JSON.stringify(res.data.user));
      navigate("/plans");
    } catch (err) {
      const msg = err.response?.data?.error || "Signup failed — try again.";
      setError(msg);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <h1>Sign Up</h1>
          <p>Create your account to access WiFi plans</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit} noValidate>
          <div className="input-group">
            <input
              id="username"
              name="username"
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoComplete="username"
            />
          </div>

          <div className="input-group">
            <input
              id="email"
              name="email"
              type="email"
              placeholder="Enter your email (e.g., user@example.com)"
              value={email}
              onChange={handleEmailChange}
              required
              autoComplete="email"
              className={emailError ? "input-error" : ""}
            />
            {emailError && <div className="validation-error">{emailError}</div>}
          </div>

          <div className="input-group">
            <input
              id="password"
              name="password"
              type="password"
              placeholder="Password (max 10 chars, A-z, 0-9 or special)"
              value={password}
              onChange={handlePasswordChange}
              required
              maxLength="10"
              autoComplete="new-password"
              className={passwordError ? "input-error" : ""}
            />
            {passwordError && <div className="validation-error">{passwordError}</div>}
          </div>

          <div className="input-group">
            <input
              id="confirm"
              name="confirm"
              type="password"
              placeholder="Confirm your password"
              value={confirm}
              onChange={handleConfirmChange}
              required
              maxLength="10"
              autoComplete="new-password"
              className={confirmError ? "input-error" : ""}
            />
            {confirmError && <div className="validation-error">{confirmError}</div>}
          </div>

          {error && <p className="error">{error}</p>}

          <button
            type="submit"
            disabled={emailError || passwordError || confirmError || !username || !email || !password || !confirm}
            className={emailError || passwordError || confirmError || !username || !email || !password || !confirm ? "button-disabled" : ""}
          >
            Create Account
          </button>
        </form>

        <p className="auth-footer">
          Already have an account?{" "}
          <a href="/login" className="auth-link">
            Sign in here
          </a>
        </p>
      </div>
    </div>
  );
}
