import os
import pyfiglet
import requests
from A1_Injection.SQL_injection_advanced.SQL_injection_advanced import run_script as sqli_scripts
from A1_Injection.Path_traversal.path_traversal import run_script as path_traversal_script
from A2_Broken_Authentication.Authentication_bypasses.authentication_bypass_chall import run_script as auth_bypass_script
from A2_Broken_Authentication.JWT_tokens.jwt_brut_force_secret import run_script as jwt_dict_attack
from A2_Broken_Authentication.Password_reset.security_question_brut_force import run_script as crack_security_question
from A4_XML_External_Entities_XXE.XXE.xxe_injection import run_script as xxe_injection
from A5_Broken_Access_Control.Insecure_Direct_Object_References.idor import run_script as idor
from A5_Broken_Access_Control.Missing_Function_Level_Access_Control.MFLAC import run_script as mflac
from A7_CrossSiteScripting_XSS.XSS.xss import run_script as xss
from A9_Vulnerable_Components.Vulnerable_Components.cve_2013_7285 import run_script as cve20137285
import logging

#Registre de challenges
class ChallRegistry:

    challenges = {}

    def __init__(self):
        ...

    def register(self, chall):
        self.challenges[chall.name] = chall

    @classmethod
    def categories(self):
        return set([chall.category for chall in self.challenges.values()])

    @classmethod
    def vulnerabilities(self):
        return set([chall.vuln_type for chall in self.challenges.values()])

    @classmethod
    def get_chall_by_name(self, name):
        # return list(filter(lambda x: x.name == name, self.challenges))[0]
        return self.challenges[name]

    @classmethod
    def get_chall_by_category(self, category):
        return list(filter(lambda x: x.category == category, self.challenges.values()))

    @classmethod
    def run_all_script(self):
        ...

#class d'initialisation d'un challenge qui sera enregister dans la class ChallRegistry
class Challenge:

    def __init__(self, name, category="cat", url="url",  proxy="127.0.0.1:8081", func=None, default_kwargs={}):
        self.name = name
        self.category = category
        self.url = url
        self.proxy = proxy
        self.script = func
        self.kwargs = default_kwargs

    def exec(self, cookie):
        return self.script(self.url, cookie, self.proxy)

    def getName(self):
        return self.name

    def isValid(self, url, cookie, proxy):
        ...

#Check de la validation d'un challenge (bug avec webgoat 8.0 car le serveur ne met pas correctement à jour les chall validés)
def checkValidChallenge(cookie, proxy):

    proxies = {
        'http': f'http://{proxy}',
        'https': f'https://{proxy}'
    }
    burp0_url = "http://127.0.0.1:8080/WebGoat/service/lessonmenu.mvc"
    burp0_headers = {"Cookie": cookie, "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
                     "X-Requested-With": "XMLHttpRequest", "Connection": "close", "Referer": "http://127.0.0.1:8080/WebGoat/start.mvc", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "X-PwnFox-Color": "red"}
    response = requests.get(burp0_url, headers=burp0_headers, proxies=proxies)
    response_json = response.json()
    print(response_json)
    completed_lessons = []

    for category in response_json:
        for lesson in category['children']:
            if lesson['complete'] == True:
                completed_lessons.append(lesson['name'])

    return completed_lessons

#Controlleur permettant de créer tous les challenges
def controlleur(registry):
    registry.register(Challenge(name="SQL injection (advanved)", category="(A1) Injection",
                      url=url+"/WebGoat/SqlInjectionAdvanced/challenge", func=sqli_scripts))
    registry.register(Challenge(name="Path traversal", category="(A1) Injection", url=url+"/WebGoat/PathTraversal/profile-upload",
                      func=path_traversal_script))
    registry.register(Challenge(name="Authentication bypass", category="(A2) Broken Authentication", url=url+"/WebGoat/auth-bypass/verify-account",
                      func=auth_bypass_script))
    registry.register(Challenge(name="JWT secret cracking", category="(A2) Broken Authentication", url=url+"/WebGoat/JWT/secret",
                                func=jwt_dict_attack))
    registry.register(Challenge(name="Cracking security question", category="(A2) Broken Authentication", url=url+"/WebGoat/PasswordReset/questions",
                                func=crack_security_question))
    registry.register(Challenge(name="XXE Injection", category="(A4) XML External Entities (XXE)", url=url+"/WebGoat/xxe/simple",
                                func=xxe_injection))
    registry.register(Challenge(name="Insecure Direct Object Reference", category="(A5) Broken Access Control", url=url,
                                func=idor))
    registry.register(Challenge(name="Missing Function Level Access Control", category="(A5) Broken Access Control", url=url+"/WebGoat/users",
                                func=mflac))
    registry.register(Challenge(name="Cross Site Scripting", category="(A7) Cross Site Scripting (XSS)", url=url+"/WebGoat/CrossSiteScripting/phone-home-xss",
                                func=xss))
    registry.register(Challenge(name="CVE-2013-7285", category="(A9) Vulnerable Components", url=url+"/WebGoat/VulnerableComponents/attack1",
                                func=cve20137285))
    return registry


