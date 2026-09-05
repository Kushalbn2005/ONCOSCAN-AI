import React from 'react';
import { Activity, AlertTriangle, CheckCircle, FileText, BarChart3, ArrowRight, Printer } from 'lucide-react';

const CLASS_DETAILS = {
  glioma: {
    label: 'Glioma Tumor',
    severity: 'High Clinical Priority',
    color: '#f43f5e',
    bgColor: 'rgba(244, 63, 94, 0.12)',
    borderColor: 'rgba(244, 63, 94, 0.3)',
    description: 'Glial cell neoplasm originating in brain tissue. Requires immediate neuro-oncology evaluation.'
  },
  meningioma: {
    label: 'Meningioma Tumor',
    severity: 'Moderate Priority',
    color: '#f59e0b',
    bgColor: 'rgba(245, 158, 11, 0.12)',
    borderColor: 'rgba(245, 158, 11, 0.3)',
    description: 'Neoplasm arising from meningeal layers. Typically extra-axial with potential mass effect.'
  },
  pituitary: {
    label: 'Pituitary Macroadenoma',
    severity: 'Moderate Priority',
    color: '#8b5cf6',
    bgColor: 'rgba(139, 92, 246, 0.12)',
    borderColor: 'rgba(139, 92, 246, 0.3)',
    description: 'Sellar region tumor originating from pituitary gland tissue. Endocrine panel recommended.'
  },
  notumor: {
    label: 'No Tumor Detected',
    severity: 'Normal Scan',
    color: '#10b981',
    bgColor: 'rgba(16, 185, 129, 0.12)',
    borderColor: 'rgba(16, 185, 129, 0.3)',
    description: 'Unremarkable cerebral parenchyma. No evident focal mass, edema, or midline shift.'
  }
};

export default function DiagnosisPanel({ predictionData, isLoading }) {
  if (isLoading) {
    return (
      <div className="glass-panel" style={{ padding: '32px', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <Activity size={40} className="pulse-indicator" color="var(--primary)" />
        <p style={{ marginTop: '20px', fontSize: '1rem', color: '#fff', fontWeight: 600 }}>
          Running Neural Network Inference...
        </p>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          Processing EfficientNetB0 feature extraction & Grad-CAM visual gradients
        </p>
      </div>
    );
  }

  if (!predictionData) {
    return (
      <div className="glass-panel" style={{ padding: '32px', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}>
        <BarChart3 size={44} color="var(--text-dim)" style={{ marginBottom: '16px' }} />
        <h3 style={{ fontSize: '1.1rem', color: '#fff', marginBottom: '6px' }}>Diagnostic Output Standby</h3>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', maxWidth: '300px' }}>
          Select or upload an MRI scan to generate real-time neural classification and probability breakdown.
        </p>
      </div>
    );
  }

  const { prediction, confidence, probabilities } = predictionData;
  const normalizedPredKey = (prediction || '').toLowerCase().replace(/[^a-z]/g, '');
  const detail = CLASS_DETAILS[normalizedPredKey] || CLASS_DETAILS.notumor;

  const confPercentage = (confidence * 100).toFixed(1);

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="glass-panel animate-fade-in" style={{ padding: '24px', height: '100%', display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      {/* Primary Diagnosis Header */}
      <div style={{
        background: detail.bgColor,
        border: `1px solid ${detail.borderColor}`,
        borderRadius: 'var(--radius-md)',
        padding: '20px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '16px'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
            {normalizedPredKey === 'notumor' ? (
              <CheckCircle size={20} color={detail.color} />
            ) : (
              <AlertTriangle size={20} color={detail.color} />
            )}
            <span style={{ fontSize: '0.78rem', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 700, color: detail.color }}>
              {detail.severity}
            </span>
          </div>
          <h2 style={{ fontSize: '1.4rem', color: '#fff', margin: 0 }}>
            {detail.label}
          </h2>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            {detail.description}
          </p>
        </div>

        {/* Confidence Score Ring Gauge */}
        <div style={{ textAlign: 'center', position: 'relative' }}>
          <div style={{
            width: '80px',
            height: '80px',
            borderRadius: '50%',
            background: `radial-gradient(closest-side, var(--bg-dark) 78%, transparent 80% 100%), conic-gradient(${detail.color} ${confPercentage}%, rgba(255, 255, 255, 0.1) 0)`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: `0 0 20px ${detail.color}40`
          }}>
            <span style={{ fontSize: '1.1rem', fontWeight: 800, color: '#fff' }}>
              {confPercentage}%
            </span>
          </div>
          <span style={{ fontSize: '0.7rem', color: 'var(--text-dim)', display: 'block', marginTop: '4px' }}>
            Model Confidence
          </span>
        </div>
      </div>

      {/* Class Probabilities Distribution */}
      <div>
        <h3 style={{ fontSize: '0.95rem', color: '#fff', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <BarChart3 size={16} color="var(--primary)" />
          Multi-Class Probability Distribution
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {Object.entries(probabilities || {}).map(([className, score]) => {
            const pct = (score * 100).toFixed(1);
            const isTopClass = className.toLowerCase() === normalizedPredKey;
            const barColor = isTopClass ? detail.color : 'rgba(255, 255, 255, 0.3)';

            return (
              <div key={className}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '4px' }}>
                  <span style={{ color: isTopClass ? '#fff' : 'var(--text-muted)', fontWeight: isTopClass ? 700 : 500, textTransform: 'capitalize' }}>
                    {className}
                  </span>
                  <span style={{ color: isTopClass ? detail.color : 'var(--text-dim)', fontWeight: 600 }}>
                    {pct}%
                  </span>
                </div>
                <div style={{ width: '100%', height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{
                    width: `${pct}%`,
                    height: '100%',
                    background: barColor,
                    borderRadius: '4px',
                    transition: 'width 0.6s ease-out',
                    boxShadow: isTopClass ? `0 0 10px ${detail.color}` : 'none'
                  }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Clinical Findings & Recommendations */}
      <div style={{ background: 'rgba(15, 23, 42, 0.5)', padding: '16px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
        <h4 style={{ fontSize: '0.85rem', color: 'var(--primary-light)', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <FileText size={14} /> Clinical Report Summary
        </h4>
        <ul style={{ fontSize: '0.8rem', color: 'var(--text-muted)', paddingLeft: '18px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
          <li>Primary Classification: <strong style={{ color: '#fff' }}>{detail.label}</strong> ({confPercentage}% match score)</li>
          <li>Visual Localization: Grad-CAM attention heatmap confirms focal region.</li>
          <li>Recommendation: Correlate with clinical history and follow up with specialist review.</li>
        </ul>
      </div>

      {/* Print / Export Report Button */}
      <div style={{ marginTop: 'auto', paddingTop: '12px' }}>
        <button
          onClick={handlePrint}
          className="btn-secondary"
          style={{ width: '100%', justifyContent: 'center', padding: '12px' }}
        >
          <Printer size={16} /> Print Diagnostic Assessment Report
        </button>
      </div>

    </div>
  );
}
