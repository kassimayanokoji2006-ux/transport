document.addEventListener('DOMContentLoaded', function () {
  // Count-up animation
  document.querySelectorAll('.card-value[data-count]').forEach(function (el) {
    var target = parseInt(el.getAttribute('data-count') || '0', 10);
    var current = 0;
    var step = Math.max(1, Math.round(target / 60));
    var timer = setInterval(function () {
      current += step;
      if (current >= target) { current = target; clearInterval(timer); }
      el.textContent = current.toString();
    }, 16);
  });

  // Reveal animations
  var observer = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){
        entry.target.classList.add('in-view');
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll('[data-animate]').forEach(function(el){
    observer.observe(el);
  });

  // Active nav state
  var path = window.location.pathname;
  document.querySelectorAll('aside nav a').forEach(function(a){
    if(a.getAttribute('href') === path){
      a.style.background = 'rgba(255,255,255,.16)';
    }
  });

  // Ripple effect on primary buttons
  document.querySelectorAll('.btn-primary, .btn-secondary, .btn-danger').forEach(function(btn){
    btn.classList.add('ripple');
    btn.addEventListener('click', function(e){
      var rect = btn.getBoundingClientRect();
      btn.style.setProperty('--x', (e.clientX - rect.left)+'px');
      btn.style.setProperty('--y', (e.clientY - rect.top)+'px');
      btn.classList.add('active');
      setTimeout(function(){ btn.classList.remove('active'); }, 250);
    });
  });

  // Simple form validation feedback
  document.querySelectorAll('form').forEach(function(form){
    form.addEventListener('submit', function(e){
      var invalid = [];
      form.querySelectorAll('input[required], select[required]').forEach(function(field){
        if(!field.value){ invalid.push(field); }
      });
      if(invalid.length){
        e.preventDefault();
        invalid[0].focus();
        invalid.forEach(function(f){ f.style.borderColor = '#ef4444'; });
        setTimeout(function(){ invalid.forEach(function(f){ f.style.borderColor=''; }); }, 1200);
      }
    });
  });
});


