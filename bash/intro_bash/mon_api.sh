#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# Script pour tester l'API Market Hall
# ═══════════════════════════════════════════════════════════════

# Variable globale pour stocker le PID (Process ID) de Flask
API_PID=""

# ═══════════════════════════════════════════════════════════════
# FONCTION 1: Démarrer l'API
# ═══════════════════════════════════════════════════════════════
function demarrer_api {
    echo "🚀 Démarrage de l'API Flask..."
    
    # Lance Flask en arrière-plan avec &
    # > /dev/null 2>&1 redirige les logs (les supprime)
    python -m flask run > /dev/null 2>&1 &
    
    # $! récupère le PID du dernier processus lancé
    API_PID=$!
    
    # Attends un peu que Flask démarre
    sleep 3
    
    echo "✅ API démarrée (PID: $API_PID)"
    return 0
}

# ═══════════════════════════════════════════════════════════════
# FONCTION 2: Tester un endpoint
# ═══════════════════════════════════════════════════════════════
function tester_endpoint {
    local url=$1  # Premier argument passé à la fonction
    
    echo ""
    echo "🧪 Test de l'endpoint: $url"
    
    # Utilise cURL pour faire une requête GET
    # -s: mode silencieux (pas de barre de progression)
    # -o /dev/null: ne pas afficher la réponse
    # -w "%{http_code}": afficher seulement le code HTTP
    response_code=$( curl -s -o /dev/null -w "%{http_code}" "$url" )
    
    echo "Code HTTP reçu: $response_code"
    
    # Vérifie si le code est 200 (succès)
    if (( response_code == 200 ))
    then
        echo "✅ Endpoint OK!"
        return 0
    else
        echo "❌ Endpoint en erreur (code: $response_code)"
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════════
# FONCTION 3: Arrêter l'API
# ═══════════════════════════════════════════════════════════════
function arreter_api {
    echo ""
    echo "⏹️  Arrêt de l'API..."
    
    # Vérifie que API_PID n'est pas vide
    if [ -z "$API_PID" ]
    then
        echo "❌ Aucune API en cours d'exécution"
        return 1
    fi
    
    # kill envoie un signal SIGTERM au processus
    # Le processus s'arrête proprement
    kill $API_PID 2>/dev/null
    
    # Attends un peu que Flask s'arrête
    sleep 2
    
    echo "✅ API arrêtée"
    return 0
}

# ═══════════════════════════════════════════════════════════════
# APPELS DES FONCTIONS
# ═══════════════════════════════════════════════════════════════

echo "═══════════════════════════════════════════════════════════════"
echo "   Test automatisé de l'API Market Hall"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Étape 1: Démarrer l'API
demarrer_api

# Étape 2: Tester des endpoints
tester_endpoint "http://localhost:5000/api/v1/products"
tester_endpoint "http://localhost:5000/api/v1/users"
tester_endpoint "http://localhost:5000/api/v1/carts"

# Étape 3: Arrêter l'API
arreter_api

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "   Test terminé!"
echo "═══════════════════════════════════════════════════════════════"
