/**
 * Mermaid Pan & Zoom Interactive Controls for MkDocs Material
 * Enables interactive navigation for all Mermaid sequence and flowchart diagrams:
 * Buttons: Zoom In (+), Zoom Out (-), Reset (↺), Pan (↑, ↓, ←, →), plus mouse drag & wheel.
 */

(function () {
  'use strict';

  function initMermaidPanZoom() {
    // Target both direct .mermaid and superfences containers
    const mermaidContainers = document.querySelectorAll('.mermaid, div.mermaid, pre.mermaid');

    mermaidContainers.forEach((container) => {
      // Avoid duplicate wrappers
      if (container.closest('.mermaid-panzoom-wrapper')) {
        return;
      }

      // Check if SVG is already present or wait for it
      const svg = container.querySelector('svg');
      if (!svg) {
        // Observe container until mermaid finishes rendering SVG
        const observer = new MutationObserver((mutations, obs) => {
          const loadedSvg = container.querySelector('svg');
          if (loadedSvg) {
            obs.disconnect();
            setupPanZoom(container, loadedSvg);
          }
        });
        observer.observe(container, { childList: true, subtree: true });
        return;
      }

      setupPanZoom(container, svg);
    });
  }

  function setupPanZoom(container, svg) {
    // Create wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'mermaid-panzoom-wrapper';

    const viewport = document.createElement('div');
    viewport.className = 'mermaid-panzoom-viewport';

    // Insert wrapper before container
    container.parentNode.insertBefore(wrapper, container);
    viewport.appendChild(container);
    wrapper.appendChild(viewport);

    // Initial transform state
    let scale = 1.0;
    let panX = 0;
    let panY = 0;
    const minScale = 0.3;
    const maxScale = 4.0;
    const stepScale = 0.2;
    const stepPan = 60;

    function applyTransform() {
      svg.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
    }

    // Create floating controls
    const controls = document.createElement('div');
    controls.className = 'mermaid-panzoom-controls';
    controls.setAttribute('role', 'toolbar');
    controls.setAttribute('aria-label', 'Controles de navegación de diagrama');

    function createBtn(label, title, onClick) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'mermaid-panzoom-btn';
      btn.innerHTML = label;
      btn.title = title;
      btn.setAttribute('aria-label', title);
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        onClick();
      });
      return btn;
    }

    function createDivider() {
      const d = document.createElement('div');
      d.className = 'mermaid-panzoom-divider';
      return d;
    }

    // Zoom Buttons
    controls.appendChild(createBtn('+', 'Acercar (Zoom In)', () => {
      scale = Math.min(maxScale, scale + stepScale);
      applyTransform();
    }));

    controls.appendChild(createBtn('−', 'Alejar (Zoom Out)', () => {
      scale = Math.max(minScale, scale - stepScale);
      applyTransform();
    }));

    controls.appendChild(createBtn('↺', 'Restablecer escala y posición', () => {
      scale = 1.0;
      panX = 0;
      panY = 0;
      applyTransform();
    }));

    controls.appendChild(createDivider());

    // Directional Arrows
    controls.appendChild(createBtn('↑', 'Desplazar arriba', () => {
      panY += stepPan;
      applyTransform();
    }));

    controls.appendChild(createBtn('↓', 'Desplazar abajo', () => {
      panY -= stepPan;
      applyTransform();
    }));

    controls.appendChild(createBtn('←', 'Desplazar izquierda', () => {
      panX += stepPan;
      applyTransform();
    }));

    controls.appendChild(createBtn('→', 'Desplazar derecha', () => {
      panX -= stepPan;
      applyTransform();
    }));

    wrapper.appendChild(controls);

    // Mouse Dragging
    let isDragging = false;
    let startX = 0;
    let startY = 0;

    wrapper.addEventListener('mousedown', (e) => {
      // Ignore if clicking on control buttons
      if (e.target.closest('.mermaid-panzoom-controls')) return;
      isDragging = true;
      startX = e.clientX - panX;
      startY = e.clientY - panY;
      wrapper.style.cursor = 'grabbing';
      e.preventDefault();
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      panX = e.clientX - startX;
      panY = e.clientY - startY;
      applyTransform();
    });

    window.addEventListener('mouseup', () => {
      if (isDragging) {
        isDragging = false;
        wrapper.style.cursor = 'grab';
      }
    });

    // Mouse Wheel Zoom
    wrapper.addEventListener('wheel', (e) => {
      if (e.ctrlKey || wrapper.matches(':hover')) {
        e.preventDefault();
        const delta = e.deltaY < 0 ? 0.12 : -0.12;
        const newScale = Math.min(maxScale, Math.max(minScale, scale + delta));
        scale = newScale;
        applyTransform();
      }
    }, { passive: false });
  }

  // Hook into MkDocs Material instant loading or window DOMContentLoaded
  if (typeof document$ !== 'undefined') {
    document$.subscribe(() => {
      setTimeout(initMermaidPanZoom, 200);
    });
  } else {
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(initMermaidPanZoom, 200);
    });
  }
})();
