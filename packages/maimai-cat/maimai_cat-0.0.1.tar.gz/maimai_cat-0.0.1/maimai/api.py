import requests
import json


class Params:
    base_url = "https://maimai.cn/api/ent"  # Base API URL
    channel = "www"
    version = "1.0.0"

    search_data = {
            "search": {
                "cities": "",
                "companyscope": 0,
                "degrees": "",
                "is_direct_chat": 0,
                "positions": "",
                "professions": "",
                "provinces": "",
                "query": "LLM",
                "schools": "",
                "sortby": "0",
                "worktimes": "",
                "gender": "",
                "age": "",
                "salary": "",
                "region_scope": "",
                "ht_provinces": "",
                "ht_cities": "",
                "query_relation": 0,
                "major": "",
                "only_bachelor_degree": None,
                "min_only_bachelor_degree": None,
                "max_only_bachelor_degree": None,
                "graduation_year": None,
                "dynamic_valid_days": 0,
                "has_social_relation": "",
                "company_interaction": "",
                "open_job_preferences": 0,
                "uploaded_resume": 0,
                "delivered_or_can_chat": 0,
                "exclude_recently_viewed": 0,
                "recently_untouched_valid_days": 0,
                "remark": {
                    "remarked": 0,
                    "content": ""
                },
                "in_project": 0,
                "is_friend": 0,
                "paginationParam": {
                    "page": 1,
                    "size": 30
                },
                "page": 3,
                "size": 30,
                "total": 1000,
                "total_match": 2,
                # "sid": "pc1729696331481240195775",
                # "sessionid": "pc1734190526200240195775",
                "highlight_exp": 1,
                "data_version": "4.1",
                "allcompanies": "",
                "search_query": "LLM",
                "is_985": 0,
                "is_211": 0,
                "is_top_500": 0,
                "is_world_500": 1,
                "mapping_pfs": "",
                "usePfUpdate": True
            }
        }

    # search_data  = {"search":{"cities":"","companyscope":0,"degrees":"","is_direct_chat":0,"positions":"","professions":"","provinces":"","query":"吕唐杰","schools":"","sortby":9,"worktimes":"","gender":"","age":"","salary":"","region_scope":"","ht_provinces":"","ht_cities":"","query_relation":0,"major":"","only_bachelor_degree":"","min_only_bachelor_degree":"","max_only_bachelor_degree":"","graduation_year":"","dynamic_valid_days":0,"has_social_relation":"","company_interaction":"","uploaded_resume":0,"delivered_or_can_chat":0,"job_hunting_status":[],"exclude_recently_viewed":0,"recently_untouched_valid_days":0,"remark":{"remarked":0,"content":""},"in_project":0,"is_friend":0,"page":0,"size":30,"total":2,"total_match":2,"sid":"pc1734190526200240195775","sessionid":"pc1734190526200240195775","highlight_exp":1,"data_version":"4.1","allcompanies":"","search_query":"吕唐杰","is_985":0,"is_211":0,"is_top_500":0,"is_world_500":0,"mapping_pfs":""}}



class LoginManager:
    def __init__(self, cookies_file="cookies.json"):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        self.cookies_file = cookies_file
        self.session = self._get_session()

    def _load_cookies(self):
        """
        Load cookies from a JSON file and ensure the correct format.

        :param file_path: Path to the cookies.json file
        :return: Dictionary of cookies
        """
        cookies_data = {}
        try:
            with open(self.cookies_file, 'r') as file:
                cookies_data = json.load(file)
        except FileNotFoundError:
            print("Cookies file not found.", self.cookies_file)

        finally:
            return cookies_data

    def _get_session(self):
        """
        Load cookies from a JSON file and return a requests session with the cookies.
        :param cookie_file_path:
        :return:
        """
        # 加载cookies
        cookies = self._load_cookies()

        # 创建session对象，并加载cookies
        session = requests.Session()
        # 如果cookies为空，则提示用户提供有效的cookies.json文件
        if not cookies:
            print("No cookies found. Please provide a valid cookies.json file.")
            return
        # 设置cookies
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        return session

