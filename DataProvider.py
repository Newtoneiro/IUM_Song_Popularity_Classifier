import pandas as pd
import numpy as np
from random import sample

MS_TO_MIN = 1.66e-5


class DataProvider:
    def __init__(self):
        pd.set_option("mode.chained_assignment", None)
        print("[Getting raw data...]")
        self._get_raw_data()
        print("[Preprocessing...]")
        self._preprocess()
        print("[Data Provider ready]")

    def get_x_and_y(self, artists):
        x = []
        y = []
        for artist in artists:
            x.append(
                [
                    avg_playtime
                    for avg_playtime in self._artists_playtime[artist].values[:-1]
                ]
            )
            y.append(self._artists_playtime[artist].values[-1])
        x, y = np.array(x), np.array(y)
        return x.reshape((x.shape[0], x.shape[1], 1)), y

    def get_artists(self):
        return self._all_artists

    def get_train_test_sets(self, proportions=0.5):
        artists = self._artists_playtime.keys()
        train = sample(artists, round(proportions * len(artists)))
        test = artists - train
        return train, test

    def _get_raw_data(self):
        artists = pd.read_json("data_v2/artists.jsonl", lines=True)
        sessions = pd.read_json("data_v2/sessions.jsonl", lines=True)
        tracks = pd.read_json("data_v2/tracks.jsonl", lines=True)
        data = sessions.merge(
            tracks[["id", "id_artist", "duration_ms"]],
            left_on="track_id",
            right_on="id",
            how="left",
        )
        data = data.merge(
            artists[["id", "name"]], left_on="id_artist", right_on="id", how="left"
        )
        self._raw_data = data

    def _approximate_playtime(self, data):
        play_playtime = (
            data[data["event_type"] == "PLAY"]
            .groupby("weeks_ordered")["duration_ms"]
            .sum()
            * MS_TO_MIN
        )
        # skip_playtime = data[data['event_type'] == 'SKIP'] \
        # .groupby('weeks_ordered')['duration_ms'].sum() / 2
        return play_playtime

    def _preprocess(self):
        # Last week data is meager, therefore we cut it off
        data = self._raw_data[self._raw_data["timestamp"] < "2023-04-10"]
        data["weeks_ordered"] = self._raw_data["timestamp"].apply(
            lambda data: data.week
        )

        # Only consider data from consistent artists
        self._all_artists = data["name"].unique()
        consistent_artists = []

        for artist in self._all_artists:
            if len(data[data["name"] == artist]["weeks_ordered"].unique()) == 12:
                consistent_artists.append(artist)
        self._consistent_artists = consistent_artists

        artists_playtime = {
            artist: self._approximate_playtime(data[data["name"] == artist])
            for artist in consistent_artists
        }

        self._artists_playtime = artists_playtime
