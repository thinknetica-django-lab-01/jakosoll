

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


def test_add_view_status_code(vendor_client):
    """Test: add view returns 200 status"""
    response = vendor_client.get('/goods/add/')
    assert response.status_code == 200


def test_vendor_can_add_product(vendor_client, category):
    response = vendor_client.post(
        '/goods/add/',
        data={
            "name": "test_name",
            "description": "test_discription",
            "category": category.id,
            "price": 200,
        }
    )
    assert b'test_name' in response.content


def test_edit_view_status_code(vendor_client, product):
    """Test: edit view returns 200 status"""
    response = vendor_client.get(f'/goods/{product.id}/edit/')
    assert response.status_code == 200


def test_vendor_can_edit_product(vendor_client, product):
    """Test: vendor can edit product"""
    response = vendor_client.post(
        f'/goods/{product.id}/edit/',
        data={
            "name": "new_name",
            # "description": "test_discription",
            # "category": product.category.id,
            # "price": 200,
        }
    )
    assert b'new_name' in response.content
