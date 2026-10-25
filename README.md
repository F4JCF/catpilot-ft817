# CAT Pilot FT-817 — Yaesu FT-817, FT-818, FT-857, FT-897

Logiciel Windows et Linux de pilotage CAT des Yaesu **FT-817, FT-818, FT-857 et FT-897**,
avec partage du CAT vers WSJT-X, JTDX, Log4OM, N1MM… grâce à un serveur
compatible rigctld.

C'est un logiciel **distinct** de CAT Pilot (FT-991A) : il s'installe à part, a
ses propres réglages (`Documents\CATPilot-FT817`) et ses propres mises à jour.
Les deux peuvent tourner en même temps sur le même PC (ports différents, voir
plus bas).

## Installation

- **Installateur** : `CATPilot-FT817-Setup-x.y.z.exe` dans la dernière version
  publiée (https://github.com/F4JCF/catpilot-ft817/releases/latest). Installation
  pour l'utilisateur, sans droits d'administrateur.
- **Sans installation** : `CATPilot-FT817.exe` de la même page, à lancer tel quel.
- Ensuite, les mises à jour se font depuis le logiciel (menu « Mise à jour »).

### Linux

- Télécharger `CATPilot-FT817-linux-x86_64.tar.gz` sur la même page, le
  décompresser, puis dans un terminal ouvert dans ce dossier : `./install.sh`
- Installation pour l'utilisateur (dans `~/.local/bin`), avec une entrée
  « CAT Pilot FT-817 » dans le menu des applications. Aucun Python à installer.
- Le script propose d'ajouter votre compte au groupe `dialout` (accès au câble
  CAT ; fermer puis rouvrir la session ensuite) et d'installer PortAudio
  (`libportaudio2`), nécessaire à l'audio (chute d'eau, FT8, messages vocaux).
- Le câble CAT apparaît comme `/dev/ttyUSB0` (ou `/dev/ttyACM0`).
- Distributions 64 bits récentes : Ubuntu 22.04, Debian 12, Linux Mint 21,
  Fedora 36 ou plus récentes.
- Mises à jour automatiques comme sous Windows ; désinstallation :
  `./install.sh --desinstaller`.

## Réglage du poste

- Câble CAT : CT-62 (ou équivalent USB-série), Digirig, SCU-17… branché sur la
  prise ACC (FT-817/818) ou CAT/LINEAR (FT-857/897).
- Menu **CAT RATE** du poste (FT-817/818 : menu 14 ; FT-857/897 : menu 019) :
  4800 bauds par défaut. Même valeur dans le logiciel (« Vitesse »), **2 bits de
  stop**.
- Le logiciel garde les lignes RTS et DTR au repos : une interface qui fait
  émettre le poste sur RTS (Digirig…) ne passe pas en émission à la connexion.
