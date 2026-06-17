# Azure Policy Tag Governance Lab

## Objetivo

Implementar un laboratorio básico de gobernanza de tags en Azure usando **Azure Policy** sobre **Resource Groups**.

El lab demuestra tres controles principales:

* Agregar automáticamente la fecha de creación del Resource Group.
* Registrar un identificador técnico del responsable.
* Exigir un tag requerido como plantilla para futuros controles de tagging.

---

## Tags del lab

| Tag           | Tipo                    | Propósito                                                             |
| ------------- | ----------------------- | --------------------------------------------------------------------- |
| `CreatedDate` | Automático              | Registra la fecha y hora de creación del Resource Group.              |
| `CreatedById` | Automático / controlado | Registra el Object ID del usuario responsable.                        |
| `Billing`     | Requerido               | Identifica el área, unidad o centro de costo responsable del recurso. |

Resultado esperado:

```text
CreatedDate = 2026-06-16 23:28 UTC
CreatedById = f15166e1-17a8-4223-a4cc-a78e1add095a
Billing = CoreBanking
```

---

# 1. Policy: Append CreatedDate Tag

## Propósito

Agregar automáticamente el tag `CreatedDate` a los Resource Groups que no lo tengan.

## Nombre recomendado

```text
Append CreatedDate Tag
```


## Funcionamiento

La policy valida si el Resource Group no tiene el tag `CreatedDate`. Si no existe, lo agrega automáticamente usando el efecto `modify`.

La fecha se genera con `utcNow()` y se formatea con `substring()` y `concat()` para que sea más legible.

Se mantiene en UTC porque Azure trabaja comúnmente con hora universal, lo cual evita confusiones entre regiones y zonas horarias.

## Código

```json
{
  "mode": "All",
  "policyRule": {
    "if": {
      "allOf": [
        {
          "field": "type",
          "equals": "Microsoft.Resources/subscriptions/resourceGroups"
        },
        {
          "field": "tags['CreatedDate']",
          "exists": "false"
        }
      ]
    },
    "then": {
      "effect": "modify",
      "details": {
        "roleDefinitionIds": [
          "/providers/Microsoft.Authorization/roleDefinitions/4a9ae827-6dc8-4573-8ac7-8239d42aa03f"
        ],
        "operations": [
          {
            "operation": "addOrReplace",
            "field": "tags['CreatedDate']",
            "value": "[concat(substring(utcNow(), 0, 10), ' ', substring(utcNow(), 11, 5), ' UTC')]"
          }
        ]
      }
    }
  }
}
```

---

# 2. Policy: Append CreatedById Tag

## Propósito

Agregar el tag `CreatedById` para registrar el **Object ID** del usuario responsable del Resource Group.

Object ID utilizado:

```text
f15166e1-17a8-4223-a4cc-a78e1add095a
```

## Nombre recomendado

```text
Append CreatedById Tag
```

## Descripción

```text
Automatically appends the CreatedById tag to Resource Groups using the configured user Object ID.
```

## Funcionamiento

La policy valida si el Resource Group no tiene el tag `CreatedById`. Si no existe, agrega el valor definido en el parámetro `createdById`.

Se utiliza el Object ID porque Azure Policy no permite traducir automáticamente ese identificador al nombre del usuario dentro de una policy con efecto `modify`.

## Código

```json
{
  "mode": "All",
  "parameters": {
    "createdById": {
      "type": "String",
      "metadata": {
        "displayName": "Created By ID",
        "description": "Object ID of the user responsible for the Resource Group."
      },
      "defaultValue": "f15166e1-17a8-4223-a4cc-a78e1add095a"
    }
  },
  "policyRule": {
    "if": {
      "allOf": [
        {
          "field": "type",
          "equals": "Microsoft.Resources/subscriptions/resourceGroups"
        },
        {
          "field": "tags['CreatedById']",
          "exists": "false"
        }
      ]
    },
    "then": {
      "effect": "modify",
      "details": {
        "roleDefinitionIds": [
          "/providers/Microsoft.Authorization/roleDefinitions/4a9ae827-6dc8-4573-8ac7-8239d42aa03f"
        ],
        "operations": [
          {
            "operation": "addOrReplace",
            "field": "tags['CreatedById']",
            "value": "[parameters('createdById')]"
          }
        ]
      }
    }
  }
}
```

---

# 3. Policy: Require Billing Tag

## Propósito

Exigir el tag `Billing` en los Resource Groups.

Este tag permite identificar la unidad, área o centro de costo responsable del recurso.

Ejemplo:

```text
Billing = CoreBanking
```

## Nombre recomendado

```text
Require Billing Tag
```

## Descripción

```text
Requires the Billing tag on Resource Groups to support cost allocation and financial accountability.
```

## Funcionamiento

Esta policy utiliza el efecto `deny`.

