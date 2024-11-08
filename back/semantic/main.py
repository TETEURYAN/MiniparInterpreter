from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from semantic import SemanticAnalyzer
from syntax_tree import SyntaxNode

app = FastAPI()

class SyntaxTreeInput(BaseModel):
    syntax_tree: dict

@app.post("/analyze")
def analyze_semantics(input_data: SyntaxTreeInput):
    try:
        # Converte o JSON de entrada em uma árvore sintática
        root = SyntaxNode.from_dict(input_data.syntax_tree)
        
        # Cria o analisador semântico
        analyzer = SemanticAnalyzer()
        
        # Executa a análise semântica
        errors = analyzer.analyze(root)
        
        # Se houver erros semânticos, retorna com status de erro
        if errors:
            return {"status": "error", "errors": errors}
        
        # Se a análise semântica for bem-sucedida, retorna uma mensagem de sucesso
        return {"status": "success", "message": "Semantic analysis completed successfully"}
    
    except Exception as e:
        # Se ocorrer um erro durante a conversão ou análise, retorna um erro HTTP
        raise HTTPException(status_code=400, detail=f"Error during semantic analysis: {str(e)}")
