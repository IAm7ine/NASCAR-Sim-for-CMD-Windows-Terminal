import random
import time
import copy
import tkinter as tk
from tkinter import messagebox

# ==========================================
# 1. SETTINGS GUI
# ==========================================
def get_game_settings():
    root = tk.Tk()
    root.title("NASCAR Sim 2025 - Setup")
    root.geometry("400x300")
    root.configure(bg="#1e1e1e")
    
    tk.Label(root, text="SETTINGS", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#00ff00").pack(pady=15)
    
    sim_mode = tk.IntVar(value=3) 
    modes = [("Race-by-Race (Pause all)", 1), ("Playoff Mode (Skip to playoffs)", 2), ("Fast Sim (No pauses)", 3)]

    for text, val in modes:
        tk.Radiobutton(root, text=text, variable=sim_mode, value=val, font=("Arial", 11), bg="#1e1e1e", fg="white", selectcolor="#333333", activebackground="#1e1e1e", activeforeground="#00ff00").pack(anchor="w", padx=40, pady=5)

    def on_start():
        root.quit()
        root.destroy()

    tk.Button(root, text="START SEASON", command=on_start, font=("Arial", 12, "bold"), bg="#00ff00", fg="black", width=20).pack(pady=25)
    root.mainloop()
    return sim_mode.get()

# ==========================================
# 2. GLOBAL DATA
# ==========================================
team_performance = {
    "#5": 99, "#9": 99, "#24": 99, "#48": 91,   # Hendrick
    "#11": 98, "#20": 98, "#54": 91, "#19": 97, # JGR
    "#12": 97, "#22": 97, "#2": 90,             # Penske
    "#45": 97, "#23": 95, "#35": 86,            # 23XI
    "#1": 93, "#99": 92, "#88": 95,             # Trackhouse
    "#6": 95, "#17": 94, "#60": 90,             # RFK
    "#8": 89, "#3": 88,                         # RCR
    "#4": 86, "#34": 85, "#38": 85,             # Front Row
    "#43": 84, "#42": 84,                       # Legacy MC
    "#7": 82, "#77": 81, "#71": 81,             # Spire
    "#21": 80, "#47": 80, "#41": 82,            # Wood, Hyak, Haas
    "#16": 80, "#10": 79,                       # Kaulig
    "#51": 70,                                  # RWR
}

PROTECTED_NUMBERS = ["#3", "#21", "#43", "#24", "#48", "#5", "#9", "#11", "#20", "#2", "#12", "#22", "#6", "#17", "#23", "#45", "#1", "#34"]

pt_numbers = {"RCR": "#33", "RFK": "#06", "Trackhouse": "#91", "23XI": "#67", "Team AmeriVet": "#50", "Live Fast Motorsports": "#78", "Tricon Garage": "#55", "JR Motorsports": "#40", "NY Racing": "#44", "MBM Motorsports": "#66", "Rick Ware Racing": "#15", "Kaulig": "#13", "Legacy MC": "#84", "Front Row": "#36", "Team Penske": "#02"}

TRACK_POOL = [
    ("Rockingham", "ST", 3), ("Chicagoland", "SW", 2), ("Kentucky", "SW", 2),
    ("Road America", "RC", 3), ("Montreal", "RC", 3), ("Portland", "RC", 3),
    ("North Wilkesboro", "ST", 3), ("Laguna Seca", "RC", 3), ("Long Beach", "RC", 4),
    ("Eldora Dirt", "ST", 5), ("Mexico City", "RC", 3), ("Iowa", "ST", 2)
]

initial_schedule = [
    ("Daytona 500", "SS", 5), ("Atlanta", "SS", 4), ("COTA", "RC", 2), ("Phoenix", "ST", 1),
    ("Las Vegas", "SW", 1), ("Homestead", "SW", 1), ("Martinsville", "ST", 3), ("Darlington", "SW", 3),
    ("Bristol", "ST", 3), ("Talladega", "SS", 5), ("Texas", "SW", 2), ("Kansas", "SW", 1),
    ("Coca-Cola 600", "SW", 3), ("Nashville", "SW", 2), ("Michigan", "SW", 2), ("Mexico City", "RC", 3),
    ("Pocono", "SW", 2), ("Atlanta 2", "SS", 4), ("Chicago Street", "RC", 3), ("Sonoma", "RC", 2),
    ("Dover", "ST", 2), ("Indianapolis", "SW", 2), ("Iowa", "ST", 2), ("Watkins Glen", "RC", 2),
    ("Richmond", "ST", 1), ("Daytona 2", "SS", 5),
    ("Darlington 2", "SW", 3), ("Gateway", "ST", 2), ("Bristol 2", "ST", 3),
    ("New Hampshire", "ST", 1), ("Kansas 2", "SW", 1), ("Charlotte Roval", "RC", 3),
    ("Las Vegas 2", "SW", 1), ("Talladega 2", "SS", 5), ("Martinsville 2", "ST", 3),
    ("Phoenix Finale", "ST", 1)
]

initial_roster = [
    {"name": "Kyle Larson", "age": 32, "num": "#5", "team": "Hendrick", "contract": 3, "lifer": True, "legacy_points": 5, "ratings": {"SS": 88, "SW": 99, "RC": 95, "ST": 98}},
    {"name": "Christopher Bell", "age": 30, "num": "#20", "team": "JGR", "contract": 2, "lifer": False, "legacy_points": 1, "ratings": {"SS": 85, "SW": 98, "RC": 96, "ST": 97}},
    {"name": "William Byron", "age": 27, "num": "#24", "team": "Hendrick", "contract": 4, "lifer": True, "legacy_points": 4, "ratings": {"SS": 92, "SW": 97, "RC": 94, "ST": 93}},
    {"name": "Denny Hamlin", "age": 44, "num": "#11", "team": "JGR", "contract": 1, "lifer": True, "legacy_points": 10, "ratings": {"SS": 94, "SW": 96, "RC": 88, "ST": 98}},
    {"name": "Tyler Reddick", "age": 29, "num": "#45", "team": "23XI", "contract": 2, "lifer": False, "legacy_points": 1, "ratings": {"SS": 86, "SW": 98, "RC": 97, "ST": 90}},
    {"name": "Ryan Blaney", "age": 31, "num": "#12", "team": "Penske", "contract": 3, "lifer": True, "legacy_points": 3, "ratings": {"SS": 99, "SW": 94, "RC": 89, "ST": 93}},
    {"name": "Chase Elliott", "age": 29, "num": "#9", "team": "Hendrick", "contract": 3, "lifer": True, "legacy_points": 5, "ratings": {"SS": 93, "SW": 92, "RC": 96, "ST": 90}},
    {"name": "Joey Logano", "age": 35, "num": "#22", "team": "Penske", "contract": 2, "lifer": True, "legacy_points": 6, "ratings": {"SS": 97, "SW": 91, "RC": 88, "ST": 94}},
    {"name": "Brad Keselowski", "age": 41, "num": "#6", "team": "RFK", "contract": 2, "lifer": True, "legacy_points": 5, "ratings": {"SS": 96, "SW": 88, "RC": 80, "ST": 92}},
    {"name": "Chris Buescher", "age": 32, "num": "#17", "team": "RFK", "contract": 2, "lifer": False, "legacy_points": 0, "ratings": {"SS": 90, "SW": 89, "RC": 94, "ST": 91}},
    {"name": "Ty Gibbs", "age": 22, "num": "#54", "team": "JGR", "contract": 3, "lifer": True, "legacy_points": 0, "ratings": {"SS": 82, "SW": 90, "RC": 93, "ST": 88}},
    {"name": "Ross Chastain", "age": 32, "num": "#1", "team": "Trackhouse", "contract": 2, "lifer": False, "legacy_points": 0, "ratings": {"SS": 89, "SW": 91, "RC": 92, "ST": 85}},
    {"name": "Kyle Busch", "age": 40, "num": "#8", "team": "RCR", "contract": 2, "lifer": False, "legacy_points": 10, "ratings": {"SS": 88, "SW": 85, "RC": 82, "ST": 89}},
    {"name": "Bubba Wallace", "age": 31, "num": "#23", "team": "23XI", "contract": 2, "lifer": True, "legacy_points": 0, "ratings": {"SS": 95, "SW": 88, "RC": 80, "ST": 82}},
    {"name": "Alex Bowman", "age": 32, "num": "#48", "team": "Hendrick", "contract": 2, "lifer": False, "legacy_points": 0, "ratings": {"SS": 88, "SW": 87, "RC": 86, "ST": 84}},
    {"name": "Chase Briscoe", "age": 30, "num": "#19", "team": "JGR", "contract": 3, "lifer": False, "legacy_points": 0, "ratings": {"SS": 80, "SW": 84, "RC": 82, "ST": 88}},
    {"name": "Daniel Suarez", "age": 33, "num": "#99", "team": "Trackhouse", "contract": 1, "lifer": False, "legacy_points": 0, "ratings": {"SS": 85, "SW": 82, "RC": 89, "ST": 78}},
    {"name": "Austin Cindric", "age": 26, "num": "#2", "team": "Penske", "contract": 2, "lifer": False, "legacy_points": 0, "ratings": {"SS": 90, "SW": 79, "RC": 88, "ST": 77}},
    {"name": "Shane van Gisbergen (R)", "age": 36, "num": "#88", "team": "Trackhouse", "contract": 2, "lifer": False, "legacy_points": 0, "ratings": {"SS": 76, "SW": 74, "RC": 100, "ST": 75}}, 
    {"name": "Michael McDowell", "age": 40, "num": "#71", "team": "Spire", "contract": 1, "lifer": False, "legacy_points": 0, "ratings": {"SS": 92, "SW": 76, "RC": 91, "ST": 75}},
    {"name": "Noah Gragson", "age": 26, "num": "#4", "team": "Front Row", "contract": 2, "lifer": False, "legacy_points": 0, "ratings": {"SS": 84, "SW": 80, "RC": 72, "ST": 78}},
    {"name": "Josh Berry", "age": 34, "num": "#21", "team": "Wood Bros", "contract": 2, "lifer": False, "legacy_points": 0, "ratings": {"SS": 75, "SW": 76, "RC": 70, "ST": 88}},
    {"name": "Erik Jones", "age": 29, "num": "#43", "team": "LMC", "contract": 2, "lifer": False, "legacy_points": 0, "ratings": {"SS": 86, "SW": 80, "RC": 75, "ST": 78}},
    {"name": "Carson Hocevar", "age": 22, "num": "#77", "team": "Spire", "contract": 3, "lifer": False, "legacy_points": 0, "ratings": {"SS": 78, "SW": 79, "RC": 76, "ST": 82}},
    {"name": "Ricky Stenhouse Jr", "age": 37, "num": "#47", "team": "Hyak", "contract": 1, "lifer": False, "legacy_points": 0, "ratings": {"SS": 91, "SW": 75, "RC": 72, "ST": 76}},
    {"name": "Austin Dillon", "age": 35, "num": "#3", "team": "RCR", "contract": 2, "lifer": True, "legacy_points": 0, "ratings": {"SS": 88, "SW": 74, "RC": 70, "ST": 75}},
    {"name": "Todd Gilliland", "age": 25, "num": "#34", "team": "Front Row", "contract": 1, "lifer": False, "legacy_points": 0, "ratings": {"SS": 82, "SW": 78, "RC": 78, "ST": 75}},
    {"name": "Justin Haley", "age": 26, "num": "#7", "team": "Spire", "contract": 1, "lifer": False, "legacy_points": 0, "ratings": {"SS": 80, "SW": 76, "RC": 75, "ST": 74}},
    {"name": "John H. Nemechek", "age": 28, "num": "#42", "team": "LMC", "contract": 2, "lifer": False, "legacy_points": 0, "ratings": {"SS": 78, "SW": 77, "RC": 73, "ST": 74}},
    {"name": "Cole Custer", "age": 27, "num": "#41", "team": "Haas", "contract": 2, "lifer": False, "legacy_points": 0, "ratings": {"SS": 76, "SW": 78, "RC": 76, "ST": 77}},
    {"name": "Ryan Preece", "age": 34, "num": "#60", "team": "RFK", "contract": 1, "lifer": False, "legacy_points": 0, "ratings": {"SS": 75, "SW": 74, "RC": 70, "ST": 80}},
    {"name": "Zane Smith", "age": 26, "num": "#38", "team": "Front Row", "contract": 2, "lifer": False, "legacy_points": 0, "ratings": {"SS": 75, "SW": 74, "RC": 74, "ST": 73}},
    {"name": "AJ Allmendinger", "age": 43, "num": "#16", "team": "Kaulig", "contract": 1, "lifer": False, "legacy_points": 0, "ratings": {"SS": 80, "SW": 75, "RC": 93, "ST": 78}},
    {"name": "Ty Dillon", "age": 33, "num": "#10", "team": "Kaulig", "contract": 1, "lifer": False, "legacy_points": 0, "ratings": {"SS": 72, "SW": 68, "RC": 65, "ST": 68}},
    {"name": "Cody Ware", "age": 29, "num": "#51", "team": "RWR", "contract": 1, "lifer": False, "legacy_points": 0, "ratings": {"SS": 70, "SW": 66, "RC": 65, "ST": 66}},
    {"name": "Riley Herbst (R)", "age": 26, "num": "#35", "team": "23XI", "contract": 2, "lifer": False, "legacy_points": 0, "ratings": {"SS": 78, "SW": 75, "RC": 72, "ST": 70}},
]

part_timers = [
    {"name": "Corey LaJoie", "age": 33, "ratings": {"SS": 85, "SW": 70, "RC": 68, "ST": 72}},
    {"name": "JJ Yeley", "age": 48, "ratings": {"SS": 70, "SW": 65, "RC": 60, "ST": 65}},
    {"name": "Timmy Hill", "age": 32, "ratings": {"SS": 72, "SW": 64, "RC": 62, "ST": 66}},
    {"name": "Chad Finchum", "age": 30, "ratings": {"SS": 68, "SW": 60, "RC": 55, "ST": 62}},
    {"name": "BJ McLeod", "age": 41, "ratings": {"SS": 75, "SW": 62, "RC": 58, "ST": 63}},
    {"name": "Josh Bilicki", "age": 29, "ratings": {"SS": 65, "SW": 65, "RC": 75, "ST": 64}},
    {"name": "Brennan Poole", "age": 34, "ratings": {"SS": 69, "SW": 66, "RC": 64, "ST": 65}},
]

real_prospects = [
    {"name": "Connor Zilisch", "age_base": 19, "ratings": {"SS": 78, "SW": 82, "RC": 95, "ST": 85}},
    {"name": "Corey Heim", "age_base": 23, "ratings": {"SS": 82, "SW": 88, "RC": 80, "ST": 86}},
    {"name": "Jesse Love", "age_base": 20, "ratings": {"SS": 85, "SW": 80, "RC": 75, "ST": 78}},
    {"name": "Christian Eckes", "age_base": 24, "ratings": {"SS": 80, "SW": 85, "RC": 70, "ST": 84}},
    {"name": "Chandler Smith", "age_base": 23, "ratings": {"SS": 80, "SW": 86, "RC": 72, "ST": 85}},
    {"name": "Nick Sanchez", "age_base": 24, "ratings": {"SS": 84, "SW": 80, "RC": 70, "ST": 78}},
    {"name": "William Sawalich", "age_base": 18, "ratings": {"SS": 70, "SW": 75, "RC": 78, "ST": 88}},
    {"name": "Rajah Caruth", "age_base": 23, "ratings": {"SS": 78, "SW": 78, "RC": 70, "ST": 75}},
    {"name": "Sam Mayer", "age_base": 22, "ratings": {"SS": 80, "SW": 82, "RC": 85, "ST": 78}},
]

phrases = {
    "BigOne": ["MASSIVE CRASH!", "The Big One strikes!", "Huge pileup!", "Major incident!", "Red flag!"],
    "Spin": ["spun out.", "lost control.", "loops it!", "goes around!", "loses the rear end."],
    "Wall": ["slammed the wall.", "hit the SAFER barrier.", "brushes the fence.", "pounds the outside wall."],
    "Mech": ["engine failure.", "broken transmission.", "mechanical issue.", "terminal failure."],
    "Dumped": ["was turned by", "dumped by", "wrecked by", "sent spinning by"],
    "Flip": ["lands on his wheels after a violent tumble.", "is on his roof!", "has turned over!"],
    "Suspension": ["SUSPENDED for retaliation.", "SUSPENDED for conduct violation."]
}

pending_departures = []

# ==========================================
# 3. HELPERS
# ==========================================
def get_regular_points(pos):
    if pos == 0: return 40
    if pos == 1: return 35
    if pos == 2: return 34
    if pos == 3: return 33
    return max(1, 33 - (pos - 3))

def get_avg_rating(driver):
    r = driver['ratings']
    return (r['SS'] + r['SW'] + r['RC'] + r['ST']) / 4

def get_available_number(active_roster):
    used_numbers = [d['num'] for d in active_roster]
    for _ in range(100):
        pick = f"#{random.randint(0, 99)}"
        if pick not in used_numbers: return pick
    return f"#{random.randint(100, 199)}"

def get_new_rookie(current_year, permanent=True):
    if len(real_prospects) > 0:
        if permanent: p = real_prospects.pop(0)
        else: p = copy.deepcopy(random.choice(real_prospects))
        years_passed = current_year - 2025
        p['age'] = p['age_base'] + years_passed
        return {"name": f"{p['name']} (R)", "age": p['age'], "ratings": p['ratings'], "contract": random.randint(3, 5), "lifer": False, "legacy_points": 0}
    
    first = ["Jett", "Cannon", "Hunter", "Ryder", "Axel", "Bodie", "Cruz", "Dash", "Ace", "Blaze", "Keagan"]
    last = ["Speed", "Racer", "Thunder", "Driver", "Earnhardt", "Petty", "Gordon", "Johnson", "Smith", "Jones"]
    return {
        "name": f"{random.choice(first)} {random.choice(last)} (R)",
        "age": random.randint(18, 22),
        "contract": random.randint(3, 5),
        "lifer": False,
        "legacy_points": 0,
        "ratings": {"SS": random.randint(70, 90), "SW": random.randint(60, 85), "RC": random.randint(70, 95), "ST": random.randint(60, 80)}
    }

# SEASON AUDITION/SUB GENERATOR (New)
def get_audition_driver(current_year, permanent=False):
    # 50/50: Vet vs Rookie
    if not permanent and random.random() < 0.5:
        v = random.choice(part_timers)
        return {
            "name": v['name'], "age": v['age'], 
            "ratings": v['ratings'], "contract": 1, 
            "lifer": False, "legacy_points": 0
        }
    return get_new_rookie(current_year, permanent)
    
    # Use Rookie Pool (Standard Logic)
    if len(real_prospects) > 0:
        if permanent:
            p = real_prospects.pop(0)
        else:
            p = copy.deepcopy(random.choice(real_prospects))

    first = ["Jett", "Cannon", "Hunter", "Ryder", "Axel", "Bodie", "Cruz", "Dash", "Ace", "Blaze", "Keagan"]
    last = ["Speed", "Racer", "Thunder", "Driver", "Earnhardt", "Petty", "Gordon", "Johnson", "Smith", "Jones"]
    return {
        "name": f"{random.choice(first)} {random.choice(last)} (R)",
        "age": random.randint(18, 22),
        "contract": random.randint(3, 5),
        "lifer": False,
        "legacy_points": 0,
        "ratings": {"SS": random.randint(70, 90), "SW": random.randint(60, 85), "RC": random.randint(70, 95), "ST": random.randint(60, 80)}
    }

def mutate_schedule(current_schedule):
    new_schedule = copy.deepcopy(current_schedule)
    changes_made = False
    
    if random.random() < 0.7: 
        if random.random() < 0.5:
            idx1 = random.randint(1, 25)
            idx2 = random.randint(1, 25)
            if idx1 != 12 and idx2 != 12: 
                new_schedule[idx1], new_schedule[idx2] = new_schedule[idx2], new_schedule[idx1]
                if not changes_made: print("\n📅 NASCAR SCHEDULE ANNOUNCEMENT:")
                print(f"   - DATE SWAP: {new_schedule[idx1][0]} and {new_schedule[idx2][0]} trade dates.")
                changes_made = True
            
    if random.random() < 0.3:
        candidates = [i for i in range(1, 26) if i != 12]
        if candidates:
            drop_idx = random.choice(candidates)
            dropped_race = new_schedule[drop_idx]
            new_track = random.choice(TRACK_POOL)
            new_schedule[drop_idx] = new_track
            if not changes_made: print("\n📅 NASCAR SCHEDULE ANNOUNCEMENT:")
            print(f"   - NEW TRACK: {dropped_race[0]} removed. {new_track[0]} added to schedule!")
            changes_made = True
            
    return new_schedule

# ==========================================
# 4. SIMULATION ENGINE
# ==========================================

def generate_incident(active_drivers, track_type):
    if len(active_drivers) < 2: return [], None
    weights = {"Spin": 30, "Wall": 30, "Mech": 24, "Dumped": 5, "BigOne": 5, "Flip": 1}
    if track_type == "SS": weights.update({"BigOne": 40, "Flip": 15})
    incident = random.choices(list(weights.keys()), weights=list(weights.values()), k=1)[0]
    dnfs, narrative = [], ""

    if incident == "BigOne":
        count = random.randint(5, 12)
        involved = random.sample(active_drivers, min(count, len(active_drivers)))
        inv_nums = [d.get('num', '??') for d in involved]
        narrative = f"{random.choice(phrases['BigOne'])} ({', '.join(inv_nums)})"
        for car in involved:
            if random.random() < 0.5:
                if car in active_drivers:
                    active_drivers.remove(car)
                    dnfs.append({**car, "reason": "Accident", "status": "DNF"})
    elif incident == "Mech":
        victim = random.choice(active_drivers)
        active_drivers.remove(victim)
        narrative = f"{victim['name']} {victim['num']} {random.choice(phrases['Mech'])}"
        dnfs.append({**victim, "reason": "Mechanical", "status": "DNF"})
    elif incident == "Dumped":
        aggressor, victim = random.sample(active_drivers, 2)
        narrative = f"{victim['name']} {victim['num']} {random.choice(phrases['Dumped'])} {aggressor['name']}!"
        if random.random() < 0.6:
             active_drivers.remove(victim)
             dnfs.append({**victim, "reason": "Accident", "status": "DNF"})
    elif incident == "Flip":
        victim = random.choice(active_drivers)
        active_drivers.remove(victim)
        narrative = f"{victim['name']} {victim['num']} {random.choice(phrases['Flip'])}"
        dnfs.append({**victim, "reason": "Accident", "status": "DNF"})
    else: 
        victim = random.choice(active_drivers)
        narrative = f"{victim['name']} {victim['num']} {random.choice(phrases.get(incident, ['crash']))}"
        if random.random() < 0.25:
            active_drivers.remove(victim)
            dnfs.append({**victim, "reason": "Accident", "status": "DNF"})
    return dnfs, narrative

def simulate_stage(active_drivers, stage_num, chaos_level, track_type):
    stage_dnfs, stage_logs = [], []
    potential_cautions = random.randint(0, chaos_level)
    for _ in range(potential_cautions):
        if random.random() < 0.4: 
             new_dnfs, story = generate_incident(active_drivers, track_type)
             if story:
                for d in new_dnfs: d['stage'] = stage_num
                stage_dnfs.extend(new_dnfs)
                stage_logs.append(f"Stage {stage_num}: {story}")

    scored = []
    for d in active_drivers:
        driver_skill = d['ratings'][track_type]
        car_speed = team_performance.get(d['num'], 75)
        base_performance = (driver_skill * 0.5) + (car_speed * 0.5)
        var = random.uniform(0, 35)
        scored.append((d, base_performance + var))
        
    scored.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in scored], stage_dnfs, stage_logs

