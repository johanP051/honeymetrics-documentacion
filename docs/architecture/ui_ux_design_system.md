# 🎨 Design System UI/UX — Dark CTI Premium Theme

> **Identidad Visual:** Dark CTI Premium. Inspirado en interfaces SIEM enterprise (Darktrace, CrowdStrike Falcon).
> **Regla fundamental:** Ningún componente usa CSS inline. Todo se controla con clases Tailwind y variables CSS.

## 1. Tokens de Diseño (Paleta Corporativa)

| Token (Clase Tailwind) | Valor Hexadecimal | Uso Semántico |
|---|---|---|
| `hm-bg` | `#0d1117` | Background global de la aplicación. |
| `hm-card` | `#161b22` | Superficie de tarjetas y paneles. |
| `hm-border` | `#30363d` | Bordes sutiles entre elementos. |
| `hm-text` | `#e6edf3` | Texto principal de alta legibilidad. |
| `hm-muted` | `#8b949e` | Texto secundario, metadatos, fechas. |
| `hm-gold` | `#d4af37` | Acento principal, botones primarios, bordes de énfasis. |
| `hm-gold-dim` | `#a07d20` | Estado hover del dorado. |
| `hm-red` | `#f85149` | Alertas críticas, errores, amenazas altas. |
| `hm-orange` | `#e3b341` | Alertas medias, botnets, warnings. |
| `hm-green` | `#3fb950` | Estado OK, compliance aprobado, score positivo. |
| `hm-blue` | `#58a6ff` | Información, links, IPs neutrales. |

```javascript
// tailwind.config.js — Fragmento de extend.colors
module.exports = {
  theme: {
    extend: {
      colors: {
        'hm-bg':       '#0d1117',
        'hm-card':     '#161b22',
        'hm-border':   '#30363d',
        'hm-text':     '#e6edf3',
        'hm-muted':    '#8b949e',
        'hm-gold':     '#d4af37',
        'hm-gold-dim': '#a07d20',
        'hm-red':      '#f85149',
        'hm-orange':   '#e3b341',
        'hm-green':    '#3fb950',
        'hm-blue':     '#58a6ff',
      }
    }
  }
}
```

## 2. Sistema de Glassmorfismo

> [!IMPORTANT]
> Todo contenedor de datos (tarjetas, modales, drawers, tooltips) DEBE usar `.glass-card` o `.glass-modal`. Está prohibido usar fondos sólidos opacos.

```css
/* src/index.css */

/* Tarjetas y Paneles Estándar */
.glass-card {
  background: rgba(22, 27, 34, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(48, 54, 61, 0.6);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  border-radius: 12px;
}

/* Modales Premium / Destacados */
.glass-modal {
  background: rgba(13, 17, 23, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(212, 175, 55, 0.2); /* borde dorado sutil */
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7);
  border-radius: 12px;
}
```

## 3. Máquina de Estados de UI (UX States)

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Loading: Llamada al hook/API
    
    state Loading {
        direction LR
        [*] --> Skeleton
        note right of Skeleton: Animado con animate-pulse de Tailwind
    }
    
    Loading --> Success: Datos correctos
    Loading --> Error: Timeout, 4xx, 5xx
    
    state Success {
        direction LR
        [*] --> Render
        note right of Render: transition-all duration-500 ease-in-out
    }
    
    state Error {
        direction LR
        [*] --> Toast
        note right of Toast: Toast rojo 3s. No revelar stack trace ni HTTP code.
    }
    
    Success --> Idle: Usuario interactúa/Refresca
    Error --> Idle: Usuario hace clic en "Reintentar"
