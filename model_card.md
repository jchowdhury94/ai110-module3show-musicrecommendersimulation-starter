# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

VibeMatch is a small CLI simulation. It takes a "taste profile" — a favorite genre, a favorite mood, a target energy level, and whether the listener likes acoustic music — and ranks a fixed 18-song catalog to find the closest matches, printing the top 5 with a plain-language explanation of why each song scored the way it did.

It assumes a user's taste can be boiled down to those four things, and that "favorite genre" and "favorite mood" are single fixed values rather than a mix (nobody actually likes only one genre). It's meant to be run against the sample profiles in `src/main.py`, not real listeners, so it's a teaching tool for understanding how scoring and ranking logic works under the hood — the kind of thing a real app like Spotify does at much larger scale.

---

## 3. How the Model Works  

Every song starts at a score of 0, and points get added for each way it matches what the user asked for:

- If the song's genre matches the user's favorite genre, add **1.0 point**.
- If the song's mood matches the user's favorite mood, add **1.0 point**.
- Look at how close the song's energy is to the user's target energy. The closer they are, the more points it earns — a perfect match earns **4.0 points**, and the points shrink the further apart they are.
- If the user says they like acoustic music, add points based on how acoustic the song actually is (up to **1.0 point**).

Add all of that up, do the same for every song in the catalog, then sort from highest score to lowest and hand back the top 5.

The starter file I began with didn't score anything — it just returned the first 5 songs in the file and a placeholder explanation. I wrote the actual scoring, matching, and ranking logic from scratch. I also ran an experiment changing the weights: I originally had genre worth 2.0 points and energy worth up to 2.0 points, then shifted to genre worth 1.0 and energy worth up to 4.0. That change is discussed in [Section 7](#7-evaluation) — it made energy similarity a much bigger driver of the final ranking than genre or mood.

---

## 4. Data  

The catalog is `data/songs.csv`, 18 songs total, and I didn't add or remove any rows. Each song has a genre, mood, energy, tempo, valence, danceability, and acousticness value.

The genres are almost all unique — pop, lofi (the only genre with more than one song, at 3), rock, jazz, synthwave, indie pop, r&b, country, metal, classical, hip hop, reggae, electronic, blues, and ambient. Moods are similarly spread thin: chill (3 songs) and intense/happy (2 each) are the only moods with more than one song; the rest (relaxed, moody, focused, romantic, nostalgic, angry, peaceful, confident, laid-back, euphoric, sad) each have exactly one.

