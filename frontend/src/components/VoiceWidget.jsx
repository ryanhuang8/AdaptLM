import React from 'react';

const VoiceWidget = ({ isVapiActive }) => {
  return (
    <div className="services-widget">
      <div className="services-widget-header">
        <h3>Voice</h3>
      </div>
      <div className="services-list">
        <div className={`service-item ${isVapiActive ? 'active' : ''}`}>
          <div className="service-icon">
            <span>🎤</span>
          </div>
          <div className="service-info">
            <div className="service-name">Vapi</div>
            <div className="service-description">Voice AI</div>
          </div>
          {isVapiActive && (
            <div className="service-status active">
              <span className="status-dot"></span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VoiceWidget; 