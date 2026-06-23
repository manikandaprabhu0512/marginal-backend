from pathlib import Path

PROMPTS_DIR = Path(__file__).parent

def load_prompt(agent_name: str) -> str:
    prompt_path = PROMPTS_DIR / f"{agent_name}.txt"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8").strip()