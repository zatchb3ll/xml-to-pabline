#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
from datetime import datetime
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def extrair_texto_pdf(caminho_pdf):
    """Extrai texto de um arquivo PDF"""
    texto_completo = ""
    num_paginas = 0
    
    try:
        with open(caminho_pdf, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            num_paginas = len(leitor.pages)
            
            for pagina in leitor.pages:
                texto = pagina.extract_text()
                if texto:
                    texto_completo += texto + "\n"
    except Exception as e:
        print(f"Erro ao extrair texto: {e}")
        raise
    
    return texto_completo.strip(), num_paginas

def escapar_xml(texto):
    """Escapa caracteres especiais para XML"""
    if not texto:
        return ""
    
    texto = texto.replace("&", "&amp;")
    texto = texto.replace("<", "&lt;")
    texto = texto.replace(">", "&gt;")
    texto = texto.replace('"', "&quot;")
    texto = texto.replace("'", "&apos;")
    
    return texto

def criar_xml(caminho_pdf, texto, num_paginas):
    """Cria um documento XML a partir dos dados do PDF"""
    
    # Informações do arquivo
    tamanho_bytes = os.path.getsize(caminho_pdf)
    nome_arquivo = os.path.basename(caminho_pdf)
    data_conversao = datetime.now().isoformat()
    
    # Criar estrutura XML
    root = ET.Element("documento")
    
    # Metadados
    metadados = ET.SubElement(root, "metadados")
    
    ET.SubElement(metadados, "nome_arquivo").text = nome_arquivo
    ET.SubElement(metadados, "tamanho_bytes").text = str(tamanho_bytes)
    ET.SubElement(metadados, "tamanho_kb").text = f"{tamanho_bytes / 1024:.2f}"
    ET.SubElement(metadados, "data_conversao").text = data_conversao
    ET.SubElement(metadados, "total_paginas").text = str(num_paginas)
    ET.SubElement(metadados, "tipo_origem").text = "application/pdf"
    ET.SubElement(metadados, "tipo_destino").text = "text/xml"
    
    # Conteúdo
    conteudo = ET.SubElement(root, "conteudo")
    texto_element = ET.SubElement(conteudo, "texto")
    texto_element.text = escapar_xml(texto)
    
    # Formatar XML com indentação
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    
    # Remover linhas vazias
    xml_str = "\n".join([linha for linha in xml_str.split("\n") if linha.strip()])
    
    return xml_str

def converter_pdf_para_xml(caminho_pdf, caminho_saida=None):
    """Função principal de conversão"""
    
    print(f"📄 Processando: {caminho_pdf}")
    print("⏳ Extraindo texto...")
    
    # Extrair texto
    texto, num_paginas = extrair_texto_pdf(caminho_pdf)
    
    print(f"✅ Texto extraído ({num_paginas} páginas)")
    print("🔄 Criando XML...")
    
    # Criar XML
    xml_content = criar_xml(caminho_pdf, texto, num_paginas)
    
    # Salvar arquivo
    if caminho_saida is None:
        caminho_saida = caminho_pdf.replace(".pdf", ".xml")
    
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Arquivo salvo: {caminho_saida}")
    
    return xml_content, caminho_saida

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python converter.py <caminho_pdf> [caminho_saida]")
        sys.exit(1)
    
    caminho_pdf = sys.argv[1]
    caminho_saida = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(caminho_pdf):
        print(f"❌ Arquivo não encontrado: {caminho_pdf}")
        sys.exit(1)
    
    try:
        converter_pdf_para_xml(caminho_pdf, caminho_saida)
        print("\n✨ Conversão concluída com sucesso!")
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)
