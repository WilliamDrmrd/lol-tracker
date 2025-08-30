#!/usr/bin/env python3
"""
🎮 LoL Rank Tracker - Version Ultra Sexy 🎮
Pas de dépendances externes, que du Python pur !
"""
import os
import json
from datetime import datetime

# Configuration
STORAGE_FILE = 'progression_data.json'

# Les ranks avec leurs couleurs ANSI
RANK_COLORS = {
    'Iron': '\033[90m',      # Gris foncé
    'Bronze': '\033[33m',    # Jaune/Orange
    'Silver': '\033[37m',    # Blanc
    'Gold': '\033[93m',      # Jaune brillant
    'Platinum': '\033[96m',  # Cyan
    'Emerald': '\033[92m',   # Vert brillant
    'Diamond': '\033[94m',   # Bleu
    'Master': '\033[95m',    # Magenta
    'Grandmaster': '\033[91m', # Rouge brillant
    'Challenger': '\033[97m\033[41m'  # Blanc sur fond rouge
}

RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# Construction des ranks avec style
RANKS = []
for tier in ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Emerald", "Diamond"]:
    for div in ["IV", "III", "II", "I"]:
        RANKS.append(f"{tier} {div}")
RANKS.extend(["Master", "Grandmaster", "Challenger"])

def colorize_rank(rank):
    """Applique la couleur appropriée au rang"""
    for tier, color in RANK_COLORS.items():
        if rank.startswith(tier):
            return f"{color}{rank}{RESET}"
    return rank

def colorize_grade(grade):
    """Applique la couleur appropriée à la note (alignée sur la logique KDA)"""
    if grade in ['S+', 'S', 'S-']:
        return f"\033[95m{grade}{RESET}"  # Magenta/Violet pour S
    elif grade in ['A+', 'A', 'A-']:
        return f"\033[93m{grade}{RESET}"  # Or/Jaune pour A
    elif grade in ['B+', 'B', 'B-']:
        return f"\033[92m{grade}{RESET}"  # Vert pour B
    elif grade in ['C+', 'C', 'C-']:
        return f"\033[96m{grade}{RESET}"  # Cyan pour C
    elif grade in ['D+', 'D', 'D-']:
        return f"\033[91m{grade}{RESET}"  # Rouge pour D
    return grade

def format_kda(kills, deaths, assists):
    """Formate le KDA avec couleurs selon la performance"""
    kda_ratio = (kills + assists) / max(deaths, 1)
    
    if kda_ratio >= 4.0:
        color = '\033[95m'  # Magenta/Violet (Légendaire)
    elif kda_ratio >= 3.0:
        color = '\033[93m'  # Or/Jaune (Excellent)
    elif kda_ratio >= 2.5:
        color = '\033[92m'  # Vert (Très bon)
    elif kda_ratio >= 2.0:
        color = '\033[96m'  # Cyan (Bon)
    elif kda_ratio >= 1.5:
        color = '\033[97m'  # Blanc (Correct)
    elif kda_ratio >= 1.0:
        color = '\033[33m'  # Jaune foncé (Moyen)
    else:
        color = '\033[91m'  # Rouge (Mauvais)
    
    return f"{color}{kills}/{deaths}/{assists}{RESET}"

def pad_colored_string(text, width):
    """Pad une chaîne colorée en tenant compte des codes ANSI"""
    # Calculer la longueur visible (sans codes ANSI)
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_text = ansi_escape.sub('', text)
    visible_len = len(clean_text)
    
    if visible_len >= width:
        return text
    
    padding = width - visible_len
    return text + ' ' * padding

def print_banner():
    """Affiche un banner sexy"""
    banner = f"""
{BOLD}\033[95m╔══════════════════════════════════════╗
║        🎮 LoL Rank Tracker 🎮        ║
║           Version Ultra Sexy         ║
╚══════════════════════════════════════╝{RESET}
    """
    print(banner)