```

## 4. Tabla de Micro-interacciones Obligatorias

| Elemento UI | Clase Tailwind de transición obligatoria | Descripción del comportamiento |
|---|---|---|
| Botón CTA (Dorado) | `transition-all duration-300 ease-in-out hover:bg-hm-gold-dim` | Cambio suave de color en hover. |
| Panel Lateral / Drawer | `transition-all duration-500 ease-in-out translate-x-0` | Deslizamiento lateral fluido. |
| Tarjeta de Datos | `hover:border-hm-gold/30 hover:shadow-lg transition-all duration-300` | Borde dorado sutil al hacer hover. |
| Tooltip | `transition-opacity duration-200 opacity-0 hover:opacity-100` | Aparición suave por opacidad. |
| Modal | `transition-all duration-300 scale-95 opacity-0 hover:scale-100 hover:opacity-100` | Efecto pop-in (zoom in suave). |
| Pestañas / Iconos SVG | `transition-all duration-500 ease-in-out` | Prohibido el cambio brusco de color/icono. |

## 5. Árbol de Decisión de Iconografía

```mermaid
flowchart LR
    A["¿Necesito un icono?"] --> B{"¿Es un icono de\nUI genérico?"}
    
    B -->|Sí| C["Usar lucide-react\n(Shield, AlertTriangle, Download)"]
    B -->|No| D{"¿Es un elemento\nCore de identidad?"}
    
    D -->|Sí| E["Crear SVG puro como React Component\nUsar stroke='currentColor' y clases Tailwind"]
    D -->|No| C
    
    style C fill:#161b22,color:#e6edf3,stroke:#30363d
    style E fill:#d4af37,color:#0d1117,stroke:#d4af37
```

**Ejemplo SVG Core Custom:**
```jsx
// src/common/icons/HoneyMetricsLogo.jsx
export const HoneyMetricsLogo = ({ className = "w-8 h-8 text-hm-gold" }) => (
  <svg className={className} viewBox="0 0 24 24" fill="none"
       stroke="currentColor" strokeWidth={1.5} strokeLinecap="round">
    <path d="M12 2 L20 6.5 V15.5 L12 20 L4 15.5 V6.5 Z" />
    <circle cx="12" cy="11" r="2.5" />
  </svg>
);
```

## 6. Integración de Plotly.js en Dark Mode (Regla Obligatoria)

Plotly.js por defecto usa fondo blanco. En HoneyMetrics, TODOS los gráficos deben tener fondo transparente para integrarse con el glassmorfismo del contenedor `.glass-card`.

```jsx
// Configuración Obligatoria para componentes Plotly
<Plot
  data={chartData}
  layout={{
    paper_bgcolor: 'transparent', // OBLIGATORIO
    plot_bgcolor: 'transparent',  // OBLIGATORIO
    font: { color: '#e6edf3', family: 'Inter, sans-serif' },
    xaxis: { gridcolor: '#30363d', zerolinecolor: '#30363d' },
    yaxis: { gridcolor: '#30363d', zerolinecolor: '#30363d' },
    margin: { t: 30, r: 10, b: 40, l: 50 },
  }}
  config={{ displayModeBar: false, responsive: true }}
  useResizeHandler={true} // OBLIGATORIO para responsive
  style={{ width: '100%', height: '100%' }}
  className="w-full"
/>
```

## 7. RBAC Visual: Árbol de Decisión por Rol

```mermaid
flowchart TD
    A["Usuario autenticado\n(Leer role desde AuthContext)"] --> B{Rol del Usuario}
    
    B -->|admin| C["Administrador\nPanel de Gestión visible\nBotones CRUD habilitados\nAcciones destructivas c/confirmación"]
    B -->|consultor| D["Consultor\nAcciones operativas (ej. añadir a blacklist)\nSin gestión de usuarios"]
    B -->|analista| E["Analista\nExportaciones (PDF/JSONL) habilitadas\nAnálisis ML habilitado\nSin config. de sistema"]
    B -->|directivo| F["Directivo / Solo Lectura\nBotones disabled\nTooltip: 'Solo lectura para tu rol'"]
    
    style C fill:#3fb950,color:#0d1117,stroke:#3fb950
    style D fill:#58a6ff,color:#0d1117,stroke:#58a6ff
    style E fill:#d4af37,color:#0d1117,stroke:#d4af37
    style F fill:#8b949e,color:#0d1117,stroke:#8b949e
```

**Ejemplo de componente RoleGuard:**
```jsx
// src/layout/RoleGuard.jsx
import { useContext } from 'react';
import { AuthContext } from '@/context/AuthContext';

export const RoleGuard = ({ allowedRoles, children, fallback = null }) => {
  const { user } = useContext(AuthContext);
  if (!user || !allowedRoles.includes(user.role)) return fallback;
  return children;
};
```
