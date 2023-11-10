import chess
import chess.engine
import time

board = chess.Board()

def Init(skill_level):
    global engine
    engine = chess.engine.SimpleEngine.popen_uci('.\\stockfish\\stockfish-windows-x86-64-avx2.exe')
    engine.configure({"Skill Level": skill_level})

def GetPiece(idx):
    if board.piece_at(idx) != None:
        return board.piece_at(idx).symbol()
    else:
        return ' '

def GetNextMove(movetime):
    global engine, board
    return engine.play(board, chess.engine.Limit(time=movetime)).move.uci()

def Move(x=''):
    global board
    board.push(chess.Move.from_uci(x))
    print(x)

def QuitEngine():
    global engine
    engine.quit()