def run_qualifying(active_roster, track_type):
    qual_scores = []
    for d in active_roster:
        driver_skill = d['ratings'][track_type]
        car_speed = team_performance.get(d['num'], 75)
        score = (driver_skill * 0.4) + (car_speed * 0.6) + random.uniform(0, 10)
        qual_scores.append((d, score))
    qual_scores.sort(key=lambda x: x[1], reverse=True)
    return qual_scores[0][0]

def process_pre_race_events(race_idx, track, current_year, active_roster, roster, suspended_driver):
    """Handles all the drama before the engines start."""
    global pending_departures
    
    # 1. SILLY SEASON (Contracts & Rumors)
    if race_idx >= 15: 
        expiring_drivers = [d for d in active_roster if d.get('contract', 0) <= 1 and d not in pending_departures]
        expiring_drivers = [d for d in expiring_drivers if not d.get('lifer', False)]
        if expiring_drivers and random.random() < 0.7: 
            news_maker = random.choice(expiring_drivers)
            roll = random.random()
            if roll < 0.4: 
                years = random.randint(2, 4)
                orig = next((d for d in roster if d['name'] == news_maker['name']), None)
                if orig: orig['contract'] = years
                news_maker['contract'] = years 
                print(f"\n📝 BREAKING: {news_maker['name']} signs {years}-year extension with {news_maker['team']}!")
            elif roll < 0.7: 
                pending_departures.append(news_maker)
                print(f"\n📣 OFFICIAL: {news_maker['name']} announces departure from {news_maker['team']} at end of {current_year}.")
            else: 
                rumor_team = random.choice(["23XI", "Trackhouse", "RCR", "Haas", "Spire"])
                print(f"\n👀 RUMOR: Sources link {news_maker['name']} to a potential seat at {rumor_team}.")

    # 2. MID-SEASON FIRING
    # (Only happens in Regular Season usually, but we check specific race index)
    # You can remove the 'race_idx == 18' check if you want firings in playoffs
    
    # 3. FIELD EXPANSION (Open Cars)
    is_crown_jewel = track in ["Daytona 500", "Coca-Cola 600", "Daytona 2", "Talladega", "Talladega 2"]
    num_open_entries = 0
    if is_crown_jewel:
        if random.random() < 0.9: num_open_entries = random.randint(1, 4)
    elif race_idx % 6 == 0 and random.random() < 0.6:
        num_open_entries = 1

    if num_open_entries > 0:
        available_pt_teams = list(pt_numbers.keys())
        random.shuffle(available_pt_teams)
        
        # Build Safe Pool (Vets + Prospects)
        active_names = [d['name'] for d in active_roster]
        safe_pool = []
        for v in part_timers:
            if v['name'] not in active_names: safe_pool.append(v)
        for p in real_prospects:
            r_name = f"{p['name']} (R)"
            if r_name not in active_names:
                safe_pool.append({"name": r_name, "ratings": p['ratings'], "age": p['age_base'] + (current_year - 2025)})
        random.shuffle(safe_pool)
        
        print(f"\n🆕 FIELD EXPANSION ({track}):")
        for _ in range(num_open_entries):
            if not available_pt_teams or not safe_pool: break 
            host_team = available_pt_teams.pop()
            p_num = pt_numbers[host_team]
            d_data = safe_pool.pop()
            
            spd = random.randint(85, 95) if ("Daytona" in track or "Talladega" in track) else random.randint(75, 90)
            team_performance[p_num] = spd
            active_roster.append({"name": d_data['name'], "num": p_num, "team": host_team, "ratings": d_data['ratings'], "is_part_time": True})
            print(f"   + ENTRY: {host_team} fields the {p_num} for {d_data['name']} (Rating: {spd})")

    # 4. DNQ LOGIC
    if len(active_roster) > 40:
        event_name = "THE DUELS" if track == "Daytona 500" else "QUALIFYING"
        print(f"\n⚔️  {event_name} CUT LINE ({len(active_roster)} entries for 40 spots)")
        charters = [d for d in active_roster if not d.get('is_part_time')]
        opens = [d for d in active_roster if d.get('is_part_time')]
        spots = 40 - len(charters)
        if spots < 0: spots = 0
        
        if len(opens) > spots:
            for d in opens: 
                # Determine qualifying speed
                d['qual_speed'] = team_performance.get(d['num'], 75) + (d['ratings']['SS'] * 0.2 if "Daytona" in track or "Talladega" in track else get_avg_rating(d) * 0.4) + random.uniform(0, 5)
            
            opens.sort(key=lambda x: x['qual_speed'], reverse=True)
            qualifiers = opens[:spots]
            go_homers = opens[spots:]
            
            method = "races" if track == "Daytona 500" else "times"
            for q in qualifiers: print(f"   ✅ QUALIFIED: {q['name']} ({q['num']}) {method} their way in!")
            for loser in go_homers:
                print(f"   ❌ DNQ: {loser['name']} ({loser['num']} {loser['team']}) is sent home.")
                if loser in active_roster: active_roster.remove(loser)
        time.sleep(1)

    # 5. SUSPENSIONS
    if suspended_driver is None and random.random() < 0.03:
        target = random.choice(active_roster)
        active_names = [d['name'] for d in active_roster]
        subs = [x for x in part_timers + real_prospects if (x['name'] not in active_names and f"{x['name']} (R)" not in active_names)]
        
        if subs:
            s = random.choice(subs)
            s_name = f"{s['name']} (R) (Sub)" if 'age_base' in s else f"{s['name']} (Sub)"
            rep = {**target, "name": s_name, "ratings": s['ratings'], "car_perf": target.get('car_perf', 80)}
            active_roster.remove(target)
            active_roster.append(rep)
            suspended_driver = {"orig": target, "sub": rep, "return": race_idx + 1}
            print(f"\n🚨 NEWS: {target['name']} SUSPENDED. {s_name} fills in.")
            
    elif suspended_driver and race_idx > suspended_driver["return"]:
        print(f"\n✅ RETURN: {suspended_driver['orig']['name']} reinstated.")
        if suspended_driver['sub'] in active_roster: active_roster.remove(suspended_driver['sub'])
        active_roster.append(suspended_driver['orig'])
        suspended_driver = None

    return suspended_driver

