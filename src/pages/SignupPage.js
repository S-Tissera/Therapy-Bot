import React, { useState } from "react";
import axios from "axios";
import Logo from '../Logo.png';
import "../styles/LoginPage.css"; 

const SignupPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/signup", {
        username,
        password
      });
      setMessage("Signup successful!");
    } catch (err) {
      if (err.response?.status === 409) {
        setMessage("Username already exists.");
      } else {
        setMessage("Signup failed.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-logo-container">
        <img 
          src={Logo} 
          alt="Company Logo" 
          className="login-logo"
        />
      </div>
      
      <form className="login-form" onSubmit={handleSignup}>
        <h2 className="login-title">Create Account</h2>
        <p className="welcome-message">Please register to continue</p>

        <input
          className="login-input"
          placeholder="Username"
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          className="login-input"
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button 
          className="login-button" 
          type="submit"
          disabled={loading}
        >
          {loading ? "Creating Account..." : "Sign Up"}
        </button>

        <div className="signup-link">
          Already have an account? <a href="/login">Log in</a>
        </div>
        
        {message && (
          <p className="auth-message" style={{ 
            color: message.includes("successful") ? "#48bb78" : "#f56565",
            textAlign: "center",
            marginTop: "1rem"
          }}>
            {message}
          </p>
        )}
      </form>
    </div>
  );
};

export default SignupPage;