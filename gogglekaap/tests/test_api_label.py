
def test_get_labels(client):
    r = client.get(
        '/api/labels',
        follow_redirects = True
    )
    assert r.status_code == 200
    assert r.json == []


def test_post_label(client):
    label = {
        'content': 'label'
    }
    r = client.post(
        '/api/labels',
        data = label
    )
    assert r.status_code == 201
    assert r.json.get('content') == label['content']


def test_delete_label(client):
    r = client.delete(
        '/api/labels/1' # 위에서 만들어진 데이터의 id 는 1 일 것이므로.
    )
    assert r.status_code == 204
    r = client.get(
        '/api/labels',
        follow_redirects=True
    )
    assert r.status_code == 200
    assert r.json == []