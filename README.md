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
Loaded songs: 18

Top recommendations:

1. Sunrise City — Neon Echo
   Score: 4.96
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+1.96)

2. Gym Hero — Max Pulse
   Score: 3.74
   Reasons: genre match (+2.0), energy similarity (+1.74)

3. Rooftop Lights — Indigo Parade
   Score: 2.92
   Reasons: mood match (+1.0), energy similarity (+1.92)

4. Concrete Bloom — MC Kestrel
   Score: 2.00
   Reasons: energy similarity (+2.00)

5. Night Drive Loop — Neon Echo
   Score: 1.90
   Reasons: energy similarity (+1.90)

```
**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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



