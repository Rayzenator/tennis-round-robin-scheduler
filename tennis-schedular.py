import streamlit as st
import itertools
import random

st.set_page_config(page_title="Tennis Round Robin Scheduler", layout="centered")
st.title("🎾 Tennis Round Robin Scheduler")

# Step 1: Court numbers
st.header("Step 1: Enter Court Numbers")
court_input = st.text_input("Enter court numbers separated by commas (e.g., 1, 2, 17, 18):")
courts = []

if court_input:
    try:
        courts = [int(c.strip()) for c in court_input.split(",") if c.strip()]
        st.success(f"Courts entered: {courts}")
    except ValueError:
        st.error("Please enter valid integers separated by commas.")

# Step 2: Match format
st.header("Step 2: Choose Match Format")
main_format = st.radio("Main match format", ["Singles", "Doubles"])

# Step 3: Fallback handling
fallback_action = st.radio("If players are left over:", [
    "Let extra players rest",
    "Use American Doubles if possible"
])

# Step 4: Player names
st.header("Step 3: Enter Players")
players = st.text_area("Enter one player per line:").splitlines()
players = [p.strip() for p in players if p.strip()]
random.shuffle(players)

if players:
    st.success(f"{len(players)} players entered: {', '.join(players)}")

# Match generation
def schedule_matches(players, courts, main_format, fallback_action):
    rounds = []
    pool = players[:]

    while pool:
        round_matches = []
        court_index = 0
        working_pool = pool[:]
        used_players = set()

        while court_index < len(courts) and len(working_pool) >= (2 if main_format == "Singles" else 4):
            if main_format == "Singles" and len(working_pool) >= 2:
                p1, p2 = working_pool.pop(), working_pool.pop()
                round_matches.append(("Singles", courts[court_index], (p1, p2)))
                used_players.update([p1, p2])

            elif main_format == "Doubles" and len(working_pool) >= 4:
                match_players = [working_pool.pop() for _ in range(4)]
                round_matches.append(("Doubles", courts[court_index],
                                      ((match_players[0], match_players[1]), (match_players[2], match_players[3]))))
                used_players.update(match_players)

            court_index += 1

        # Handle leftovers
        leftovers = [p for p in pool if p not in used_players]
        if fallback_action == "Use American Doubles if possible":
            if len(leftovers) >= 3 and court_index < len(courts):
                ad_group = [leftovers.pop() for _ in range(3)]
                round_matches.append(("American Doubles", courts[court_index], tuple(ad_group)))
                used_players.update(ad_group)

        pool = [p for p in pool if p not in used_players]
        rounds.append(round_matches)

    return rounds

# Step 5: Generate schedule
if st.button("Generate Schedule"):
    if len(players) < 2:
        st.error("You need at least 2 players.")
    elif not courts:
        st.error("Please enter courts.")
    else:
        match_rounds = schedule_matches(players, courts, main_format, fallback_action)

        st.header("📅 Match Schedule")
        for round_num, matches in enumerate(match_rounds, 1):
            st.subheader(f"Round {round_num}")
            for match_type, court, match in matches:
                if match_type == "Singles":
                    st.markdown(f"**Court {court}** (Singles): {match[0]} vs {match[1]}")
                elif match_type == "Doubles":
                    t1, t2 = match
                    st.markdown(f"**Court {court}** (Doubles): {t1[0]} & {t1[1]} vs {t2[0]} & {t2[1]}")
                elif match_type == "American Doubles":
                    st.markdown(f"**Court {court}** (American Doubles): {match[0]}, {match[1]}, {match[2]} (rotate partners)")