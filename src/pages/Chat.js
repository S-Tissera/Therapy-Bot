import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import "./Chat.css";

const Chat = () => {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [userId, setUserId] = useState(null);
  const [feedbackTarget, setFeedbackTarget] = useState(null);
  const [feedbackText, setFeedbackText] = useState({
    is_correct: 1,
    corrected_emotion: "",
    comment: "",
  });

  const navigate = useNavigate();

  useEffect(() => {
    const storedUserId = localStorage.getItem("user_id");
    if (storedUserId) {
      setUserId(storedUserId);
    } else {
      alert("No user is logged in. Please login first.");
      navigate("/login");
    }
  }, [navigate]);

  const sendMessage = async () => {
    if (!message.trim() || !userId) return;
    const userMsg = { from: "user", text: message };
    setChatHistory((prev) => [...prev, userMsg]);

    try {
      const res = await axios.post("http://localhost:5000/chat", {
        message,
        user_id: userId,
      });

      const botMsg = {
        from: "bot",
        text: res.data.response,
        emotion_id: res.data.emotion_id,
      };

      setChatHistory((prev) => [...prev, botMsg]);
    } catch (error) {
      alert("Error: " + (error.response?.data?.error || error.message));
    }

    setMessage("");
  };

  const handleFeedbackSubmit = async () => {
    if (feedbackTarget === null) return;

    const botMessageEntry = chatHistory[feedbackTarget];
    if (!botMessageEntry || !botMessageEntry.emotion_id) {
      alert("Emotion ID not found for feedback.");
      return;
    }

    try {
      await axios.post("http://localhost:5000/feedback", {
        user_id: userId,
        emotion_id: botMessageEntry.emotion_id,
        is_correct: feedbackText.is_correct,
        corrected_emotion: feedbackText.corrected_emotion,
        comment: feedbackText.comment,
      });

      alert("Feedback submitted!");
      setFeedbackText({ is_correct: 1, corrected_emotion: "", comment: "" });
      setFeedbackTarget(null);
    } catch (error) {
      alert("Failed to submit feedback.");
    }
  };

  return (
    <div className="chat-page-container">
      <Navbar />
      <div className="chat-container">
        <h2 className="chat-header">Therapy Chat</h2>
        
        <div className="chat-history">
          {chatHistory.map((msg, idx) => (
            <div className="message-container" key={idx}>
              <div className={msg.from === "user" ? "user-message" : "bot-message"}>
                <p className="message-from">{msg.from}:</p>
                <p>{msg.text}</p>
                
                {msg.from === "bot" && (
                  <>
                    <button 
                      className="feedback-button"
                      onClick={() => setFeedbackTarget(idx)}
                    >
                      Give Feedback
                    </button>
                    
                    {feedbackTarget === idx && (
                      <div className="feedback-form">
                        <label className="feedback-label">
                          Was the detected emotion correct?
                        </label>
                        <select
                          className="feedback-select"
                          value={feedbackText.is_correct}
                          onChange={(e) =>
                            setFeedbackText((prev) => ({
                              ...prev,
                              is_correct: e.target.value === "true" ? 1 : 0,
                            }))
                          }
                        >
                          <option value="true">Yes</option>
                          <option value="false">No</option>
                        </select>

                        {feedbackText.is_correct === 0 && (
                          <>
                            <label className="feedback-label">
                              Correct Emotion:
                            </label>
                            <select
                              className="feedback-select"
                              value={feedbackText.corrected_emotion}
                              onChange={(e) =>
                                setFeedbackText((prev) => ({
                                  ...prev,
                                  corrected_emotion: e.target.value,
                                }))
                              }
                            >
                              <option value="">--Select Emotion--</option>
                              <option value="happy">Happy</option>
                              <option value="sad">Sad</option>
                              <option value="angry">Angry</option>
                              <option value="fear">Fear</option>
                              <option value="disgust">Disgust</option>
                              <option value="surprise">Surprise</option>
                              <option value="neutral">Neutral</option>
                            </select>
                          </>
                        )}

                        <label className="feedback-label">
                          Comment:
                        </label>
                        <textarea
                          className="feedback-textarea"
                          value={feedbackText.comment}
                          onChange={(e) =>
                            setFeedbackText((prev) => ({
                              ...prev,
                              comment: e.target.value,
                            }))
                          }
                        />

                        <button 
                          className="submit-feedback-button"
                          onClick={handleFeedbackSubmit}
                        >
                          Submit
                        </button>
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>
          ))}
        </div>

        <div className="input-container">
          <input
            className="chat-input"
            type="text"
            placeholder="Type your message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button className="send-button" onClick={sendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;