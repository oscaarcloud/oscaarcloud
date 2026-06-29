# Implementación de Etiquetado Automático con Azure Function y Event Grid

## Objetivo

Automatizar el etiquetado de recursos creados en Azure usando **Azure Function**, **Event Grid** y **Managed Identity**.

Tags automáticos implementados:

- `CreateDate`
- `Subscription`
- `Location`

---

## Arquitectura

```text
Usuario crea recurso
        ↓
Azure Resource Manager
        ↓
Resource Write Success
        ↓
Azure Event Grid
        ↓
Azure Function en Python
        ↓
Azure Resource Manager
        ↓
Actualización automática de tags
```

---

## Herramientas utilizadas

| Herramienta | Propósito |
|---|---|
| Visual Studio Code | Desarrollo local de la Azure Function |
| Azure Functions Extension | Gestión y despliegue de Azure Functions |
| Azure Functions Core Tools | Creación y ejecución local de Azure Functions |
| Azure CLI | Administración de Azure por línea de comandos |
| Python 3.13 | Lenguaje utilizado |
| Microsoft Entra ID | Gestión de identidad y permisos |
| Azure Event Grid | Detección de creación de recursos |
| Azure Function | Automatización del etiquetado |
| Azure Resource Manager | Consulta y actualización de recursos |
| Azure Policy | Gobernanza y validación de tags |

---

## 1. Creación de Azure Function App

Configuración usada:

| Parámetro | Valor |
|---|---|
| Hosting Plan | Flex Consumption |
| Runtime | Python |
| Versión | Python 3.13 |
| Sistema Operativo | Linux |
| Región | Central US |
| Nombre | `func-auto-tag` |

---

## 2. Habilitar Managed Identity

Ruta:

```text
Function App
→ Identity
→ System Assigned
→ On
```

Esto permite que la Function se autentique sin guardar credenciales en el código.

---

## 3. Asignar permisos RBAC

Ruta:

```text
Subscription
→ Access Control (IAM)
→ Add Role Assignment
```

Roles asignados:

| Rol | Propósito |
|---|---|
| Reader | Leer propiedades del recurso |
| Tag Contributor | Crear y modificar tags |

Alcance usado:

```text
Subscription 1
```

---

## 4. Registrar Microsoft.EventGrid

Comando:

```powershell
az provider register --namespace Microsoft.EventGrid
```

Verificación:

```powershell
az provider show --namespace Microsoft.EventGrid --query registrationState -o table
```

Resultado esperado:

```text
Registered
```

---

## 5. Instalación y verificación de herramientas

### Azure CLI

```powershell
az --version
az login
```

### Azure Functions Core Tools

```powershell
func --version
```

### Python

```powershell
python --version
```

Resultado esperado:

```text
Python 3.13.x
```

Extensiones usadas en VS Code:

- Azure Functions
- Azure Resources
- Python

---

## 6. Crear proyecto local en VS Code

```powershell
func init . --python
```

Luego:

```powershell
func new
```

Template seleccionado:

```text
EventGridTrigger
```

Nombre de la Function:

```text
createDateTag
```

---

## 7. Dependencias

Archivo:

```text
requirements.txt
```

Contenido:

```txt
azure-functions
azure-identity
azure-mgmt-resource
azure-mgmt-subscription
```

---

## 8. Código de la Function

Archivo:

```text
function_app.py
```

Código:

```python
import logging
import json
import azure.functions as func

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.resource.resources.models import TagsPatchResource

app = func.FunctionApp()
credential = DefaultAzureCredential()


def extract_subscription_id(resource_id: str) -> str:
    parts = resource_id.split("/")
    return parts[parts.index("subscriptions") + 1]


def get_subscription_name(subscription_id: str) -> str:
    try:
        sub_client = SubscriptionClient(credential)
        sub = sub_client.subscriptions.get(subscription_id)
        return sub.display_name
    except Exception:
        return subscription_id


@app.event_grid_trigger(arg_name="event")
def createDateTag(event: func.EventGridEvent):
    data = event.get_json()

    resource_id = data.get("resourceUri")

    if not resource_id:
        return

    subscription_id = extract_subscription_id(resource_id)

    resource_client = ResourceManagementClient(
        credential,
        subscription_id
    )

    resource = resource_client.resources.get_by_id(
        resource_id,
        api_version="2021-04-01"
    )

    create_date = event.event_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    subscription_name = get_subscription_name(subscription_id)
    location = resource.location or "Global"

    tags = {
        "CreateDate": create_date,
        "Subscription": subscription_name,
        "Location": location
    }

    tag_patch = TagsPatchResource(
        operation="Merge",
        properties={
            "tags": tags
        }
    )

    resource_client.tags.begin_update_at_scope(
        scope=resource_id,
        parameters=tag_patch
    ).result()
```

