import { useState, useEffect } from 'react'

const LLMModelWidget = ({ currentLLM }) => {
  // LLM configurations with logos and display names
  const llmConfigs = {
    gpt: {
      name: 'GPT-4',
      provider: 'OpenAI',
      logo: '🤖',
      color: '#10a37f'
    },
    gemini: {
      name: 'Gemini',
      provider: 'Google',
      logo: '🔷',
      color: '#4285f4'
    },
    claude: {
      name: 'Claude',
      provider: 'Anthropic',
      logo: '🧠',
      color: '#d97706'
    },
    hume: {
      name: 'Hume',
      provider: 'Hume AI',
      logo: '🎭',
      color: '#7c3aed'
    }
  }

  return (
    <div className="llm-widget">
      <div className="llm-widget-header">
        <h3>LLM Models</h3>
      </div>
      <div className="llm-models-list">
        {Object.entries(llmConfigs).map(([key, config]) => (
          <div 
            key={key}
            className={`llm-model-item ${currentLLM === key ? 'active' : ''}`}
          >
            <div 
              className="llm-logo"
              style={{ 
                backgroundColor: currentLLM === key ? config.color : '#4a4b53',
                opacity: currentLLM === key ? 1 : 0.6
              }}
            >
              {config.logo}
            </div>
            <div className="llm-info">
              <div className="llm-name">{config.name}</div>
              <div className="llm-provider">{config.provider}</div>
            </div>
            {currentLLM === key && (
              <div className="llm-status">
                <span className="status-dot"></span>
                <span className="status-text">Active</span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default LLMModelWidget 