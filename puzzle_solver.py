import math
import sys
from itertools import combinations

# ============================================================
# GREAT CIRCLE PUZZLE SOLVER
# ============================================================
# HOW TO USE:
# 1. Run as-is to see all possible solutions for unconstrained rows
# 2. Edit CONFIRMED dict below to lock in answers you know
# 3. Edit group dicts if you discover new city group assignments
# 4. Adjust BOAT_CONSTRAINTS if you get more boat color screenshots
# ============================================================


def haversine(lat1, lon1, lat2, lon2):
    r = 6371
    a = (
        math.sin(math.radians(lat2 - lat1) / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    )
    return 2 * r * math.asin(math.sqrt(a))


def cross_track(plat, plon, alat, alon, blat, blon):
    """Cross-track distance in km from point P to great circle A->B."""
    r = 6371

    def bearing(la1, lo1, la2, lo2):
        la1, lo1, la2, lo2 = map(math.radians, [la1, lo1, la2, lo2])
        x = math.sin(lo2 - lo1) * math.cos(la2)
        y = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(
            lo2 - lo1
        )
        return (math.degrees(math.atan2(x, y)) + 360) % 360

    d13 = haversine(alat, alon, plat, plon) / r
    t13 = math.radians(bearing(alat, alon, plat, plon))
    t12 = math.radians(bearing(alat, alon, blat, blon))
    return abs(math.asin(math.sin(d13) * math.sin(t13 - t12))) * r


# ============================================================
# STAGE 1 CITIES BY GROUP (boat color)
# Brown = A, Yellow = E, Silver = R, Green = S, Purple = T
# ============================================================
GROUPS = {
    "A": {
        "Accra": (5.5461, -0.2067),
        "Ankara": (39.9358, 32.8387),
        "Buffalo": (42.8864, -78.8781),
        "DeKalb": (41.9314, -88.7503),
        "Eyjafjallajokull": (63.6314, -19.6083),
        "Kabul": (34.5553, 69.2075),
        "Kupang": (-10.1633, 123.5778),
        "Queensland": (-22.5752, 144.0848),
        "Thane": (19.2183, 72.9781),
        "Tijuana": (32.5364, -117.0372),
    },
    "E": {
        "Ascension Island": (-7.9467, -14.3559),
        "Copenhagen": (55.6761, 12.5689),
        "Ile de la Possession": (-46.4269, 51.7378),
        "Kandi": (6.3176, 5.6145),
        "Male": (4.1753, 73.5091),
        "New Orleans": (29.9761, -90.0783),
        "South Pole": (-90.0, 0.0),
        "Yellowknife": (62.4422, -114.3975),
        "Yellowstone": (44.5979, -110.5612),
    },
    "R": {
        "Armavir": (44.9833, 41.1167),
        "Comuna Horia": (46.9063, 26.9201),
        "Heard Island": (-53.0818, 73.5042),
        "Lima": (-12.06, -77.0375),
        "Montreal": (45.5089, -73.5617),
        "North York": (43.7615, -79.4111),
        "Tampa Bay": (27.7625, -82.5458),
        "Windsor": (42.3173, -83.0353),
    },
    "S": {
        "Algiers": (36.7764, 3.0586),
        "Arles": (43.6769, 4.6286),
        "Casablanca": (33.5992, -7.62),
        "Gaborone": (-24.658, 25.9077),
        "Lahore": (31.5497, 74.3436),
        "Moscow": (55.751244, 37.6184),
        "Nome": (64.5, -165.4),
        "Seoul": (37.5326, 127.024612),
        "Sucre": (-19.0475, -65.26),
        "Tashkent": (41.311081, 69.240562),
        "Tbilisi": (41.6938, 44.8015),
        "Tierra del Fuego": (-54.0, -70.0),
        "Toad Suck": (35.0756, -92.56),
    },
    "T": {
        "Antananarivo": (-18.9386, 47.5214),
        "Cairo": (30.0444, 31.2358),
        "Dimtu": (2.88, 41.05),
        "Divo": (5.8372, -5.3572),
        "Doha": (25.2854, 51.531),
        "Iturup": (45.0649, 147.8403),
        "Lower Hutt": (-41.2167, 174.9167),
        "Maputo": (-25.9692, 32.5732),
        "Nazare": (39.6016, -9.071),
        "Quito": (-0.22, -78.5125),
        "Silver Coast": (39.6016, -9.0678),
        "Tallinn": (59.4372, 24.745),
        "Wichita": (37.6889, -97.3361),
    },
}

ALL_S1 = {}
CITY_GROUP = {}
for group, cities in GROUPS.items():
    for city, coords in cities.items():
        ALL_S1[city] = coords
        CITY_GROUP[city] = group

# ============================================================
# STAGE 2 CITIES
# ============================================================
STAGE2 = {
    "Casper": (42.8347, -106.325),
    "Arzamas": (55.3833, 43.8),
    "Mubi": (10.2692, 13.2531),
    "Baku": (40.4093, 49.8671),
    "Moora": (-30.6413, 116.0081),
    "Surat": (21.205, 72.84),
    "Marquette": (46.5436, -87.3956),
    "Beatty": (36.9094, -116.7544),
    "Mosul": (36.3667, 43.1167),
    "Visby": (57.629, 18.3071),
    "Istanbul": (41.01, 28.9603),
    "Genoa": (44.4072, 8.934),
    "Mayotte": (-12.8275, 45.1662),
    "Giresun": (40.9, 38.4167),
    "L'Ascension": (46.55, -74.8333),
    "Okato": (-39.191, 173.88),
    "Nova Russas": (-4.7, -40.5667),
    "Ceske Budejovice": (48.9747, 14.4747),
    "Christchurch": (-43.5309, 172.6365),
    "Castelo Branco": (39.8228, -7.4931),
    "Sokode": (8.9833, 1.1333),
    "Curico": (-34.9854, -71.2394),
    "Monkey Bay": (-14.0667, 34.9167),
    "Antalya": (36.9081, 30.6956),
    "Ambanja": (-13.6786, 48.4522),
    "Saint-Pierre": (46.7839, -56.1764),
    "Krasnodar": (45.0333, 38.9833),
    "San Miguel de Tucuman": (-26.8167, -65.2167),
    "Derby Wharf": (-17.3111, 123.6349),
    "Manaus": (-3.1189, -60.0217),
    "Pune": (18.5196, 73.8553),
    "Natif waterfalls": (17.0322, 54.1425),
    "Velingrad": (42.0276, 23.9913),
    "Marrakesh": (31.6295, -7.9811),
    "Orlando": (28.5336, -81.3867),
    "Charlotte": (35.2269, -80.8433),
    "Edmonton": (53.5333, -113.5),
    "Vladivostok": (43.115, 131.8853),
    "Cochabamba": (-17.3935, -66.157),
    "Tacurong": (6.6833, 124.6667),
}

CONFIRMED = {
    "L'Ascension": ("South Pole", "Montreal"),
    "Nova Russas": ("Accra", "Lima"),
    "Sokode": ("Doha", "Divo"),
    "Ambanja": ("Wichita", "North York"),
    "Charlotte": ("Buffalo", "Tampa Bay"),
}

BOAT_CONSTRAINTS = {
    1: ("A", "E"),
    2: ("E", "R"),
    7: ("E", "E"),
    10: ("R", "S"),
    14: ("A", "T"),
    17: ("T", "E"),
    20: ("T", "T"),
    23: ("A", "R"),
    29: ("T", "R"),
    30: ("S", "S"),
    35: ("A", "E"),
    37: ("A", "R"),
}

CT_THRESHOLD = 5.0


def solve_city(s2_name, group1=None, group2=None, top_n=5):
    """Find best Stage 1 pairs for a given Stage 2 city."""
    s2c = STAGE2[s2_name]

    if group1 and group2:
        if group1 == group2:
            g_cities = list(GROUPS[group1].items())
            pairs = list(combinations(g_cities, 2))
        else:
            g1_cities = list(GROUPS[group1].items())
            g2_cities = list(GROUPS[group2].items())
            pairs = [(a, b) for a in g1_cities for b in g2_cities]
    else:
        all_cities = list(ALL_S1.items())
        pairs = list(combinations(all_cities, 2))

    results = []
    for (a_name, a_coords), (b_name, b_coords) in pairs:
        ct = cross_track(
            s2c[0], s2c[1], a_coords[0], a_coords[1], b_coords[0], b_coords[1]
        )
        results.append((ct, a_name, b_name))

    results.sort()
    return results[:top_n]


def flag(ct):
    if ct < 2:
        return "✓"
    if ct < 5:
        return "~"
    if ct < 15:
        return "!"
    return "❌"


def print_all_results(top_n=5, threshold=None):
    print("=" * 80)
    print("GREAT CIRCLE PUZZLE — ALL STAGE 2 CITIES")
    print(f"Showing top {top_n} candidates per city (threshold={threshold}km if set)")
    print("=" * 80)

    for s2_name in sorted(STAGE2.keys()):
        s2c = STAGE2[s2_name]

        if s2_name in CONFIRMED:
            left, right = CONFIRMED[s2_name]
            lc, rc = ALL_S1[left], ALL_S1[right]
            ct = cross_track(s2c[0], s2c[1], lc[0], lc[1], rc[0], rc[1])
            print(f"★ {s2_name}")
            print(f"    CONFIRMED: {left} → {s2_name} → {right}  CT={ct:.4f}km")
            print()
            continue

        print(f"  {s2_name}  (coords: {s2c})")
        results = solve_city(s2_name, top_n=top_n)
        for i, (ct, left, right) in enumerate(results):
            if threshold and ct > threshold:
                break
            lg = CITY_GROUP.get(left, "?")
            rg = CITY_GROUP.get(right, "?")
            print(f"    {flag(ct)} #{i+1}  CT={ct:>7.4f}km  {left}({lg}) → {right}({rg})")
        print()


def print_constrained_rows(top_n=5):
    """Print solutions for rows where we know boat colors."""
    print("=" * 80)
    print("BOAT-CONSTRAINED ROWS (from green-highlighted rows image)")
    print("=" * 80)
    print(
        f"{'Row':<5} {'Constraint':<8} {'Left':<22} {'Stage2':<22} {'Right':<22} {'CT':>8}"
    )
    print("-" * 85)

    for row_num, (g1, g2) in sorted(BOAT_CONSTRAINTS.items()):
        best_overall = []
        for s2_name in STAGE2:
            results = solve_city(s2_name, group1=g1, group2=g2, top_n=1)
            if results:
                ct, left, right = results[0]
                best_overall.append((ct, left, s2_name, right))

        best_overall.sort()
        for i, (ct, left, s2, right) in enumerate(best_overall[:top_n]):
            marker = "★" if s2 in CONFIRMED else flag(ct)
            prefix = f"{row_num:<5} [{g1}×{g2}]  " if i == 0 else f"{'':5} {'':8}  "
            print(f"{marker} {prefix}{left:<22} {s2:<22} {right:<22} {ct:>8.4f}")
        print()


def solve_single(s2_name, top_n=10):
    """Deep dive on one specific Stage 2 city."""
    print(f"\n=== DEEP DIVE: {s2_name} ===")
    print(f"Coords: {STAGE2[s2_name]}\n")

    if s2_name in CONFIRMED:
        left, right = CONFIRMED[s2_name]
        s2c = STAGE2[s2_name]
        ct = cross_track(
            s2c[0],
            s2c[1],
            ALL_S1[left][0],
            ALL_S1[left][1],
            ALL_S1[right][0],
            ALL_S1[right][1],
        )
        print(f"★ CONFIRMED: {left} → {s2_name} → {right}  CT={ct:.4f}km\n")
        return

    results = solve_city(s2_name, top_n=top_n)
    print(f"{'#':<4} {'CT':>8}  {'Left':<24} {'Right':<24} {'Groups'}")
    print("-" * 70)
    for i, (ct, left, right) in enumerate(results):
        lg = CITY_GROUP.get(left, "?")
        rg = CITY_GROUP.get(right, "?")
        print(f"#{i+1:<3} {ct:>8.4f}km  {left:<24} {right:<24} ({lg}×{rg})")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_single(sys.argv[1], top_n=15)
    else:
        print_all_results(top_n=3, threshold=CT_THRESHOLD)
        print("\n\n")
        print_constrained_rows(top_n=3)
