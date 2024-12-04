# Integración con WhatsApp

## Configuración

### 1. WhatsApp Business API
- Requisitos de configuración
- Proceso de verificación
- Límites y restricciones

### 2. Templates de Mensajes
#### Plantillas Requeridas
1. **Bienvenida**
   ```
   Hola [NOMBRE], gracias por tu interés en [EMPRESA].
   Para comenzar tu proceso de postulación, necesitaré hacerte algunas preguntas.
   ¿Estás de acuerdo en continuar?
   ```

2. **Solicitud de CV**
   ```
   Por favor, envía tu CV en formato PDF o Word.
   Asegúrate que el archivo esté actualizado y contenga tu información de contacto.
   ```

3. **Confirmación**
   ```
   Hemos recibido tu CV correctamente.
   En breve comenzaremos con el análisis de tu perfil.
   Te mantendremos informado sobre el proceso.
   ```

4. **Actualización de Estado**
   ```
   Hola [NOMBRE],
   Tu postulación para [PUESTO] ha sido [ESTADO].
   [SIGUIENTE_PASO]
   ```

## Manejo de Conversaciones

### Estados de Conversación
1. INICIAL
2. RECOPILANDO_INFO
3. ESPERANDO_CV
4. EN_EVALUACION
5. PROGRAMANDO_ENTREVISTA
6. FINALIZADO

### Timeouts y Recordatorios
- Tiempo máximo de espera por respuesta
- Recordatorios automáticos
- Cierre de conversaciones inactivas

## Limitaciones y Consideraciones
- Tamaño máximo de archivos
- Formatos soportados
- Frecuencia de mensajes
- Horarios de atención