def print_progress_bar(current_lp, max_lp=100):
    """Affiche une barre de progression stylée"""
    if max_lp <= 0:
        return ""
    
    progress = min(current_lp / max_lp, 1.0)
    bar_length = 20
    filled = int(progress * bar_length)
    
    bar = "█" * filled + "░" * (bar_length - filled)
    percentage = int(progress * 100)
    
    # Couleur selon le pourcentage
    if percentage >= 80:
        color = '\033[92m'  # Vert
    elif percentage >= 60:
        color = '\033[93m'  # Jaune
    elif percentage >= 40:
        color = '\033[96m'  # Cyan
    else:
        color = '\033[91m'  # Rouge
    
    return f"{color}[{bar}] {percentage}%{RESET}"

def load_data():
    """Charge les données avec gestion d'erreur sexy"""
    try:
        if os.path.exists(STORAGE_FILE):
            with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ {len(data)} entrées chargées avec succès !")
                return data
    except Exception as e:
        print(f"⚠️  Erreur lors du chargement: {e}")
    
    print("🆕 Nouveau fichier de progression créé !")
    return []

def save_data(data):
    """Sauvegarde avec feedback visuel"""
    try:
        with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Données sauvegardées ({len(data)} entrées)")
        return True
    except Exception as e:
        print(f"❌ Erreur de sauvegarde: {e}")
        return False

def get_next_rank(rank):
    """Obtient le rang suivant"""
    try:
        idx = RANKS.index(rank)
        return RANKS[idx + 1] if idx + 1 < len(RANKS) else rank
    except ValueError:
        return rank

def get_prev_rank(rank):
    """Obtient le rang précédent"""
    try:
        idx = RANKS.index(rank)
        return RANKS[idx - 1] if idx > 0 else rank
    except ValueError:
        return rank

def format_lp_change(lp_change):
    """Formate le changement de LP avec couleurs"""
    try:
        if lp_change > 0:
            return f"{BOLD}\033[92m+{lp_change} LP{RESET}"
        elif lp_change < 0:
            return f"{BOLD}\033[91m{lp_change} LP{RESET}"
        else:
            return f"{BOLD}\033[93m±0 LP{RESET}"
    except:
        return f"{BOLD}\033[93m±0 LP{RESET}"

def display_data(data):
    """Affichage ultra sexy des données"""
    if not data:
        print(f"{BOLD}📊 Aucune donnée à afficher{RESET}")
        return
    
    print(f"\n{BOLD}{UNDERLINE}📈 HISTORIQUE DE PROGRESSION{RESET}")
    print(f"Nombre de parties: {BOLD}{UNDERLINE}{len(data)}{RESET}")
    print("─" * 120)
    
    # En-tête avec largeurs fixes pour l'alignement
    print(f"{'Date':<20} {'Rang':<20} {'LP Change':<15} {'LP Total':<12} {'KDA':<15} {'Grade':<8} {'Notes'}")
    print("─" * 120)

    # Données - affiche les 500 dernières entrées
    for entry in data[-500:]:
        timestamp = entry['timestamp'][:16] if len(entry['timestamp']) > 16 else entry['timestamp']
        
        # Rang avec couleur
        rank_colored = colorize_rank(entry['rank'])
        
        # Format LP change avec couleur
        lp_change = entry.get('lp_change', 0)
        lp_change_colored = format_lp_change(lp_change)
        
        lp_total = f"{entry['lp_total']} LP"
        
        # KDA et Grade (avec gestion des anciennes entrées qui n'ont pas ces champs)
        kills = entry.get('kills', 0)
        deaths = entry.get('deaths', 1)  # Éviter division par 0
        assists = entry.get('assists', 0)
        kda_colored = format_kda(kills, deaths, assists) if 'kills' in entry else "N/A"
        
        grade = entry.get('grade', 'N/A')
        grade_colored = colorize_grade(grade) if grade != 'N/A' else grade
        
        # Notes spéciales - inclut les notes custom si elles existent
        notes = entry.get('note', '')  # Récupère la note si elle existe
        if 'promote' in entry:
            promo_note = f"🚀 → {entry['promote']['to']}"
            notes = f"{notes} {promo_note}" if notes else promo_note
        elif 'demote' in entry:
            demo_note = f"📉 → {entry['demote']['to']}"
            notes = f"{notes} {demo_note}" if notes else demo_note
        
        # Affichage avec format fixe - utiliser le padding correct pour les chaînes colorées
        timestamp_padded = f"{timestamp:<20}"
        rank_padded = pad_colored_string(rank_colored, 20)
        lp_change_padded = pad_colored_string(lp_change_colored, 15)
        lp_total_padded = f"{lp_total:<12}"
        kda_padded = pad_colored_string(kda_colored, 15)
        grade_padded = pad_colored_string(grade_colored, 8)
        
        print(f"{timestamp_padded} {rank_padded} {lp_change_padded} {lp_total_padded} {kda_padded} {grade_padded} {notes}")
    
    # Statistiques actuelles
    if data:
        current = data[-1]
        print("\n" + "═" * 120)
        print(f"{BOLD}🎯 STATUT ACTUEL{RESET}")
        print(f"Rang: {colorize_rank(current['rank'])}")
        print(f"LP: {BOLD}{current['lp_total']}{RESET}")
        
        # Barre de progression (si pas Master+)
        if not any(tier in current['rank'] for tier in ['Master', 'Grandmaster', 'Challenger']):
            lp_in_rank = current['lp_total'] % 100
            progress_bar = print_progress_bar(lp_in_rank)
            print(f"Progression: {progress_bar}")
        
        print("═" * 120)

