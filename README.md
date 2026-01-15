# 📄 Conversor PDF para XML

Site completo para converter arquivos PDF em XML.

## 🚀 Como Instalar e Usar

### Pré-requisitos
- Node.js (v14 ou superior) - [Baixar aqui](https://nodejs.org/)

### Instalação

1. **Abra o PowerShell** na pasta do projeto:
```powershell
cd "C:\Users\Paulo Henrique\Documents\PH Github\projeto xml"
```

2. **Instale as dependências**:
```powershell
npm install
```

3. **Inicie o servidor**:
```powershell
npm start
```

4. **Abra no navegador**:
```
http://localhost:3000
```

## 📝 Funcionalidades

✅ Interface moderna e intuitiva
✅ Upload de arquivo PDF via drag-and-drop ou clique
✅ Conversão automática para XML
✅ Extração de metadados do PDF
✅ Download do arquivo XML gerado
✅ Validação de arquivo (máximo 50MB)

## 📦 Arquivos do Projeto

- **index.html** - Interface do usuário (frontend)
- **server.js** - Servidor Node.js (backend)
- **package.json** - Dependências do projeto
- **README.md** - Este arquivo

## 🔧 Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript Vanilla
- **Backend**: Node.js, Express.js
- **Processamento**: pdf-parse, js2xmlparser

## 📤 Upload e Conversão

1. Clique na área de upload ou arraste um PDF
2. Clique em "Converter para XML"
3. Aguarde o processamento
4. Baixe o arquivo XML gerado

## ✨ Resultado XML

O arquivo XML gerado contém:
- Metadados do PDF (nome, tamanho, datas)
- Informações do documento (título, autor, criador)
- Conteúdo de texto extraído
- Estrutura XML bem formatada

## 🐛 Solução de Problemas

### Erro: "Cannot find module"
```powershell
npm install
```

### Porta 3000 já em uso
Altere a porta no `server.js`:
```javascript
const PORT = 3001; // ou outra porta
```

### Problema na conversão
- Certifique-se que o PDF não está corrompido
- Verifique se o arquivo tem menos de 50MB
- Reinicie o servidor

## 📞 Suporte

Para mais informações, consulte a documentação:
- [Express.js](https://expressjs.com/)
- [pdf-parse](https://www.npmjs.com/package/pdf-parse)
- [js2xmlparser](https://www.npmjs.com/package/js2xmlparser)
