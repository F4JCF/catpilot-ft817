#!/bin/sh
# Installation de CAT Pilot FT-817 sous Linux (pour l'utilisateur, sans droits administrateur).
#   ./install.sh              installe ou met à jour
#   ./install.sh --desinstaller   retire le logiciel (vos données dans ~/Documents/CATPilot-FT817 restent)
#
# Le programme va dans ~/.local/bin (la mise à jour automatique du logiciel le remplace là),
# avec une entrée dans le menu des applications. Seules les vérifications facultatives
# (port série, PortAudio) demandent le mot de passe administrateur, et toujours après accord.
set -e
cd "$(dirname "$0")"
BIN="$HOME/.local/bin"
APPS="$HOME/.local/share/applications"
ICONS="$HOME/.local/share/icons/hicolor/256x256/apps"
EXE="$BIN/catpilot-ft817"

if [ "$1" = "--desinstaller" ] || [ "$1" = "--uninstall" ]; then
    rm -f "$EXE" "$APPS/catpilot-ft817.desktop" "$ICONS/catpilot-ft817.png"
    echo "CAT Pilot FT-817 est désinstallé (vos données dans ~/Documents/CATPilot-FT817 sont conservées)."
    exit 0
fi

mkdir -p "$BIN" "$APPS" "$ICONS"
install -m 755 CATPilot-FT817-linux-x86_64 "$EXE"
install -m 644 catpilot-ft817.png "$ICONS/catpilot-ft817.png"
cat > "$APPS/catpilot-ft817.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=CAT Pilot FT-817
Comment=Pilotage CAT des Yaesu FT-817, FT-818, FT-857 et FT-897
Exec=$EXE
Icon=catpilot-ft817
Terminal=false
Categories=HamRadio;Utility;
EOF
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APPS" >/dev/null 2>&1 || true
echo "Installé : $EXE (menu des applications : « CAT Pilot FT-817 »)."

ask() {  # ask "question" -> 0 si oui
    printf "%s [o/N] " "$1"
    read -r rep || rep=""
    case "$rep" in o|O|oui|Oui|y|Y) return 0 ;; *) return 1 ;; esac
}

# Accès au port série : groupe dialout (Debian, Ubuntu, Mint, Fedora) ou uucp (Arch)
GRP=dialout
getent group dialout >/dev/null 2>&1 || GRP=uucp
if getent group "$GRP" >/dev/null 2>&1 && ! id -nG "$USER" | tr ' ' '\n' | grep -qx "$GRP"; then
    echo
    echo "Pour utiliser le câble CAT, votre compte doit faire partie du groupe « $GRP »."
    if ask "L'ajouter maintenant (mot de passe administrateur demandé) ?"; then
        sudo usermod -aG "$GRP" "$USER" && echo "Fait. Fermez la session puis reconnectez-vous pour que ce soit pris en compte."
    else
        echo "Plus tard : sudo usermod -aG $GRP \$USER  (puis fermer et rouvrir la session)"
    fi
fi

# Audio (chute d'eau, FT8, messages vocaux) : bibliothèque PortAudio du système
if ! ldconfig -p 2>/dev/null | grep -q "libportaudio.so"; then
    echo
    echo "La bibliothèque audio PortAudio n'est pas installée (nécessaire pour la chute d'eau, FT8, etc.)."
    if command -v apt-get >/dev/null 2>&1; then CMD="sudo apt-get install -y libportaudio2"
    elif command -v dnf >/dev/null 2>&1; then CMD="sudo dnf install -y portaudio"
    elif command -v pacman >/dev/null 2>&1; then CMD="sudo pacman -S --needed portaudio"
    elif command -v zypper >/dev/null 2>&1; then CMD="sudo zypper install -y libportaudio2"
    else CMD=""; fi
    if [ -n "$CMD" ] && ask "L'installer maintenant ($CMD) ?"; then
        sh -c "$CMD" || echo "Installation impossible : à faire à la main ($CMD)."
    elif [ -n "$CMD" ]; then
        echo "Plus tard : $CMD"
    else
        echo "Installez le paquet PortAudio de votre distribution."
    fi
fi
echo
echo "Terminé. Lancez « CAT Pilot FT-817 » depuis le menu des applications, ou : $EXE"