def get_user_input(prompt, input_type=str, validation=None):
    """Fonction d'input sécurisée avec validation"""
    while True:
        try:
            value = input(f"{BOLD}🔸 {prompt}: {RESET}").strip()
            if not value:
                continue
                
            # Conversion de type
            if input_type == int:
                value = int(value)
            
            # Validation personnalisée
            if validation and not validation(value):
                print("❌ Valeur invalide, réessayez.")
                continue
                
            return value
        except ValueError:
            print(f"❌ Veuillez entrer un {input_type.__name__} valide.")
        except KeyboardInterrupt:
            print("\n👋 Au revoir !")
            exit(0)

def add_entry(data):
    """Ajoute une nouvelle entrée avec style"""
    print(f"\n{BOLD}➕ AJOUTER UNE NOUVELLE ENTRÉE{RESET}")
    print("─" * 40)
    
    # Déterminer le rang et LP actuels
    if data:
        current_rank = data[-1]['rank']
        current_lp = data[-1]['lp_total']
        print(f"Statut actuel: {colorize_rank(current_rank)} - {current_lp} LP")
    else:
        print("🆕 Première entrée ! Définissons votre rang initial.")
        current_rank = get_user_input("Rang initial (ex: Silver II)")
        current_lp = get_user_input("LP initial", int, lambda x: x >= 0)
    
    # Changement de LP
    lp_change = get_user_input("Changement de LP (+/-)", int)
    new_lp_total = current_lp + lp_change

    # Grade input with validation
    valid_grades = ['S+', 'S', 'S-', 'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-']
    grade = get_user_input("Grade (S+, S, S-, A+, A, A-, B+, B, B-, C+, C, C-, D+, D, D-)", str, lambda x: x in valid_grades)
    
    # KDA input
    kills = get_user_input("Kills", int, lambda x: x >= 0)
    deaths = get_user_input("Deaths", int, lambda x: x >= 0)
    assists = get_user_input("Assists", int, lambda x: x >= 0)
    
    # Note optionnelle
    note = input(f"{BOLD}📝 Note optionnelle (Entrée pour ignorer): {RESET}").strip()
    
    # Création de l'entrée
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rank": current_rank,
        "lp_change": lp_change,
        "lp_total": new_lp_total,
        "kills": kills,
        "deaths": deaths,
        "assists": assists,
        "grade": grade
    }
    
    # Ajouter la note si elle existe
    if note:
        entry["note"] = note
    
    # Gestion des promotions/démotions avec correction LP
    if new_lp_total >= 100 and not any(tier in current_rank for tier in ['Master', 'Grandmaster', 'Challenger']):
        next_rank = get_next_rank(current_rank)
        if next_rank != current_rank:
            promote = input(f"🚀 {new_lp_total} LP - Promotion vers {colorize_rank(next_rank)} ? (o/N): ").strip().lower()
            if promote == 'o':
                start_lp = get_user_input(f"LP de départ en {next_rank}", int, lambda x: 0 <= x <= 100)
                # Calculer le vrai changement LP pour la promotion
                # LP pour atteindre 100 + LP de départ dans le nouveau rang
                real_lp_change = (100 - current_lp) + start_lp
                entry["lp_change"] = real_lp_change
                entry["promote"] = {"to": next_rank, "start_lp": start_lp}
                entry["rank"] = next_rank
                entry["lp_total"] = start_lp
                print(f"🎉 Félicitations pour votre promotion en {colorize_rank(next_rank)} !")
    
    elif new_lp_total < 0:
        prev_rank = get_prev_rank(current_rank)
        if prev_rank != current_rank:
            demote = input(f"📉 {new_lp_total} LP - Démotion vers {colorize_rank(prev_rank)} ? (o/N): ").strip().lower()
            if demote == 'o':
                start_lp = get_user_input(f"LP de départ en {prev_rank}", int, lambda x: 0 <= x <= 100)
                # Pour les démotions, lp_change doit rester négatif pour refléter que c'est une loss
                # On garde le changement négatif original qui a causé la démotion
                entry["demote"] = {"to": prev_rank, "start_lp": start_lp}
                entry["rank"] = prev_rank
                entry["lp_total"] = start_lp
                print(f"💪 Pas de souci, on remonte depuis {colorize_rank(prev_rank)} !")
    
    data.append(entry)
    print(f"\n✅ Entrée ajoutée: {colorize_rank(entry['rank'])} - {entry['lp_total']} LP")
    return data

