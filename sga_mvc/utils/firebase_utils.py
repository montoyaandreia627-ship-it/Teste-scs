import json
import os
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
            cred = credentials.Certificate("secrets/key.json")
        
        firebase_admin.initialize_app(cred)
    
    return firestore.client()
