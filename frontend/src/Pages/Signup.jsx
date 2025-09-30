import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { API_ENDPOINTS } from "../config";

const validationSchema = Yup.object({
  username: Yup.string()
    .min(3, "Username must be at least 3 characters")
    .max(20, "Username must not exceed 20 characters")
    .required("Username is required"),
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
    .required("Password is required"),
  confirm: Yup.string()
    .oneOf([Yup.ref('password'), null], "Passwords must match")
    .required("Confirm password is required")
});

export default function Signup() {
  const navigate = useNavigate();

  const handleSubmit = async (values, { setSubmitting, setStatus }) => {
    try {
      const response = await fetch(API_ENDPOINTS.REGISTER, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: values.username,
          email: values.email,
          password: values.password
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Registration failed");
      }

      const data = await response.json();
      console.log("Registration successful:", data);
      navigate("/login");
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
          <h2>Sign Up</h2>
          <p>Create your account to access WiFi plans</p>
        </div>

        <Formik
          initialValues={{ username: "", email: "", password: "", confirm: "" }}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting, status, errors, touched }) => (
            <Form className="auth-form">
              <div className="input-group">
                <Field
                  type="text"
                  name="username"
                  placeholder="Enter your username"
                  className={errors.username && touched.username ? "input-error" : ""}
                />
                <ErrorMessage name="username" component="div" className="validation-error" />
              </div>

              <div className="input-group">
                <Field
                  type="email"
                  name="email"
                  placeholder="Enter your email (e.g., user@example.com)"
                  className={errors.email && touched.email ? "input-error" : ""}
                />
                <ErrorMessage name="email" component="div" className="validation-error" />
              </div>

              <div className="input-group">
                <Field
                  type="password"
                  name="password"
                  placeholder="Password (max 10 chars, A-z, 0-9 or special)"
                  className={errors.password && touched.password ? "input-error" : ""}
                />
                <ErrorMessage name="password" component="div" className="validation-error" />
              </div>

              <div className="input-group">
                <Field
                  type="password"
                  name="confirm"
                  placeholder="Confirm your password"
                  className={errors.confirm && touched.confirm ? "input-error" : ""}
                />
                <ErrorMessage name="confirm" component="div" className="validation-error" />
              </div>

              {status && <p className="error">{status}</p>}

              <button type="submit" disabled={isSubmitting} className="auth-button">
                {isSubmitting ? "Creating Account..." : "Create Account"}
              </button>
            </Form>
          )}
        </Formik>

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