def show_help():
    """Affiche l'aide avec style"""
    help_text = f"""
{BOLD}🎮 COMMANDES DISPONIBLES{RESET}
─────────────────────────────
{BOLD}a{RESET} - ➕ Ajouter une entrée
{BOLD}p{RESET} - 📊 Afficher l'historique
{BOLD}s{RESET} - 📈 Statistiques
{BOLD}h{RESET} - ❓ Cette aide
{BOLD}q{RESET} - 👋 Quitter et sauvegarder
"""
    print(help_text)

def calculate_streaks(data):
    """Calcule les win/lose streaks en se basant sur les vraies W/L pas les LP"""
    if not data:
        return {"current": 0, "best_win": 0, "worst_lose": 0, "type": "none"}
    
    current_streak = 0
    best_win_streak = 0
    worst_lose_streak = 0
    streak_type = "none"
    
    # Streak actuel - on regarde depuis la fin
    for entry in reversed(data):
        lp_change = entry.get('lp_change', 0)
        
        # Les démotions comptent comme des losses même si elles ont une promotion/demotion flag
        if 'demote' in entry:
            # C'est une loss (démotion)
            if current_streak <= 0:
                current_streak -= 1
                streak_type = "lose"
            else:
                break
        elif 'promote' in entry:
            # C'est une win (promotion)
            if current_streak >= 0:
                current_streak += 1
                streak_type = "win"
            else:
                break
        elif lp_change > 0:  # Win normale
            if current_streak >= 0:
                current_streak += 1
                streak_type = "win"
            else:
                break
        elif lp_change < 0:  # Loss normale
            if current_streak <= 0:
                current_streak -= 1
                streak_type = "lose"
            else:
                break
        # Ignorer les ±0 LP
    
    # Calcul des meilleurs streaks de toute la session
    temp_streak = 0
    for entry in data:
        lp_change = entry.get('lp_change', 0)
        
        # Les démotions comptent comme des losses
        if 'demote' in entry:
            if temp_streak <= 0:
                temp_streak -= 1
            else:
                temp_streak = -1
            worst_lose_streak = min(worst_lose_streak, temp_streak)
        elif 'promote' in entry:
            if temp_streak >= 0:
                temp_streak += 1
            else:
                temp_streak = 1
            best_win_streak = max(best_win_streak, temp_streak)
        elif lp_change > 0:  # Win
            if temp_streak >= 0:
                temp_streak += 1
            else:
                temp_streak = 1
            best_win_streak = max(best_win_streak, temp_streak)
        elif lp_change < 0:  # Loss
            if temp_streak <= 0:
                temp_streak -= 1
            else:
                temp_streak = -1
            worst_lose_streak = min(worst_lose_streak, temp_streak)
        # Ignorer les ±0 LP
    
    return {
        "current": abs(current_streak),
        "best_win": best_win_streak,
        "worst_lose": abs(worst_lose_streak),
        "type": streak_type
    }

