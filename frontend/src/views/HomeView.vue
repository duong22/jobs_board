<template>
    <div>
  
      <!-- NAV -->
      <nav class="nav">
        <span class="logo">JobBoard</span>
        <div>
          <router-link to="/jobs" class="nav-link">Browse jobs</router-link>
          <router-link to="/login" class="nav-link">Login</router-link>
          <router-link to="/register" class="nav-btn">Register</router-link>
        </div>
      </nav>
  
      <!-- HERO -->
      <section class="hero">
        <h1>Find your next job</h1>
        <p>Browse open positions, apply easily, and track your applications.</p>
        <div class="hero-actions">
          <router-link to="/jobs" class="btn-primary">Browse jobs</router-link>
          <router-link to="/register" class="btn-outline">Post a job</router-link>
        </div>
      </section>
  
      <!-- STATS -->
      <section class="stats">
        <div class="stat">
          <strong>124</strong>
          <span>Open positions</span>
        </div>
        <div class="stat">
          <strong>38</strong>
          <span>Companies hiring</span>
        </div>
        <div class="stat">
          <strong>6</strong>
          <span>Categories</span>
        </div>
      </section>
  
      <!-- HOW IT WORKS -->
      <section class="how">
        <h2>How it works</h2>
        <div class="steps">
          <div class="step">
            <div class="step-num">1</div>
            <h3>Create account</h3>
            <p>Sign up as a candidate or employer.</p>
          </div>
          <div class="step">
            <div class="step-num">2</div>
            <h3>Browse & apply</h3>
            <p>Filter jobs by category, location, or type.</p>
          </div>
          <div class="step">
            <div class="step-num">3</div>
            <h3>Track status</h3>
            <p>Follow your applications from your dashboard.</p>
          </div>
        </div>
      </section>
  
      <!-- FOOTER -->
      <footer class="footer">
        <p>JobBoard &copy; {{ new Date().getFullYear() }}</p>
      </footer>
  
    </div>
  </template>
  
  <script setup>
  // Nothing needed here for now.
  // Later: import { useAuthStore } from '@/stores/auth'
  </script>
  
  <style scoped>
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  
  /* NAV */
  .nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
    height: 60px;
    background: #fff;
    border-bottom: 1px solid #e5e5e5;
  }
  .logo {
    font-size: 1.2rem;
    font-weight: 700;
    color: #111;
  }
  .nav-link {
    margin-right: 1rem;
    color: #555;
    text-decoration: none;
    font-size: 0.9rem;
  }
  .nav-link:hover { color: #111; }
  .nav-btn {
    padding: 0.4rem 1rem;
    background: #111;
    color: #fff;
    border-radius: 6px;
    text-decoration: none;
    font-size: 0.9rem;
  }
  .nav-btn:hover { background: #333; }
  
  /* HERO */
  .hero {
    text-align: center;
    padding: 5rem 2rem;
    background: #f9f9f9;
  }
  .hero h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #111;
    margin-bottom: 1rem;
  }
  .hero p {
    font-size: 1.1rem;
    color: #555;
    margin-bottom: 2rem;
  }
  .hero-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
  }
  .btn-primary {
    padding: 0.7rem 1.5rem;
    background: #111;
    color: #fff;
    border-radius: 6px;
    text-decoration: none;
    font-size: 0.95rem;
  }
  .btn-primary:hover { background: #333; }
  .btn-outline {
    padding: 0.7rem 1.5rem;
    background: #fff;
    color: #111;
    border: 1.5px solid #ccc;
    border-radius: 6px;
    text-decoration: none;
    font-size: 0.95rem;
  }
  .btn-outline:hover { border-color: #111; }
  
  /* STATS */
  .stats {
    display: flex;
    justify-content: center;
    gap: 4rem;
    padding: 2.5rem 2rem;
    background: #fff;
    border-top: 1px solid #e5e5e5;
    border-bottom: 1px solid #e5e5e5;
    text-align: center;
  }
  .stat strong {
    display: block;
    font-size: 2rem;
    font-weight: 700;
    color: #111;
  }
  .stat span {
    font-size: 0.85rem;
    color: #888;
    margin-top: 0.2rem;
  }
  
  /* HOW IT WORKS */
  .how {
    padding: 4rem 2rem;
    max-width: 900px;
    margin: 0 auto;
    text-align: center;
  }
  .how h2 {
    font-size: 1.8rem;
    font-weight: 700;
    color: #111;
    margin-bottom: 2.5rem;
  }
  .steps {
    display: flex;
    gap: 2rem;
    justify-content: center;
  }
  .step {
    flex: 1;
    padding: 2rem 1.5rem;
    background: #f9f9f9;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    text-align: center;
  }
  .step-num {
    width: 40px;
    height: 40px;
    background: #111;
    color: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    margin: 0 auto 1rem;
  }
  .step h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #111;
    margin-bottom: 0.5rem;
  }
  .step p {
    font-size: 0.875rem;
    color: #666;
    line-height: 1.6;
  }
  
  /* FOOTER */
  .footer {
    text-align: center;
    padding: 1.5rem;
    font-size: 0.85rem;
    color: #aaa;
    border-top: 1px solid #e5e5e5;
  }
  </style>