# 🚀 Passo a Passo: Testar a Aplicação no Streamlit

## ✅ PASSO 1: Verifique se Tudo Está Instalado

### 1.1 - Abra o Terminal

**Windows (PowerShell):**
```powershell
# Abra a pasta do projeto
cd a:\Users\Downloads\sga_mvc
```

### 1.2 - Verifique Python e Pip

```powershell
# Ver versão do Python
python --version

# Esperado:
# Python 3.12.10
```

---

## ✅ PASSO 2: Instale as Dependências (Se Não Fez)

```powershell
cd a:\Users\Downloads\sga_mvc

# Instale tudo do requirements.txt
python -m pip install -r requirements.txt

# Ou use o caminho completo:
& "C:\Users\User\AppData\Local\Programs\Python\Python312\python.exe" -m pip install -r requirements.txt
```

**Aguarde até aparecer:**
```
Successfully installed ... firebase-admin ... streamlit ... pandas ... plotly
```

---

## ✅ PASSO 3: Execute o Streamlit

```powershell
# Na pasta do projeto
cd a:\Users\Downloads\sga_mvc

# Inicie o app
streamlit run app.py
```

**Você verá:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## ✅ PASSO 4: Abra no Navegador

Clique no link ou acesse manualmente:

```
http://localhost:8501
```

**Você verá:**
```
🔐 SGA — Sistema de Gestão de Ambientes

Login ou Registro (2 abas)
```

---

## ✅ PASSO 5: Teste CRIAR CONTA (Primeira Vez)

### 5.1 - Clique em "Criar Conta"

Você verá:
```
📝 Criar Conta

Nome Completo: [________]
Email: [________]
Senha: [________]
Confirmar Senha: [________]
```

### 5.2 - Preencha os Dados

```
Nome Completo: João Silva
Email: joao@example.com
Senha: 123456
Confirmar: 123456
```

### 5.3 - Clique "✅ Criar Conta"

**Se funcionar, você verá:**
```
✅ Conta criada com sucesso!
💥 Balloons (confete!)
```

**Se der erro, você verá:**
```
❌ [Mensagem de erro]
```

---

## ✅ PASSO 6: Verifique o Login Automático

Depois de criar conta, a página deve **automaticamente**:
```
1. Fazer login
2. Mostrar dashboard
3. Exibir sidebar com seu nome
```

---

## ✅ PASSO 7: Teste LOGOUT

1. Abra a sidebar (canto superior esquerdo)
2. Role até o final
3. Clique **"🚪 Logout"**

**Resultado esperado:**
```
Volta para tela de Login
```

---

## ✅ PASSO 8: Teste LOGIN (Conta Existente)

### 8.1 - Clique "🔓 Voltar ao Login"

### 8.2 - Digite seu email

```
Email: joao@example.com
```

### 8.3 - Clique "🔓 Entrar"

**Se funcionar:**
```
✅ Bem-vindo, João Silva!
👥 Dashboard abre
```

---

## ✅ PASSO 9: Teste PERFIL

### 9.1 - Na sidebar, clique "⚙️ Perfil"

Você verá:
```
⚙️ Meu Perfil

📋 Informações da Conta
✏️ Editar Perfil
🔒 Segurança
⚠️ Zona de Perigo
```

### 9.2 - Clique "✏️ Salvar Alterações"

Teste mudar seu nome e salvar.

---

## ✅ PASSO 10: Teste Criar Múltiplas Contas

Crie 3 contas diferentes:

**Conta 1 (Usuário):**
```
Nome: Maria Silva
Email: maria@example.com
Senha: 123456
```

**Conta 2 (Professor):**
```
Nome: Prof João
Email: prof@example.com
Senha: 123456
```

**Conta 3 (Admin):**
```
Nome: Admin Sistema
Email: admin@example.com
Senha: 123456
```

---

## 🧪 TESTANDO FUNCIONALIDADES

### **Teste 1: Criar Conta Inválida**

```
❌ Teste: Senha muito curta (< 6 caracteres)
Nome: João
Email: joao@test.com
Senha: 123
   ↓
Esperado: ❌ Erro "Senha deve ter no mínimo 6 caracteres"

✅ Resultado: Passou!
```

