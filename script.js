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

// Newsletter form — Brevo integration
const BREVO_API_KEY  = 'PASTE_YOUR_BREVO_API_KEY_HERE';
const BREVO_LIST_ID  = 0; // Replace 0 with your Brevo list ID number

document.getElementById('newsletterForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const btn   = this.querySelector('button[type="submit"]');
  const email = document.getElementById('nl-email').value.trim();
  const firstName = document.getElementById('nl-first').value.trim();

  btn.textContent = 'Subscribing…';
  btn.disabled = true;

  try {
    const res = await fetch('https://api.brevo.com/v3/contacts', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'content-type': 'application/json',
        'api-key': BREVO_API_KEY
      },
      body: JSON.stringify({
        email,
        attributes: { FIRSTNAME: firstName },
        listIds: [BREVO_LIST_ID],
        updateEnabled: true
      })
    });

    if (res.ok || res.status === 204) {
      this.style.display = 'none';
      document.getElementById('nlSuccess').style.display = 'block';
    } else {
      const err = await res.json();
      // If contact already exists, still show success
      if (res.status === 400 && err.code === 'duplicate_parameter') {
        this.style.display = 'none';
        document.getElementById('nlSuccess').style.display = 'block';
      } else {
        btn.textContent = 'Try again';
        btn.disabled = false;
        console.error('Brevo error:', err);
      }
    }
  } catch (err) {
    btn.textContent = 'Try again';
    btn.disabled = false;
    console.error('Network error:', err);
  }
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
