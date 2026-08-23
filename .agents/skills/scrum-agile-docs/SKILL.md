---
name: scrum-agile-docs
description: >-
  Skill maestra de documentación viva en Scrum y MkDocs. Gobierna la creación del Product Backlog, 
  Slicing de Historias de Usuario, criterios BDD con Gherkin, y diagramación arquitectónica en Mermaid.js.
---

# 📖 Scrum & MkDocs Agile Standards (HoneyMetrics Docs)

Esta Skill define las reglas estrictas de redacción técnica, levantamiento de requerimientos y diagramación requeridas por el Director de Proyecto. Todo agente o desarrollador que altere la documentación debe acatar esto.

---

## 1. 🎯 Product Backlog Sin Sesgo Técnico
- **Enfoque de Negocio:** Queda **estrictamente prohibido** redactar el backlog en términos técnicos ("Implementar endpoint", "Crear tabla alerts").
- **Regla del "QUÉ" y no el "CÓMO":** Las descripciones del backlog deben expresar valor. Ej: *"El usuario debe poder solicitar la extracción de eventos y ser notificado cuando el archivo esté listo."*
- **Priorización:** Las Historias de Usuario se priorizan exclusivamente por el impacto real y el valor de negocio, nunca por la complejidad técnica de su implementación subyacente.

---

## 2. 🔪 Slicing Obligatorio (CRUD Dividido)
- **Prohibición de Macro-Historias:** Queda **prohibido** agrupar operaciones CRUD enteras en una sola HU (Ej: "HU-01: Gestionar usuarios").
- **División Atómica:** Todo módulo CRUD debe dividirse en 4 historias independientes: Listar, Crear, Editar, Eliminar.
- **Sintaxis Canónica Obligatoria:** 
  `Como <Rol> Quiero <Acción> Para <Beneficio de negocio>`
- **Desglose Técnico:** Dentro de la HU, en la sección de "Tareas de Desarrollo", se deben enumerar los detalles técnicos (Backend, Frontend, BD) necesarios para cumplir la historia.

---

## 3. 🎲 Estimaciones (Fibonacci Strict)
- Las estimaciones de Story Points solo pueden usar la **Serie de Fibonacci**: `1, 2, 3, 5, 8, 13, 21`.
- Si una Historia de Usuario supera los **13 Story Points**, se considera una "Épica encubierta" y **debe ser descompuesta** obligatoriamente en historias más pequeñas (Vertical Slicing).

---

## 4. 🧪 Behavior-Driven Development (Gherkin)
- Todos los Criterios de Aceptación dentro de una Historia de Usuario DEBEN seguir el patrón Gherkin:
  ```gherkin
  Dado que <contexto previo / estado del sistema>
  Cuando <el usuario realiza una acción>
  Entonces <resultado observable, medible y verificable>
  ```
- **Escenarios Mínimos:** Cada HU debe contar con al menos 2 escenarios BDD: El "Happy Path" (flujo ideal) y un "Error/Exception Path" (flujo alternativo de falla controlada).
- **Prohibido:** Redactar criterios de aceptación como simples bullet points genéricos sin estructura.

---

## 5. 🗺️ Diagramación Arquitectónica (Mermaid.js)
- **Cero Imágenes Estáticas:** Queda estrictamente prohibido usar imágenes PNG/JPG para diagramar arquitectura dentro de los archivos Markdown de MkDocs. Las imágenes (`/mockups/`) solo se usan para referencias visuales de UI.
- **Uso Obligatorio de Mermaid.js:**
  - **Diagramas de Secuencia:** Usar `sequenceDiagram` asegurando el tag `autonumber`.
  - **Flujos de Proceso:** Usar `flowchart TD` (Top-Down) o `flowchart LR` (Left-Right).
  - **Modelos Entidad-Relación:** Usar `erDiagram`.
  - **Máquinas de Estado:** Usar `stateDiagram-v2`.

---

## 6. 📁 Estructura de MkDocs
- Toda documentación estructurada debe seguir la jerarquía definida en el archivo raíz `mkdocs.yml`.
- Los sprints y las Historias de Usuario se alojan en `docs/sprints/`.
- Los diagramas de arquitectura en Mermaid se documentan centralizadamente en `docs/arquitectura/`.
