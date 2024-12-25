
from src import FrechetMusicDistance

fmd = FrechetMusicDistance()
score = fmd.score("../data/midi/maestro_2004", "../data/midi/maestro_2008")
print(f"FMD: {score}")