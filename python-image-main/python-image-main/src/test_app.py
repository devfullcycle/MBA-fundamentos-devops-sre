import pytest
from flask import Flask
from app import app 

@pytest.fixture
def client():
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Seja bem-vindo!'

def test_get_times(client):
    response = client.get('/times')
    assert response.status_code == 200
    assert response.json == []

def test_create_time(client):
    response = client.post('/times', json={"nome": "Time A"})
    assert response.status_code == 200
    assert response.json['message'] == 'Time adicionado com sucesso!'

    response = client.get('/times')
    assert response.json == [{"nome": "Time A"}]

def test_get_campeonatos(client):
    response = client.get('/campeonatos')
    assert response.status_code == 200
    assert response.json == []

def test_create_campeonato(client):
    response = client.post('/campeonatos', json={"nome": "Campeonato A"})
    assert response.status_code == 200
    assert response.json['message'] == 'Campeonato adicionado com sucesso!'

    response = client.get('/campeonatos')
    assert response.json == [{"nome": "Campeonato A"}]

def test_404_error(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert response.json['error'] == 'Página não encontrada'

if __name__ == '__main__':
    pytest.main()
