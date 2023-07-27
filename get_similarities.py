import typing
import time
import requests
import json


API_KEY = ''


def get_similarities(artist: str, limit: int = 3) -> list:
    url = 'https://ws.audioscrobbler.com/2.0/'
    response = requests.api.get(
        url=url,
        params={
            'api_key': API_KEY,
            'method': 'artist.getsimilar',
            'artist': artist,
            'format': 'json',
            'limit': limit,
        }
    )
    assert response.status_code == 200
    content = json.loads(response.content.decode('utf-8'))
    return [
        {
            'name': artist['name'],
            'match': artist['match'],
        }
        for artist
        in content['similarartists']['artist']
    ]

def get_similarity_graph(
        starting_artist: str,
        edges_limit: int,
        nodes_limit: int,
        match_threshold: float,
        sleep_ms: int = 1000,
):
    queue = [starting_artist]
    graph: typing.Dict[str, typing.Dict] = {}
    index: int = 0
    while index < len(queue) and index < nodes_limit:
        artist = queue[index]
        print(f'Get similar artist for {artist}')
        similarities = get_similarities(artist, edges_limit)
        filtered_similarities = []
        for entry in similarities:
            if float(entry['match']) >= match_threshold:
                filtered_similarities.append(entry)
        graph[artist] = filtered_similarities
        for artist in filtered_similarities:
            if queue.count(artist['name']) == 0:
                queue.append(artist['name'])
        index += 1
        time.sleep(sleep_ms / 1000.0)
    return graph

graph = get_similarity_graph('Кино', 8, 100, 0.4, 100)
with open('result_kino.json', 'w') as f:
    f.write(json.dumps(graph, indent=2, ensure_ascii=False))

# print(json.dumps(get_similarities('Слава КПСС', 20), indent=2, ensure_ascii=False))