That's the biggest gap in the dataset: with so few songs sharing a genre or mood, most user profiles simply don't have enough matching songs to fill a top-5 list, so the model has to lean on energy similarity to fill the rest (see [Section 6](#6-limitations-and-bias)). The dataset also has no lyrics, artist popularity, or listening history — so it can't capture anything about why someone likes a song beyond these four numeric/categorical tags.

---

## 5. Strengths  

The model works best when the catalog actually has a song that matches the user's genre, mood, and energy target all at once — in every one of my four standard test profiles, the #1 recommendation was a song that hit all three, and it was scored clearly ahead of the rest of the list (for example, "Storm Runner" for Deep Intense Rock at 5.96 vs. 4.88 for 2nd place). That matched my intuition every time: when someone asks for pop/happy/high-energy, the model's top pick should be a genuinely upbeat pop song, and it was.

The acoustic bonus also works the way I'd expect — for the Chill Lofi and Acoustic Jazz Lover profiles, the acoustic-heavy songs ("Library Rain," "Coffee Shop Stories") get a noticeable boost that pop and rock songs never receive, which nudges the ranking toward music that actually fits an acoustic listener.

It's also fairly robust to a weird input: when I gave it an energy target above the valid range (1.5, in the Out-of-Range Energy test), it didn't crash or break — it just let the energy term shrink toward zero for every song and let the genre+mood match win instead, which is arguably a *more* sensible result than a normal in-range request.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Testing a "Conflicting Sad + High Energy" profile (genre: blues, mood: sad, energy: 0.95) exposed a real weakness in how the score is weighted. The one song that actually matched both genre and mood, "Backroad Blues," landed in 5th place with a score of 3.52, while four songs that matched neither genre nor mood outranked it, purely because their energy happened to be close to 0.95. This happens because the energy term is scaled by a factor of 4, so a strong energy match (up to +4.0) can outweigh both the genre match (+1.0) and mood match (+1.0) combined. In effect, the model overfits to energy similarity and can bury the most contextually relevant song for a user whose stated mood and target energy pull in opposite directions, which is exactly the kind of nuanced, conflicting taste real listeners have. A fairer design would need to weight the categorical matches (genre, mood) more heavily relative to energy, or treat a genre+mood match as a floor that energy differences can't fully cancel out.

---

## 7. Evaluation  

**Weight-shift experiment.** I originally scored genre matches at +2.0 and energy similarity at up to +2.0 (genre worth more than a perfect energy match). I then shifted to genre +1.0 and energy up to +4.0, to see how sensitive the rankings actually are to these numbers. For the well-behaved profiles the top pick didn't change, but the *margins* did — e.g. for High-Energy Pop, the gap between the #1 pick ("Sunrise City," a full genre+mood+energy match) and an energy-only song like "Concrete Bloom" shrank from 3.00 points (4.94 vs. 1.94) down to 2.00 points (5.88 vs. 3.88), because energy-only songs now score much higher. The clearest effect showed up in the Conflicting Sad + High Energy edge case: under the old weights, "Backroad Blues" (the one genre+mood match) still won 1st place at 3.76 despite its energy being far from the target. Under the new weights, it drops to 5th at 3.52, and four songs with zero genre or mood match take the top 4 spots purely on energy closeness. So the exact same catalog and the exact same user request can flip a recommendation from "the contextually right song" to "buried on page one" just by changing how much weight energy gets — a small implementation choice, not a fact about the music.

I ran `recommend_songs` against six profiles defined in `src/main.py`: four "standard" tastes — **High-Energy Pop** (pop/happy/0.85), **Chill Lofi** (lofi/chill/0.3, acoustic), **Deep Intense Rock** (rock/intense/0.9), and **Acoustic Jazz Lover** (jazz/relaxed/0.4, acoustic) — plus two adversarial edge cases: **Conflicting Sad + High Energy** (blues/sad/0.95, no song in the catalog combines "sad" with high energy) and **Out-of-Range Energy** (metal/angry/1.5, a target outside the valid 0–1 range). What surprised me was how often songs that matched *neither* genre nor mood still cracked the top 5 purely on energy closeness — e.g. "Pulse Horizon" and "Concrete Bloom" showed up in the High-Energy Pop top 5 with zero categorical matches, and the same near-miss pattern showed up in Deep Intense Rock and the Conflicting Sad profile. For the well-behaved profiles this mostly matched my expectations (the #1 pick always had genre+mood+energy all aligned), but the edge cases confirmed the ranking can be dominated by energy alone when a full match isn't available.

Genre and mood each contribute a flat +1.0, acoustic preference adds up to +1.0 only when `likes_acoustic` is true, but energy similarity can contribute up to +4.0 — so a close energy match alone routinely outscores one or even two categorical matches. This is visible any time the target energy sits near a cluster of same-vibe songs: the model rewards "sounds similar" over "is what you asked for" whenever the two disagree.

- **High-Energy Pop vs. Chill Lofi**: Zero song overlap in the top 5 (5.88–3.80 vs. 6.66–4.61 score ranges). The two profiles sit at opposite ends of the energy axis (0.85 vs. 0.3), so the ±4.0 energy term pushes each toward a completely different song cluster, and Chill Lofi's `likes_acoustic=True` adds a further +0.7–0.9 bump that Pop songs never get.
- **High-Energy Pop vs. Deep Intense Rock**: Despite different genre/mood, three songs ("Gym Hero," "Pulse Horizon," "Sunrise City") appear in both top 5s because their target energies are close (0.85 vs. 0.9). Rock's #1, "Storm Runner" (5.96), edges out Pop's #1, "Sunrise City" (5.88), because Storm Runner gets a genre+mood match at a very close energy fit, showing that when energy targets nearly coincide, the categorical matches decide the ordering.
- **Chill Lofi vs. Deep Intense Rock**: No overlap at all — the 0.3 vs. 0.9 energy gap is the largest of any pair tested, so it swamps any incidental genre/mood similarity, and Chill Lofi's acoustic bonus (absent for Rock) widens the gap further.
- **Conflicting Sad + High Energy vs. Deep Intense Rock**: Because both target energy near 0.9–0.95, the same songs ("Gym Hero," "Storm Runner," "Pulse Horizon") show up in both lists. But Deep Intense Rock has a song ("Storm Runner") that matches genre+mood *and* energy, so it cleanly wins the #1 spot (5.96); the Conflicting profile has no blues+sad+high-energy song, so its top 4 are pure energy matches with no categorical bonus, and the one genre+mood match ("Backroad Blues") is pushed to 5th purely because its energy (0.75-ish) is farther from 0.95 than the energy-only songs' — the exact failure mode flagged in [Section 6](#6-limitations-and-bias).
- **Out-of-Range Energy vs. High-Energy Pop**: With a target of 1.5 (above every song's actual energy), the energy term shrinks for *every* candidate, which flattens its influence and lets the genre+mood match dominate instead — "Neon Requiem" wins clearly (3.88) with a 2.16-point gap over 2nd place, a much wider margin than High-Energy Pop's #1-to-#2 gap (1.20). This shows that an impossible energy target doesn't break the system; it inadvertently rebalances scoring back toward genre/mood, which is closer to what I'd want by default.

---

## 8. Future Work  

The biggest fix I'd want to make is rebalancing the weights so a genre+mood match sets a floor that energy differences can't fully cancel out — right now a great energy fit can outrank the one song that's actually the right vibe, which is backwards. I'd also add negative preferences (a "disliked genre/mood" the user wants to avoid), since right now the model has no way to push a song *down*.

I'd put the unused columns — `tempo_bpm`, `valence`, and `danceability` — to work instead of just `energy` and `acousticness`, so two songs with the same energy but very different tempo or mood-valence aren't treated as equivalent. I'd also add a diversity rule so the top 5 doesn't repeat the same artist twice (LoRoom shows up twice in the Chill Lofi top 5), and I'd grow the catalog past 18 songs so more genre/mood combinations actually have more than one candidate to choose from. Finally, I'd rewrite the explanations in plainer language ("this is upbeat and matches your energy level" instead of a raw list of point values) so they'd make sense to someone who isn't reading the code.

---

## 9. Personal Reflection  

My biggest "aha" moment was the weight-shift experiment in Section 7. I expected changing genre from +2.0 to +1.0 and energy from ×2 to ×4 to just shuffle the scores a little — instead it flipped "Backroad Blues" from the clear #1 pick down to 5th place for the Conflicting Sad + High Energy profile, even though it was still the only song that actually matched the requested genre and mood. That made it click for me that a recommender's "accuracy" isn't some fixed, objective thing — it's a direct consequence of numbers I picked somewhat arbitrarily, and small tweaks to those numbers can completely change what counts as a "good" recommendation.

Claude Code was most useful for the mechanical, repetitive parts: building out the `PROFILES` dictionary in `src/main.py` with realistic profiles plus deliberately adversarial ones (the sad/high-energy conflict, the out-of-range energy value), and running the same comparison logic across all six profiles so I could see the score breakdowns side by side. Where I had to slow down and check its work was the actual numbers — I re-ran `python -m src.main` myself to confirm every score and ranking claim in this model card matched real output, rather than trusting a written-out description of what the scores "should" be. I also caught that `README.md`'s sample output section is now stale (it still shows the old +2.0 genre / ×2 energy weights), which is a good reminder that generated docs drift out of sync with code the moment you tweak something and forget to regenerate the example.

It's a little surprising that such a simple weighted sum — four numbers added together — can feel personalized at all. I think it works because those four features (genre, mood, energy, and "do you like acoustic stuff") are genuinely close to how people describe their own taste in casual conversation, so even a crude match against them produces something that *feels* relevant. But it's a shallow kind of personalization: it has no memory of what I listened to yesterday, no sense of songs I specifically don't want, and with only 18 songs it often has to pad out a "top 5" with songs that only match on one axis. It changed how I think about real recommendation apps — the sense of "this app really gets me" is probably built on the same kind of arithmetic, just with thousands of features and a much bigger catalog smoothing over the rough edges that show up so clearly here.
