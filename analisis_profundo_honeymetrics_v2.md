# 🔬 Análisis Exhaustivo de Datos Reales — HoneyMetrics v2.0

> **Base de datos analizada:** 165.247 eventos únicos | 5 meses consecutivos (Abril — Agosto 2026)  
> **Fuentes:** 22 archivos JSONL + API Wazuh Indexer en tiempo real  
> **Agentes monitoreados:** `srvotsub1`, `svm100`, `sprox1`, `wazuh.manager`

---

## 📊 Tabla Maestra: Lo que encontramos vs lo que podemos hacer

| Dimensión Analizada | Hallazgo Clave | Feature para v2.0 |
|---|---|---|
| Horario de ataques | Pico consistente 11-12 UTC todos los meses | Heatmap predictivo + alertas proactivas |
| Rotación de IPs | 9 IPs vuelven en 2-3 meses distintos | Threat Score dinámico + "Enemigos Recurrentes" |
| Diccionario SSH | 1.412 usuarios distintos probados, categorizados | Honeypot Advisor: "esto buscan hoy" |
| Botnets por subred | 4 subredes con 6-13 IPs coordinadas | Bloqueo automático por rango CIDR |
| Velocidad de ataque | Hasta 6.315 eventos/hora (un bot solo) | Detector de bots vs humanos real-time |
| CVEs | 2.516 CVEs únicos, 6.017 activos, 1.721 críticos | Panel de Priorización de Parches |
| FIM | 441 archivos con cambios, 50+ en rutas críticas | Timeline de integridad del sistema |
| Rootcheck | 1.139 detecciones de posibles troyanos en `/bin/passwd`, `/usr/bin/chsh` | Monitor de Troyanos con veredicto humano |
| MITRE ATT&CK | 8 tácticas mapeadas, la cadena de ataque real visible | Kill Chain Visualizer |
| SCA / Compliance | Score 45-50% en todos los agentes (reprobado CIS Benchmark) | Panel de Cumplimiento con plan de acción |
| Software (dpkg) | 156 paquetes con cambios, kernel actualizado 5 veces | Línea de tiempo de cambios de software |
| Correlación | Los meses de más CVEs activos NO coinciden con más ataques | Insight: las oleadas SSH son oportunistas, no dirigidas |
| Solo 49 reglas | De miles posibles en Wazuh, solo 49 se dispararon | Simplificación de UI: mostrar solo lo relevante |

---

## 1. 🕐 El Horario del Crimen: El Sistema Nunca Duerme

### Hallazgo real
Los ataques no son aleatorios. Cada mes sin excepción, el pico está en **11:00-12:00 UTC**:
- Abril: pico a las 11h con 11.987 eventos
- Mayo, Junio, Julio: pico a las 12h con 1.805 a 3.637 eventos

Los ataques bajan drásticamente de 18:00 a 00:00 UTC. Esto corresponde a zonas horarias de Europa del Este / Asia Central (donde el mediodía UTC es hora de trabajo).

### Por día de la semana (sorprendente)
- **Lunes: 40.062 eventos** (el día más atacado)
- Sábado/Domingo: ~13.000-9.000 (los bots también "descansan" más)
- Esto sugiere infraestructura botnet administrada por humanos que la activan durante la semana laboral.

### Feature v2.0: **Heatmap de Riesgo Temporal**
- Un calendario de calor (como GitHub contributions pero de amenazas) que muestre intensidad de ataques por hora y día de semana.
- **Alerta proactiva:** "Los lunes entre 11-12 UTC históricamente concentran el 28% de todos tus ataques. Activa reglas reforzadas automáticamente en ese horario."
- **Ventaja de negocio:** Ninguna herramienta open source de honeypot hace esto. Es diferenciador inmediato.

---

## 2. 🧟 Los Atacantes Persistentes: Los que Vuelven

### Hallazgo real
De 1.107 IPs externas únicas, **9 volvieron a atacar en meses distintos**:

| IP | Meses en que atacó | Nivel promedio |
|---|---|---|
| `45.227.254.170` | Abril, Junio, Julio | 5.5 |
| `45.148.10.151` | Abril, Junio, Julio | 5.5 |
| `45.148.10.141` | Abril, Junio, Julio | 5.5 |
| `45.148.10.147` | Abril, Junio, Julio | 5.5 |
| `2.57.122.238` | Abril, Junio | — |
| `75.111.120.108` | Abril, Junio | — |

El grupo `45.148.10.X` es claramente **una botnet coordinada** — múltiples IPs de la misma subred atacando en los mismos meses.

### Feature v2.0: **Threat Score Dinámico (0-100)**

La Blacklist actual es binaria (sí/no). El nuevo sistema calcula:

