---
name: session-handoff-and-context-continuity
description: >-
  Protocolo de compactación de memoria, persistencia en Engram/project_state.json y
  generación automatizada de prompts de transferencia (Handoff Snapshots) para reanudar
  sesiones en chats limpios sin pérdida de contexto, sin alucinaciones y sin fatiga de tokens.
---

# 🔁 Session Handoff, Memory Compaction & Context Continuity Standard

## 1. Propósito y Principio de Cero Fricción
Esta skill previene la **degradación de contexto (*Context Rot*)** cuando una sesión de desarrollo se vuelve extensa. Compacta el estado exacto de ingeniería en un artefacto denso ($\le 1.500\text{ tokens}$) para transferir el 100% del contexto a una nueva sesión (AI Studio, OpenCode, Codex o Antigravity).

## 2. Disparadores de Activación
1. **Explícito:** Cuando el usuario pida *"nuevo chat"*, *"prepara el handoff"*, *"dame el prompt de reanudación"* o *"el chat está muy largo"*.
2. **Al Cerrar un Gate o Bloque de Commits:** Actualizar proactivamente el estado en disco.

## 3. Persistencia Local (Puente Engram + Orchestrator)
Al generar un handoff o cerrar un bloque, el agente DEBE:
1. Registrar la memoria en Engram (si la herramienta está disponible en el entorno).
2. Actualizar `.agents/orchestrator/project_state.json` con rama, commit, tests y pendientes.
3. Escribir el prompt de reanudación en `.agents/orchestrator/prompt_reanudacion.md`.

## 4. Los 5 Bloques Obligatorios del Handoff Snapshot
1. **Estado de Git y Entorno Real:** Repositorio, rama activa, último commit (`git log -1 --oneline`) y estado de `git status --short`.
2. **Quality Gates y Pruebas Verificadas:** Conteo exacto de tests (`pytest`, Vitest/Node), SAST (`bandit`, `pip-audit`, `npm audit`) y builds.
3. **Decisiones Técnicas Tomadas (ADRs en Caliente):** Decisiones ya acordadas que la nueva sesión NO debe reabrir ni revertir.
4. **Próximos 3 Pasos Inmediatos:** Lista numerada con rutas exactas de archivos y acciones concretas.
5. **Instrucción de Arranque:** Bloque listo para copiar y pegar en el nuevo chat.

## 5. Plantilla Canónica del Prompt de Reanudación (`prompt_reanudacion.md`)
```markdown
# 🚀 PROMPT DE REANUDACIÓN DE SESIÓN (HANDOFF CANÓNICO)

## 1. Identidad y Estado de Git
- Repositorio: <nombre>
- Rama activa: <branch>
- Último commit: <hash> - <mensaje>
- Estado de working tree: <clean | archivos pendientes>

## 2. Quality Gates y Verificación Técnica
- Tests unitarios/integración: <X aprobados, 0 fallidos>
- SAST / Auditoría de Seguridad: <Bandit 0 / pip-audit 0 / npm audit 0>
- Build de producción: <Aprobado>

## 3. Decisiones Arquitectónicas Cerradas (No Reabrir)
- <Decisión 1>
- <Decisión 2>

## 4. Próximos 3 Pasos Inmediatos
1. <Paso 1 con ruta exacta de archivo>
2. <Paso 2 con ruta exacta de archivo>
3. <Paso 3 con comando o verificación esperada>

## 5. Instrucción Inmediata para el Agente
Lee este estado, valida `git status` y procede directamente con el Paso 1 sin hacer resúmenes innecesarios.
```

## 6. Gobernanza de Engram y Prevención de Fatiga Cognitiva (Memorias Canónicas)

- **Prohibición de Acumulación de Memorias Sueltas:** No crear una memoria nueva en Engram por cada comando menor. Mantener y actualizar **Memorias Canónicas por Proyecto/Dominio** (ej. una única memoria maestra para la topología de red e infraestructura de cada repositorio), consolidando o marcando como obsoletas las versiones anteriores.
- **Documentación al Lado del Código (*Close-to-Code*):** Mantener la información crítica de puertos, túneles y arranque en `INFRASTRUCTURE.md` y en comentarios claros dentro de `.env.example` para que el desarrollador no dependa de buscar en decenas de notas externas de Obsidian.
