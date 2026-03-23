from gpt4all import GPT4All

class AIEngine:
    def __init__(self, model_name="qwen2-1_5b-instruct-q4_0.gguf"):
        # GPT4All automatically looks in its default download path for the model.
        print(f"Loading local GPT4All model: {model_name}...")
        try:
            # Added device='cpu' and n_ctx=256 to prevent memory access violations 
            # and CUDA errors on Ryzen. 256 Context uses VERY little RAM.
            self.model = GPT4All(model_name, allow_download=False, device='cpu', n_ctx=256)
            print("Model loaded successfully!")
        except Exception:
            print(f"Warning: Model {model_name} not found. Trying to fallback/download...")
            self.model = GPT4All(model_name, allow_download=True, device='cpu', n_ctx=256)

    def generate_suggestions(self, prompt, num_suggestions=3):
        # Qwen2 requires proper ChatML formatting. GPT4All's chat_session handles this automatically!
        system_prompt = f"You are a casual friend on WhatsApp. Reply to the message in a short, friendly manner. If the message is in Roman Urdu, reply in Roman Urdu ONLY. Provide exactly {num_suggestions} different short replies separated by a new line. Do not use numbers or bullet points."
        
        try:
            with self.model.chat_session(system_prompt=system_prompt):
                # Lowering max_tokens to 45 increases generation speed significantly on CPUs without cutting off short replies.
                output = self.model.generate(prompt, max_tokens=45, temp=0.4)
            
            # Extract lines and clean them
            lines = [line.strip("- 1234567890.*\"'") for line in output.split('\n') if line.strip()]
            suggestions = [line for line in lines if len(line) > 2]
            
            while len(suggestions) < num_suggestions:
                suggestions.append("...")
                
            return suggestions[:num_suggestions]
        except Exception as e:
            print(f"Error generating text: {e}")
            return ["Error generating reply 1", "Error generating reply 2", "Error generating reply 3"]
