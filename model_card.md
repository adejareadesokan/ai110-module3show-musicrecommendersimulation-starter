# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  
ChooseYourGroove
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 
It is meant to recommend songs based on one's listening preferences (e.g pop, rock,etc). It assumes that the user is binary when it comes to song choices(e.g either he likes one genre or not. he likes acoustic or not). It's intended for classroom exploration
Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  
it uses features which are weighted such as mood and energy, then a score is calculated. Each feature a has a formula specific to it and a weight attached to it. Mood energy and genre are the heaviest when it comes to the total score. The total score is calculated and ranked from highest to lowest. the highest scorers are recommended to the user.
Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  
the dataset consists of 18 songs with 15 distinct genres and 11 moods. the songs are ranked based on both categorical features like mood and numerical features like energy level. There are still missing parts of music taste such as soul and afrobeats.
Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  
The code runs without errors, generating recommendations for the user and stating the reasons why based off the user's profile.
Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  
It doesn't consider artist familiarity or tempo direction, as well  as listening history orplay count. It also has a heavy bias towards energy and mood, neglecting facors like genre and acousticness. The dataset is also small and non-diverse so most genres don't have flexibility of choice

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 
I brainstormed certain usual profiles to see how the code will react, then I also got some from AI as wll. I looked for which results were out of place then I would revise the code and prompt AI to change the anomalies. One thing I was surprised about was the fact that there are some bugs caused from code that do not cause errors in running.
At a point in time, some of my methods in the recommender weren't implemented, but the code still excuted with no errors.

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  
In the future, I would make the scoring logic more flexible, have more genres and subgenres, add AI modules and improve modularity
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
This was very enlightening. I was able to learn how various apps use data I give to them to give me information. I learnt new metrics of calculation as well as how algorithms are used to retrieve data and produce info. I would approach music recommendation apps as well as music apps differently because I am more knowledgeable of the ways they recommend music to me now
