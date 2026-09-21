import json
import os
import sys
import firebase_admin
from firebase_admin import credentials, firestore


def init_firestore():
    """
    Inicializa o cliente Firestore do Firebase.
    
    Tenta primeiro carregar as credenciais de uma variável de ambiente (FIREBASE_SERVICE_ACCOUNT_JSON).
    Se não encontrar, tenta carregar do arquivo 'secrets/key.json'.
    
    Returns:
        firestore.Client: Cliente Firestore inicializado
    """
    if not firebase_admin._apps:
        service_account_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")
        if service_account_json:
            cred_info = json.loads(service_account_json)
            cred = credentials.Certificate(cred_info)
        else:
            # Tentar múltiplos caminhos possíveis
            possible_paths = [
                # Caminho relativo
                "secrets/key.json",
                # Caminho absoluto a partir do arquivo atual
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "secrets", "key.json"),
                # Caminho a partir de sys.modules para Streamlit
                os.path.join(os.getcwd(), "secrets", "key.json"),
                # Caminho hardcoded (última opção)
                "a:\\Users\\Downloads\\sga_mvc\\secrets\\key.json"
            ]
            
            key_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    key_path = path
                    print(f"✅ Firebase encontrado em: {key_path}")
                    break
            
            if not key_path:
                error_msg = (
                    f"❌ Arquivo 'secrets/key.json' não encontrado!\n"
                    f"Caminhos procurados:\n"
                    + "\n".join([f"  - {p}" for p in possible_paths])
                )
                raise FileNotFoundError(error_msg)
            
            cred = credentials.Certificate(key_path)
        
        firebase_admin.initialize_app(cred)
    
    return firestore.client()
