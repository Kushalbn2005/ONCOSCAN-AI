import React from 'react';
import { Activity, ShieldCheck, Cpu, Info, RefreshCw } from 'lucide-react';

export default function Header({ isConnected, onOpenInfo, onReset }) {
  return (
    <header className="glass-panel" style={{ padding: '16px 28px', marginBottom: '28px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        
        {/* Brand & Title */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '44px',
            height: '44px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%)',
            border: '1px solid var(--border-glow)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 16px rgba(6, 182, 212, 0.25)'
          }}>
            <Activity size={24} color="var(--primary)" />
          </div>

          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <h1 style={{ fontSize: '1.4rem', color: '#fff', margin: 0, fontWeight: 700 }}>
                OncoScan <span style={{ color: 'var(--primary)' }}>AI</span>
              </h1>
              <span style={{
                background: 'rgba(6, 182, 212, 0.12)',
                color: 'var(--primary-light)',
                border: '1px solid rgba(6, 182, 212, 0.3)',
                fontSize: '0.72rem',
                fontWeight: 600,
                padding: '2px 8px',
                borderRadius: '20px',
                textTransform: 'uppercase',
                letterSpacing: '0.05em'
              }}>
                Studio v1.0
              </span>
            </div>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', margin: 0 }}>
              Brain Tumor Classification & Grad-CAM Explainability Neural Engine
            </p>
          </div>
        </div>

        {/* Status Indicators & Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          {/* API Server status */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            padding: '6px 14px',
            borderRadius: '20px',
            background: isConnected ? 'rgba(16, 185, 129, 0.1)' : 'rgba(244, 63, 94, 0.1)',
            border: `1px solid ${isConnected ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)'}`,
            fontSize: '0.8rem',
            fontWeight: 600,
            color: isConnected ? 'var(--status-safe)' : 'var(--status-danger)'
          }}>
            <span className={isConnected ? "pulse-indicator" : ""} style={{
              background: isConnected ? 'var(--status-safe)' : 'var(--status-danger)'
            }} />
            {isConnected ? 'FastAPI Connected' : 'Connecting to Backend...'}
          </div>

          {/* Model Tech Badge */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '6px 14px',
            borderRadius: '20px',
            background: 'rgba(255, 255, 255, 0.04)',
            border: '1px solid var(--border-subtle)',
            fontSize: '0.8rem',
            color: 'var(--text-muted)'
          }}>
            <Cpu size={14} color="var(--accent-purple)" />
            <span>EfficientNetB0</span>
          </div>

          {/* Info Button */}
          <button 
            onClick={onOpenInfo}
            className="btn-secondary" 
            style={{ padding: '8px 14px', fontSize: '0.82rem' }}
            title="Model Architecture & Info"
          >
            <Info size={16} />
            <span>Architecture</span>
          </button>

          {/* Reset Studio */}
          <button 
            onClick={onReset}
            className="btn-secondary" 
            style={{ padding: '8px 12px' }}
            title="Reset MRI Scan"
          >
            <RefreshCw size={16} />
          </button>
        </div>

      </div>
    </header>
  );
}
