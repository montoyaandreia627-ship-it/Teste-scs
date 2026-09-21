# 🔥 Guia: Usando Firebase no SGA

## 1️⃣ Verificar Conexão

No seu `app.py`, Firebase já está inicializado automaticamente em `st.session_state.firestore_db`.

---

## 2️⃣ Usar no MODEL (Camada de dados)

**Exemplo: `models/usuario_model.py`**

```python
import streamlit as st

def criar_usuario(nome, email):
    """Cria um novo usuário no Firestore"""
    db = st.session_state.firestore_db
    
    usuario = {
        'nome': nome,
        'email': email,
        'criado_em': __import__('datetime').datetime.now(),
    }
    
    # Salvar no Firestore
    doc_ref = db.collection('usuarios').document(email)
    doc_ref.set(usuario)
    
    return usuario


def obter_usuario(email):
    """Busca um usuário no Firestore"""
    db = st.session_state.firestore_db
    
    doc = db.collection('usuarios').document(email).get()
    
    if doc.exists:
        return doc.to_dict()
    return None


def listar_usuarios():
    """Lista todos os usuários"""
    db = st.session_state.firestore_db
    
    usuarios = []
    for doc in db.collection('usuarios').stream():
        usuarios.append(doc.to_dict())
    
    return usuarios
```

---

## 3️⃣ Usar no CONTROLLER (Orquestra casos de uso)

**Exemplo: `controllers/usuario_controller.py`**

```python
import streamlit as st
from models import usuario_model

def handle_novo_usuario(nome, email):
    """Processa criação de novo usuário"""
    
    # Validação
    if not nome or not email:
        return False, "Nome e email são obrigatórios"
    
    if "@" not in email:
        return False, "Email inválido"
    
    # Tenta criar
    try:
        usuario_model.criar_usuario(nome, email)
        st.session_state.mensagem = f"✅ Usuário {nome} criado com sucesso!"
        return True, "Usuário criado!"
    
    except Exception as e:
        return False, f"❌ Erro: {str(e)}"


def carregar_usuarios():
    """Carrega lista de usuários para exibir"""
    try:
        usuarios = usuario_model.listar_usuarios()
        return usuarios
    except Exception as e:
        st.error(f"Erro ao carregar usuários: {e}")
        return []
```

---

## 4️⃣ Usar na VIEW (Apresentação)

**Exemplo: `views/membros_view.py`**

```python
import streamlit as st
from controllers import usuario_controller

def render():
    """Renderiza página de membros"""
    st.title("👥 Gerenciar Membros")
    
    # Formulário para novo usuário
    with st.form("novo_membro_form"):
        nome = st.text_input("Nome do membro")
        email = st.text_input("Email")
        
        if st.form_submit_button("➕ Adicionar Membro"):
            sucesso, mensagem = usuario_controller.handle_novo_usuario(nome, email)
            
            if sucesso:
                st.success(mensagem)
                st.rerun()
            else:
                st.error(mensagem)
    
    # Listar membros
    st.divider()
    st.subheader("📋 Lista de Membros")
    
    usuarios = usuario_controller.carregar_usuarios()
    
    if usuarios:
        for usuario in usuarios:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{usuario.get('nome')}**")
            with col2:
                st.write(usuario.get('email'))
            with col3:
                if st.button("🗑️", key=usuario.get('email')):
                    # Deletar
                    db = st.session_state.firestore_db
                    db.collection('usuarios').document(usuario.get('email')).delete()
                    st.rerun()
    else:
        st.info("Nenhum membro cadastrado")
```

---

## 5️⃣ Operações Comuns Firebase

### 📝 **Criar** (CREATE)
```python
db = st.session_state.firestore_db
db.collection('usuarios').document('id_unico').set({
    'nome': 'João',
    'email': 'joao@example.com'
})
```

### 📖 **Ler** (READ)
```python
db = st.session_state.firestore_db

# Um documento
doc = db.collection('usuarios').document('id_unico').get()
if doc.exists:
    dados = doc.to_dict()

# Vários documentos
docs = db.collection('usuarios').stream()
for doc in docs:
    print(doc.to_dict())

# Com filtro
docs = db.collection('usuarios').where('email', '==', 'joao@example.com').stream()
```

### ✏️ **Atualizar** (UPDATE)
```python
db = st.session_state.firestore_db

# Atualizar um campo
db.collection('usuarios').document('id_unico').update({
    'nome': 'João Silva'
})
```

### 🗑️ **Deletar** (DELETE)
```python
db = st.session_state.firestore_db

db.collection('usuarios').document('id_unico').delete()
```

---

## 6️⃣ Exemplo Completo: Função de Login

```python
# models/auth_model.py
import streamlit as st

def validar_login(email, senha):
    """Valida credenciais no Firestore"""
    db = st.session_state.firestore_db
    
    user_doc = db.collection('usuarios').document(email).get()
    
    if not user_doc.exists:
        return False, "Usuário não encontrado"
    
    user_data = user_doc.to_dict()
    
    # ⚠️ IMPORTANTE: Em produção, senhas devem ser hash!
    if user_data.get('senha') == senha:
        return True, "Login bem-sucedido"
    
    return False, "Senha incorreta"
```

---

## 7️⃣ Tratamento de Erros

```python
try:
    db = st.session_state.firestore_db
    usuarios = list(db.collection('usuarios').stream())
except KeyError:
    st.error("❌ Firebase não foi inicializado. Verifique 'secrets/key.json'")
except PermissionError:
    st.error("❌ Sem permissão. Verifique regras Firestore")
except Exception as e:
    st.error(f"❌ Erro Firebase: {e}")
```

---

## 8️⃣ Testes Rápidos no Terminal

```bash
# Ver se Firebase está acessível
$ python -c "
import streamlit as st
from utils.firebase_utils import init_firestore
db = init_firestore()
print('✅ Firestore conectado!')
print('Coleções:', db.collections())
"
```

---

## ⚙️ Estrutura Recomendada

```
models/
├── usuario_model.py      (CRUD de usuários)
├── ambiente_model.py     (CRUD de ambientes)
└── reserva_model.py      (CRUD de reservas)

controllers/
├── usuario_controller.py (Lógica de usuários)
├── auth_controller.py    (Lógica de autenticação)
└── reserva_controller.py (Lógica de reservas)

views/
├── membros_view.py
├── reservas_view.py
└── dashboard_view.py
```

---

## 🔑 Resumo: Fluxo de Dados

```
View (membros_view.py)
  ↓ (usuário clica botão)
Controller (usuario_controller.py)
  ↓ (valida e orquestra)
Model (usuario_model.py)
  ↓ (interage com Firebase)
Firestore 🔥
```

**Nunca acesse Firebase direto nas Views!** Sempre passe pelo Controller/Model.

---

Pronto para começar! 🚀
