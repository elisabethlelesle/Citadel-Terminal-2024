# What is Terminal?

Terminal is an online games-based programming competition for university students around the globe studying software engineering and data science.
Top teams win a cash prize.
Organized by Citadel Securities LLC, one of the most prestigious American market making firms, this competition allows for motivated students to collaborate.

# To join

You must first apply through the website, then receive confirmation to participate in the competition. For this Europe Spring 2024 Terminal competition, only 60 students were selected to participate.
Only undergraduate/graduate students in good standing pursuing a bachelor’s or master’s degree in Math, Engineering, Statistical Modeling, Calculus, Computer Science, Physics, or Economics were considered.

# Goal

Deploy a game strategy algorithm to defeat the most bosses (and other teams' algorithms)

# About the game

At our disposal, we had defense and offense components to place on the board. The defense are static and have the ability to destroy the opponent's attacking pieces, and the latter move in zigzag to reach the other side of the board. If they reach their goal, the HP of the opponent goes down.
Depending on the boss, the components are set differently on the board, with a more defensive or offensive strategy. 

This game strategy script is structured around the `AlgoStrategy` class, extending `gamelib.AlgoCore`. It initializes with a random seed and sets up game configurations, unit types, and initial defenses. The core logic resides in the `on_turn` method, which processes game states, performs strategic moves, and deploys units. Defensive measures are enhanced based on enemy scoring locations, while offensive strategies adapt to enemy base defenses, deploying units like Scouts, Demolishers, and Interceptors as needed. 

# About my team's strategy

## Upgrades on Reactive Defense:

<li>Starter Strategy: Builds reactive defenses based on enemy scoring locations by placing turrets one space above the scoring location. </li>
<li>Enhanced Strategy: Improves reactive defense by also placing and upgrading walls directly on the scoring location, providing additional protection.</li>


## Upgrades on Offensive Tactics:

<li>Starter Strategy: Uses Scouts for quick attacks and Demolishers for long-range attacks if the enemy has many units in the front. </li>
<li>Enhanced Strategy: Introduces an adaptive offense in the adaptive_offense method, which dynamically chooses between Demolisher attacks and Scout deployments based on the analysis of enemy defenses. Also includes support unit upgrades for enhancing offensive capabilities. </li>

## How we used our resoures

The Starter Strategy builds basic defenses and then upgrades walls to soak more damage. However, from the get-go, our Enhanced Strategy expands the initial wall setup with extra walls and upgrades them for better early-game defense. It also upgrades support units to enhance unit effectiveness.

## As a whole

Our new strategy first aimed to improve defense from the beginning, using a more comprehensive initial defense setup with additional walls and upgrades provides better early-game protection.
As for our offensive strategy, we made it more adaptive to better respond to different enemy setups, improving the chances of successful attacks.

It ended up beating bosses 2 and 3.

We did not focus much on the optimization of the code, but rather on the efficiency in the game.
