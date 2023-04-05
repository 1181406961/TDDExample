import pytest
from api import app, TODORepo


@pytest.fixture(scope='class')
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_todos_post_api(client):
    item = {
        'task': 'learn python',
        'username': "zhangshan"
    }
    response = client.post(f'/todos', json=item)
    repo = TODORepo()
    assert response.status_code == 201
    assert len(repo.all()) == 4
    new_item = repo.retrieve('task', item['task'])
    assert new_item is not None
    assert new_item['username'] == item['username']
    assert new_item.get('id') == 4


