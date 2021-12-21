

# getting all the posts 
def test_get_all(authorized_client,create_posts):
    res = authorized_client.get("/api/v1/posts/")
    print(res.json())
    assert res.status_code == 200 