def run_season(current_year, roster, schedule, sim_mode):
    stats = {d["name"]: {"pts": 0, "wins": 0, "s_wins": 0, "dnfs": 0, "playoff_pts": 0, "top5": 0, "top10": 0, "poles": 0} for d in roster}
    active_roster = copy.deepcopy(roster)
    suspended_driver = None
    champion_name = ""
    global pending_departures
    pending_departures = [] 
    
    print(f"\n\n🏁 STARTING THE {current_year} NASCAR CUP SERIES SEASON 🏁")
    time.sleep(1)

    # === REGULAR SEASON ===
    for race_idx, (track, track_type, chaos) in enumerate(schedule[:26], 1):
        
        # CALL THE CHAOS MANAGER
        suspended_driver = process_pre_race_events(race_idx, track, current_year, active_roster, roster, suspended_driver)

        # Race Execution
        print(f"\n🏁 RACE {race_idx}/36: {track.upper()}")
        pole_winner = run_qualifying(active_roster, track_type)
        if pole_winner['name'] in stats: stats[pole_winner['name']]['poles'] += 1
        print(f"   ⏱️ Pole Position: {pole_winner['name']} {pole_winner['num']}")
        
        field = active_roster[:]
        race_dnfs, logs = [], []
        num_stages = 4 if track == "Coca-Cola 600" else 3
        
        for stage in range(1, num_stages + 1):
            res, s_dnfs, s_logs = simulate_stage(field, stage, chaos, track_type)
            race_dnfs.extend(s_dnfs)
            logs.extend(s_logs)
            winner = res[0]
            if stage < num_stages:
                print(f"   🚩 Stage {stage} Winner: {winner['name']} {winner['num']}")
                if winner['name'] in stats: 
                    stats[winner['name']]['s_wins'] += 1
                    stats[winner['name']]['playoff_pts'] += 1
            else:
                if random.random() < 0.01:
                    print(f"   ❌ DISQUALIFIED: {winner['name']} {winner['num']}")
                    race_dnfs.append({**winner, "reason": "DQ", "status": "DQ"})
                    res.remove(winner)
                    winner = res[0]
                    print(f"   🥇 OFFICIAL WINNER: {winner['name']} {winner['num']} (Inherited)")
                else:
                    print(f"   🥇 OFFICIAL WINNER: {winner['name']} {winner['num']}")
                if winner['name'] not in stats: # Add open driver if winning
                     stats[winner['name']] = {"pts": 0, "wins": 0, "s_wins": 0, "dnfs": 0, "playoff_pts": 0, "top5": 0, "top10": 0, "poles": 0}
                stats[winner['name']]['wins'] += 1
                stats[winner['name']]['playoff_pts'] += 5
                
                full_res = res + race_dnfs[::-1]
                for pos, d in enumerate(full_res):
                    if d['name'] in stats:
                        stats[d['name']]['pts'] += get_regular_points(pos)
                        if "status" in d: stats[d['name']]['dnfs'] += 1
                        if pos < 5: stats[d['name']]['top5'] += 1
                        if pos < 10: stats[d['name']]['top10'] += 1
        
        if logs: 
            print("   ⚠️  Caution Log:")
            for l in logs: print(f"      - {l}")
        
        if sim_mode == 1:
            input(f"\n[Press Enter to proceed to Race {race_idx + 1}...] ")
        
        active_roster = [d for d in active_roster if not d.get('is_part_time')]
        time.sleep(0.05)

    # === PLAYOFFS ===
    print(f"\n⚔️  {current_year} PLAYOFFS BEGIN ⚔️")
    valid_names = [n for n in stats if "Sub" not in n]
    sorted_stats = sorted([(n, stats[n]) for n in valid_names], key=lambda x: (x[1]['wins'], x[1]['pts']), reverse=True)
    playoff_drivers = [x[0] for x in sorted_stats[:16]]
    
    print("PLAYOFF GRID: " + ", ".join(playoff_drivers))
    for p in playoff_drivers: stats[p]['pts'] = 2000 + stats[p]['playoff_pts']
    
    rounds = [("Round of 16", 3, 12, 3000), ("Round of 12", 3, 8, 4000), ("Round of 8", 3, 4, 5000)]
    race_counter = 27
    
    for r_name, length, survivors, reset_base in rounds:
        print(f"\n🔥 {r_name.upper()} 🔥")
        print(f"📊 LIVE CUT LINE ({r_name})")
        grid_sorted = sorted(playoff_drivers, key=lambda x: stats[x]['pts'], reverse=True)
        for i, d in enumerate(grid_sorted):
            status = " "
            if i == survivors - 1: status = "--- CUT LINE ---"
            print(f"   {i+1}. {d:<20} {stats[d]['pts']} pts  {status}")
        print("-" * 40)
        time.sleep(2)

        round_winners = []
        for _ in range(length):
            track, t_type, chaos = schedule[race_counter-1]
            
            # CALL THE CHAOS MANAGER (Now in Playoffs too!)
            suspended_driver = process_pre_race_events(race_counter, track, current_year, active_roster, roster, suspended_driver)

            print(f"\n🏁 RACE {race_counter}: {track.upper()}")
            pole_winner = run_qualifying(active_roster, track_type)
            if pole_winner['name'] in stats: stats[pole_winner['name']]['poles'] += 1
            print(f"   ⏱️ Pole Position: {pole_winner['name']} {pole_winner['num']}")

            field = active_roster[:]
            race_dnfs, logs = [], []
            for stage in [1, 2, 3]:
                res, s_dnfs, s_logs = simulate_stage(field, stage, chaos, t_type)
                race_dnfs.extend(s_dnfs)
                logs.extend(s_logs)
                winner = res[0]
                if stage < 3:
                    print(f"   🚩 Stage {stage} Winner: {winner['name']} {winner['num']}")
                else:
                    print(f"   🏁 WINNER: {winner['name']} {winner['num']}")
                    if winner['name'] not in stats:
                         stats[winner['name']] = {"pts": 0, "wins": 0, "s_wins": 0, "dnfs": 0, "playoff_pts": 0, "top5": 0, "top10": 0, "poles": 0}
                    stats[winner['name']]['wins'] += 1
                    if winner['name'] in playoff_drivers:
                        round_winners.append(winner['name'])
                        stats[winner['name']]['playoff_pts'] += 5
                    full_res = res + race_dnfs[::-1]
                    for pos, d in enumerate(full_res):
                        if d['name'] in stats: 
                            stats[d['name']]['pts'] += get_regular_points(pos)
                            if pos < 5: stats[d['name']]['top5'] += 1
                            if pos < 10: stats[d['name']]['top10'] += 1
            
            # ADDED: Caution Logs for Playoffs
            if logs: 
                print("   ⚠️  Caution Log:")
                for l in logs: print(f"      - {l}")

            if sim_mode in [1, 2]:
                input(f"\n[Press Enter to proceed to Race {race_counter}...] ")
            
            # Reset active roster (remove auditions)
            active_roster = [d for d in active_roster if not d.get('is_part_time')]
            race_counter += 1
            time.sleep(0.2)
        
        print(f"\n🔪 {r_name} ELIMINATIONS")
        ranked = sorted(playoff_drivers, key=lambda x: (x in round_winners, stats[x]['pts']), reverse=True)
        advancing = ranked[:survivors]
        eliminated_drivers = ranked[survivors:]
        for e in eliminated_drivers:
            print(f"   ❌ ELIMINATED: {e} ({stats[e]['pts']} pts)")
            
        playoff_drivers = advancing
        if survivors > 4:
            for p in playoff_drivers: stats[p]['pts'] = reset_base + stats[p]['playoff_pts']
        else:
            for p in playoff_drivers: stats[p]['pts'] = 5000

    print(f"\n🏆 CHAMPIONSHIP 4: {', '.join(playoff_drivers)}")
    track, t_type, chaos = schedule[35]
    print(f"🏁 RACE 36: {track.upper()}")
    
    field = active_roster[:]
    race_dnfs = []
    for stage in [1, 2, 3]:
        res, s_dnfs, _ = simulate_stage(field, stage, chaos, t_type)
        race_dnfs.extend(s_dnfs)
        if stage < 3: print(f"   🚩 Stage {stage} Winner: {res[0]['name']} {res[0]['num']}")
    
    final_order = res + race_dnfs[::-1]
    print(f"   🏁 RACE WINNER: {final_order[0]['name']}")
    
    # final 4 standings fix
    c4_finishers = []
    
    for pos, d in enumerate(final_order):
        # Update Stats for final race
        if d['name'] in stats:
            if pos < 5: stats[d['name']]['top5'] += 1
            if pos < 10: stats[d['name']]['top10'] += 1
        
        if d['name'] in playoff_drivers:
            c4_finishers.append(d['name']) # Appends in order of finish (1st to last)

    # this assigns proper points
    # The first driver in c4_finishers is the champion
    if len(c4_finishers) > 0: 
        champion_name = c4_finishers[0]
        stats[champion_name]['pts'] = 5040 # Max points for Champ
        
    if len(c4_finishers) > 1: stats[c4_finishers[1]]['pts'] = 5035 # 2nd in standings
    if len(c4_finishers) > 2: stats[c4_finishers[2]]['pts'] = 5034 # 3rd in standings
    if len(c4_finishers) > 3: stats[c4_finishers[3]]['pts'] = 5033 # 4th in standings

    print(f"\n👑👑👑 {current_year} CHAMPION: {champion_name} 👑👑👑")

    # Final Standings (finally works yippie)
    print(f"\n📊 {current_year} FINAL STANDINGS (Sorted by Points)")
    print(f"{'POS':<4} {'DRIVER':<20} {'TEAM':<5} {'PTS':<5} {'WINS':<4} {'T5':<4} {'T10':<4} {'POLES':<5}")
    print("-" * 70)
    
    final_standings = sorted(stats.items(), key=lambda x: x[1]['pts'], reverse=True)
    
    for i, (name, data) in enumerate(final_standings[:25]):
        # Find number for the table
        driver_obj = next((d for d in roster if d['name'] == name), None)
        num = driver_obj['num'] if driver_obj else "??"
        print(f"{i+1:<4} {name:<20} {num:<5} {data['pts']:<5} {data['wins']:<4} {data['top5']:<4} {data['top10']:<4} {data['poles']:<5}")

    # 4. Legacy Updates
    print("\n🏢 FRONT OFFICE & LEGACY UPDATE:")
    for name, data in stats.items():
        driver_obj = next((d for d in roster if d['name'] == name), None)
        if driver_obj and not driver_obj.get('lifer', False):
            earned_points = 0
            if data['wins'] >= 3: earned_points += 1
            if name in playoff_drivers: earned_points += 1 
            if name == champion_name: earned_points += 2
            
            if earned_points > 0:
                driver_obj['legacy_points'] = driver_obj.get('legacy_points', 0) + earned_points
                print(f"   🌟 {name} earns +{earned_points} Legacy Points (Total: {driver_obj['legacy_points']})")
                if driver_obj['legacy_points'] >= 3:
                    driver_obj['lifer'] = True
                    driver_obj['contract'] = 5 
                    print(f"   🔒 FRANCHISE TAG: {driver_obj['team']} locks down {name} as a Franchise Lifer!")

    return champion_name