def draw_winrate_chart(winrate):
    """Dessine un graphique de winrate en ASCII"""
    bar_length = 40
    filled = int(winrate / 100 * bar_length)
    empty = bar_length - filled
    
    if winrate >= 70:
        color = '\033[92m'  # Vert
        icon = "🔥"
    elif winrate >= 60:
        color = '\033[93m'  # Jaune
        icon = "⚡"
    elif winrate >= 50:
        color = '\033[96m'  # Cyan
        icon = "⚖️"
    else:
        color = '\033[91m'  # Rouge
        icon = "💀"
    
    bar = "█" * filled + "░" * empty
    return f"{color}[{bar}] {winrate:.1f}% {icon}{RESET}"

def draw_lp_trend(data, last_n=10):
    """Dessine un graphique de tendance LP"""
    if len(data) < 2:
        return "Pas assez de données"
    
    # Prendre les derniers points
    recent_data = data[-last_n:] if len(data) >= last_n else data
    lp_values = [entry['lp_total'] for entry in recent_data]
    
    min_lp = min(lp_values)
    max_lp = max(lp_values)
    height = 8
    width = min(len(lp_values), 30)
    
    if max_lp == min_lp:
        return "LP stable " + "─" * width
    
    # Normaliser les valeurs
    normalized = []
    for lp in lp_values[-width:]:
        norm = int((lp - min_lp) / (max_lp - min_lp) * (height - 1))
        normalized.append(norm)
    
    # Dessiner le graphique
    lines = []
    for y in range(height - 1, -1, -1):
        line = ""
        for x, norm_val in enumerate(normalized):
            if norm_val == y:
                line += "●"
            elif norm_val > y:
                line += "│"
            else:
                line += " "
        lines.append(line)
    
    # Couleur selon la tendance
    trend = lp_values[-1] - lp_values[0]
    if trend > 0:
        color = '\033[92m'  # Vert
        arrow = "📈"
    elif trend < 0:
        color = '\033[91m'  # Rouge
        arrow = "📉"
    else:
        color = '\033[93m'  # Jaune
        arrow = "➡️"
    
    result = f"{arrow} Tendance LP (dernières {width} games):\n"
    for line in lines:
        result += f"    {color}{line}{RESET}\n"
    
    result += f"    {min_lp} LP {' ' * (width-10)} {max_lp} LP"
    return result

def get_rank_distribution(data):
    """Calcule la distribution des rangs"""
    ranks = {}
    for entry in data:
        rank = entry['rank']
        ranks[rank] = ranks.get(rank, 0) + 1
    
    return sorted(ranks.items(), key=lambda x: x[1], reverse=True)

