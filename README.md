# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works


This recommender compares the user's preferences with every song in the dataset to find the best matches. It calculates a similarity score for each song, ranks the songs from highest to lowest score, and recommends the top matches.

**Song features:**
- Genre
- Mood
- Energy
- Acousticness

**UserProfile features:**
- Favorite genre
- Favorite mood
- Target energy
- Likes acoustic music

### Algorithm Recipe

1. Start each song with a score of 0.
2. Add **2.0 points** if the song's genre matches the user's favorite genre.
3. Add **1.0 point** if the song's mood matches the user's favorite mood.
4. Calculate energy similarity using:
   ```
   energy_points = (1 - abs(song_energy - target_energy)) * 2
   ```
   Songs with energy closer to the user's target receive more points.
5. If the user likes acoustic music, add **1.0 point** for songs with high acousticness.
6. Add the points to get a final score.
7. Rank the songs by score and recommend the top matches.

### Potential Biases

This recommender may over-prioritize genre and overlook songs from other genres that have a similar mood or energy. It also only considers a few song features and does not account for lyrics, artists, or personal listening history.
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
=== Profile: High-Energy Pop ===
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.85, 'likes_acoustic': False}

Top 5 recommendations:

1. Sunrise City — Neon Echo
   Score: 4.94
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+1.94)

2. Gym Hero — Max Pulse
   Score: 3.84
   Reasons: genre match (+2.0), energy similarity (+1.84)

3. Rooftop Lights — Indigo Parade
   Score: 2.82
   Reasons: mood match (+1.0), energy similarity (+1.82)

4. Pulse Horizon — Kilowatt Youth
   Score: 1.94
   Reasons: energy similarity (+1.94)

5. Concrete Bloom — MC Kestrel
   Score: 1.90
   Reasons: energy similarity (+1.90)
```

```
=== Profile: Chill Lofi ===
Preferences: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'likes_acoustic': True}

Top 5 recommendations:

1. Library Rain — Paper Lanterns
   Score: 5.76
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+1.90), acoustic preference (+0.86)

2. Midnight Coding — LoRoom
   Score: 5.47
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+1.76), acoustic preference (+0.71)

3. Focus Flow — LoRoom
   Score: 4.58
   Reasons: genre match (+2.0), energy similarity (+1.80), acoustic preference (+0.78)

4. Spacewalk Thoughts — Orbit Bloom
   Score: 3.88
   Reasons: mood match (+1.0), energy similarity (+1.96), acoustic preference (+0.92)

5. Coffee Shop Stories — Slow Stereo
   Score: 2.75
   Reasons: energy similarity (+1.86), acoustic preference (+0.89)
```

```
=== Profile: Deep Intense Rock ===
Preferences: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}

Top 5 recommendations:

1. Storm Runner — Voltline
   Score: 4.98
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+1.98)

2. Gym Hero — Max Pulse
   Score: 2.94
   Reasons: mood match (+1.0), energy similarity (+1.94)

3. Pulse Horizon — Kilowatt Youth
   Score: 1.96
   Reasons: energy similarity (+1.96)

4. Neon Requiem — Glass Cathedral
   Score: 1.86
   Reasons: energy similarity (+1.86)

5. Sunrise City — Neon Echo
   Score: 1.84
   Reasons: energy similarity (+1.84)
```

```
=== Profile: Acoustic Jazz Lover ===
Preferences: {'genre': 'jazz', 'mood': 'relaxed', 'energy': 0.4, 'likes_acoustic': True}

Top 5 recommendations:

1. Coffee Shop Stories — Slow Stereo
   Score: 5.83
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+1.94), acoustic preference (+0.89)

2. Focus Flow — LoRoom
   Score: 2.78
   Reasons: energy similarity (+2.00), acoustic preference (+0.78)

3. Library Rain — Paper Lanterns
   Score: 2.76
   Reasons: energy similarity (+1.90), acoustic preference (+0.86)

4. Spacewalk Thoughts — Orbit Bloom
   Score: 2.68
   Reasons: energy similarity (+1.76), acoustic preference (+0.92)

5. Midnight Coding — LoRoom
   Score: 2.67
   Reasons: energy similarity (+1.96), acoustic preference (+0.71)
```

```
=== Profile: Conflicting Sad + High Energy ===
Preferences: {'genre': 'blues', 'mood': 'sad', 'energy': 0.95, 'likes_acoustic': False}

Top 5 recommendations:

1. Backroad Blues — Otis Rambler
   Score: 3.76
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+0.76)

2. Gym Hero — Max Pulse
   Score: 1.96
   Reasons: energy similarity (+1.96)

3. Neon Requiem — Glass Cathedral
   Score: 1.96
   Reasons: energy similarity (+1.96)

4. Storm Runner — Voltline
   Score: 1.92
   Reasons: energy similarity (+1.92)

5. Pulse Horizon — Kilowatt Youth
   Score: 1.86
   Reasons: energy similarity (+1.86)
```

```
=== Profile: Out-of-Range Energy ===
Preferences: {'genre': 'metal', 'mood': 'angry', 'energy': 1.5, 'likes_acoustic': False}

Top 5 recommendations:

1. Neon Requiem — Glass Cathedral
   Score: 3.94
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+0.94)

2. Gym Hero — Max Pulse
   Score: 0.86
   Reasons: energy similarity (+0.86)

3. Storm Runner — Voltline
   Score: 0.82
   Reasons: energy similarity (+0.82)

4. Pulse Horizon — Kilowatt Youth
   Score: 0.76
   Reasons: energy similarity (+0.76)

5. Sunrise City — Neon Echo
   Score: 0.64
   Reasons: energy similarity (+0.64)
```
**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

### Accuracy and Surprises

For the High-Energy Pop profile, the top result ("Sunrise City") felt reasonable because it matched both the preferred genre (pop) and mood (happy), and its energy (0.82) was close to the target (0.85). It earned points in all three major categories — genre (+2.0), mood (+1.0), and energy (+1.94) — for a score of 4.94, well ahead of the runner-up ("Gym Hero," 3.84), which only matched on genre and energy.

One surprising pattern: songs like "Pulse Horizon" and "Concrete Bloom" still made the High-Energy Pop top 5 with no genre or mood match at all — their entire score came from energy similarity alone (+1.94 and +1.90). The same thing happens for Deep Intense Rock, where 4 of the top 5 songs match on energy only. With just 18 songs in the catalog, there usually aren't enough genre-and-mood matches to fill five slots, so the scorer falls back to ranking by energy alone. That's a useful signal, but it means "top 5" doesn't always mean "a good match" — it can just mean "the least bad option available."

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



