{{- define "taskboard.name" -}}taskboard{{- end }}
{{- define "taskboard.labels" -}}
app.kubernetes.io/name: {{ include "taskboard.name" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