```
Threat Score = (Volumen × 0.3) + (Persistencia × 0.4) + (Severidad × 0.2) + (Variedad táctica × 0.1)

Ejemplo IP 45.148.10.151:
  Volumen: 1.172 eventos → 25 puntos
  Persistencia: 3 meses distintos → 40 puntos
  Severidad promedio 5.5 → 18 puntos
  Tácticas: Credential Access + Lateral Movement → 10 puntos
  TOTAL: 93/100 → "Amenaza Persistente Avanzada"
```

**Badge visual automático:** 🔴 APT / 🟠 Botnet / 🟡 Scanner / 🟢 Único

---

## 3. 🎯 El Diccionario de los Atacantes: Saben a Quién Buscan

### Hallazgo real: 1.412 usuarios únicos probados, clasificados por categoría

| Categoría | Intentos | Qué significa |
|---|---|---|
| Administración (`root`, `admin`) | **108.282** | Objetivo principal: tomar control total |
| Cloud/SaaS (`ubuntu`, `debian`, `centos`) | 3.350 | Buscan servidores cloud mal configurados |
| Usuarios genéricos (`user`, `test`, `guest`) | 5.946 | Diccionario básico automatizado |
| Software empresarial (`odoo`, `vpn`, `confluence`) | 552 | **Ataques dirigidos a empresas** |
| Bases de datos (`postgres`, `oracle`, `mysql`) | 981 | Buscan datos, no solo acceso |
| DevOps (`deploy`, `git`, `jenkins`, `gitlab`) | 978 | Buscan pipelines CI/CD para comprometer |
| Entretenimiento (`steam`, `minecraft`) | 558 | Buscan servidores de juego para usar como proxies |

**Dato alarmante:** Se encontraron usuarios probados **solo por una IP específica**:
- `ethereum` — probado solo por `2.57.122.238` (8 veces) → buscan wallets de cripto
- `dircreate` — probado solo por `87.251.64.149` (42 veces) → exploit específico
- `chia` — probado solo por `89.190.156.34` (24 veces) → otro minero de cripto

### Feature v2.0: **Honeypot Advisor — "Esto buscan hoy"**
- Panel que muestra en tiempo real qué tipo de usuario/servicio están intentando explotar los atacantes esta semana.
- Recomendación automática: *"Esta semana el 8% de los atacantes buscan acceso a `odoo`. Si tienes Odoo expuesto, te recomendamos verificar permisos y activar 2FA inmediatamente."*
- **Monetización:** Esta inteligencia es valiosa como suscripción semanal para empresas que tienen esos servicios expuestos.

---

## 4. 🕸️ Botnets: Enemigos Coordinados

### Hallazgo real: 4 botnets identificadas por patrón de subred

| Subred | Eventos | IPs coordinadas | Característica |
|---|---|---|---|
| `2.57.122.0/24` | 9.394 | **13 IPs** | La botnet más diversa y coordinada |
| `87.251.64.0/24` | 8.454 | 6 IPs | Cada IP prueba 84-323 usuarios distintos |
| `45.148.10.0/24` | 5.613 | 7 IPs | **Persistente en 3 meses** — APT |
| `2.57.121.0/24` | 5.555 | 7 IPs | Coordina con `2.57.122.X` (mismo /16) |

La botnet `87.251.64.X` es especialmente sofisticada: una sola IP de esa red probó **323 usuarios distintos** en 1.998 intentos — tiene el diccionario más completo.

### Feature v2.0: **Detección Automática de Botnets**
- Cuando 3+ IPs de la misma subred /24 atacan en la misma ventana de tiempo → alerta automática de "Posible botnet coordinada".
- Sugerencia automática de bloqueo CIDR: *"Detectamos coordinación entre 7 IPs en `45.148.10.0/24`. ¿Bloquear el rango completo?"*
- El analista aprueba con un clic → se registra en la Blacklist v2 con categoría "Botnet confirmada".

---

## 5. ⚡ Velocidad de Ataque: Midiendo la Agresividad

### Hallazgo real: Bots de hasta 6.315 eventos/HORA

| IP | Velocidad | Total eventos | Ventana activa |
|---|---|---|---|
| `200.69.204.22` | **6.315 ev/hora** | 1.703 | Solo 0.3 horas (18 min) |
| `177.101.164.50` | 3.593 ev/hora | 1.718 | 0.5 horas |
| Grupo Vietnam (`116.99.X`, `116.110.X`) | ~2.400 ev/hora | ~140 c/u | 0.1 horas (6 min) |

La IP `200.69.204.22` disparó **~100 intentos por minuto** durante 18 minutos y desapareció. Eso es un ataque de barrido automatizado ultra-agresivo.