def line():
    print('--------------------------------------')

#Affichage du menu
def display_menu(registry,cookie):
    challenges = dict(enumerate(sorted(registry.categories())))
    print("Choisissez une catégorie :")
    line()
    max_key = 0
    all_chall=[]
    for key, value in challenges.items():
        print(f"| {key} - {value}")
        for chall in registry.get_chall_by_category(value):
            all_chall.append(chall.getName())
        if key > max_key:
            max_key = key
    print(f"| {max_key + 1} - Executer tous les scripts")
    print(f"| {max_key + 2} - Quitter")
    line()
    while 1:
        try:
            choice = int(input("Entrez le numéro de votre choix : "))
            if choice == max_key + 1:
                print(
                    f"\nVous avez choisi d'executer tous les scripts :\n")
                for chall in all_chall:
                    print(
                        f'Execution : {chall}\n')
                    registry.get_chall_by_name(
                        chall).exec(cookie)
                print('\n')
                exit(0)
            elif choice == max_key + 2:
                exit(0)
            chall = challenges.get(choice, None)
            if not chall:
                raise ValueError()
            return chall
        except ValueError:
            print(
                '\nChoix de numéro non valide, veuillez réessayer.\n')

#affichage du header
def display_header():
    ascii_banner = pyfiglet.figlet_format("WebGoat Solver")
    print(ascii_banner)


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    cookie = input("Veuillez entrer un cookie authentifié : ")
    # url=input("Veuillez entrer l'adresse et le port du docker tournant webgoat : ")
    # cookie="JSESSIONID=o8Z7vtOs_Hmupm4OhZRHTMdmTnVrxgC8iAI9xDo5"
    url = "http://127.0.0.1:8080"
    registry = ChallRegistry()
    controlleur(registry)
    logging.basicConfig(format='%(message)s',level=logging.INFO)
    while 1:
        clear_console()
        #print(checkValidChallenge(cookie, '127.0.0.1:8080'))
        display_header()
        selected_category = display_menu(registry,cookie)
        print(f"\nVous avez choisi : {selected_category}\n")
        back_to_menu = 1
        list_chall = []
        while back_to_menu:
            i = 0
            print(
                f'Voici la liste des challenges pour la catégorie {selected_category} :')
            line()
            for chall in registry.get_chall_by_category(selected_category):
                i += 1
                print(f'| {i} - {chall.getName()}')
                list_chall.append(chall.getName())

            print(f'| {i+1} - Executer tous les scripts')
            print(f'| {i+2} - Retour')
            line()
            try:
                choice = int(
                    input("Veuillez choisir un challenge à résoudre : "))

                if choice > i+2 or choice <= 0:
                    raise ValueError

                if choice == i+2:
                    back_to_menu = 0
                    break

                if choice == i+1:
                    print(
                        f"\nVous avez choisi d'executer tous les scripts :\n")
                    for chall in registry.get_chall_by_category(selected_category):
                        print(
                            f'Execution : {chall.getName()}\n')
                        registry.get_chall_by_name(
                            chall.getName()).exec(cookie)
                    print('\n')

                if choice <= i:
                    print(
                        f"\nVous avez choisi d'executer : {registry.get_chall_by_name(list_chall[choice-1]).getName()}\n")
                    registry.get_chall_by_name(registry.get_chall_by_name(
                        list_chall[choice-1]).getName()).exec(cookie)

            except ValueError:
                print(
                    '\nChoix de numéro non valide, veuillez réessayer.\n')
