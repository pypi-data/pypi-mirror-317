# coding=utf-8
from mewtools.wordpress import custom
from mewtools.wordpress import files
from mewtools.wordpress import posts
from mewtools.wordpress import category
from carehttp import Carehttp
import json


class WpApi:
    def __init__(
        self, wp_url, wp_user, api_key, wp_user_id=1, default_cat=1, verify=True
    ):
        if wp_url.endswith("/"):
            wp_url = wp_url[:-1]

        self.wp_root_url = wp_url
        self.wp_user = wp_user
        self.wp_user_id = wp_user_id
        self.api_url = f"{wp_url}/wp-json/wp/v2"
        self.api_key = api_key
        self.default_cat_id = default_cat
        self.verify = verify

    def get_media(self, media_id):
        return files.get_media(cls=self, media_id=media_id)

    def post_file(self, target_file, title):
        return files.post_file(cls=self, target_file=target_file, title=title)

    def post_normal_article(
        self, article, title, cat_id=1, feature_pic=None, post_type="posts"
    ):
        """
        Rest api post article
        :return:
        """
        return posts.post_normal_article(
            cls=self,
            article=article,
            title=title,
            cat_id=cat_id,
            feature_pic=feature_pic,
            post_type=post_type,
        )

    def submit(self, payload, status="publish", post_type="posts"):
        """
        Submit news to WP
        :param payload: Api data, Can be dict or Addict
        :param status: Post status, publish, pending, draft
        :param post_type: Default is posts, you can post videos, pages, custom post type
        :return: Json/False
        """
        return posts.submit(
            cls=self, payload=payload, status=status, post_type=post_type
        )

    def cat_create(self, cat_name, cat_parent_id=0):
        """
        Create a category
        :return: category id
        """
        return category.create(cls=self, cat_name=cat_name, cat_parent_id=cat_parent_id)

    def is_post_exist(self, check_param):
        """Check if already scraped"""
        return custom.check_exist_by_param(self, check_param)

    def get_user_by_email(self, email):
        """
        Get user by email
        :return: user id
        """
        api_url = f"{self.wp_root_url}/wp-json/wp/v2/users?search={email}"
        r = Carehttp(f"Get user {email}").get(
            url=api_url, auth=(self.wp_user, self.api_key), verify=False
        )
        if r.status_code == 200:
            if r.json():
                return r.json()[0]["id"]
            else:
                return False
        else:
            return False

    def get_user_by_id(self, user_id):
        """
        Get user by id
        :return: user id
        """
        api_url = f"{self.wp_root_url}/wp-json/wp/v2/users/{user_id}"
        r = Carehttp(f"Get user {user_id}").get(
            url=api_url, auth=(self.wp_user, self.api_key), verify=False
        )
        if r.status_code == 200:
            if r.json():
                return r.json()
            else:
                return False
        else:
            return False

    def quick_create_user_by_email(self, email):
        """
        Create a user by email
        :return: user id
        """

        def generate_secure_random_string(size=16):
            import random
            import string

            return "".join(random.choices(string.ascii_letters + string.digits, k=size))

        username = email.split("@")[0] + generate_secure_random_string(4)
        api_url = f"{self.wp_root_url}/wp-json/wp/v2/users"
        payload = {
            "email": email,
            "username": username,
            "password": generate_secure_random_string(),
            "roles": ["customer"],
        }
        headers = {"content-type": "Application/json"}
        r = Carehttp(f"Create user {email}").post(
            url=api_url,
            data=json.dumps(payload),
            headers=headers,
            auth=(self.wp_user, self.api_key),
            verify=False,
        )
        if r.status_code == 201:
            return r.json()["id"]
        else:
            return False
