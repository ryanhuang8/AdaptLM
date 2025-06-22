import React from 'react';

const VoiceWidget = ({ isVapiActive }) => {
  return (
    <div className="voice-widget">
      <div className="voice-widget-header">
        <h3>Voice</h3>
      </div>
      <div className="llm-models-list">
        <div className={`llm-model-item ${isVapiActive ? 'active' : ''}`}>
          <div 
            className="llm-logo" 
            style={{ 
              backgroundColor: '#c175ff', 
              opacity: isVapiActive ? 1 : 0.6 
            }}
          >
            <span>🎤</span>
          </div>
          <div className="llm-info">
            <div className="llm-name">Vapi</div>
            <div className="llm-provider">Voice AI</div>
          </div>
          {isVapiActive && (
            <div className="llm-status">
              <span className="status-dot"></span>
              <span className="status-text">Active</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VoiceWidget; 