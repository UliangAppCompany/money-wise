import pytest 

@pytest.mark.django_db
@pytest.mark.usefixtures("register_new_user", "validate_new_user") 
def test_click_submit_and_continue_button_fires_api_post_request(driver): 
    pass
     