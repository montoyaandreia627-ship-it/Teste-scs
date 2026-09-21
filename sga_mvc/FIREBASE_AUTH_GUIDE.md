# 🔐 Guia de Autenticação com Firebase Auth

## 📝 Configuração Inicial

### 1️⃣ **Ativar Firebase Authentication**

1. Vá para [Firebase Console](https://console.firebase.google.com)
2. Selecione seu projeto **"projeto-devangers"**
3. Clique em **Authentication** → **Get Started**
4. Selecione **Email/Password**
5. Habilite **Email/Password** e **Email link sign-in** (opcional)
6. Configure usuários de teste se necessário

### 2️⃣ **Criar Usuário de Teste**

```javascript
// No Firebase Console (Auth → Users)
Email: admin@sga.local
Senha: admin123456
```

---

## 🏗️ Arquitetura de Autenticação

```
┌─────────────────┐
│  auth_view.py   │  ← Formulário Login/Registro
└────────┬────────┘
         │
┌────────▼──────────────────┐
│ auth_controller.py        │  ← Gerencia st.session_state
│ (fazer_login, registro)   │
└────────┬──────────────────┘
         │
┌────────▼──────────────────┐
│ auth_model.py             │  ← Lógica de autenticação
│ (criar_conta, fazer_login)│
└────────┬──────────────────┘
         │
┌────────▼──────────────────┐
│ Firebase Auth             │  ← Autenticação
│ + Firestore (perfil)      │
└──────────────────────────┘
```

---

## 🔑 Fluxo de Login

```
Usuario Clica "Entrar"
         ↓
auth_view.render_login()
         ↓
auth_controller.fazer_login(email)
         ↓
auth_model.fazer_login(email)
         ↓
utils.auth_utils.obter_usuario_por_email(email)
         ↓
Firebase Auth retorna User
         ↓
Busca perfil em Firestore
         ↓
Armazena em st.session_state.user_uid
         ↓
App rerun() - Mostra dashboard
```

---

## 📝 Fluxo de Registro

```
Usuario Clica "Criar Conta"
         ↓
auth_view.render_registro()
         ↓
auth_controller.fazer_registro(email, senha, nome)
         ↓
auth_model.criar_nova_conta(email, senha, nome)
         ↓
utils.auth_utils.registrar_usuario(email, senha)
         ↓
Firebase Auth cria user com email/senha
         ↓
Salva perfil em Firestore (role='usuario')
         ↓
Armazena em st.session_state
         ↓
App rerun() - Mostra dashboard
```

---

## 🚀 Usando Autenticação no Seu Código

### **1. Verificar se está logado**

```python
from controllers import auth_controller

if auth_controller.is_logged_in():
    st.write("✅ Usuário autenticado!")
else:
    st.write("❌ Faça login")
```

### **2. Obter informações do usuário**

```python
info = auth_controller.obter_info_usuario()

print(info['uid'])      # "user123"
print(info['nome'])     # "João Silva"
print(info['email'])    # "joao@example.com"
print(info['role'])     # "usuario|professor|admin"
```

### **3. Verificar permissões**

```python
if auth_controller.tem_permissao('gerenciar_usuarios'):
    st.write("Você pode gerenciar usuários")
else:
    st.write("Sem permissão")
```

### **4. Fazer logout**

```python
if st.button("Logout"):
    auth_controller.fazer_logout()
    st.rerun()
```

### **5. Atualizar perfil do usuário**

```python
sucesso, msg = auth_controller.atualizar_perfil({
    'nome': 'João Silva',
    'role': 'professor'
})

if sucesso:
    st.success(msg)
```

---

## 🎯 Papéis e Permissões

### **Usuário**
- ✅ Ver agenda
- ✅ Fazer reservas
- ❌ Gerenciar usuários

### **Professor**
- ✅ Ver agenda
- ✅ Fazer reservas
- ✅ Gerenciar aulas
- ❌ Gerenciar usuários

### **Admin**
- ✅ Ver agenda
- ✅ Fazer reservas
- ✅ Gerenciar aulas
- ✅ Gerenciar usuários
- ✅ Acessar logs
- ✅ Alterar papéis

---

## 🧪 Testando Autenticação

### **Em Desenvolvimento (Demo)**

Use estas credenciais de teste:

| Email | Senha | Papel |
|-------|-------|-------|
| admin@sga.local | admin123456 | admin |
| prof@sga.local | prof123456 | professor |
| user@sga.local | user123456 | usuario |

Para criar, você precisa:
1. Executar `streamlit run app.py`
2. Clicar em "Criar Conta"
3. Preencher dados

### **Verificar no Firebase Console**

1. Vá em **Authentication** → **Users**
2. Veja todos os usuários cadastrados
3. Altere papéis manualmente para testes

---

## 🔒 Segurança

### ✅ Boas Práticas

```python
# ✅ BOM: Verificar autenticação
if auth_controller.is_logged_in():
    dados = buscar_dados_usuario()

# ❌ RUIM: Confiar no cliente
if st.session_state.get('user_uid'):  # Não confiável!
    dados = buscar_dados_usuario()
```

### ⚠️ Importante

- **Senhas:** Já são criptografadas por Firebase
- **Sessions:** Armazenadas apenas em `st.session_state` (não em cookies)
- **CORS:** Firebase controla acesso entre origem e Firebase
- **Firestore Rules:** Validam acesso a dados (veja `FIRESTORE_SECURITY_RULES.md`)

---

## 🚀 Próximos Passos

### 1. **Verificação de Email**
```python
# Enviar email de verificação
auth_utils.enviar_email_verificacao(email)

# Verificar se email foi verificado
if perfil.get('email_verificado'):
    st.success("Email verificado!")
```

### 2. **Reset de Senha**
```python
sucesso, msg = auth_utils.resetar_senha(email)
if sucesso:
    st.info("Email de reset enviado!")
```

### 3. **Autenticação Federada**
```
Firebase Console → Authentication → Sign-in Method
+ Google Sign-In
+ GitHub Sign-In
+ Microsoft Account
```

### 4. **Two-Factor Authentication (2FA)**
```
Usar Firebase Admin SDK para gerar totp
ou integrar com serviço externo
```

---

## 📚 Referências

- [Firebase Authentication Docs](https://firebase.google.com/docs/auth)
- [Firebase Admin Python SDK](https://firebase.google.com/docs/database/admin/start)
- [Firebase Security Rules](https://firebase.google.com/docs/firestore/security/start)
- [Email Templates](https://console.firebase.google.com/project/projeto-devangers/authentication/templates)

---

## 🆘 Troubleshooting

### **"ModuleNotFoundError: No module named 'firebase_admin'"**
```bash
pip install -r requirements.txt
```

### **"Failed to initialize Firebase"**
- Verifique `secrets/key.json` existe
- Verifique JSON é válido: `python -m json.tool secrets/key.json`

### **"User not found"**
- Verifique email no Firebase Console
- Email deve estar no banco de usuários

### **"Permission denied"**
- Verifique Firestore Security Rules
- Verifique papel do usuário no Firestore

---

Pronto para implementar autenticação! 🎉