---

## 9. Publicar la Function

Iniciar sesión:

```powershell
az login
```

Publicar:

```powershell
func azure functionapp publish func-auto-tag
```

Resultado esperado:

```text
Deployment successful
```

---

## 10. Configurar Event Grid

Ruta:

```text
Subscription
→ Events
→ Event Subscription
```

Configuración usada:

| Campo | Valor |
|---|---|
| Name | `AutoTagCreateDate` |
| Topic Type | `Microsoft.Resources.Subscriptions` |
| System Topic | `st-auto-tag-resources` |
| Event Type | `Resource Write Success` |
| Endpoint Type | `Azure Function` |
| Function App | `func-auto-tag` |
| Function | `createDateTag` |

---

## 11. Flujo de funcionamiento

```text
1. Usuario crea un recurso en Azure.
2. Azure Resource Manager completa la creación.
3. Event Grid detecta Resource Write Success.
4. Event Grid envía el evento a la Azure Function.
5. La Function obtiene el Resource ID.
6. La Function obtiene la suscripción.
7. La Function obtiene la región del recurso.
8. La Function genera la fecha del evento.
9. La Function actualiza los tags.
```

---

## 12. Tags generados automáticamente

| Tag | Descripción | Ejemplo |
|---|---|---|
| `CreateDate` | Fecha y hora detectada por Event Grid | `2026-06-19 01:30:30 UTC` |
| `Subscription` | Nombre de la suscripción | `Subscription 1` |
| `Location` | Región del recurso | `East US` |

---

## 13. Problemas encontrados durante la implementación

### Azure Functions Core Tools no instalado

Error:

```text
func : The term 'func' is not recognized
```

Solución:

Instalar Azure Functions Core Tools v4 y reiniciar VS Code.

---

### Azure CLI no instalado

Error:

```text
az : The term 'az' is not recognized
```

Solución:

Instalar Azure CLI y reiniciar VS Code.

---

### Error de autenticación MFA

Error:

```text
AADSTS50076
```

Solución:

Completar autenticación multifactor y ejecutar:

```powershell
az login
```

---

### Microsoft.EventGrid no registrado

Error:

```text
The subscription is not registered to use namespace Microsoft.EventGrid
```

Solución:

```powershell
az provider register --namespace Microsoft.EventGrid
```

---

### Permisos insuficientes para modificar tags

Problema:

La Azure Function no podía actualizar etiquetas.

Solución:

Asignar los roles:

```text
Reader
Tag Contributor
```

a la Managed Identity de la Function.

---

## 14. Validación

Se creó una Virtual Network de prueba.

Resultado:

```text
CreateDate = 2026-06-19 01:30:30 UTC
Subscription = Subscription 1
Location = East US
```

La solución funcionó correctamente y agregó los tags automáticamente.

---

## 15. Beneficios

- Automatiza el etiquetado de recursos.
- Reduce errores manuales.
- Mejora la gobernanza cloud.
- Facilita auditorías.
- Ayuda a la organización de costos.
- Permite extender la solución a nuevos tags.

---

## 16. Mejoras futuras

### CreateBy

Agregar el nombre del usuario creador usando Microsoft Graph.

### Billing

Usar Azure Policy para permitir solo valores aprobados:

```text
Banco Dominicano
Qik
Popularbank
Abre
```

### Environment

Agregar valores como:

```text
Dev
QA
Prod
```