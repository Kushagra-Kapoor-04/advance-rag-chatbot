import requests


def get_llm(provider: str="ollama"):
    # Uses Ollama running locally on http://localhost:11434
    # Make sure Ollama is running: ollama serve
    
    class OllamaLLM:
        def __init__(self, model="mistral"):
            self.model = model
            self.api_url = "http://localhost:11434/api/generate"
        
        def invoke(self, text):
            try:
                response = requests.post(
                    self.api_url,
                    json={
                        "model": self.model,
                        "prompt": text,
                        "stream": False,
                        "temperature": 0.1,
                        "num_predict": 200  # Limit output to 200 tokens for speed
                    },
                    timeout=300  # 5 minute timeout for Mistral
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get('response', 'No response generated')
                else:
                    return f"Error: Ollama API returned status {response.status_code}"
            except requests.exceptions.ConnectTimeout:
                return "Error: Ollama took too long to respond. Try asking simpler questions."
            except requests.exceptions.ConnectionError:
                return "Error: Ollama is not running. Please run 'ollama serve' in a terminal."
            except Exception as e:
                return f"Error: {str(e)}"
    
    return OllamaLLM(model="mistral")
