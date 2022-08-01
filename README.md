# SGAI - Outbreak - Q Learning AI
This is the repository for the MIT Beaverworks' SGAI 2022 serious games and reinforcement learning project.

## Team Willy I
The best team out there!

## How to run
### VS Code version
DO NOT run main.py when the current directory is SGAI-Outbreak.
You must open the folder SGAI_MK3 with vscode. Then, you can
run main.py from VS Code.
### cmd line version
First, `cd ./SGAI_MK3`. Then, `python main.py`

## Game Options
Train Mode: Runs for around 1000 times before learning to win

Test Mode: Uses Preloaded Q-Table, runs with pre-trained AI, wins often

Hospital Mode: Zombies heal in hospital zone with only one attempt, two attempts are needed in no hospital zones.

Stat Charts are stored in the Stats-Current-Run directory every 10 games.

Game can be slowed down by increasing the value of AI_PLAY_WAITTIME_MS
