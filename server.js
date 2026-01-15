const express = require('express');
const multer = require('multer');
const pdfParse = require('pdf-parse');
const fs = require('fs');
const path = require('path');
const js2xmlparser = require('js2xmlparser');

const app = express();
const PORT = 3000;

// Configurar multer para upload
const storage = multer.memoryStorage();
const upload = multer({
    storage: storage,
    limits: { fileSize: 50 * 1024 * 1024 },
    fileFilter: (req, file, cb) => {
        if (file.mimetype === 'application/pdf') {
            cb(null, true);
        } else {
            cb(new Error('Apenas arquivos PDF são permitidos'), false);
        }
    }
});

// Servir arquivos estáticos
app.use(express.static(__dirname));

// Rota para conversão PDF to XML
app.post('/api/convert', upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'Nenhum arquivo foi enviado' });
        }

        // Parse PDF
        const pdfData = await pdfParse(req.file.buffer);

        // Estruturar dados para XML
        const xmlData = {
            '@': {
                xmlns: 'http://www.example.com/pdf-to-xml',
                version: '1.0'
            },
            metadata: {
                filename: req.file.originalname,
                filesize: req.file.size,
                uploadDate: new Date().toISOString(),
                totalPages: pdfData.numpages,
                totalText: pdfData.text.length
            },
            content: {
                text: sanitizeText(pdfData.text)
            }
        };

        // Se houver informações adicionais do PDF
        if (pdfData.info) {
            xmlData.metadata.pdfInfo = {
                title: pdfData.info.Title || 'N/A',
                author: pdfData.info.Author || 'N/A',
                subject: pdfData.info.Subject || 'N/A',
                creator: pdfData.info.Creator || 'N/A',
                producer: pdfData.info.Producer || 'N/A'
            };
        }

        // Converter para XML
        const xmlString = js2xmlparser.parse('document', xmlData, {
            declaration: {
                include: true,
                encoding: 'UTF-8'
            },
            format: {
                doubleQuotes: true
            }
        });

        res.json({
            success: true,
            xml: xmlString
        });

    } catch (error) {
        console.error('Erro na conversão:', error);
        res.status(500).json({
            error: `Erro ao processar o arquivo: ${error.message}`
        });
    }
});

// Função para limpar e estruturar texto
function sanitizeText(text) {
    // Remove espaços em branco excessivos
    return text
        .trim()
        .replace(/\n\n+/g, '\n')
        .replace(/\s+/g, ' ')
        .trim();
}

// Rota para verificar se o servidor está rodando
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`🚀 Servidor rodando em http://localhost:${PORT}`);
    console.log('Pronto para receber arquivos PDF');
});

// Tratamento de erros
app.use((err, req, res, next) => {
    console.error(err);
    res.status(500).json({
        error: 'Erro no servidor: ' + err.message
    });
});
