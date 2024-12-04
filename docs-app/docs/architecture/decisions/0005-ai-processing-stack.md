# 5. Stack de Procesamiento de IA

Fecha: 2023-11-15

## Estado

Propuesto

## Contexto

Necesitamos un sistema robusto para:
- Procesar y analizar CVs a escala
- Búsqueda semántica de candidatos
- Orquestación compleja de flujos de IA
- Monitoreo y optimización de prompts
- Almacenamiento vectorial eficiente

## Decisión

Implementaremos un stack completo de procesamiento de IA:

### 1. LangChain
- **Propósito**: Framework para aplicaciones de IA
- **Usos**:
  * Cadenas de procesamiento de documentos
  * Manejo de memoria y contexto
  * Integración con múltiples LLMs
  * Plantillas de prompts reutilizables

### 2. LangGraph
- **Propósito**: Orquestación de flujos de IA
- **Usos**:
  * Flujos de trabajo complejos
  * Máquinas de estado para procesos
  * Toma de decisiones multi-paso
  * Retroalimentación y ciclos

### 3. Qdrant
- **Propósito**: Base de datos vectorial
- **Usos**:
  * Almacenamiento de embeddings de CV
  * Búsqueda semántica de candidatos
  * Filtrado por metadatos
  * Clustering de perfiles

### 4. LangSmith
- **Propósito**: Monitoreo y debugging
- **Usos**:
  * Evaluación de prompts
  * Trazabilidad de decisiones
  * Métricas de rendimiento
  * Testing de cadenas

## Implementación

### Procesamiento de CVs
```python
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Qdrant

class CVProcessor:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Qdrant(
            client=QdrantClient(),
            collection_name="cvs",
            embeddings=self.embeddings
        )
    
    async def process_cv(self, cv_file: UploadFile) -> str:
        # Cargar y dividir documento
        loader = PyPDFLoader(cv_file)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter()
        splits = text_splitter.split_documents(documents)
        
        # Almacenar en Qdrant
        ids = await self.vector_store.aadd_documents(splits)
        return ids[0]
```

### Flujo de Evaluación
```python
from langgraph.graph import Graph
from langchain.chat_models import ChatOpenAI

def create_evaluation_graph():
    # Nodos del grafo
    nodes = {
        "extract": extract_info,
        "evaluate": evaluate_candidate,
        "recommend": make_recommendation
    }
    
    # Definir flujo
    graph = Graph(nodes)
    graph.add_edge("extract", "evaluate")
    graph.add_edge("evaluate", "recommend")
    
    return graph

async def run_evaluation(cv_id: str, job_requirements: List[str]):
    graph = create_evaluation_graph()
    result = await graph.arun({
        "cv_id": cv_id,
        "requirements": job_requirements
    })
    return result
```

### Búsqueda de Candidatos
```python
class CandidateSearch:
    async def search_similar(
        self,
        description: str,
        top_k: int = 5
    ) -> List[dict]:
        results = await self.vector_store.asimilarity_search_with_score(
            description,
            k=top_k
        )
        return [
            {
                "candidate_id": doc.metadata["candidate_id"],
                "score": score,
                "summary": doc.page_content
            }
            for doc, score in results
        ]
```

### Monitoreo con LangSmith
```python
from langsmith import Client

class EvaluationMonitor:
    def __init__(self):
        self.client = Client()
    
    async def track_evaluation(
        self,
        cv_id: str,
        evaluation_result: dict
    ):
        run = await self.client.create_run(
            name="cv_evaluation",
            inputs={
                "cv_id": cv_id,
                "result": evaluation_result
            }
        )
        await self.client.update_run(
            run.id,
            outputs=evaluation_result,
            end_time=datetime.utcnow()
        )
```

## Consecuencias

### Positivas
- Framework completo y probado
- Búsqueda semántica potente
- Flujos de trabajo flexibles
- Monitoreo detallado
- Escalabilidad

### Negativas
- Complejidad adicional
- Costos de infraestructura
- Mantenimiento de vectores
- Curva de aprendizaje

### Mitigaciones
1. **Complejidad**:
   - Documentación detallada
   - Patrones comunes
   - Testing exhaustivo

2. **Costos**:
   - Caching de embeddings
   - Optimización de chunks
   - Monitoreo de uso

3. **Mantenimiento**:
   - Actualización periódica
   - Pruebas de regresión
   - Backups regulares

## Referencias
- LangChain Documentation
- Qdrant Documentation
- LangGraph Examples
- LangSmith Best Practices
