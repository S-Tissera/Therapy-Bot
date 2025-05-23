import React from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import "./Dashboard.css";

function Dashboard() {
  const navigate = useNavigate();

  const handleStartChat = () => {
    navigate("/chat");
  };

  return (
    <div className="dashboard-container">
      <Navbar />
      
      <div className="dashboard-content">
        <h1 className="dashboard-title">Your Mental Health Companion</h1>

        <p className="dashboard-intro">
          A safe space for emotional support, self-care guidance, and personal growth. 
          Available 24/7 with empathetic AI-powered assistance.
        </p>

        <div className="dashboard-divider" />

        <div className="dashboard-grid">
          <div className="feature-card">
            <h3>📊 Mood Tracking</h3>
            <p>Visualize your emotional patterns with our weekly mood chart</p>
          </div>
          
          <div className="feature-card">
            <h3>📝 Journal Prompts</h3>
            <p>Daily guided writing exercises for self-reflection</p>
          </div>

          <div className="feature-card">
            <h3>🧘 Mindfulness</h3>
            <p>Curated meditation sessions & breathing exercises</p>
          </div>

          <div className="feature-card">
            <h3>📚 Resources</h3>
            <p>Personalized reading recommendations and tools</p>
          </div>
        </div>

        <div className="dashboard-section">
          <h2 className="section-title">🌟 Core Features</h2>
          <ul className="features-list">
            <li className="feature-item">🤖 AI-Powered Emotional Analysis</li>
            <li className="feature-item">🌱 Personalized Growth Plans</li>
            <li className="feature-item">🔔 Daily Check-in Reminders</li>
            <li className="feature-item">📈 Progress Tracking Dashboard</li>
            <li className="feature-item">🤝 Peer Support Community Access</li>
          </ul>
        </div>

        <div className="dashboard-section tip-section">
          <h2 className="section-title">💡 Daily Wellness Tip</h2>
          <p className="tip-text">
            "Practice gratitude: Take 2 minutes daily to write down three things you're thankful for. 
            This simple exercise can boost positive thinking by 25% over time."
          </p>
        </div>

        <div className="dashboard-section emergency-section">
          <h2 className="section-title">🚨 Sri Lanka Mental Health Support</h2>
          <p className="emergency-text">
            If you need immediate assistance:
            <br />
            • <strong>National Mental Health Helpline:</strong> 1926 (24/7)
            <br />
            • <strong>Sumithrayo:</strong> 011-2696666 (9 AM - 8 PM)
            <br />
            • <strong>CCCline:</strong> 1333 (7 AM - 11 PM)
            <br />
            • <strong>National Institute of Mental Health:</strong> 011-2756855
            <br />
            • <strong>Police Emergency:</strong> 119
            <br /><br />
            All services are confidential and free of charge.
          </p>
        </div>

        <button 
          className="dashboard-button"
          onClick={handleStartChat}
        >
          🗨️ Start Confidential Chat
        </button>

        <div className="privacy-notice">
          <h3 className="section-title">🔐 Your Security</h3>
          <p>
            All conversations are encrypted. We never share your data. 
            Regular security audits ensure your privacy protection.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;