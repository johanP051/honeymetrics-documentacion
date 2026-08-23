# 🚫 Reglas Inquebrantables del Director de Proyecto (Scrum & Product)

Estas son las reglas supremas que gobiernan la redacción técnica en este repositorio. Su incumplimiento significa el rechazo automático del entregable.

1. **Cero Sesgo Técnico en el Backlog:** Jamás escribas el "CÓMO" (bases de datos, endpoints, librerías) en la hoja de Product Backlog. Solo se redacta el "QUÉ" y el valor de negocio.
2. **Desacoplamiento de CRUDs:** Prohibido hacer un CRUD completo en una sola Historia de Usuario. Debe partirse en "Listar", "Crear", "Editar" y "Eliminar".
3. **Criterios de Aceptación Gherkin:** Prohibidos los bullet points libres. Todo criterio es: `Dado que... Cuando... Entonces...`.
4. **Estimación Fibonacci:** Solo se acepta `1, 2, 3, 5, 8, 13, 21`. HU mayores a 13 puntos deben rebanarse (Vertical Slicing).
5. **Diagramación Viva:** Toda arquitectura, flujo o entidad-relación DEBE ser dibujada mediante código (Mermaid.js). Las imágenes estáticas solo se permiten para mockups de Interfaz de Usuario.
