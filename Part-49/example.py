class Playlist:
    def __init__(self, name):
        self.name = name
        self._songs = []

    def add(self, song):
        self._songs.append(song)

    def __len__(self):
        return len(self._songs)

    def __repr__(self):
        return f"Playlist('{self.name}', {len(self)} songs)"

p = Playlist("Workout Mix")
p.add("Eye of the Tiger")
p.add("Lose Yourself")

print(len(p))   # 2
print(p)        # Playlist('Workout Mix', 2 songs)