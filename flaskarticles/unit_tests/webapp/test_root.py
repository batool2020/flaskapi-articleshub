from flaskarticles.unit_tests.webapp import client


def testing_home(client):
    home = client.get("/")
    html = home.data.decode() #gets the response to that
    assert home.status_code == 200
    # assert "<a class='nav-item nav-link' href=\"/about\">About</a>  <meta charset='utf-8'> " in html
    # Spot check important text


def test_home_aliases(client):
    home = client.get("/")
    assert client.get("/home").data == home.data



def testing_About(client):
    about = client.get("/about")
    about_html = about.data.decode() #gets the response to that
    assert about.status_code == 200
    assert "About Page" in about_html


