'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { auth } from '@/lib/firebase';
import { createUserWithEmailAndPassword } from 'firebase/auth';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSignUp = async () => {
    try {
      await createUserWithEmailAndPassword(auth, email, password);
      router.push('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Signup failed');
    }
  };

  return (
    <div 
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '1rem',
        backgroundColor: '#0a0a0a',
        color: '#fff',
        fontFamily: 'system-ui, -apple-system, sans-serif',
        backgroundImage: 'radial-gradient(circle at 50% 50%, rgba(255,20,147,0.1) 0%, transparent 70%)'
      }}
    >
      <div 
        style={{
          width: '100%',
          maxWidth: '28rem',
          padding: '2.5rem',
          borderRadius: '1rem',
          border: '1px solid rgba(255, 20, 147, 0.3)',
          backgroundColor: 'rgba(10, 10, 10, 0.8)',
          boxShadow: '0 0 25px rgba(255, 20, 147, 0.2)',
          backdropFilter: 'blur(8px)',
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        {/* Glowy border effect */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '2px',
          background: 'linear-gradient(90deg, transparent, #ff1493, transparent)',
          boxShadow: '0 0 10px #ff1493',
          animation: 'scan 3s linear infinite'
        }}></div>

        <h1 style={{ 
          fontSize: '2rem', 
          fontWeight: '700', 
          marginBottom: '2rem',
          textAlign: 'center',
          color: '#fff',
          letterSpacing: '0.5px'
        }}>
          Create Your Account
        </h1>

        {error && (
          <p style={{ 
            color: '#ff355e',
            marginBottom: '1.5rem',
            padding: '0.75rem',
            backgroundColor: 'rgba(255, 53, 94, 0.1)',
            borderRadius: '0.5rem',
            border: '1px solid rgba(255, 53, 94, 0.3)',
            textAlign: 'center',
            animation: 'errorPulse 2s infinite'
          }}>{error}</p>
        )}

        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ 
            display: 'block', 
            marginBottom: '0.75rem',
            color: 'rgba(255,255,255,0.8)',
            fontSize: '0.95rem',
            fontWeight: '500'
          }}>
            Email Address
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={{
              width: '100%',
              backgroundColor: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255, 20, 147, 0.3)',
              borderRadius: '0.75rem',
              padding: '0.9rem 1.25rem',
              color: '#fff',
              outline: 'none',
              transition: 'all 0.3s ease',
              fontSize: '1rem'
            }}
            onFocus={(e) => {
              e.target.style.borderColor = '#ff1493';
              e.target.style.boxShadow = '0 0 0 3px rgba(255, 20, 147, 0.2)';
            }}
            onBlur={(e) => {
              e.target.style.borderColor = 'rgba(255, 20, 147, 0.3)';
              e.target.style.boxShadow = 'none';
            }}
            placeholder="Enter your email"
          />
        </div>

        <div style={{ marginBottom: '2rem' }}>
          <label style={{ 
            display: 'block', 
            marginBottom: '0.75rem',
            color: 'rgba(255,255,255,0.8)',
            fontSize: '0.95rem',
            fontWeight: '500'
          }}>
            Password
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              width: '100%',
              backgroundColor: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255, 20, 147, 0.3)',
              borderRadius: '0.75rem',
              padding: '0.9rem 1.25rem',
              color: '#fff',
              outline: 'none',
              transition: 'all 0.3s ease',
              fontSize: '1rem'
            }}
            onFocus={(e) => {
              e.target.style.borderColor = '#ff1493';
              e.target.style.boxShadow = '0 0 0 3px rgba(255, 20, 147, 0.2)';
            }}
            onBlur={(e) => {
              e.target.style.borderColor = 'rgba(255, 20, 147, 0.3)';
              e.target.style.boxShadow = 'none';
            }}
            placeholder="Create a password"
          />
        </div>

        <button
          onClick={handleSignUp}
          style={{
            width: '100%',
            background: 'linear-gradient(90deg, #ff1493, #ff6b9d)',
            color: '#fff',
            padding: '1rem',
            borderRadius: '0.75rem',
            fontWeight: '600',
            cursor: 'pointer',
            border: 'none',
            fontSize: '1rem',
            transition: 'all 0.3s ease',
            boxShadow: '0 4px 15px rgba(255, 20, 147, 0.4)',
            position: 'relative',
            overflow: 'hidden'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.boxShadow = '0 6px 20px rgba(255, 20, 147, 0.6)';
            e.currentTarget.style.transform = 'translateY(-2px)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.boxShadow = '0 4px 15px rgba(255, 20, 147, 0.4)';
            e.currentTarget.style.transform = 'translateY(0)';
          }}
        >
          <span style={{
            position: 'relative',
            zIndex: 2
          }}>Sign Up</span>
          <span style={{
            position: 'absolute',
            top: '-50%',
            left: '-50%',
            width: '200%',
            height: '200%',
            background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent)',
            transform: 'rotate(45deg)',
            animation: 'shine 3s infinite'
          }}></span>
        </button>

        <p style={{ 
          marginTop: '2rem', 
          textAlign: 'center',
          color: 'rgba(255,255,255,0.7)',
          fontSize: '0.95rem'
        }}>
          Already have an account?{' '}
          <a 
            href="/login" 
            style={{ 
              color: '#ff6b9d',
              textDecoration: 'none',
              fontWeight: '500',
              transition: 'all 0.3s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.color = '#ff1493';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.color = '#ff6b9d';
            }}
          >
            Log in
          </a>
        </p>

        {/* Add this style tag for animations */}
        <style jsx global>{`
          @keyframes scan {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
          }
          @keyframes shine {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(100%) rotate(45deg); }
          }
          @keyframes errorPulse {
            0% { opacity: 0.9; }
            50% { opacity: 1; }
            100% { opacity: 0.9; }
          }
        `}</style>
      </div>
    </div>
  );
}