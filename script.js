// Navbar scroll effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 60);
});

// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
navToggle.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

// Close mobile nav on link click
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => navLinks.classList.remove('open'));
});

// Scroll animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll(
  '.about-grid, .speaking-card, .shop-card, .community-inner, ' +
  '.episode-item, .testimonial-card, .contact-grid, .pod-stat, ' +
  '.pillar, .contact-option, .comm-card, .nl-free-gift'
).forEach(el => {
  el.classList.add('fade-up');
  observer.observe(el);
});

// Staggered animation for grids
document.querySelectorAll('.speaking-grid, .shop-grid, .testimonials-grid, .podcast-stats').forEach(grid => {
  Array.from(grid.children).forEach((child, i) => {
    child.style.transitionDelay = `${i * 0.1}s`;
  });
});

// Newsletter form — first name, last name, email all required
// On success: show success state + auto-download PDF

function triggerPdfDownload() {
  const a = document.createElement('a');
  a.href = 'eq-self-assessment-guide.pdf';
  a.download = 'The-Real-Work-Self-Reflection-Journal-Brittany-Clausen.pdf';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

document.getElementById('newsletterForm').addEventListener('submit', async function(e) {
  e.preventDefault();

  const firstInput = document.getElementById('nl-first');
  const lastInput  = document.getElementById('nl-last');
  const emailInput = document.getElementById('nl-email');
  const errFirst   = document.getElementById('err-first');
  const errLast    = document.getElementById('err-last');
  const errEmail   = document.getElementById('err-email');
  const btn        = this.querySelector('button[type="submit"]');

  const firstName = firstInput.value.trim();
  const lastName  = lastInput.value.trim();
  const email     = emailInput.value.trim();

  // ── Validation — all three fields required ───────────────────────────────
  let valid = true;

  if (!firstName) {
    firstInput.classList.add('input-error');
    errFirst.style.display = 'block';
    valid = false;
  } else {
    firstInput.classList.remove('input-error');
    errFirst.style.display = 'none';
  }

  if (!lastName) {
    lastInput.classList.add('input-error');
    errLast.style.display = 'block';
    valid = false;
  } else {
    lastInput.classList.remove('input-error');
    errLast.style.display = 'none';
  }

  const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  if (!email || !emailOk) {
    emailInput.classList.add('input-error');
    errEmail.style.display = 'block';
    valid = false;
  } else {
    emailInput.classList.remove('input-error');
    errEmail.style.display = 'none';
  }

  if (!valid) return;

  // ── Submit to Brevo ──────────────────────────────────────────────────────
  btn.textContent = 'One moment…';
  btn.disabled = true;

  try {
    const res = await fetch('https://brevo-subscribe.brittany-60b.workers.dev', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, firstName, lastName }),
    });

    const data = await res.json();

    if (data.success) {
      this.style.display = 'none';
      document.getElementById('nlSuccess').style.display = 'block';
      triggerPdfDownload();
    } else {
      btn.textContent = 'Try again';
      btn.disabled = false;
    }
  } catch (err) {
    // Network hiccup — still deliver the PDF
    this.style.display = 'none';
    document.getElementById('nlSuccess').style.display = 'block';
    triggerPdfDownload();
  }
});

// Clear error state on input
['nl-first', 'nl-email'].forEach(id => {
  document.getElementById(id).addEventListener('input', function() {
    this.classList.remove('input-error');
    const errId = id === 'nl-first' ? 'err-first' : 'err-email';
    document.getElementById(errId).style.display = 'none';
  });
});


// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = 80;
      window.scrollTo({ top: target.offsetTop - offset, behavior: 'smooth' });
    }
  });
});
