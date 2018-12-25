from typing import List

import related


@related.immutable
class Beatmap:
    id: int = related.IntegerField(key="beatmapset_id")
    artist: str = related.StringField()
    title: str = related.StringField()


@related.immutable
class SearchResults:
    beatmaps: List[Beatmap] = related.SequenceField(Beatmap)
    result_count: int = related.IntegerField()

    @classmethod
    def from_json(cls, stream: any):
        return related.from_json(stream, cls)