### **Teste 2: Email Inválido**

```
❌ Teste: Email sem @
Nome: João
Email: joaotest.com
Senha: 123456
   ↓
Esperado: ❌ Erro

✅ Resultado: Passou!
```

### **Teste 3: Conta Duplicada**

```
✅ Criar conta com: maria@test.com

❌ Tentar criar NOVAMENTE com mesmo email
   ↓
Esperado: ❌ Erro "Email já está registrado"

✅ Resultado: Passou!
```

### **Teste 4: Logout e Login**

```
✅ 1. Faça login
✅ 2. Clique Logout
✅ 3. Faça login novamente com mesmo email
   ↓
Esperado: ✅ Funciona

✅ Resultado: Passou!
```

---

## 🆘 RESOLVENDO PROBLEMAS

### **Problema 1: "ModuleNotFoundError: No module named 'firebase_admin'"**

```powershell
# Solução:
python -m pip install -r requirements.txt

# Aguarde terminar, depois tente novamente:
streamlit run app.py
```

---

### **Problema 2: "Failed to initialize Firebase"**

```
Causas possíveis:
1. secrets/key.json não existe
2. secrets/key.json está corrompido
3. Caminho errado do arquivo

Solução:
1. Verifique se existe: a:\Users\Downloads\sga_mvc\secrets\key.json
2. Abra com editor de texto - deve começar com { e terminar com }
3. Se corrupto, copie novamente do Firebase Console
```

---

### **Problema 3: "Erro ao conectar Firebase"**

```
Causas:
1. Firestore Database não foi criado no Firebase Console
2. Security Rules muito restritivas

Solução:
1. Firebase Console → Firestore Database → Create
2. Locação: south-america-east1
3. Mode: Production mode
4. Depois publicar as Security Rules
```

---

### **Problema 4: Criar Conta Funciona, mas não Faz Login**

```
Causa: Firestore Rules não foram publicadas

Solução:
1. Abra: FIRESTORE_SECURITY_RULES.md
2. Copie TODO o código
3. Firebase Console → Firestore Database → Rules
4. Cole e clique "Publish"
5. Aguarde "Publicado com sucesso"
6. Volte ao Streamlit e tente novamente
```

---

## 📊 CHECKLIST DE TESTES

- [ ] 1. Terminal aberto na pasta correta
- [ ] 2. Python e Pip funcionando
- [ ] 3. Dependências instaladas (pip install -r requirements.txt)
- [ ] 4. Streamlit rodando (`streamlit run app.py`)
- [ ] 5. Navegador abriu em localhost:8501
- [ ] 6. Tela de login/registro apareceu
- [ ] 7. Criei uma conta com sucesso
- [ ] 8. Fiz login automaticamente
- [ ] 9. Vi o dashboard
- [ ] 10. Cliquei em Perfil
- [ ] 11. Fiz Logout
- [ ] 12. Fiz Login novamente
- [ ] 13. Todos os testes acima passaram ✅

---

## 🎯 RESUMO RÁPIDO

```
Terminal aberto em: a:\Users\Downloads\sga_mvc
   ↓
streamlit run app.py
   ↓
http://localhost:8501 abre
   ↓
Criar Conta → Preencher dados
   ↓
✅ Conta criada!
   ↓
Dashboard abre automaticamente
   ↓
TESTE COMPLETO! 🎉
```

---

## 🚀 PRÓXIMOS PASSOS (Depois que Testar)

1. ✅ **Criar mais contas** (usuario, professor, admin)
2. ✅ **Testar roles** (mudar em Firebase Console)
3. ✅ **Testar Firestore Rules** (Firebase Simulator)
4. ✅ **Implementar CRUD de ambientes**
5. ✅ **Implementar sistema de reservas**

---

## 📞 SE NÃO FUNCIONAR

1. Verifique se todos os 14 itens do checklist estão ✅
2. Leia a seção "🆘 RESOLVENDO PROBLEMAS"
3. Se ainda não funcionar, me chama com a mensagem de erro exata!

---

**Pronto para testar?** 🚀 Vamos lá!
