def test_get_all_posts(auth_client, test_posts):
    res = auth_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200
     