def calculate_kda_stats(data):
    """Calcule les statistiques KDA"""
    entries_with_kda = [e for e in data if 'kills' in e]
    if not entries_with_kda:
        return None
    
    total_kills = sum(e['kills'] for e in entries_with_kda)
    total_deaths = sum(e['deaths'] for e in entries_with_kda)
    total_assists = sum(e['assists'] for e in entries_with_kda)
    games_count = len(entries_with_kda)
    
    avg_kills = total_kills / games_count
    avg_deaths = total_deaths / games_count
    avg_assists = total_assists / games_count
    avg_kda = (avg_kills + avg_assists) / max(avg_deaths, 0.1)
    
    # Meilleurs et pires performances
    best_kda = max((e['kills'] + e['assists']) / max(e['deaths'], 1) for e in entries_with_kda)
    worst_kda = min((e['kills'] + e['assists']) / max(e['deaths'], 1) for e in entries_with_kda)
    
    # Pentakills et multikills (supposons que 15+ kills = performance exceptionnelle)
    exceptional_games = len([e for e in entries_with_kda if e['kills'] >= 15])
    
    return {
        'games_count': games_count,
        'avg_kills': avg_kills,
        'avg_deaths': avg_deaths,
        'avg_assists': avg_assists,
        'avg_kda': avg_kda,
        'total_kills': total_kills,
        'total_deaths': total_deaths,
        'total_assists': total_assists,
        'best_kda': best_kda,
        'worst_kda': worst_kda,
        'exceptional_games': exceptional_games
    }

def calculate_grade_stats(data):
    """Calcule les statistiques de grades"""
    entries_with_grade = [e for e in data if 'grade' in e and e['grade'] != 'N/A']
    if not entries_with_grade:
        return None
    
    # Distribution des grades
    grade_counts = {}
    for entry in entries_with_grade:
        grade = entry['grade']
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    
    # Convertir les grades en points pour calculer la moyenne
    grade_points = {
        'S+': 13, 'S': 12, 'S-': 11,
        'A+': 10, 'A': 9, 'A-': 8,
        'B+': 7, 'B': 6, 'B-': 5,
        'C+': 4, 'C': 3, 'C-': 2,
        'D+': 1, 'D': 0, 'D-': -1
    }
    
    total_points = sum(grade_points.get(e['grade'], 0) for e in entries_with_grade)
    avg_grade_points = total_points / len(entries_with_grade)
    
    # Reconvertir en grade moyen approximatif
    for grade, points in sorted(grade_points.items(), key=lambda x: x[1], reverse=True):
        if avg_grade_points >= points:
            avg_grade = grade
            break
    else:
        avg_grade = 'D-'
    
    return {
        'games_count': len(entries_with_grade),
        'grade_counts': grade_counts,
        'avg_grade': avg_grade,
        'avg_grade_points': avg_grade_points
    }