### Feature v2.0: **Clasificador Bot vs Humano**
- Un bot tiene velocidad > 100 ev/hora. Un humano nunca puede pasar de 10-20.
- Clasificación automática en la UI: 🤖 Bot automatizado / 🧑 Ataque manual dirigido
- Los ataques manuales son **MÁS PELIGROSOS** aunque sean menos en volumen — el analista debe priorizarlos.

---

## 6. 🐛 Las 1.721 Vulnerabilidades Que No Han Sido Parchadas

### Hallazgo real: Sistema bajo ataque con CVEs críticos activos hace meses

**2.516 CVEs únicos detectados. 6.017 eventos de CVEs activos (sin parche). 1.721 son Críticos o Altos (score ≥ 7.0).**

Los CVEs más graves tienen score **9.8/10** en el kernel de Linux — la pieza más crítica del sistema operativo.

Lo más preocupante: **1.915 CVEs aparecen en múltiples meses** (abril, mayo, junio, julio) — llevan 4 meses sin parcharse.

| CVE | Presente desde | Score | Paquete afectado |
|---|---|---|---|
| `CVE-2022-25837` | Abril → Julio (4 meses) | Alto | Kernel Linux |
| `CVE-2020-14304` | Abril → Julio (4 meses) | Alto | Kernel Linux |
| `CVE-2026-23241` | Abril → Julio (4 meses) | Crítico | Kernel Linux |

### Feature v2.0: **Panel de Priorización de Parches (Patch Intelligence)**

El dolor número uno de los equipos de TI es que tienen miles de vulnerabilidades y no saben por cuál empezar. HoneyMetrics resuelve eso cruzando dos fuentes:

```
CVE activo en tus servidores + Atacante intentando explotarlo = PRIORIDAD 1
CVE activo sin actividad atacante relacionada = PRIORIDAD 3
```

**El dashboard mostraría:**
- 🔴 **Parchar HOY:** CVEs con score ≥ 9 que llevan >30 días activos
- 🟠 **Esta semana:** CVEs con score 7-8.9
- 🟡 **Este mes:** CVEs con score < 7

**Monetización:** Esta pantalla sola justifica un tier Enterprise. Los equipos de TI en empresas medianas pagarían por un reporte semanal automático de "qué parchar primero".

---

## 7. 📁 El Sistema por Dentro: FIM y Rootcheck

### Hallazgo real: 50+ archivos críticos del SO cambiaron

Los 1.716 eventos FIM muestran cambios en archivos que deberían ser inmutables:
- `/boot/vmlinuz` (el kernel del sistema) — cambió **5 veces**
- `/usr/bin/openssl` — cambió **3 veces**
- `/usr/bin/curl` — cambió **3 veces**  
- `/usr/bin/sshd` — cambió **2 veces**

> ⚠️ Algunos de estos cambios son actualizaciones legítimas del sistema (dpkg lo corrobora). Pero `/usr/bin/sshd` cambiando 2 veces en un honeypot que está siendo atacado activamente es algo que un analista debe verificar manualmente.

### Hallazgo Rootcheck: Troyanos detectados en binarios básicos

El sistema detectó repetidamente firmas de troyanos en:
- `/bin/passwd` — **195 detecciones**
- `/usr/bin/chsh` — **191 detecciones**
- `/usr/bin/chfn` — **188 detecciones**

Wazuh usa comparación de firmas para detectar versiones "troyanizadas" de estos binarios. La pregunta para el analista: ¿son falsos positivos (firmas desactualizadas) o compromisos reales?

### Feature v2.0: **Timeline de Integridad del Sistema**

Una línea de tiempo cronológica que correlaciona:
1. Cuándo llegó un ataque externo
2. Cuándo cambió un archivo del sistema después
3. Si hay un CVE relacionado con ese binario

Si los tres coinciden en el tiempo → **alerta roja correlacionada**: "Posible compromiso post-explotación".

---

## 8. 🛡️ El Diagnóstico de Cumplimiento: Reprobado

### Hallazgo real: Score CIS Benchmark 45-50% en todos los agentes

| Fecha | Agente | Score | Pasó | Falló |
|---|---|---|---|---|
| 2026-04-02 | `srvotsub1` | 45% 🔴 | 83/207 | 101 |
| 2026-07-12 | `svm100` | 47% 🔴 | 112/279 | 125 |
| 2026-07-28 | `svm100` | 47% 🔴 | 112/279 | 125 |
| 2026-08-11 | `svm100` | 47% 🔴 | 113/279 | 124 |

**El mismo servidor falló el mismo CIS Benchmark con casi los mismos números durante 4 meses.** Nadie está revisando ni actuando sobre estas recomendaciones.

