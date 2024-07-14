import React, { useState, useEffect, useRef } from "react";
import "./ChatWindow.css";
import { getAIMessage } from "../api/api";
import { marked } from "marked";

function ChatWindow() {
  const defaultMessage = [{
    role: "assistant",
    content: "Hi, how can I help you today?"
  }];

  const suggestedQuestions = [
    "What are common refrigerator problems?",
    "How do I replace a dishwasher pump?",
    "What's the lifespan of a washing machine?"
  ];

  const [messages, setMessages] = useState(defaultMessage);
  const [input, setInput] = useState("");

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (messageToSend) => {
    if (messageToSend.trim() !== "") {
      // Set user message
      setMessages(prevMessages => [...prevMessages, { role: "user", content: messageToSend }]);
      setInput("");

      // Call API & set assistant message
      const newMessage = await getAIMessage(messageToSend);
      setMessages(prevMessages => [...prevMessages, newMessage]);
    }
  };

  const handleSuggestedQuestion = (question) => {
    setInput(question);
    handleSend(question);
  };

  return (
    <div className="chat-container">
      <div className="messages-container">
        {messages.map((message, index) => (
          <div key={index} className={"${message.role}-message-container"}>
            {message.content && (
              <div className={"message ${message.role}-message"}>
                <div dangerouslySetInnerHTML={{__html: marked(message.content).replace(/<p>|<\/p>/g, "")}}></div>
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-container">
        <div className="suggested-questions">
          {suggestedQuestions.map((question, index) => (
            <button 
              key={index} 
              className="suggested-question-button"
              onClick={() => handleSuggestedQuestion(question)}
            >
              {question}
            </button>
          ))}
        </div>
        <div className="input-area">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            onKeyPress={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend(input);
              }
            }}
          />
          <button className="send-button" onClick={() => handleSend(input)}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;