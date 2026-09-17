# IaaS - Infrastructure as a Service (Proyecto Cloud Computing)

## Descripción

Este proyecto es un ejercicio de la asignatura de **Cloud Computing** cursada en 4º de grado en la rama de Computación. Se trata de la implementación de una plataforma completa de **Infraestructura como Servicio (IaaS)** que permite gestionar recursos de virtualización a través de una API REST y una interfaz de línea de comandos (CLI).

El sistema permite a los usuarios administrar hosts físicos, imágenes de máquinas virtuales y VM (máquinas virtuales), con un sistema de permisos y autenticación basado en tokens.

---

## Objetivos del Proyecto

- Comprender y aplicar los conceptos de **Cloud Computing** y **IaaS** en un escenario práctico.
- Implementar un sistema de gestión de virtualización completo utilizando **libvirt**, **Ansible**, **NFS** y **qemu/KVM**.
- Diseñar y desarrollar una **API RESTful** con Flask para la interacción con el sistema.
- Implementar un sistema de **autenticación y autorización** basado en tokens cifrados.
- Gestionar **permisos granulares** sobre recursos (imágenes y VMs) entre usuarios.
- Utilizar **Ansible** para la automatización del despliegue y configuración de infraestructura.
- Trabajar con bases de datos **SQLite** para el almacenamiento persistente de metadatos.

---

## Arquitectura

El proyecto sigue una arquitectura en capas:

| Capa | Módulo | Descripción |
|------|--------|-------------|
| **CLI** | `cli.py` | Interfaz de línea de comandos que envía peticiones HTTP a la API REST |
| **API REST** | `iaas_rest.py` | Servidor Flask con endpoints REST para todos los recursos |
| **Lógica de Negocio** | `iaas.py` | Autenticación, autorización, gestión de usuarios y reglas de negocio |
| **Núcleo (Core)** | `core.py` | Operaciones de bajo nivel: libvirt, Ansible, gestión de archivos |
| **Infraestructura** | `plays/` | Playbooks de Ansible para provisión de hosts y configuración del IaaS |
| **Base de Datos** | `iaas.db` | Base de datos SQLite con tablas para hosts, VMs, imágenes, usuarios y permisos |
| **Plantillas** | `template.xml` | Plantilla XML de libvirt para definición de VMs |

---

## Componentes y Funcionalidades

### 1. Usuarios (`iaas.py` / `cli.py`)
- **Registro y autenticación** de usuarios con email y contraseña.
- Sistema de **roles**: usuario normal y administrador (`root` por defecto).
- Los administradores pueden crear, eliminar y actualizar usuarios.
- Sistema de **cuotas** por usuario.
- Autenticación basada en **tokens cifrados** (usando la librería `cryptocode`).

### 2. Hosts (`core.py` / `iaas.py`)
- Añadir, eliminar, actualizar y listar hosts físicos.
- Los hosts son gestionados mediante **Ansible** y accesibles a través de **libvirt** vía SSH.
- Preparación automática de hosts con el playbook `host_add.yaml` (instalación de Libvirt, NFS, montaje de directorios compartidos).

### 3. Imágenes (`core.py` / `iaas.py`)
- **Añadir imágenes** descargándolas de una URL remota.
- **Guardar una VM como imagen** (snapshot del disco).
- Eliminar imágenes.
- Sistema de **compartición** de imágenes entre usuarios con permisos granulares.
- Las imágenes se almacenan en formato **qcow2** en `/export/iaas/images/`.

### 4. Máquinas Virtuales (`core.py` / `iaas.py`)
- **Crear VMs** a partir de una imagen existente, seleccionando un host automáticamente.
- **Arrancar** y **parar** VMs mediante libvirt.
- **Eliminar VMs** (con eliminación del disco y definición del dominio).
- **Guardar una VM como nueva imagen**.
- **Compartir VMs** con otros usuarios.
- Las VMs se definen con la plantilla `template.xml` y se gestionan con libvirt.
- Memoria configurable (por defecto 256 MB).

### 5. Compartición de Recursos
- Compartir y dejar de compartir imágenes y VMs con otros usuarios.
- Listar los permisos sobre un recurso específico.
- Control de acceso basado en permisos almacenados en la tabla `perms` de SQLite.
- Los administradores tienen acceso ilimitado a todos los recursos.

### 6. Infraestructura con Ansible
- **`plays/iaas_init.yaml`**: Instala paquetes (libvirt, NFS), crea directorios, configura el export NFS.
- **`plays/iaas_destroy.yaml`**: Deshace la configuración del IaaS.
- **`plays/host_add.yaml`**: Prepara un host remoto (instala Libvirt, NFS, monta el repositorio compartido).
- **`plays/host_remove.yaml`**: Elimina la configuración de un host.

---