- Audio (FT8, chute d'eau, messages vocaux) : ces postes n'ont pas de carte son
  USB ; choisir l'entrée de l'interface audio (Digirig, SCU-17, Signalink…).
- Pour FT8 : mode **DATA-U** du logiciel = mode DIG du poste ; régler le menu
  « DIG MODE » du poste sur **USER-U**.

## Ce que le CAT de ces postes permet

Le protocole CAT des FT-817/818/857/897 est très limité par rapport à celui du
FT-991A. Le logiciel n'affiche donc que ce qui se pilote réellement :

| Fonction | |
|---|---|
| Fréquence (affichage, molette, saisie, bandes 160 m à 70 cm) | ✔ |
| Mode : USB, LSB, CW, CW-R, AM, FM, DATA-U (DIG), DATA-FM (PKT) | ✔ |
| Émission (MOX, PTT pour WSJT-X…), sécurité TX, coupure hors bande | ✔ |
| S-mètre | ✔ |
| En émission : puissance, ROS et ALC (FT-817/818/897) ; puissance et alarme ROS (FT-857) | ✔ |
| VFO A/B (bascule), A>B, B>A, VFO B réglable à la molette | ✔ |
| Split | ✔ |
| LOCK (verrouillage du bouton d'accord) | ✔ |
| Clarifier RX (±10 / ±100 Hz, CLR) | ✔ |
| Relais FM : décalage +/−, tonalité CTCSS (TSQ, émission) ou DCS | ✔ |
| Allumer / éteindre le poste | ✔ |
| Volume, gain HF, squelch, puissance, micro, VOX, processeur | ✘ (sur le poste) |
| Filtres, NB, DSP, AGC, ATT, IPO, keyer, vitesse CW | ✘ (sur le poste) |
| Menus et mémoires du poste | ✘ (non accessibles par le CAT) |

Notes :
- Le poste ne renvoie pas l'état du décalage relais, de la tonalité ni du
  clarifier : le logiciel affiche ce qu'il a lui-même réglé.
- Le split est relu dans le poste sur FT-817/818 ; sur FT-857/897 il est suivi
  par le logiciel.
- Au démarrage, le logiciel lit la fréquence du VFO B (bascule A/B très brève).
- Le logiciel n'écrit **jamais** dans l'EEPROM du poste (risque de perdre les
  réglages d'usine) ; il la lit seulement sur FT-817/818 pour l'état du split.

## Mémoires (bouton « Mémoires »)

Les mémoires du poste ne sont pas lisibles par le CAT. Le panneau gère donc une
**banque de canaux sur le PC** (`Documents\CATPilot-FT817\memoires_pc.json`) :
- « Ajouter un canal » (fréquence et mode actuels), édition par double-clic,
  import / export CSV (compatible avec les fichiers de CAT Pilot) ;
- « Enregistrer la banque PC » : enregistre les lignes modifiées (en jaune) ;
- double-clic sur le numéro : le poste se règle sur le canal (fréquence, mode,
  décalage relais, mode de tonalité) ;
- scan des canaux du tableau ou d'une plage de fréquences, arrêt sur signal.

## CW au clavier (bouton « CW clavier »)

Pas de keyer pilotable par le CAT sur ces postes : la manipulation se fait par la
ligne **DTR ou RTS** d'une interface reliée à la prise KEY (Digirig, interface CW
série…). Vitesse réglée dans le panneau. Messages programmables F1 à F5 et CQ
automatique comme dans CAT Pilot.

## Carnet : département et carte du QSO

- **Département** du correspondant (France) : numéro et nom (« 38 — Isère »),
  trouvé d'après son code postal (QRZ.com, HamQTH) ou à défaut son locator
  (6 caractères) ; DOM d'après le préfixe (FG, FM, FY, FR, FH). Modifiable à la
  main ; enregistré dans le carnet (champ ADIF STATE) et affiché dans la colonne
  Pays.
- **Carte du QSO** à droite de la fiche : ma station, le correspondant, le
  trajet entre les deux locators, distance et cap, département du correspondant
  en surbrillance. Molette : zoom ; double-clic : recadrer.
- Contours des départements : IGN Admin Express (Licence ouverte Etalab), via
  le projet france-geojson.

## Plusieurs indicatifs, chacun son matériel

Dans le carnet, « Je trafique en » garde la liste de vos indicatifs (F4JCF,
F4JCF/P, FR/F4JCF/P… : taper le nouvel indicatif puis Entrée). Le bouton
**Matériel…** associe à l'indicatif choisi un poste, une antenne, une puissance
et, si besoin, un locator (pour un /P).

- Exemple : F4JCF = FT-991A, 100 W, verticale ; F4JCF/P = FT-817, 5 W, EFHW,
  JN33KN.
- En passant d'un indicatif à l'autre, le locator de la station suit, et si le
  poste est l'un de ceux que ce logiciel pilote, il est choisi dans « Liaison »
  avec le port et la vitesse utilisés la dernière fois.
- Chaque QSO enregistre le matériel (ADIF MY_RIG, MY_ANTENNA, TX_PWR,
  MY_GRIDSQUARE) ; la puissance sert aussi quand le poste ne la donne pas par
  le CAT (cas des FT-817/857/897).

## Partager le CAT avec WSJT-X

Cocher « Serveur rigctld » (port **4534**). Dans WSJT-X : Radio « Hamlib NET
rigctl », serveur `127.0.0.1:4534`, PTT « CAT », mode « Data/Pkt ».
(Le port est 4534 et non 4532 pour pouvoir utiliser CAT Pilot FT-991A en même
temps. L'accès à distance utilise le port 4541.)

## Autres fonctions (identiques à CAT Pilot)

### Trafic au quotidien
- **Profils** (barre du haut) : « FT8 20 m », « BLU 40 m »… règlent d'un clic
  fréquence, mode, puissance et filtres. « Enregistrer… » crée un profil à
  partir des réglages actuels.
- **Puissance mémorisée par bande** : chaque bande retrouve sa dernière puissance.
- **Sécurité TX** : coupure de l'émission au-delà d'une durée réglable, quel que
  soit le logiciel qui émet (3 min par défaut, 0 = désactivée).
- **Clic sur la chute d'eau** : en BLU, DATA ou CW, le poste s'accorde sur le
  signal cliqué ; la ligne pointillée montre où il sera placé (1500 Hz, ou la
  note CW du poste).
- **Raccourcis** (menu Aide) : F12 = MOX, Ctrl+↑/↓ = accord, Page préc./suiv. =
  bande, Ctrl+M = mémoires, Ctrl+W = chute d'eau, Échap = arrêt du scan. Un
  bouton d'accord USB se programme pour envoyer Ctrl+↑ / Ctrl+↓.


### Horloge et propagation (barre du haut)
- Heure UTC (et locale), flux solaire, indices A et K, taches solaires, et état
  des bandes 80-40 / 30-20 / 17-15 / 12-10 (vert bonne, orange moyenne, rouge
  mauvaise, jour ou nuit selon l'heure locale). Données hamqsl.com (N0NBH),
  actualisées toutes les 30 min ou par un clic. Détails dans l'infobulle.


### Enregistrement de la réception
- « ● Enregistrer » sous la chute d'eau : fichier WAV de l'audio reçu, nommé avec
  la date, la fréquence et le mode, dans Documents\CATPilot-FT817\enregistrements.


### Affichage (menu « Affichage »)
- **Plan de bandes** sous la fréquence : segments IARU Région 1 (CW, numérique,
  BLU, balises, relais, satellites…) et repère de fréquence, à titre indicatif.
- **Émission hors bande** : si le poste émet hors des bandes amateurs, l'émission
  est coupée (option dans le menu Poste) ou signalée.
- **Mode nuit** (Ctrl+N) : tout en rouge sombre pour le portable de nuit.
- **Taille du texte** : 90 à 130 %.
- **Mode compact** (Ctrl+K) : petite fenêtre (fréquence, bande, mode, S-mètre,
  MOX), éventuellement au premier plan, à garder à côté de WSJT-X.


### Position de la station (menu Poste ou clic sur le locator)
- Locator saisi, GPS intégré de l'IC-705, ou GPS NMEA sur un port COM (GPS USB,
  sortie GPS de l'IC-705 sur son 2e port COM). Le locator s'affiche dans la barre
  du haut ; il servira aux spots, aux satellites et au rotor.


### Messages vocaux (bouton « Messages vocaux »)
- 6 messages enregistrés au micro du PC (« CQ CQ de… »), renommables, émis d'un
  clic ou par Ctrl+F1 à F4. CAT Pilot passe en émission, joue le message sur la
  sortie audio USB du poste, puis repasse en réception.
- Par défaut le mode bascule en DATA pendant le message, pour que le poste prenne
  sa modulation sur l'USB, puis revient au mode d'origine.
- Appel en boucle : « Répéter toutes les N s ». Échap ou Stop arrêtent tout.
- Régler le niveau pour que l'ALC bouge à peine.


### Spots (bouton « Spots »)
- Onglets **POTA** (api.pota.app), **SOTA** (sota.org.uk) et **DX cluster**
  (telnet, par défaut dxc.ve7cc.net:23, connexion avec votre indicatif).
- Filtres par bande et par mode, « bandes de mon poste » ; distance et cap
  depuis votre locator quand le spot en donne un. Les indicatifs déjà
  contactés sont grisés.
- **Double-clic** : le poste s'accorde (fréquence et mode) et le QSO est
  préparé dans le carnet avec la référence du parc ou du sommet.


### Carnet de trafic (bouton « Carnet », Ctrl+L)
- Saisie rapide : indicatif (Entrée = recherche HamQTH : nom, QTH, locator,
  distance et cap), RST préremplis selon le mode, fréquence et heure UTC prises
  sur le poste, références POTA/SOTA (la sienne et la vôtre en activation).
- « Déjà contacté » s'affiche dès la saisie de l'indicatif.
- Import et export ADIF, et **export de l'activation du jour** au nom de
  fichier attendu par POTA (INDICATIF@REF-DATE.adi).
- Le carnet est enregistré dans Documents\CATPilot-FT817\carnet.sqlite.
- Réglages (menu Carnet) : votre indicatif et votre compte HamQTH (gratuit).


### Liaison WSJT-X (bouton « WSJT-X »)
- Dans WSJT-X : Paramètres > Rapports > Serveur UDP 127.0.0.1, port 2237,
  cocher « Accepter les requêtes UDP ». Puis « Écouter WSJT-X » dans CAT Pilot.
- Liste des stations entendues (SNR, locator, distance) ; en vert les CQ
  d'indicatifs jamais contactés. Double-clic : WSJT-X appelle la station.
- Les QSO journalisés dans WSJT-X sont inscrits au carnet (sans doublon).
- Si JTAlert ou GridTracker écoutent déjà WSJT-X, utilisez l'adresse
  multicast 224.0.0.1 dans WSJT-X et dans CAT Pilot.


### Satellites (bouton « Satellites »)
- Orbites CelesTrak et transpondeurs SatNOGS (mis en cache, actualisés chaque
  jour ; liste intégrée de secours : ISS, SO-50, PO-101, RS-44, AO-7).
- Passages des prochaines 24 h au-dessus d'une élévation choisie, position en
  temps réel (azimut, élévation, distance, vitesse radiale).
- **Suivre ce satellite** : réception sur le VFO A, émission sur le VFO B en
  split, correction Doppler en continu, tonalité CTCSS des relais FM, et rotor
  piloté en azimut et élévation. Sur un transpondeur linéaire, tournez le VFO
  pour vous déplacer : l'émission suit (inversion gérée).
- Fonctionnement en semi-duplex (FT-991A, IC-705…) : on n'entend pas sa propre
  voie descendante pendant l'émission.


### Panoramique SDR (bouton « SDR »)
- Clé RTL-SDR (NooElec…) en USB (pilote WinUSB installé avec Zadig) ou via
  rtl_tcp sur le réseau (clé sur un Raspberry Pi par exemple).
- Spectre et chute d'eau jusqu'à 1,9 MHz de large, centrés automatiquement sur
  la fréquence du poste (trait rouge). **Clic sur un signal : le poste s'y
  accorde.**
- HF : convertisseur (Ham It Up : décalage 125 MHz) ou échantillonnage direct
  (clé V3). Réglages de gain et de correction ppm.
- **Le SDR doit avoir sa propre antenne** ou un coupleur protégé : jamais sur
  la sortie de l'émetteur.


### Pilotage à distance (bouton « À distance »)
- **Sur le PC relié au poste** : cocher « Autoriser l'accès à distance »,
  choisir un mot de passe (6 caractères au moins) et les entrées/sorties audio
  du poste (USB Audio CODEC).
- **Sur le PC distant** : indiquer l'adresse de la station (ex.
  192.168.1.20:4540, ou son adresse VPN) et le mot de passe, le micro et les
  haut-parleurs, puis choisir « Poste distant (CAT Pilot) » dans la liste des
  postes et cliquer sur Connecter. Toute l'interface fonctionne comme en local,
  y compris le serveur rigctld pour WSJT-X sur le PC distant.
- Audio dans les deux sens (µ-law 8 kHz, environ 64 kbit/s par sens).
- Sécurité : mot de passe par défi-réponse (il ne circule jamais), blocage de
  10 min après 5 essais faux, PTT coupé si le distant se déconnecte ou si son
  audio s'interrompt plus de 3 s. Les échanges ne sont pas chiffrés : pour
  Internet, passez de préférence par un VPN (WireGuard, Tailscale) plutôt
  qu'une redirection de port sur la box.


### Langue (menu Affichage > Langue)
- Français ou anglais, au prochain démarrage (proposé tout de suite).


### Mise à jour (menu « Mise à jour », à côté de « Aide »)
- « Vérifier les mises à jour… » consulte la dernière version publiée sur
  GitHub ; « Mettre à jour maintenant » télécharge CATPilot-FT817.exe, vérifie son
  empreinte, ferme le logiciel, remplace l'exécutable et le relance (le poste
  n'est pas éteint pendant ce redémarrage).
- Vérification automatique au démarrage (désactivable) ; un « ● » sur le menu
  signale une nouvelle version.
- Chaque changement du numéro de version publie automatiquement une
  « Release » sur GitHub. Le dépôt doit être **public** pour que les
  exécutables déjà installés puissent la télécharger.


### Rotor d'antenne (bouton « Rotor »)
- Yaesu GS-232A/B et compatibles (ERC, K3NG…) sur port série, ou rotctld de
  Hamlib sur le réseau ; azimut et élévation.
- Rose des vents : clic pour orienter. Cap saisi, locator visé (court ou long
  chemin), et orientation automatique lors d'un double-clic sur un spot, d'une
  recherche HamQTH ou d'un appel WSJT-X (option).


## À valider sur le poste

Le pilote a été testé sur un poste simulé reproduisant le protocole CAT binaire
(d'après les manuels Yaesu et les pilotes Hamlib). Merci de signaler tout écart
constaté sur un vrai FT-817, FT-818, FT-857 ou FT-897 (le journal
`Documents\CATPilot-FT817\journal_cat.txt` aide à comprendre une coupure).

## Licence

Voir le fichier LICENSE.
