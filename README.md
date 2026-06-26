# Mi Proyecto Flask - Sistema de Gestión Organizacional

## Descripción General

Este proyecto es una aplicación web desarrollada con **Flask (Python)** que permite gestionar información organizacional, administrar usuarios, generar reportes y visualizar indicadores clave. La plataforma está diseñada para ser escalable, segura y de alta disponibilidad, utilizando **HTML** para el frontend, **GitHub** para control de versiones y **Render** como plataforma de despliegue en la nube.

---

## Tecnologías Utilizadas

| Categoría          | Tecnología |
|--------------------|------------|
| **Backend**        | Flask (Python) |
| **Frontend**       | HTML, CSS (opcional), JavaScript (opcional) |
| **Control de Versiones** | GitHub |
| **Despliegue**     | Render (PaaS) |
| **Gestión de Dependencias** | requirements.txt |

---

## Características Principales

### Módulo de Autenticación y Usuarios
- Registro, actualización y desactivación de usuarios.
- Control de sesiones (login, logout, tiempo de inactividad).
- Asignación de perfiles y permisos según el rol.

### Gestión de Información
- Registro, modificación y desactivación de registros organizacionales.
- Filtros de búsqueda con múltiples criterios.
- Visualización de datos según permisos del usuario.

### Reportes e Indicadores
- Generación de reportes en formato PDF y Excel.
- Dashboard con indicadores actualizados cada 5 minutos.
- Exportación de reportes en formatos estándar.

### Auditoría y Seguridad
- Bitácora de eventos y cambios realizados.
- Historial de modificaciones por registro.

### Despliegue y Respaldo
- Aplicación desplegada en Render con disponibilidad del 99.5%.
- Respaldo automático diario de la base de datos.
- Recuperación de información desde respaldos en menos de 30 minutos.

---

## Estructura del Proyecto