## Endpoints REST

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/iaas/sessions` | Iniciar sesión (obtener token) |
| POST | `/iaas/users` | Crear usuario |
| GET | `/iaas/users` | Listar usuarios |
| PUT | `/iaas/users/<userId>` | Actualizar usuario |
| DELETE | `/iaas/users/<userId>` | Eliminar usuario |
| POST | `/iaas/hosts` | Añadir host |
| GET | `/iaas/hosts` | Listar hosts |
| PUT | `/iaas/hosts/<hostId>` | Actualizar host |
| DELETE | `/iaas/hosts/<hostId>` | Eliminar host |
| POST | `/iaas/images` | Añadir imagen |
| GET | `/iaas/images` | Listar imágenes |
| DELETE | `/iaas/images/<imgId>` | Eliminar imagen |
| PUT | `/iaas/images/<vmId>` | Guardar VM como imagen |
| POST | `/iaas/images/<imgId>/shares` | Compartir imagen |
| GET | `/iaas/images/<imgId>/shares` | Listar permisos de imagen |
| DELETE | `/iaas/images/<imgId>/shares/<userId>` | Dejar de compartir imagen |
| POST | `/iaas/vms` | Crear VM |
| GET | `/iaas/vms` | Listar VMs |
| PUT | `/iaas/vms/<vmId>` | Arrancar/parar VM |
| DELETE | `/iaas/vms/<vmId>` | Eliminar VM |
| POST | `/iaas/vms/<vmId>/shares` | Compartir VM |
| GET | `/iaas/vms/<vmId>/shares` | Listar permisos de VM |
| DELETE | `/iaas/vms/<vmId>/shares/<userId>` | Dejar de compartir VM |

---

## Estructura de la Base de Datos

La base de datos SQLite (`iaas.db`) contiene las siguientes tablas:

### Tabla `users`
- `id` (varchar) - Identificador único
- `email` (varchar) - Correo electrónico
- `password` (varchar) - Contraseña
- `quota` (text) - Cuota del usuario (JSON)
- `admin` (int) - Rol de administrador (0 o 1)

### Tabla `hosts`
- `id` (varchar) - Identificador único
- `addr` (varchar) - Dirección IP
- `user` (varchar) - Usuario SSH
- `password` (varchar) - Contraseña SSH

### Tabla `Vms`
- `id` (varchar) - Identificador único
- `image` (varchar) - ID de la imagen base
- `mem` (int) - Memoria en KiB
- `state` (varchar) - Estado (`running`/`stopped`)
- `host` (varchar) - ID del host donde corre

### Tabla `images`
- `id` (varchar) - Identificador único
- `name` (varchar) - Nombre de la imagen
- `description` (text) - Descripción

### Tabla `perms`
- `user` (varchar) - ID del usuario con permiso
- `resource` (varchar) - ID del recurso
- `type` (varchar) - Tipo de recurso (`image` o `vm`)

---

## Tecnologías Utilizadas

- **Python 3** - Lenguaje de programación principal
- **Flask** - Framework web para la API REST
- **SQLite** - Base de datos relacional ligera
- **libvirt** - API de virtualización para gestionar VMs
- **Ansible** - Automatización de infraestructura y configuración
- **NFS** - Sistema de ficheros en red para almacenamiento compartido
- **qemu/KVM** - Hipervisor para ejecución de máquinas virtuales
- **cryptocode** - Cifrado de tokens de autenticación
- **colorama** - Colores en la salida de la CLI
- **requests** - Cliente HTTP para la CLI

---

## Instalación y Ejecución

### Requisitos previos
- Python 3.8+
- Virtualenv
- Libvirt instalado en el sistema
- Acceso a servidores con SSH para los hosts

### Configuración del entorno virtual
```bash
source venv/bin/activate
```

### Iniciar el servidor REST
```bash
flask --app iaas_rest --debug run
```

### Iniciar la CLI
```bash
python3 cli.py
```

> **Nota**: Antes de ejecutar, es necesario desactivar el proxy si está configurado:
> ```bash
> unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
> ```

### Inicialización del IaaS
Si no existe la base de datos, el sistema se inicializa automáticamente al ejecutar `cli.py`:
```bash
python3 cli.py
```
Esto invoca `iaas.init()` que crea las tablas y ejecuta el playbook `iaas_init.yaml` mediante Ansible.

---

## Uso de la CLI (Ejemplos)

```bash
# Login
login root root

# Gestión de hosts
host ls
host add 172.23.184.138 alumno alumnonodo2
host rm <hostId>

# Gestión de usuarios
user ls
user add email@example.com password123
user rm <userId>

# Gestión de imágenes
image add <url> <nombre> <descripcion>
image ls
image rm <imgId>

# Gestión de VMs
vm ls
vm add <imageId> [<memoria_en_KiB>]
vm start <vmId>
vm stop <vmId>
vm rm <vmId>
vm save <vmId> <nombreImg> <descripcion>

# Compartición
image share <imgId> <userEmail>
vm share <vmId> <userEmail>
image shares <imgId>
vm shares <vmId>
```

---

## Estructura de Archivos

```
UNI-CC-project1/
├── cli.py              # Interfaz de línea de comandos
├── iaas.py             # Capa de lógica de negocio
├── core.py             # Núcleo: operaciones de virtualización
├── iaas_rest.py        # API REST con Flask
├── rest.py             # API REST alternativa (incompleta)
├── template.xml        # Plantilla XML de libvirt para VMs
├── iaas.db             # Base de datos SQLite
├── venv/               # Entorno virtual de Python
├── plays/              # Playbooks de Ansible
│   ├── iaas_init.yaml
│   ├── iaas_destroy.yaml
│   ├── host_add.yaml
│   └── host_remove.yaml
├── tests/              # Tests del proyecto
│   ├── core/
│   ├── iaas/
│   └── rest/
└── README.md
```

---

## Licencia

Proyecto académico para la asignatura de Cloud Computing, 4º de Grado en Computación.
