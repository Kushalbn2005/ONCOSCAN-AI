import React, { useRef, useState } from 'react';
import { UploadCloud, FileImage, Sparkles, CheckCircle2 } from 'lucide-react';
import { SAMPLES, getSampleFile } from '../utils/sampleData';

export default function UploadSection({ onFileSelect, isLoading }) {
  const fileInputRef = useRef(null);
  const [isDragOver, setIsDragOver] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0]);
    }
  };

  const handleSampleClick = async (sampleId) => {
    const file = await getSampleFile(sampleId);
    onFileSelect(file);
  };

  return (
    <div className="glass-panel" style={{ padding: '28px', marginBottom: '28px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ fontSize: '1.15rem', color: '#fff', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <UploadCloud size={20} color="var(--primary)" />
          MRI Image Upload & Sample Selection
        </h2>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          Upload a cerebral MRI slice (axial view recommended) or select a pre-loaded clinical sample scan below.
        </p>
      </div>

      {/* Drag & Drop Box */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        style={{
          border: `2px dashed ${isDragOver ? 'var(--primary)' : 'rgba(255, 255, 255, 0.15)'}`,
          borderRadius: 'var(--radius-md)',
          padding: '40px 20px',
          textAlign: 'center',
          background: isDragOver ? 'rgba(6, 182, 212, 0.08)' : 'rgba(15, 23, 42, 0.4)',
          cursor: isLoading ? 'wait' : 'pointer',
          transition: 'all var(--transition-fast)',
          position: 'relative'
        }}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          style={{ display: 'none' }}
          onChange={handleFileChange}
          disabled={isLoading}
        />

        <div style={{
          width: '56px',
          height: '56px',
          margin: '0 auto 16px',
          borderRadius: '50%',
          background: 'rgba(6, 182, 212, 0.15)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'var(--primary)'
        }}>
          <FileImage size={28} />
        </div>

        <h3 style={{ fontSize: '1rem', color: '#fff', marginBottom: '6px' }}>
          Drop MRI image file here or <span style={{ color: 'var(--primary-light)', textDecoration: 'underline' }}>Browse</span>
        </h3>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
          Supports PNG, JPG, JPEG (224×224 resolution automatically scaled)
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '8px' }}>
          {['PNG', 'JPG', 'DICOM-Converted'].map((tag, i) => (
            <span key={i} style={{
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid rgba(255, 255, 255, 0.08)',
              padding: '2px 10px',
              borderRadius: '12px',
              fontSize: '0.72rem',
              color: 'var(--text-dim)'
            }}>
              {tag}
            </span>
          ))}
        </div>
      </div>

      {/* Preset Quick Samples */}
      <div style={{ marginTop: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '12px' }}>
          <Sparkles size={16} color="var(--accent-purple)" />
          <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)' }}>
            Quick Clinical Test Samples:
          </span>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '12px'
        }}>
          {SAMPLES.map((sample) => (
            <button
              key={sample.id}
              onClick={() => handleSampleClick(sample.id)}
              disabled={isLoading}
              className="btn-secondary"
              style={{
                padding: '12px 14px',
                flexDirection: 'column',
                alignItems: 'flex-start',
                textAlign: 'left',
                borderLeft: `4px solid ${sample.color}`,
                background: 'rgba(15, 23, 42, 0.5)'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center' }}>
                <span style={{ fontWeight: 700, fontSize: '0.85rem', color: '#fff' }}>
                  {sample.name}
                </span>
                <CheckCircle2 size={14} color={sample.color} />
              </div>
              <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                {sample.description}
              </span>
            </button>
          ))}
        </div>
      </div>

    </div>
  );
}
