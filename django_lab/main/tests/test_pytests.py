

def test_index_view_status_code(client):
    """Test: main page returns 200 status"""
    response = client.get('/')
    assert response.status_code == 200


def test_list_view_status_code(client, product):
    """Test: list of goods returns 200 status"""

    response = client.get('/goods/')
    assert response.status_code == 200
    assert bytes(str(product), encoding='utf-8') in response.content


def test_delail_view_status_code(client, product):
    """Test: detail view returns 200 status"""

    response = client.get(f'/goods/{product.id}/')
    assert response.status_code == 200
    assert bytes(str(product), encoding='utf-8') in response.content


def test_add_view_status_code(client, user):
    """Test: add view returns 200 status"""
    user.profile.make_as_vendor()
    client.force_login(user)
    response = client.get('/goods/add/')
    assert response.status_code == 200


def test_edit_view_status_code(client, product, user):
    """Test: edit view returns 200 status"""
    user.profile.make_as_vendor()
    client.force_login(user)
    response = client.get(f'/goods/{product.id}/edit/')
    assert response.status_code == 200