Si el Resource Group no tiene el tag `Billing`, Azure bloquea la creación.

Para este caso se puede usar como base el enfoque de la policy integrada de Azure:

```text
Require a tag on resources
```

Este control funciona como plantilla para futuros tags requeridos, como `OperationalZone`, `DataClassification`, `Environment` o `CostCenter`.

## Código

```json
{
  "mode": "All",
  "policyRule": {
    "if": {
      "allOf": [
        {
          "field": "type",
          "equals": "Microsoft.Resources/subscriptions/resourceGroups"
        },
        {
          "field": "tags['Billing']",
          "exists": "false"
        }
      ]
    },
    "then": {
      "effect": "deny"
    }
  }
}
```

---

# Managed Identity

Las policies con efecto `modify` necesitan permisos para modificar los tags automáticamente.

Por eso, en las policies:

```text
Append CreatedDate Tag
Append CreatedById Tag
```

se habilita:

```text
System Assigned Managed Identity
```

y se asigna el rol:

```text
Tag Contributor
```

La policy `Require Billing Tag` no necesita Managed Identity porque no modifica recursos. Solo valida si el tag existe y bloquea la creación si no cumple.

---

# Pruebas del lab

## Prueba 1: CreatedDate automático

Crear un Resource Group sin el tag `CreatedDate`.

Resultado esperado:

```text
CreatedDate = 2026-06-16 23:28 UTC
```

---

## Prueba 2: CreatedById automático

Crear un Resource Group sin el tag `CreatedById`.

Resultado esperado:

```text
CreatedById = f15166e1-17a8-4223-a4cc-a78e1add095a
```

---

## Prueba 3: Billing requerido

Intentar crear un Resource Group sin el tag `Billing`.

Resultado esperado:

```text
La creación debe ser bloqueada.
```

Luego crear el Resource Group con:

```text
Billing = CoreBanking
```

Resultado esperado:

```text
La creación debe ser permitida.
```

---

# Por qué no se usó CreatedBy con nombre

Inicialmente se buscaba que el tag `CreatedBy` tomara automáticamente el nombre del usuario logueado.

Ejemplo:

```text
CreatedBy = Oscar Garcia
```

Se intentó usar:

```json
"[requestContext().principalName]"
```

Pero Azure indicó que `principalName` no existe dentro de `requestContext()`.

También se intentó usar:

```json
"[requestContext().identity]"
```

Pero Azure indicó que esa propiedad no puede usarse con el efecto `modify`.

Por eso, en esta versión del lab se usó `CreatedById`, que mantiene trazabilidad técnica mediante el Object ID.

---

# Mejora futura: obtener el nombre real del usuario

Para obtener automáticamente el nombre real del usuario, se necesitaría una automatización adicional.

Flujo propuesto:

```text
Resource Group creado
        ↓
Activity Log registra quién lo creó
        ↓
Event Grid o Logic App detecta el evento
        ↓
Logic App consulta Microsoft Graph
        ↓
Microsoft Graph traduce el Object ID al nombre del usuario
        ↓
Logic App actualiza el tag CreatedBy
```

Esta alternativa requiere más configuración:

* Logic App o Azure Function.
* Activity Log o Event Grid.
* Permisos en Microsoft Graph.
* Permisos para modificar tags.
* Manejo de errores.
* Validación de costos por ejecución.

Por eso no se implementó en esta primera versión del lab.

---

# Mejoras futuras del lab

## 1. Consolidar policies

Actualmente las policies están separadas para facilitar pruebas y troubleshooting.

Más adelante se pueden consolidar así:

```text
Policy 1: Tags automáticos
- CreatedDate
- CreatedById

Policy 2: Tags requeridos
- Billing
- OperationalZone
- DataClassification
```

## 2. Agregar más tags requeridos

Ejemplos:

```text
OperationalZone
DataClassification
Environment
ApplicationOwner
CostCenter
```

## 3. Validar valores permitidos

Actualmente `Billing` solo valida que el tag exista.

Como mejora, se puede validar que el valor pertenezca a una lista permitida.

Ejemplo:

```text
CoreBanking
DigitalBanking
Compliance
RiskManagement
CloudOperations
```

---

# Conclusión

Se implementó un lab funcional de Azure Policy para gobernanza de tags en Resource Groups.

En esta primera versión se trabajaron tres policies separadas:

```text
Append CreatedDate Tag
Append CreatedById Tag
Require Billing Tag
```

La policy `Append CreatedDate Tag` agrega automáticamente la fecha de creación en formato UTC.

La policy `Append CreatedById Tag` registra el Object ID del usuario responsable.

La policy `Require Billing Tag` funciona como plantilla para exigir tags requeridos en Resource Groups.

Este lab demuestra cómo Azure Policy puede mejorar la gobernanza, trazabilidad y control de recursos cloud en Azure.