def show_stats(data):
    """Affiche des statistiques ultra sexy avec graphiques ASCII"""
    if not data:
        print("📊 Aucune statistique disponible")
        return
    
    print(f"\n{BOLD}╔══════════════════════════════════════════════════════════════╗")
    print(f"║                    📊 STATISTIQUES DÉTAILLÉES                ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{RESET}")
    
    # Calculs de base
    total_games = len(data)
    total_lp_gained = sum(entry.get('lp_change', 0) for entry in data)
    wins = len([e for e in data if e.get('lp_change', 0) > 0])
    losses = len([e for e in data if e.get('lp_change', 0) < 0])
    promotions = len([e for e in data if 'promote' in e])
    demotions = len([e for e in data if 'demote' in e])
    winrate = (wins / total_games * 100) if total_games > 0 else 0
    
    # LP par game
    avg_lp_per_game = total_lp_gained / total_games if total_games > 0 else 0
    avg_lp_win = sum(e.get('lp_change', 0) for e in data if e.get('lp_change', 0) > 0) / wins if wins > 0 else 0
    avg_lp_loss = sum(e.get('lp_change', 0) for e in data if e.get('lp_change', 0) < 0) / losses if losses > 0 else 0
    
    # Streaks
    streaks = calculate_streaks(data)
    
    print(f"\n{BOLD}🎮 STATISTIQUES GÉNÉRALES{RESET}")
    print("═" * 60)
    print(f"  Parties jouées    │ {BOLD}{total_games:>10}{RESET}")
    print(f"  Victoires         │ {BOLD}\033[92m{wins:>10}{RESET}")
    print(f"  Défaites          │ {BOLD}\033[91m{losses:>10}{RESET}")
    print(f"  LP total gagné    │ {format_lp_change(total_lp_gained):>18}")
    print(f"  LP moyen/game     │ {BOLD}{avg_lp_per_game:>+7.1f} LP{RESET}")
    print(f"  Promotions        │ {BOLD}\033[92m{promotions:>10}{RESET}")
    print(f"  Démotions         │ {BOLD}\033[91m{demotions:>10}{RESET}")
    
    print(f"\n{BOLD}📈 WINRATE{RESET}")
    print("═" * 60)
    print(f"  {draw_winrate_chart(winrate)}")
    print(f"  LP moyen (Win)    │ {BOLD}\033[92m{avg_lp_win:>+7.1f} LP{RESET}")
    print(f"  LP moyen (Loss)   │ {BOLD}\033[91m{avg_lp_loss:>+7.1f} LP{RESET}")
    
    print(f"\n{BOLD}🔥 STREAKS{RESET}")
    print("═" * 60)
    
    # Streak actuel
    if streaks["current"] > 0:
        if streaks["type"] == "win":
            current_display = f"\033[92m{streaks['current']} Victoires 🔥{RESET}"
        else:
            current_display = f"\033[91m{streaks['current']} Défaites 💀{RESET}"
    else:
        current_display = "Aucun"
    
    print(f"  Streak actuel     │ {current_display}")
    print(f"  Meilleur streak   │ {BOLD}\033[92m{streaks['best_win']} Victoires 🏆{RESET}")
    print(f"  Pire streak       │ {BOLD}\033[91m{streaks['worst_lose']} Défaites 😵{RESET}")
    
    # Graphique de tendance
    print(f"\n{BOLD}📊 TENDANCE LP{RESET}")
    print("═" * 60)
    trend_chart = draw_lp_trend(data)
    for line in trend_chart.split('\n'):
        if line.strip():
            print(f"  {line}")
    
    # Distribution des rangs
    print(f"\n{BOLD}🏅 DISTRIBUTION DES RANGS{RESET}")
    print("═" * 60)
    rank_dist = get_rank_distribution(data)
    for rank, count in rank_dist[:5]:  # Top 5 des rangs
        percentage = (count / total_games * 100)
        bar_length = int(percentage / 100 * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        colored_rank = colorize_rank(rank)
        print(f"  {colored_rank:<30} │ {bar} {percentage:>5.1f}% ({count} games)")
    
    print(f"\n{BOLD}🎯 PERFORMANCES RÉCENTES (10 dernières games){RESET}")
    print("═" * 60)
    recent = data[-10:] if len(data) >= 10 else data
    recent_wins = len([e for e in recent if e.get('lp_change', 0) > 0])
    recent_losses = len([e for e in recent if e.get('lp_change', 0) < 0])
    recent_winrate = (recent_wins / len(recent) * 100) if recent else 0
    recent_lp = sum(e.get('lp_change', 0) for e in recent)
    
    # Forme récente
    if recent_winrate >= 70:
        form = f"\033[92mEXCELLENTE 🔥{RESET}"
    elif recent_winrate >= 60:
        form = f"\033[93mBONNE ⚡{RESET}"
    elif recent_winrate >= 40:
        form = f"\033[96mMOYENNE ⚖️{RESET}"
    else:
        form = f"\033[91mMAUVAISE 💀{RESET}"
    
    print(f"  Winrate récent    │ {recent_winrate:>6.1f}% ({recent_wins}W/{recent_losses}L)")
    print(f"  LP récent         │ {format_lp_change(recent_lp):>18}")
    print(f"  Forme             │ {form}")
    
    # Statistiques KDA
    kda_stats = calculate_kda_stats(data)
    if kda_stats:
        print(f"\n{BOLD}⚔️  STATISTIQUES KDA{RESET}")
        print("═" * 60)
        print(f"  Games avec KDA    │ {BOLD}{kda_stats['games_count']:>10}{RESET}")
        print(f"  KDA moyen         │ {format_kda(int(kda_stats['avg_kills']), int(kda_stats['avg_deaths']), int(kda_stats['avg_assists']))}")
        print(f"  Ratio KDA         │ {BOLD}{kda_stats['avg_kda']:>7.2f}{RESET}")
        print(f"  Kills total       │ {BOLD}\033[91m{kda_stats['total_kills']:>10}{RESET}")
        print(f"  Deaths total      │ {BOLD}\033[90m{kda_stats['total_deaths']:>10}{RESET}")
        print(f"  Assists total     │ {BOLD}\033[96m{kda_stats['total_assists']:>10}{RESET}")
        print(f"  Meilleur KDA      │ {BOLD}\033[93m{kda_stats['best_kda']:>7.2f} 🔥{RESET}")
        print(f"  Pire KDA          │ {BOLD}\033[91m{kda_stats['worst_kda']:>7.2f} 💀{RESET}")
        
        if kda_stats['exceptional_games'] > 0:
            print(f"  Games exceptionnelles │ {BOLD}\033[93m{kda_stats['exceptional_games']} (15+ kills) ⭐{RESET}")
    
    # Statistiques de grades
    grade_stats = calculate_grade_stats(data)
    if grade_stats:
        print(f"\n{BOLD}🏆 STATISTIQUES GRADES{RESET}")
        print("═" * 60)
        print(f"  Games avec grade  │ {BOLD}{grade_stats['games_count']:>10}{RESET}")
        print(f"  Grade moyen       │ {colorize_grade(grade_stats['avg_grade'])}")
        
        # Distribution des grades
        print(f"\n{BOLD}📊 DISTRIBUTION DES GRADES{RESET}")
        print("═" * 60)
        
        # Trier les grades par ordre décroissant de qualité
        grade_order = ['S+', 'S', 'S-', 'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-']
        for grade in grade_order:
            if grade in grade_stats['grade_counts']:
                count = grade_stats['grade_counts'][grade]
                percentage = (count / grade_stats['games_count'] * 100)
                bar_length = int(percentage / 100 * 15)
                bar = "█" * bar_length + "░" * (15 - bar_length)
                colored_grade = colorize_grade(grade)
                print("  %-12s │ %s %5.1f%% (%2d)" % (colored_grade, bar, percentage, count))
    print("═" * 60)

def main():
    """Fonction principale ultra sexy"""
    print_banner()
    
    try:
        data = load_data()
        show_help()
        
        while True:
            try:
                cmd = input(f"\n{BOLD}🎮 Commande{RESET} >> ").strip().lower()
                
                if cmd == 'q':
                    if save_data(data):
                        print(f"{BOLD}👋 Merci d'avoir utilisé LoL Rank Tracker !{RESET}")
                    break
                    
                elif cmd == 'a':
                    data = add_entry(data)
                    
                elif cmd == 'p':
                    display_data(data)
                    
                elif cmd == 's':
                    show_stats(data)
                    
                elif cmd == 'h':
                    show_help()
                    
                elif cmd == '':
                    continue
                    
                else:
                    print(f"❓ Commande '{cmd}' inconnue. Tapez 'h' pour l'aide.")
                    
            except KeyboardInterrupt:
                print(f"\n\n{BOLD}💾 Sauvegarde avant fermeture...{RESET}")
                save_data(data)
                print(f"{BOLD}👋 Au revoir !{RESET}")
                break
                
    except Exception as e:
        print(f"💥 Erreur inattendue: {e}")
        print("📧 Veuillez signaler ce bug !")

if __name__ == "__main__":
    main()
