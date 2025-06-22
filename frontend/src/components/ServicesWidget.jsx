import { useState } from 'react'

const ServicesWidget = ({ isAgentMode }) => {
  const services = [
    {
      id: 'agent',
      name: 'Agent',
      description: 'Intelligent conversation agent',
      icon: '⚙️',
      status: isAgentMode ? 'active' : 'inactive'
    }
  ]

  return (
    <div className="services-widget">
      <div className="services-widget-header">
        <h3>Services</h3>
      </div>
      
      <div className="services-list">
        {services.map((service) => (
          <div key={service.id} className={`service-item ${isAgentMode ? 'active' : ''}`}>
            <div className="service-icon">
              {service.icon}
            </div>
            <div className="service-info">
              <div className="service-name">{service.name}</div>
              <div className="service-description">{service.description}</div>
            </div>
            <div className={`service-status ${service.status}`}>
              <span className="status-dot"></span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ServicesWidget 