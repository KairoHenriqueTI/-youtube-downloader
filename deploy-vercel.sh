#!/bin/bash

# 🚀 Script de Deploy para Vercel

echo "🚀 Preparando deploy para Vercel..."

# Verificar se Vercel CLI está instalada
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI não encontrada!"
    echo "📦 Instalando Vercel CLI..."
    npm install -g vercel
fi

# Ir para o diretório do projeto
cd ~/projects/youtube-downloader

echo ""
echo "📝 Instruções:"
echo "1. Faça login na Vercel quando solicitado"
echo "2. Escolha seu usuário/organização"
echo "3. Confirme o nome do projeto"
echo "4. Escolha o diretório atual (.)"
echo ""
echo "Pressione ENTER para continuar..."
read

# Deploy
vercel --prod

echo ""
echo "✅ Deploy concluído!"
echo "🌐 Acesse o link fornecido pela Vercel"
echo ""
echo "⚠️  LEMBRE-SE: A Vercel tem limitações:"
echo "   - Vídeos muito grandes podem dar timeout"
echo "   - Para playlists grandes, use a VPS"