def run_offseason(current_year, roster):
    print(f"\n❄️  {current_year} OFFSEASON ❄️")
    time.sleep(1)
    
    global schedule
    schedule = mutate_schedule(schedule)

    for d in roster:
        if "(R)" in d['name']: d['name'] = d['name'].replace(" (R)", "")
        d['contract'] = d.get('contract', 1) - 1
        
    open_seats, free_agents = [], []
    
    print("\n✍️ DRIVER MARKET & CONTRACT NEWS:")
    global pending_departures
    for d in pending_departures:
        actual_driver = next((x for x in roster if x['name'] == d['name']), None)
        if actual_driver:
            print(f"   👋 CONFIRMED DEPARTURE: {actual_driver['name']} leaves {actual_driver['team']}.")
            open_seats.append({"num": actual_driver['num'], "team": actual_driver['team'], "car_perf": team_performance.get(actual_driver['num'], 80)})
            actual_driver['prev_team'] = actual_driver['team']
            roster.remove(actual_driver)
            free_agents.append(actual_driver)
            
    for d in list(roster):
        d['age'] += 1
        if d['contract'] <= 0:
            if d['age'] >= 38 and random.random() < 0.4:
                print(f"   👋 RETIREMENT: {d['name']} ({d['age']}) hangs it up.")
                open_seats.append({"num": d['num'], "team": d['team'], "car_perf": team_performance.get(d['num'], 80)})
                roster.remove(d)
            elif not d.get('lifer', False):
                print(f"   🔄 CONTRACT EXPIRED: {d['name']} is a Free Agent.")
                open_seats.append({"num": d['num'], "team": d['team'], "car_perf": team_performance.get(d['num'], 80)})
                d['prev_team'] = d['team']
                roster.remove(d)
                free_agents.append(d)
            else:
                d['contract'] = 3
                print(f"   ⚓ LIFER EXTENSION: {d['name']} stays at {d['team']}.")

    if random.random() < 0.1 and open_seats:
        dead_team = open_seats.pop(0)
        if dead_team['num'] in team_performance: del team_performance[dead_team['num']]
        print(f"   💀 SHUTDOWN: The {dead_team['team']} {dead_team['num']} team has ceased operations.")
        
    if random.random() < 0.1:
        new_num = get_available_number(roster)
        new_team = random.choice(["Andretti", "Jr Motorsports", "Project91", "Red Bull"])
        team_performance[new_num] = 80
        print(f"   ✨ EXPANSION: {new_team} announces a new entry: {new_num}!")
        open_seats.append({"num": new_num, "team": new_team, "car_perf": 80})
        
    for seat in open_seats:
        if random.random() < 0.05 and seat['num'] not in PROTECTED_NUMBERS:
            old_num = seat['num']
            new_num = get_available_number(roster)
            if old_num in team_performance:
                perf = team_performance[old_num]
                del team_performance[old_num]
                team_performance[new_num] = perf
            else:
                team_performance[new_num] = 75
            print(f"   🎨 REBRAND: {seat['team']} renumbers the {old_num} to the {new_num}!")
            seat['num'] = new_num

    open_seats.sort(key=lambda x: x.get('car_perf', 70), reverse=True) 
    random.shuffle(free_agents)
    
    for seat in open_seats:
        signed_driver = None
        min_rating = 0
        if seat.get('car_perf', 0) >= 90: min_rating = 80
        elif seat.get('car_perf', 0) >= 80: min_rating = 72
        
        candidates = [dr for dr in free_agents if get_avg_rating(dr) >= min_rating and dr.get('prev_team') != seat['team']]
        if candidates:
            signed_driver = random.choice(candidates)
            free_agents.remove(signed_driver)
            signed_driver['num'] = seat['num']
            signed_driver['team'] = seat['team']
            signed_driver['contract'] = random.randint(2, 4)
            if 'prev_team' in signed_driver: del signed_driver['prev_team']
            roster.append(signed_driver)
            print(f"   ✍️ SIGNING: {signed_driver['name']} signs {signed_driver['contract']}yr deal with {signed_driver['num']} {signed_driver['team']}!")
        else:
            new_kid = get_new_rookie(current_year, permanent=True)
            new_entry = {
                "name": new_kid['name'], "age": new_kid['age'], "num": seat['num'], "team": seat['team'],
                "ratings": new_kid['ratings'], "contract": new_kid['contract'], "lifer": False, "legacy_points": 0
            }
            roster.append(new_entry)
            print(f"   🎓 ROOKIE: {new_entry['name']} to drive the {new_entry['num']}!")

    print("\n   📈 DEVELOPMENT:")
    for d in roster:
        if d['age'] <= 24:
            gain = random.randint(1, 3)
            for k in d['ratings']: d['ratings'][k] = min(99, d['ratings'][k] + gain)
            if random.random() < 0.3: print(f"      - {d['name']} improves (+{gain} Skill)")
        elif d['age'] >= 37:
            loss = random.randint(1, 3)
            for k in d['ratings']: d['ratings'][k] = max(50, d['ratings'][k] - loss)
            if random.random() < 0.3: print(f"      - {d['name']} declines (-{loss} Skill)")
            
    for num in team_performance:
        if random.random() < 0.2:
            change = random.choice([-2, -1, 1, 1, 2])
            team_performance[num] = max(60, min(99, team_performance[num] + change))
            
    return roster

def main():
    print("Launching Setup Menu...")
    selected_mode = get_game_settings()
    print(f"✅ Simulation Mode Loaded: {selected_mode}")
    time.sleep(1)

    roster = copy.deepcopy(initial_roster)
    year = 2025
    history = []
    global schedule
    schedule = initial_schedule

    while True:
        champ = run_season(year, roster, schedule, selected_mode)
        history.append(f"{year}: {champ}")
        print("\n📜 DYNASTY HISTORY:")
        for h in history: print(f"   {h}")
        input(f"\n[Press Enter for Offseason...]")
        roster = run_offseason(year, roster)
        input(f"\n[Press Enter for {year+1} Season...]")
        year += 1

if __name__ == "__main__":
    main()