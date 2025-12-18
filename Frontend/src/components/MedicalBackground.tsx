import { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  opacity: number;
}

const MedicalBackground = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    const setCanvasSize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    setCanvasSize();
    window.addEventListener('resize', setCanvasSize);

    // Create particles
    const particles: Particle[] = [];
    const particleCount = 50;

    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: Math.random() * 3 + 1,
        opacity: Math.random() * 0.5 + 0.2,
      });
    }

    let animationId: number;
    let time = 0;

    const animate = () => {
      if (!ctx || !canvas) return;

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      time += 0.01;

      // Draw connecting lines between nearby particles
      particles.forEach((particle, i) => {
        particles.slice(i + 1).forEach((otherParticle) => {
          const dx = particle.x - otherParticle.x;
          const dy = particle.y - otherParticle.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 150) {
            ctx.beginPath();
            ctx.strokeStyle = `rgba(253, 184, 125, ${0.12 * (1 - distance / 150)})`;
            ctx.lineWidth = 1;
            ctx.moveTo(particle.x, particle.y);
            ctx.lineTo(otherParticle.x, otherParticle.y);
            ctx.stroke();
          }
        });
      });

      // Draw and update particles
      particles.forEach((particle) => {
        // Update position
        particle.x += particle.vx;
        particle.y += particle.vy;

        // Wrap around edges
        if (particle.x < 0) particle.x = canvas.width;
        if (particle.x > canvas.width) particle.x = 0;
        if (particle.y < 0) particle.y = canvas.height;
        if (particle.y > canvas.height) particle.y = 0;

        // Draw particle
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(253, 184, 125, ${particle.opacity})`;
        ctx.fill();

        // Add glow effect
        const gradient = ctx.createRadialGradient(
          particle.x,
          particle.y,
          0,
          particle.x,
          particle.y,
          particle.size * 3
        );
        gradient.addColorStop(0, `rgba(253, 184, 125, ${particle.opacity * 0.5})`);
        gradient.addColorStop(1, 'rgba(253, 184, 125, 0)');
        ctx.fillStyle = gradient;
        ctx.fillRect(
          particle.x - particle.size * 3,
          particle.y - particle.size * 3,
          particle.size * 6,
          particle.size * 6
        );
      });

      animationId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('resize', setCanvasSize);
      cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
      {/* Animated gradient base - disabled to use global background */}
      {/* <div className="absolute inset-0 animated-gradient-bg" /> */}

      {/* DNA Helix SVG Animation */}
      <svg
        className="absolute inset-0 w-full h-full opacity-20"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient id="helixGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#FDB87D" stopOpacity="0.25" />
            <stop offset="100%" stopColor="#F6EFBD" stopOpacity="0.25" />
          </linearGradient>
        </defs>
        {[0, 1, 2, 3].map((i) => (
          <motion.path
            key={i}
            d={`M ${i * 300} 100 Q ${i * 300 + 150} 200, ${i * 300 + 300} 100 T ${i * 300 + 600} 100`}
            stroke="url(#helixGradient)"
            strokeWidth="2"
            fill="none"
            initial={{ pathLength: 0, opacity: 0 }}
            animate={{
              pathLength: 1,
              opacity: [0.2, 0.4, 0.2],
              x: [-300, 0],
            }}
            transition={{
              pathLength: { duration: 2, delay: i * 0.2 },
              opacity: { duration: 3, repeat: Infinity, delay: i * 0.3 },
              x: { duration: 15, repeat: Infinity, ease: 'linear' },
            }}
          />
        ))}
      </svg>

      {/* Medical Cross Pattern */}
      <div className="absolute inset-0 opacity-5">
        {[...Array(8)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute"
            style={{
              left: `${(i % 4) * 25}%`,
              top: `${Math.floor(i / 4) * 50}%`,
            }}
            animate={{
              opacity: [0.05, 0.15, 0.05],
              scale: [1, 1.1, 1],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              delay: i * 0.5,
            }}
          >
            <svg width="60" height="60" viewBox="0 0 60 60">
              <path
                d="M 20 0 L 40 0 L 40 20 L 60 20 L 60 40 L 40 40 L 40 60 L 20 60 L 20 40 L 0 40 L 0 20 L 20 20 Z"
                fill="url(#helixGradient)"
              />
            </svg>
          </motion.div>
        ))}
      </div>

      {/* Canvas for particles and neural network */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full"
        style={{ mixBlendMode: 'screen' }}
      />

      {/* Floating waves */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute w-[200%] h-full"
          animate={{
            x: ['0%', '-50%'],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: 'linear',
          }}
        >
          <svg
            className="w-full h-full opacity-10"
            viewBox="0 0 1200 600"
            preserveAspectRatio="none"
          >
            <path
              d="M0,300 Q300,200 600,300 T1200,300 L1200,600 L0,600 Z"
              fill="url(#helixGradient)"
            />
          </svg>
        </motion.div>
      </div>

      {/* Pulsing medical icons */}
      <div className="absolute inset-0 pointer-events-none">
        {[
          { icon: '⚕️', x: '10%', y: '20%', delay: 0 },
          { icon: '🧬', x: '80%', y: '30%', delay: 1 },
          { icon: '💊', x: '15%', y: '70%', delay: 2 },
          { icon: '🔬', x: '85%', y: '75%', delay: 1.5 },
        ].map((item, i) => (
          <motion.div
            key={i}
            className="absolute text-4xl"
            style={{ left: item.x, top: item.y }}
            animate={{
              opacity: [0.08, 0.2, 0.08],
              scale: [1, 1.15, 1],
              rotate: [0, 10, -10, 0],
            }}
            transition={{
              duration: 6,
              repeat: Infinity,
              delay: item.delay,
            }}
          >
            {item.icon}
          </motion.div>
        ))}
      </div>

      {/* Grid overlay for tech feel */}
      <div
        className="absolute inset-0 opacity-5"
        style={{
          backgroundImage: `
            linear-gradient(rgba(255, 185, 150, 0.5) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 185, 150, 0.5) 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px',
        }}
      />
    </div>
  );
};

export default MedicalBackground;