### Feature v2.0: **Panel de Cumplimiento con Plan de Acción**

En lugar de solo mostrar "47% — Reprobado", HoneyMetrics v2 muestra:
- Las **top 10 fallas más críticas** con instrucción exacta de cómo corregirla
- Tracking de progreso: si el score sube de 47% a 52%, la UI lo celebra
- Exportable como **reporte de auditoría PDF** para presentar al área de seguridad
- **Monetización:** Las empresas pagan por demostrar cumplimiento ante auditores (ISO 27001, SOC2, PCI-DSS). Un reporte automático de CIS Benchmark bien formateado vale dinero.

---

## 9. 🔗 La Correlación Más Valiosa: El Kill Chain Completo

Con todos los datos juntos, podemos reconstruir la **cadena de ataque (Kill Chain)** completa:

```
RECONOCIMIENTO           ARMAMENTO        ENTREGA           EXPLOTACIÓN        POST-EXPLOTACIÓN
─────────────────────────────────────────────────────────────────────────────────────────────────
Bot escanea puertos  →  Diccionario SSH → Intento brute   → CVE en kernel   → Modifica /bin/passwd
(Discovery: L3)          de 1.412 users   force masivo      activo sin parche  (FIM + Rootcheck)
                                          (Credential Access) (Vulnerability)   (Defense Evasion)
                                              ↓
                                         Si entra:
                                         SSH lateral movement
                                         entre VMs (Lateral Movement)
```

### Feature v2.0: **Kill Chain Visualizer**

Una pantalla interactiva que muestra, para una IP seleccionada, todo el recorrido que intentó hacer:
- Qué hora empezó a escanear
- Qué usuarios probó y en qué orden
- Si tuvo éxito en algún intento (y cuándo)
- Si después de entrar hay evidencia FIM o Rootcheck correlacionada

Esto transforma a HoneyMetrics de "lector de logs" en **"narrador forense de ataques"** — una capacidad que solo tienen herramientas enterprise como Darktrace o CrowdStrike.

---

## 🗺️ Roadmap de Features para HoneyMetrics v2.0

### Tier Gratuito (fidelización y adquisición)
| # | Feature | Fuente de Datos | Esfuerzo |
|---|---|---|---|
| F1 | Dashboard básico de eventos (lo que ya existe) | sshd/pam | Ya implementado |
| F2 | Heatmap de ataques por hora y día de semana | @timestamp | Bajo |
| F3 | Top 10 IPs atacantes con categoría (Bot/Humano/Botnet) | srcip + velocidad | Medio |
| F4 | Kill Chain básico por IP | MITRE + timestamp | Medio |

### Tier Pro (suscripción individual ~$15-30/mes)
| # | Feature | Fuente de Datos | Esfuerzo |
|---|---|---|---|
| P1 | Threat Score dinámico (0-100) con historial | Multi-campo | Medio |
| P2 | Detección automática de botnets por subred CIDR | srcip clustering | Medio |
| P3 | Timeline de integridad del sistema (FIM correlacionado) | syscheck + dpkg + CVE | Alto |
| P4 | Panel de Cumplimiento CIS Benchmark con plan de acción | SCA data | Medio |
| P5 | Honeypot Advisor: "esto buscan esta semana" | users_tried + mitre | Bajo |

### Tier Enterprise (contrato anual ~$200-500/mes por organización)
| # | Feature | Fuente de Datos | Esfuerzo |
|---|---|---|---|
| E1 | Panel de Priorización de Parches (CVE activo + ataque correlacionado) | vulnerability + sshd | Alto |
| E2 | Kill Chain Visualizer completo e interactivo | Todos los decoders | Alto |
| E3 | Reportes PDF automáticos firmados para auditorías | Todos | Medio |
| E4 | API de Threat Intelligence (exportar lista de IPs peligrosas) | ip_events + scoring | Alto |
| E5 | Alertas predictivas: "el lunes habrá pico de ataques" | Time series ML | Muy Alto |

---

## ✅ Conclusión: Lo que HoneyMetrics puede hacer que nadie más hace gratis

1. **Correlacionar el momento del ataque externo con cambios internos del sistema** — eso es forense real.
2. **Puntuar la peligrosidad de un atacante considerando su historial de meses** — no solo el evento de hoy.
3. **Decirle al administrador qué parchar PRIMERO** cruzando CVEs activos con actividad de ataque.
4. **Mostrar que el compliance CIS está fallando** de forma accionable, no solo como número.
5. **Identificar ataques dirigidos** (usuarios custom por IP única) vs ataques genéricos de diccionario.

Ninguna de estas capacidades está disponible en herramientas open source gratuitas. Todas están documentadas con datos reales de tus propios logs.
