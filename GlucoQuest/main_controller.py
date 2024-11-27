from menu import main as menu_main
from main import main_game
from stickers import main_stickers
from challenges import main_challenges
from leaderboard import main_leaderboard
from avatar import main_avatar

def run_game():
    main_game(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)

def run_stickers():
    main_stickers(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)

def run_leaderboard():
    main_leaderboard(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)

def run_challenges():
    main_challenges(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)

def run_avatar():
    main_avatar(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)

if __name__ == "__main__":
    menu_main(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)
