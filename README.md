# chess-auto-bot
 A bot automatically plays chess for you on chess.com or lichess.org
 
## How to install
1. Clone the repository or just download the repository as a .zip and extract file
2. Make sure you have the newest version pip. If not, run `python -m pip install --upgrade pip`
3. Use pip install -r requirements.txt to install all dependencies <br>
*If you have some errors in installing Pillow, see [this](https://stackoverflow.com/questions/76997550/error-could-not-build-wheels-for-pillow-which-is-required-to-install-pyproject) and do step 3 again* 
## Settings before use(important)
- Chess.com: <br>
You must setting like this to make the bot able to play: <br>
![image](https://github.com/tiendung2306/chess-auto-bot/assets/109841830/f7bc880c-c29b-4966-bd61-d1523fb3697c)
- Lichess.org: <br>
You must setting like this to make the bot able to play: <br>
![image](https://github.com/tiendung2306/chess-auto-bot/assets/109841830/12dbb27e-0d7b-42ac-8f2d-e8acddfa1b11)
![image](https://github.com/tiendung2306/chess-auto-bot/assets/109841830/c34a143a-a000-483b-8fdf-428a7674e15e)
![image](https://github.com/tiendung2306/chess-auto-bot/assets/109841830/38a37585-28ac-46fa-aeac-076365a4db9e)

## How to use 
1. Open a Terminal
2. Change dir to the installation's folder
3. Run the command:
`python main.py`
4. A topmost app will be opened, and the interface looks like this: <br>
   ![image](https://github.com/tiendung2306/chess-auto-bot/assets/109841830/d42eb84d-d563-484b-9699-d5b371672f6a)
5. Open chess.com or lichess.org, which you want to play. **Move the 'Chess auto bot' app out of the chess's table (like the image below)**. If this's the first time you play on this site or the last time you played on another site, you need to calibrate the bot. <br>

- Play a new match versus computer, play as WHITE side 
- Click Calibrate button, you will see the text display "calibrating.."
- Click center(estimated) of 'h3' square, wait to text change to "waiting.."
![image](https://github.com/tiendung2306/chess-auto-bot/assets/109841830/2b81c4a8-c2a0-4179-a55d-2b542142ade3)
*Similar to lichess.org* <br>
*Make sure you DO NOT move any chess before start calibrating* <br>
**Note: calibrating to make bot detect where's the chess board on the screen, so if you play on a similar board's location to the last time, you don't have to calibrate again**
6. Click the "Mode: chess.com" button to change it to "Mode: lichess.org" if you play on lichess.com, or leave it as it is if you play on chess.com
7. Click Start button to start bot, the text will display "running.."
8. You can click DelayMode button to make some delay between two moves, turn it to "On" can make it harder to be banned
8. If you want to play a new game, click to "New game" button and wait text change to "waiting..". Click Start button again to start bot again

## Warnings
**DO NOT move the mouse while the bot's running** <br>
**Make sure the chess board is visible all time while the bot's running** <br>
If bot can't play, try to calibrate and start again

## Thanks
This script is made from some libraries. In developing this script I am very grateful to:
1. [StockFish](https://stockfishchess.org/download/)
2. [python-chess](https://github.com/niklasf/python-chess)
## Disclaimer
**Keep in mind Chess.com and Lichess.org would ban you for playing against other players.** <br>
**Play only against bots!** <br>

This is purely for educational purposes, I am not responsible for misuse of the script. <br>

This was not meant to be used as cheating. You can already freely do so without this script. This was just so I could see how machine learning works and how I could implement it. I saw this as a really cool idea to have a script do something automatically. I've always liked these kinds of automation projects. This was not meant to be used as a cheating tool.
