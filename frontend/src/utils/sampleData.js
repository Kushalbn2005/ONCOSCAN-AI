// Utility to generate synthetic sample MRI images for instant 1-click testing
export const SAMPLES = [
  {
    id: 'glioma',
    name: 'Glioma Tumor MRI',
    type: 'glioma',
    description: 'Axial T1-weighted contrast MRI showing hyperintense glial mass in cerebral hemisphere.',
    color: '#f43f5e',
    generateCanvas: (ctx, width, height) => {
      ctx.fillStyle = '#0a0d14';
      ctx.fillRect(0, 0, width, height);

      // Skull outline
      ctx.beginPath();
      ctx.ellipse(width / 2, height / 2, width * 0.4, height * 0.44, 0, 0, 2 * Math.PI);
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 12;
      ctx.stroke();

      // Brain Tissue background
      ctx.beginPath();
      ctx.ellipse(width / 2, height / 2, width * 0.38, height * 0.42, 0, 0, 2 * Math.PI);
      ctx.fillStyle = '#1e293b';
      ctx.fill();

      // Brain Hemispheres sulci / folds
      ctx.strokeStyle = '#0f172a';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(width / 2, height * 0.1);
      ctx.lineTo(width / 2, height * 0.9);
      ctx.stroke();

      for (let i = 0; i < 6; i++) {
        ctx.beginPath();
        ctx.arc(width * 0.35 + i * 5, height * 0.3 + i * 40, 30, 0.2, Math.PI - 0.2);
        ctx.strokeStyle = '#334155';
        ctx.stroke();
      }

      // Glioma mass (left temporal/frontal region)
      const grad = ctx.createRadialGradient(
        width * 0.35, height * 0.4, 5,
        width * 0.35, height * 0.4, 45
      );
      grad.addColorStop(0, '#ffffff');
      grad.addColorStop(0.4, '#e2e8f0');
      grad.addColorStop(0.8, '#64748b');
      grad.addColorStop(1, 'transparent');

      ctx.beginPath();
      ctx.ellipse(width * 0.35, height * 0.4, 45, 38, 0.3, 0, 2 * Math.PI);
      ctx.fillStyle = grad;
      ctx.fill();
    }
  },
  {
    id: 'meningioma',
    name: 'Meningioma MRI',
    type: 'meningioma',
    description: 'Dural-based extra-axial tumor showing homogeneous contrast enhancement.',
    color: '#f59e0b',
    generateCanvas: (ctx, width, height) => {
      ctx.fillStyle = '#0a0d14';
      ctx.fillRect(0, 0, width, height);

      // Skull outline
      ctx.beginPath();
      ctx.ellipse(width / 2, height / 2, width * 0.4, height * 0.44, 0, 0, 2 * Math.PI);
      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 14;
      ctx.stroke();

      // Brain Tissue background
      ctx.beginPath();
      ctx.ellipse(width / 2, height / 2, width * 0.37, height * 0.41, 0, 0, 2 * Math.PI);
      ctx.fillStyle = '#1e293b';
      ctx.fill();

      // Meningioma (Dural edge lesion)
      const grad = ctx.createRadialGradient(
        width * 0.68, height * 0.35, 2,
        width * 0.68, height * 0.35, 32
      );
      grad.addColorStop(0, '#ffffff');
      grad.addColorStop(0.6, '#cbd5e1');
      grad.addColorStop(1, 'transparent');

      ctx.beginPath();
      ctx.ellipse(width * 0.68, height * 0.35, 30, 25, -0.4, 0, 2 * Math.PI);
      ctx.fillStyle = grad;
      ctx.fill();
    }
  },
  {
    id: 'pituitary',
    name: 'Pituitary Macroadenoma',
    type: 'pituitary',
    description: 'Sellar/suprasellar mass with classic expansion near the optic chiasm.',
    color: '#8b5cf6',
    generateCanvas: (ctx, width, height) => {
      ctx.fillStyle = '#0a0d14';
      ctx.fillRect(0, 0, width, height);

      // Skull outline
      ctx.beginPath();
      ctx.ellipse(width / 2, height / 2, width * 0.4, height * 0.44, 0, 0, 2 * Math.PI);
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 12;
      ctx.stroke();

      // Brain Tissue background
      ctx.beginPath();
      ctx.ellipse(width / 2, height / 2, width * 0.38, height * 0.42, 0, 0, 2 * Math.PI);
      ctx.fillStyle = '#1e293b';
      ctx.fill();

      // Sellar region lesion (center-bottom skull base)
      const grad = ctx.createRadialGradient(
        width * 0.5, height * 0.62, 3,
        width * 0.5, height * 0.62, 28
      );
      grad.addColorStop(0, '#ffffff');
      grad.addColorStop(0.5, '#cbd5e1');
      grad.addColorStop(1, 'transparent');

      ctx.beginPath();
      ctx.ellipse(width * 0.5, height * 0.62, 25, 22, 0, 0, 2 * Math.PI);
      ctx.fillStyle = grad;
      ctx.fill();
    }
  },
  {
    id: 'notumor',
    name: 'Healthy Brain MRI',
    type: 'notumor',
    description: 'Normal cerebral parenchyma without focal mass, edema, or midline shift.',
    color: '#10b981',
    generateCanvas: (ctx, width, height) => {
      ctx.fillStyle = '#0a0d14';
      ctx.fillRect(0, 0, width, height);

      // Skull outline
      ctx.beginPath();
      ctx.ellipse(width / 2, height / 2, width * 0.4, height * 0.44, 0, 0, 2 * Math.PI);
      ctx.strokeStyle = '#334155';
      ctx.lineWidth = 12;
      ctx.stroke();

      // Brain Tissue background
      ctx.beginPath();
      ctx.ellipse(width / 2, height / 2, width * 0.38, height * 0.42, 0, 0, 2 * Math.PI);
      ctx.fillStyle = '#1e293b';
      ctx.fill();

      // Ventricles (normal symmetric dark butterfly pattern)
      ctx.fillStyle = '#0f172a';
      ctx.beginPath();
      ctx.ellipse(width * 0.46, height * 0.48, 8, 28, -0.2, 0, 2 * Math.PI);
      ctx.ellipse(width * 0.54, height * 0.48, 8, 28, 0.2, 0, 2 * Math.PI);
      ctx.fill();
    }
  }
];

// Helper to convert sample canvas drawing to a File object
export function getSampleFile(sampleId) {
  const sample = SAMPLES.find(s => s.id === sampleId) || SAMPLES[0];
  const canvas = document.createElement('canvas');
  canvas.width = 224;
  canvas.height = 224;
  const ctx = canvas.getContext('2d');
  sample.generateCanvas(ctx, 224, 224);

  return new Promise((resolve) => {
    canvas.toBlob((blob) => {
      const file = new File([blob], `${sample.id}_sample_mri.png`, { type: 'image/png' });
      resolve(file);
    }, 'image/png');
  });
}