class RequestManager(LoginManager):

    def _get_request(self, url, params):
        """
        Perform a GET request with the specified URL, parameters, and cookies.

        :param url: The full URL to send the request to
        :param params: Dictionary of query parameters
        :return: Parsed JSON response
        """
        try:
            response = self.session.get(url, params=params, headers=self.headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def _post_request(self, url, params):
        """
        Perform a POST request with the specified URL, parameters, and cookies.

        :param url: The full URL to send the request to
        :param params: Dictionary of form parameters
        :return: Parsed JSON response
        """
        try:
            response = self.session.post(url, data=params, headers=self.headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def _post_request_json(self, url, data):
        """
        Perform a POST request with the specified URL, parameters, and cookies.
        :param url:
        :param data:
        :return:
        """
        try:
            response = self.session.post(url, json=data, headers=self.headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

class Utility:
    def pretty_print(self, data):
        """
        Pretty print the JSON response.

        :param data: JSON data to print
        """
        print(json.dumps(data, ensure_ascii=False, indent=4))

class Group(RequestManager,Params):
    def create(self, name):
        """
        Create a new group with the specified name.

        :param name: Name of the group to create
        :return: Response from the API call
        """
        url = f"{self.base_url}/group/add"
        params = {
            "channel": self.channel,
            "name": name,
            "version": self.version
        }
        return self._post_request(url, params)

    def read(self, page=0, size=100):
        """
        Read the list of groups with pagination.

        :param page: Page number to fetch (default is 0)
        :param size: Number of groups per page (default is 100)
        :return: Response from the API call
        """
        url = f"{self.base_url}/group/list"
        params = {
            "channel": self.channel,
            "page": page,
            "size": size,
            "version": self.version
        }
        return self._get_request(url, params)

    def delete(self, group_id):
        """
        Delete a group by its ID.

        :param group_id: ID of the group to delete
        :return: Response from the API call
        """
        url = f"{self.base_url}/group/delete"
        params = {
            "channel": self.channel,
            "group_id": group_id,
            "version": self.version
        }
        return self._post_request(url, params)


    def add_user_to_group(self, uid, user_group_ids):
        """
        Add a user to specified groups.

        :param uid: The user ID to add to the groups
        :param user_group_ids: List of group IDs to which the user will be added
        :return: Response from the API call
        """
        url = f"{self.base_url}/talent_pool/group_talent/modify"
        data = {
            "user_group_ids": user_group_ids,
            "mbr_group_ids": []
        }
        params = {
            "channel": self.channel,
            "data": json.dumps(data),
            "uid2": uid,
            "version": self.version
        }
        # return self._post_request(url, params)

        return self._post_request_json(url, params)

    def star(self,uid):
        url = "https://maimai.cn/api/ent/talent/pool/v3/special_attention"
        params = {
            "channel": self.channel,
            "to_uid":  uid,
            "version": self.version
        }

        return self._get_request(url, params)

    def unstar(self,uid):
        url = "https://maimai.cn/api/ent/talent/pool/v3/cancel_special_attention"
        params = {
            "channel": self.channel,
            "to_uid": uid,
            "version": self.version
        }

        return self._get_request(url, params)




class User(RequestManager,Params):
    def read(self, to_uid):
        """
        Read basic information about a user by their UID.

        :param to_uid: UID of the user to read information for
        :return: Response from the API call
        """
        url = f"{self.base_url}/talent/basic"
        params = {
            "channel": self.channel,
            "data_version": "3.1",
            "need_ai_info": 0,
            "resume_project_id": "",
            "show_tip": 0,
            "to_uid": to_uid,
            "trackable_token": "",
            "version": self.version
        }
        return self._get_request(url, params)



from colorama import init, Fore, Style

class Search(RequestManager,Params):
    # 初始化 colorama
    init(autoreset=True)

    def print_profile(self,profile):
        print("-"*100)
        print(Fore.GREEN + f"姓名: {profile['name']} "
                           f"({profile['byname']}|"
                           f"{profile['gender_str']}|"
                           f"{profile['province']}-{profile['city']}|"
                           f"{profile['active_state']})")
        print(Fore.MAGENTA + f"公司: {profile['company']} - 职位: {profile['position']} - 工作时间: {profile['work_time']}")
        print(Fore.BLUE + f"学历: {profile['sdegree']} - 专业: {profile['major']}")

        print(Fore.GREEN + "教育背景:")
        for edu in profile['edu']:
            print(Fore.BLUE + f"- {edu['sdegree']} - {edu['school']} ({edu['department']}) - ({edu['start_date_ym']} 至 {edu['end_date_ym']})")

        print(Fore.GREEN + "工作经历:")
        for exp in profile['exp']:
            print(Fore.MAGENTA + f"- {exp['company']} - {exp['position']} - {exp['v']} ({exp['worktime']})")
            print(f"{exp['description'][:50]}")

        print(Fore.CYAN + "个人标签:")
        print(Fore.CYAN + ','.join(profile['tag_list'][:10]))


    def extract_search_result(self,json_data):
        total = json_data.get("data").get("total")
        print(Fore.RED + f"Total Page : {total}")
        person_list = json_data.get("data").get("list")

        for person in person_list:
            self.print_profile(person)

    def keyword(self, keyword,page = 0):
        url = "https://maimai.cn/api/ent/v3/search/basic?channel=www&is_mapping_pfs=1&version=1.0.0"
        data = {"search": {"query": keyword, "page": page, }}
        print(data)

        return self._post_request_json(url, data)

class MaimaiAPI(Utility):
    def connect(self):
        self.group = Group()
        self.search = Search()
        self.user = User()

        return self



