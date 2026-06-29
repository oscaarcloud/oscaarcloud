### Azure Policy Tagging

> **Objetivo**: 
Esto busca aplicar automáticamente los tags CreateDate y CreateBy a los recursos nuevos, y usar Remediation Task para agregarlos a recursos existentes que no los tengan. Esto permite mejorar la trazabilidad, auditoría y control de los recursos en Azure.


---
# 1. Policy Definition: Apply CreateDate Tag

Este tag aplica automáticamente el tag CreateDate a los recursos dentro del scope donde sea asignada la política. Todo recurso que no tenga el tag CreateDate reciba automáticamente un valor con la fecha y hora actual en formato UTC. Esto permite mejorar la trazabilidad de los recursos desplegados en Azure.

```json
{
  "mode": "All",
  "policyRule": {
    "if": {
      "field": "tags['CreateDate']",
      "exists": "false"
    },
    "then": {
      "effect": "modify",
      "details": {
        "conflictEffect": "audit",
        "roleDefinitionIds": [
          "/providers/Microsoft.Authorization/roleDefinitions/4a9ae827-6dc8-4573-8ac7-8239d42aa03f"
        ],
        "operations": [
          {
            "operation": "addOrReplace",
            "field": "tags['CreateDate']",
            "value": "[concat(substring(utcNow(), 0, 10), ' ', substring(utcNow(), 11, 5), ' UTC')]"
          }
        ]
      }
    }
  }
}
```

## Explicación de la Policy
La política utiliza el modo: 
```json
"mode": "All"
```

Este modo permite que Azure Policy evalúe diferentes tipos de recursos dentro del scope asignado, incluyendo recursos y Resource Groups.

La condición principal valida si el recurso no tiene el tag CreateDate:
```json 
"field": "tags['CreateDate']",
"exists": "false"
```

Si el tag no existe, Azure Policy ejecuta el efecto:
```json
"effect": "modify"
```

## Uso de conflictEffect
La policy incluye:

```json 
"conflictEffect": "audit"
```

Esto permite que, si Azure encuentra un recurso donde no puede aplicar la modificación del tag, no bloquee la operación. En lugar de fallar o denegar el despliegue, el recurso queda registrado para auditoría.

Esto es útil porque no todos los tipos de recursos soportan tags o modificaciones de tags de la misma forma.

## Comportamiento esperado
```
Para recursos nuevos:

Recurso desplegado
        ↓
Azure Policy evalúa el recurso
        ↓
Si no tiene CreateDate, agrega el tag automáticamente

Para recursos existentes:

Recurso existente sin CreateDate
        ↓
Azure Policy lo marca como Non-compliant
        ↓
Se ejecuta una Remediation Task
        ↓
Azure Policy agrega el tag CreateDate
```

## Resultado esperado

Después de aplicar la policy y ejecutar la remediación en recursos existentes, los recursos deben tener el tag:

```
CreateDate = 2026-06-17 23:09 UTC
```

Esta implementación permite mejorar la trazabilidad, auditoría y control de los recursos desplegados en Azure.


---
# 2. Policy Assignment y Remediation: Apply CreateDate Tag
Después de crear la Policy Definition, se debe crear un Policy Assignment para indicar en qué scope se aplicará la política.

En este caso, el scope recomendado es la suscripción, para que Azure Policy evalúe los recursos creados dentro de esa suscripción.

## Configuración del Assignment
- Policy definition: Apply CreateDate Tag 
- Scope: Subscription 
- Policy enforcement: Enabled 
- Managed Identity: Enabled 
- Managed Identity type: System assigned 
- Location: East US

## Uso de Managed Identity
Como la policy utiliza el efecto modify, Azure necesita una identidad con permisos para modificar los tags de los recursos.

Por eso, durante el assignment se debe habilitar una:

`System Assigned Managed Identity`

Esta identidad será utilizada por Azure Policy para agregar automáticamente el tag CreateDate.

## Comportamiento en recursos nuevos

Después de crear el assignment, los recursos nuevos desplegados dentro del scope serán evaluados automáticamente.

```
Recurso nuevo desplegado
        ↓
Azure Policy evalúa el recurso
        ↓
Si no tiene CreateDate
        ↓
Azure Policy agrega el tag automáticamente
```

Resultado esperado:

CreateDate = 2026-06-17 23:09 UTC

## Remediation para recursos existentes
Los recursos que ya existían antes de asignar la policy no reciben el tag automáticamente hasta que se ejecute una Remediation Task.

Estos recursos pueden aparecer como:

Non-compliant

Para corregirlos, se debe crear una tarea de remediación desde:

```Policy → Compliance → Apply CreateDate Tag → Create remediation task```

Configuración recomendada:

Policy assignment: Apply CreateDate Tag
Scope: Subscription
Resources to remediate: Non-compliant resources

La Remediation Task ejecuta la operación modify sobre los recursos existentes que no tienen el tag CreateDate.

## Flujo de remediación

```
Recurso existente sin CreateDate
        ↓
Azure Policy lo detecta como Non-compliant
        ↓
Se crea una Remediation Task
        ↓
Azure Policy usa la Managed Identity
        ↓
Se agrega el tag CreateDate al recurso
        ↓
El recurso pasa a Compliant después de la próxima evaluación
```

## Nota sobre Compliance
La Remediation Task y el estado de Compliance son procesos separados.

Por eso, un recurso puede tener el tag CreateDate aplicado correctamente, pero seguir apareciendo temporalmente como Non-compliant en Azure Policy Compliance.

Para validar correctamente, se recomienda:

1. Verificar que la Remediation Task esté en estado Complete.
2. Entrar directamente al recurso y revisar la sección Tags.
3. Confirmar que el tag CreateDate fue agregado.
4. Esperar unos minutos y refrescar el panel de Compliance.

También se puede forzar una nueva evaluación con Azure CLI:
```bash
# 1. Forzar una nueva evaluación de compliance en la suscripción actual
az policy state trigger-scan

# 2. Ver resumen general de compliance
az policy state summarize

# 3. Ver todos los recursos Non-compliant
az policy state list \
  --filter "complianceState eq 'NonCompliant'" \
  --query "[].{Resource:resourceId, Policy:policyDefinitionName, Assignment:policyAssignmentName, State:complianceState, LastEvaluated:timestamp}" \
  -o table
```


---
# Azure Policy Billing Tag
```

```