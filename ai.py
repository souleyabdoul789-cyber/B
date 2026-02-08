import requests
import json
import os

# --- CONFIGURATION ---
API_KEY = "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"
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-chat"
MEMOIRE_FILE = "memoire.json"

def load_config_files():
    """Charge les règles et connaissances."""
    with open("rules.txt", "r", encoding="utf-8") as f:
        rules = f.read()
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        knowledge = f.read()
    return f"{rules}\n\nCONNAISSANCES SPÉCIFIQUES :\n{knowledge}"

def charger_memoire():
    """Récupère l'historique des conversations si le fichier existe."""
    if os.path.exists(MEMOIRE_FILE):
        with open(MEMOIRE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def sauvegarder_memoire(messages):
    """Enregistre l'historique dans le fichier JSON."""
    with open(MEMOIRE_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=4, ensure_ascii=False)

def chatbot_puissant():
    # 1. Préparation du système
    system_prompt = load_config_files()
    
    # 2. Chargement de la mémoire (historique passé)
    historique_existant = charger_memoire()
    
    # Si l'historique est vide, on initialise avec le prompt système
    if not historique_existant:
        messages = [{"role": "system", "content": system_prompt}]
    else:
        # On met à jour le prompt système au cas où rules.txt a changé
        messages = historique_existant
        messages[0] = {"role": "system", "content": system_prompt}

    print(f"--- ⚡ JOYSERVER AI : MÉMOIRE CHARGÉE ({len(messages)-1} messages) ---")

    while True:
        user_input = input("\n[JoyServer] > ")

        if user_input.lower() == "exit":
            sauvegarder_memoire(messages)
            print("💾 Mémoire sauvegardée. À plus tard !")
            break

        messages.append({"role": "user", "content": user_input})

        payload = {
            "model": MODEL,
            "messages": messages,
            "temperature": 0.7
        }
        
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

        try:
            response = requests.post(URL, headers=headers, json=payload)
            response.raise_for_status()
            
            bot_reply = response.json()['choices'][0]['message']['content']
            print(f"\n[AI] : {bot_reply}")
            
            messages.append({"role": "assistant", "content": bot_reply})
            
            # Sauvegarde automatique après chaque réponse
            sauvegarder_memoire(messages)

        except Exception as e:
            print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    chatbot_puissant()
