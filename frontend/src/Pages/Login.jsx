import React from "react";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { API_ENDPOINTS } from "../config";

const validationSchema = Yup.object({
  email: Yup.string()
    .email("Email must be in format 'example@domain.com'")
    .matches(
      /^[^\s@]+@[^\s@]+\.(com|me|co\.ke|org|net|edu|gov|mil|int|info|biz|name|pro|aero|coop|museum)$/i,
      "Email must have a valid domain (.com, .me, .co.ke, etc.)"
    )
    .required("Email is required"),
  password: Yup.string()
    .max(10, "Password must not exceed 10 characters")
    .matches(/[A-Z]/, "Password must include at least one uppercase letter")
    .matches(/[a-z]/, "Password must include at least one lowercase letter")
    .matches(/[\d!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/, "Password must include at least one number or special character")
    .required("Password is required")
});

function Login() {
  const navigate = useNavigate();

  const handleSubmit = async (values, { setSubmitting, setStatus }) => {
    try {
      const response = await fetch(API_ENDPOINTS.LOGIN, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
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
      setStatus(err.message);
    } finally {
      setSubmitting(false);
    }
  };



  return (
    <div className="login-page">
      <div className="company-branding">
        <h1 className="company-name">M-NET INTERNET SOLUTIONS</h1>
        <p className="company-tagline">Diversified global connection.</p>
        <div className="company-contact">
          <p>PO BOX 24-90102</p>
          <p>2025mnetcare@proton.me</p>
        </div>
      </div>

      <div className="login-container">
        <div className="login-header">
          <h2>Sign In</h2>
          <p>Enter your credentials to access your WiFi plans</p>
        </div>

        <Formik
          initialValues={{ email: "", password: "" }}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting, status, errors, touched }) => (
            <Form className="auth-form">
              <div className="input-group">
                <Field
                  type="email"
                  name="email"
                  placeholder="Enter your email (e.g., user@example.com)"
                  className={errors.email && touched.email ? "input-error" : ""}
                />
                <ErrorMessage name="email" component="p" className="validation-error" />
              </div>

              <div className="input-group">
                <Field
                  type="password"
                  name="password"
                  placeholder="Enter your password (max 10 chars, A-z, 0-9 or special)"
                  className={errors.password && touched.password ? "input-error" : ""}
                />
                <ErrorMessage name="password" component="p" className="validation-error" />
              </div>

              {status && <p className="error">{status}</p>}

              <button type="submit" disabled={isSubmitting} className="auth-button">
                {isSubmitting ? "Signing In..." : "Sign In"}
              </button>
            </Form>
          )}
        </Formik>

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
