# 🛡️ Como Aplicar Regras de Segurança no Firestore

## 📺 Passo a Passo (Com Screenshots)

### **Passo 1: Abrir Firebase Console**

1. Acesse [console.firebase.google.com](https://console.firebase.google.com)
2. Clique no seu projeto **"projeto-devangers"**
3. No menu lateral, clique em **"Firestore Database"**

```
📊 Dashboard
├─ Realtime Database
├─ Firestore Database  ← CLIQUE AQUI
├─ Authentication
└─ Storage
```

---

### **Passo 2: Ir para a Aba "Rules"**

Dentro de Firestore Database, você verá:

```
┌─────────────────────────────────┐
│ Data | Indexes | Backups | Rules │  ← CLIQUE EM "Rules"
└─────────────────────────────────┘
```

---

### **Passo 3: Copiar as Regras**

1. Abra o arquivo `FIRESTORE_SECURITY_RULES.md` no seu projeto
2. Copie TODO o código dentro da seção:

```firestore_rules
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    // ... todo código aqui
  }
}
```

---

### **Passo 4: Colar no Editor**

No Firebase Console, no editor de Rules:

```
┌──────────────────────────────────────┐
│  Regras de Segurança do Firestore     │
├──────────────────────────────────────┤
│                                      │
│  [Cole o código aqui]                │
│                                      │
│                                      │
│         ✅ PUBLICAR  ❌ DESCARTAR   │
└──────────────────────────────────────┘
```

---

### **Passo 5: Revisar antes de Publicar**

O Firebase mostrará avisos se houver erros:

```
✅ Verde = Sintaxe correta, pronto para publicar
⚠️  Amarelo = Aviso (pode ser ok)
❌ Vermelho = Erro, não pode publicar
```

---

### **Passo 6: Clique em "PUBLICAR"**

```
Mensagem: "Regras publicadas com sucesso!"
```

---

## 🧪 Testar as Regras

### **Usar o Simulador de Regras**

1. Na aba **Rules**, clique em **"Simulador de Regras"** (lado direito)
2. Configure um teste:

```
Operação:     read
Documento:    usuarios/user123
Contexto de Autenticação:
  uid: user123
```

3. Clique **"Executar"**

Resultado esperado:
```
✅ Permitido, pois uid == user123
```

---

### **Exemplo de Testes**

#### **Teste 1: Ler próprio perfil**
```
read         /usuarios/user123
auth.uid:    user123
Esperado:    ✅ Permitido
```

#### **Teste 2: Ler perfil de outro usuário**
```
read         /usuarios/user456
auth.uid:    user123
Esperado:    ❌ Bloqueado
```

#### **Teste 3: Admin lê qualquer perfil**
```
read         /usuarios/user456
auth.uid:    admin123
Role:        admin (verificar em DB)
Esperado:    ✅ Permitido
```

---

## 📋 Checklist de Implementação

- [ ] 1. Abrir Firebase Console
- [ ] 2. Ir em Firestore Database
- [ ] 3. Clicar na aba "Rules"
- [ ] 4. Copiar código de `FIRESTORE_SECURITY_RULES.md`
- [ ] 5. Colar no editor
- [ ] 6. Revisar erros (se houver)
- [ ] 7. Clicar em "PUBLICAR"
- [ ] 8. Testar com Simulador de Regras
- [ ] 9. Validar no app Streamlit

---

## ⚠️ Armadilhas Comuns

### **Erro 1: "Erro de sintaxe"**

**Problema:** Código não foi copiado completamente
**Solução:** Copie TUDO desde `rules_version` até a última `}`

### **Erro 2: "Rules publicadas mas não funcionam"**

**Problema:** Regras estão muito restritivas
**Solução:** 
1. Volte para Rules
2. Use o Simulador para testar
3. Aumente permissões se necessário

### **Erro 3: "Funciona dev, mas não em produção"**

**Problema:** Usuários em prod não têm papel definido
**Solução:**
```javascript
// Na rule, verifique se doc existe antes
exists(/databases/$(database)/documents/usuarios/$(request.auth.uid))
```

---

## 🔄 Atualizar Regras Depois

Se precisar mudar as regras depois:

1. Volte para **Rules** no Console
2. Edite como antes
3. Clique **PUBLICAR** novamente
4. As mudanças valem imediatamente!

---

## 📊 Estrutura de Coleções Esperada

Para as regras funcionarem, você precisa desta estrutura no Firestore:

```
firestore/
├── usuarios/
│   ├── user123/
│   │   ├── uid: "user123"
│   │   ├── nome: "João"
│   │   ├── email: "joao@example.com"
│   │   ├── role: "usuario|professor|admin"
│   │   └── ativo: true
│   │
│   └── admin456/
│       └── role: "admin"
│
├── ambientes/
│   ├── amb001/
│   │   ├── nome: "Sala 101"
│   │   ├── criador_uid: "prof123"
│   │   └── ativo: true
│   │
│   └── amb002/
│       └── ...
│
└── reservas/
    ├── res001/
    │   ├── usuario_uid: "user123"
    │   ├── ambiente_id: "amb001"
    │   ├── status: "pendente"
    │   └── data_inicio: timestamp
    │
    └── res002/
        └── ...
```

---

## 🎯 Permissões por Papel

Depois de publicar as regras, teste cada papel:

### **Papel: usuario**
```
✅ Ler próprio perfil
✅ Fazer reservas
❌ Ver outras reservas
❌ Deletar usuários
```

### **Papel: professor**
```
✅ Ler próprio perfil
✅ Criar ambientes
✅ Gerenciar suas aulas
❌ Deletar usuários
```

### **Papel: admin**
```
✅ Ler qualquer perfil
✅ Alterar papéis
✅ Ver todas as reservas
✅ Deletar usuários
✅ Acessar logs
```

---

## 🚨 Importante: Migração de Dados

Se você JÁ TEM dados no Firestore, **CUIDADO**:

1. As novas regras podem bloquear acesso
2. Teste ANTES de publicar em produção
3. Use o Simulador para testar

**Sugestão:**
```javascript
// Temporariamente, deixe mais permissivo
"Teste pelo Simulador" → Se OK → "Publique"
```

---

## 📞 Suporte

Se as regras não funcionarem:

1. **Verifique erro no Firebase Console:**
   - Logs aparece em "Firestore Database" → "Logs"

2. **Teste no Simulador:**
   - Reproduza exatamente o acesso que está falhando

3. **Consulte a documentação:**
   - [Firebase Security Rules](https://firebase.google.com/docs/firestore/security/rules-structure)

---

🎉 Pronto! Suas regras de segurança estão em produção!
