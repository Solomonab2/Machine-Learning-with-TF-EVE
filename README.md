# Machine-Learning-with-TF-EVE
A personal project to practice learning TensorFlow on an independent data set.

## About the project

Recently, I uploaded a repository, `Machine-Learning-with-TF-diamonds`, that was a personal project for learning tensorflow. After working with TF in that project, I wanted to take things one step further and apply that knowledge towards an independent data set that had not been used for machine learning models yet. The following repository is the end result of my plan to use TensorFlow on a set of unique data from the game Eve Online. 

##### The Data Set

On my quest to find a suitable data set that had not yet been used for a ML model, I came across a fascinating area of interest. The video game *Eve Online* created by the developer *CCP Games* is a large-scale online space-themed PVP MMORPG that was released in 2003. While video games do not typically provide the conditions or motivation for creating a machine learning model around, this game held a particularly useful distinction from many others. *Eve Online* has had a long history of providing a publicly available API for accessing all sorts of in-game statistics and historical data. Due to the thousands of in-game items, ships, and locations, this public API provides access to a vast and unique pool of data that dates back more than *ten years*. Some examples of such data could be anything from historical market data including prices of items, volume of items sold, and number of items sold from particular locations in-game to other types of historical data like the unique kill-logs of *every ship that has ever been destroyed* in *Eve Online*, or data on the trends of all types of materials harevested in-game and *sinks* and *faucets* of in-game currency. 

Because of this overwhelming amount of game data, I thought that *Eve Online* was a perfect starting point for my proposed goals and I sought to create a model around some of the historical data that is provided for the game online. 

##### The Model

The most suitable idea that came to mind when exploring the game's data was a simple winner-predictor of a two-player fight. From that idea and the available data, I decided to utilize historical player-combat-logs and use them to train a TensorFlow model to predict the likelyhood of a particular ship winning a fight with another particular ship. The historical player-combat data that is provided online conveniently includes a log of *every ship that is destroyed by another player* and this log includes tidbits of useful information in the following format:
    - The ID number of the ship that was destroyed
    - The ID number of the victim that was flying the ship
    - The victim's corporation ID number
    - The exact time of the kill of the format: 'YYYY-MM-DD:HH:MM:SS'
    - The *value* of the ship that was destroyed, and all of the individual items that it was carrying
    - The exact amount of damage that the ship took
    - The exact location that the ship was destroyed in the form of: Region_ID, Constellation_ID in that region, and SolarSystem_ID inside that constellation
    - The ID number of the weapon types used to destroy the ship
    - The ID number of the player(s) who destroyed the ship (and their corporation_IDs)
    - The ID number of the ship(s) that was used to destroy the victim

By using this data, I sought to create a model that would train by looking at the ship ID's of attacker and victim ships for hundreds of thousands of kills and learn to classify the attacking ship as a likely winner or loser for a given conflict. 

Some interesting points that needed to be clarified before building the model were the following:
    - Any logs of a ship destroying another identical ship were trimmed from the data
    - Only the logs of 'solo kills' were used for the model, as the model was intended for 1 vs. 1 situations only
    - Many of the logs contained missing information that had to be cleaned before use such as:
        - Occasionally ship ID's were missing for either the attacker or victim
        - Occasionally corporation ID's were missing for players without corporations
        - Occasionally the weapon ID's were the same as ship ID's through errors in the games' logging mechanics


