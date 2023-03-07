    
def test_auth(client):
    r = client.get(
        '/auth/register',
        follow_redirects=True # page가 redirect 되면 따라가서 최종 값을 리턴하기 위함
    )
    assert r.status_code == 200

    r = client.get(
        '/auth',
        follow_redirects=True
    )
    assert r.status_code == 200

    r = client.get(
        '/auth/login',
        follow_redirects=True
    )
    assert r.status_code == 200

    r = client.get(
        '/auth/logout',
        follow_redirects=True
    )
    assert r.status_code == 200

def test_base(client):
    r = client.get(
        '/',
        follow_redirects=True
    )
    assert r.status_code == 200