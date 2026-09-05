import React from 'react';
import { X, Cpu, Database, CheckCircle2, Shield, Brain } from 'lucide-react';

export default function ModelInfoModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(7, 10, 18, 0.85)',
      backdropFilter: 'blur(10px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '20px'
    }}>
      <div className="glass-panel animate-fade-in" style={{
        maxWidth: '620px',
        width: '100%',
        padding: '28px',
        borderRadius: 'var(--radius-lg)',
        border: '1px solid var(--border-glow)',
        position: 'relative',
        maxHeight: '90vh',
        overflowY: 'auto'
      }}>
        {/* Close Button */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'rgba(255, 255, 255, 0.05)',
            border: 'none',
            color: 'var(--text-muted)',
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <X size={18} />
        </button>

        {/* Title */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: 'rgba(139, 92, 246, 0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--accent-purple)'
          }}>
            <Brain size={22} />
          </div>
          <div>
            <h2 style={{ fontSize: '1.25rem', color: '#fff', margin: 0 }}>
              OncoScan AI Engine Specifications
            </h2>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', margin: 0 }}>
              Deep Convolutional Neural Network Architecture & Explainability Matrix
            </p>
          </div>
        </div>

        {/* Specs Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '24px' }}>
          
          <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px', color: 'var(--primary-light)' }}>
              <Cpu size={18} />
              <span style={{ fontWeight: 700, fontSize: '0.85rem' }}>Backbone Architecture</span>
            </div>
            <p style={{ fontSize: '0.8rem', color: '#fff', fontWeight: 600 }}>EfficientNetB0</p>
            <span style={{ fontSize: '0.74rem', color: 'var(--text-dim)' }}>Transfer Learning fine-tuned on contrast MRI slices</span>
          </div>

          <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px', color: 'var(--status-safe)' }}>
              <CheckCircle2 size={18} />
              <span style={{ fontWeight: 700, fontSize: '0.85rem' }}>Validation Accuracy</span>
            </div>
            <p style={{ fontSize: '0.8rem', color: '#fff', fontWeight: 600 }}>98.4% Accuracy</p>
            <span style={{ fontSize: '0.74rem', color: 'var(--text-dim)' }}>Evaluated across 1,600 unseen test MRI scans</span>
          </div>

        </div>

        {/* Dataset Breakdown */}
        <div style={{ marginBottom: '24px' }}>
          <h3 style={{ fontSize: '0.95rem', color: '#fff', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Database size={16} color="var(--primary)" />
            Dataset & Multi-Class Taxonomy
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '8px', textAlign: 'center' }}>
            {[
              { name: 'Glioma', count: '1,800 scans' },
              { name: 'Meningioma', count: '1,800 scans' },
              { name: 'Pituitary', count: '1,800 scans' },
              { name: 'No Tumor', count: '1,800 scans' }
            ].map((cls, i) => (
              <div key={i} style={{ background: 'rgba(255, 255, 255, 0.04)', padding: '10px 6px', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.06)' }}>
                <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#fff', display: 'block' }}>{cls.name}</span>
                <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)' }}>{cls.count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Grad-CAM Explainability Section */}
        <div style={{ background: 'rgba(6, 182, 212, 0.06)', border: '1px solid var(--border-glow)', padding: '18px', borderRadius: '12px' }}>
          <h4 style={{ fontSize: '0.88rem', color: 'var(--primary-light)', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Shield size={16} /> Gradient-Weighted Class Activation Mapping (Grad-CAM)
          </h4>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: '1.5' }}>
            Grad-CAM computes the gradients of the target class score with respect to the final convolutional feature maps in EfficientNetB0.
            This generates a high-resolution visual heatmap indicating exact spatial anatomical regions guiding the AI decision.
          </p>
        </div>

      </div>
    </div>
  );
}
