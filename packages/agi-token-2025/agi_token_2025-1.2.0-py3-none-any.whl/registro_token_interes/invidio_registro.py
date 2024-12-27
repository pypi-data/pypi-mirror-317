import requests
import os
import re
import time
import hashlib
import json
import random
import string
import uuid
from bs4 import BeautifulSoup
import requests
import json


def generar_nombres():
    """Genera un nombre completo triplicando el nombre y apellido, junto con un número aleatorio de 3 dígitos."""
    nombres = ["Juan", "Pedro", "Maria", "Ana", "Luis", "Sofia", "Diego", "Laura", "Javier", "Isabel",
               "Pablo", "Marta", "David", "Elena", "Sergio", "Irene", "Daniel", "Alicia", "Carlos", "Sandra",
               "Antonio", "Lucia", "Miguel", "Sara", "Jose", "Cristina", "Alberto", "Blanca", "Alejandro", "Marta",
               "Francisco", "Esther", "Roberto", "Silvia", "Manuel", "Patricia", "Marcos", "Victoria", "Fernando", "Rosa",
               # Nombres comunes de EE.UU.
               "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas",
               "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
               "Kenneth", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan",
               "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon",
               "Benjamin", "Samuel", "Frank", "Gregory", "Raymond", "Alexander", "Patrick", "Jack", "Dennis", "Jerry",
               "Tyler", "Aaron", "Henry", "Douglas", "Jose", "Peter", "Adam", "Zachary", "Nathan", "Walter",
               "Kyle", "Harold", "Carl", "Arthur", "Gerald", "Roger", "Keith", "Jeremy", "Terry", "Lawrence",
               "Sean", "Christian", "Ethan", "Austin", "Joe", "Jordan", "Albert", "Jesse", "Willie", "Billy",
                "Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Alonso", "Diaz",
                 "Martin", "Ruiz", "Hernandez", "Jimenez", "Torres", "Moreno", "Gomez", "Romero", "Alvarez", "Vazquez",
                 "Gil", "Lopez", "Ramirez", "Santos", "Castro", "Suarez", "Munoz", "Gomez", "Gonzalez", "Navarro",
                 "Dominguez", "Lopez", "Rodriguez", "Sanchez", "Perez", "Garcia", "Gonzalez", "Martinez", "Fernandez", "Lopez",
                 # Apellidos comunes de EE.UU.
                 "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                 "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                 "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
                 "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
                 "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
                 "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
                 "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
                 "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ward", "Cox", "Diaz", "Richardson", "Wood"]


    nombre = random.choice(nombres)
    nombre_completo = f"{nombre}"
    return nombre_completo


def update_user_full_name(token, first_name):

    # Configurar el endpoint y los headers
    url = "https://pro-api.invideo.io/graphql"
    headers = {
        "Host": "pro-api.invideo.io",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "accept": "*/*",
        "content-type": "application/json",
        "Origin": "https://ai.invideo.io",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ai.invideo.io/",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    # Configurar los datos del body
    data = {
        "operationName": "UpdateUserFullName",
        "variables": {
            "first_name": first_name,
            "last_name": " ",
        },
        "query": """mutation UpdateUserFullName($first_name: String!, $last_name: String) {
          updateFullName(firstName: $first_name, lastName: $last_name) {
            id
            firstName
            lastName
            __typename
          }
        }"""
    }

    # Hacer la solicitud POST
    response = requests.post(url, headers=headers, json=data)

    # Verificar la respuesta
    if response.status_code == 200:
        print("Saltando pasos.", end="\rSaltando pasos.")
        #print("ACCESS_TOKEN", os.environ.get("ACCESS_TOKEN"))
        #print(first_name)
        # Ejemplo de uso interactivo
        token = os.environ.get("ACCESS_TOKEN")

        # Llamar a la función
        resultado = upsert_workspace(token, first_name)

        return response.json()  # Devolver la respuesta JSON
    else:
        return {"error": response.status_code, "message": response.text}  # Devolver error


def upsert_workspace(token, workspace_name):
    """
    Crea o actualiza un workspace mediante la API de InVideo.

    Parámetros:
        token (str): Token de autorización Bearer.
        workspace_name (str): Nombre del workspace a crear o actualizar.

    Retorno:
        dict: Respuesta de la API en formato JSON.
    """
    # Configurar el endpoint y los headers
    url = "https://pro-api.invideo.io/graphql"
    headers = {
        "Host": "pro-api.invideo.io",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "accept": "*/*",
        "content-type": "application/json",
        "Origin": "https://ai.invideo.io",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ai.invideo.io/",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    # Configurar los datos del body
    data = {
        "operationName": "UpsertWorkspace",
        "variables": {
            "name": workspace_name,
        },
        "query": """mutation UpsertWorkspace($name: String!) {
          upsertWorkspace(name: $name) {
            id
            name
            displayHandle
            handle
            createdBy
            lastViewedAt
            __typename
          }
        }"""
    }

    # Hacer la solicitud POST
    response = requests.post(url, headers=headers, json=data)

    # Verificar la respuesta
    if response.status_code == 200:
        print("Saltando pasos..", end="\rSaltando pasos..")
        #print("ACCESS_TOKEN", os.environ.get("ACCESS_TOKEN"))

        # Ejemplo de uso interactivo
        token = os.environ.get("ACCESS_TOKEN")

        # Llamar a la función
        resultado = get_current_user(token)

        return response.json()  # Devolver la respuesta JSON
    else:
        return {"error": response.status_code, "message": response.text}  # Devolver error


def get_current_user(token):
    """
    Obtiene información del usuario actual mediante la API de InVideo.

    Parámetros:
        token (str): Token de autorización Bearer.

    Retorno:
        dict: Respuesta de la API en formato JSON.
    """
    # Configurar el endpoint y los headers
    url = "https://pro-api.invideo.io/graphql"
    headers = {
        "Host": "pro-api.invideo.io",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "accept": "*/*",
        "content-type": "application/json",
        "Origin": "https://ai.invideo.io",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ai.invideo.io/",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    # Configurar los datos del body
    data = {
        "operationName": "CurrentUser",
        "variables": {},
        "query": """query CurrentUser {
          user {
            id
            emailId
            firstName
            lastName
            profilePic
            birthDate
            age
            provider
            tags
            isArchived
            archivedAt
            mobileNumber
            daysSinceFirstUse
            daysSinceFifthUse
            sessionOneWeek
            sessionFiveWeek
            signupWeek
            applicationInvite {
              id
              waitlistNumber
              state
              __typename
            }
            workspaces {
              id
              name
              handle
              displayHandle
              createdBy
              isArchived
              archivedAt
              flags {
                betaFeatures
                alphaFeatures
                multiplayerCursor
                exportVisibility
                eligibleForAlpha
                __typename
              }
              features {
                id
                workspaceId
                name
                slug
                description
                stage
                status
                workspaceId
                __typename
              }
              createdAt
              bucket
              lastViewedAt
              copilotWorkflowSettings {
                favorites
                recents
                __typename
              }
              __typename
            }
            campaign(campaignIdentifier: "Waitlist") {
              id
              state
              __typename
            }
            userAttribution {
              lastAdClickId
              lastAdClickIds {
                gclid
                fbclid
                msclkid
                ttclid
                wbraid
                gbraid
                irclickid
                twclid
                __typename
              }
              lastAdSource
              __typename
            }
            referralCode
            username
            credits {
              amount
              expiresAt
              __typename
            }
            influencerId
            joinedAt
            undismissedWaitlistFeatures {
              id
              name
              __typename
            }
            countryCode
            __typename
          }
        }"""
    }

    # Hacer la solicitud POST
    response = requests.post(url, headers=headers, json=data)

    # Verificar la respuesta
    if response.status_code == 200:
        print("Saltando pasos...", end="\rSaltando pasos...")
        #print("ACCESS_TOKEN", os.environ.get("ACCESS_TOKEN"))

        # Ejemplo de uso interactivo
        token = os.environ.get("ACCESS_TOKEN")
        # Llamar a la función
        resultado = get_workspace_owner(token)

        return response.json()  # Devolver la respuesta JSON
    else:
        return {"error": response.status_code, "message": response.text}  # Devolver error



def get_workspace_owner(token):
    """
    Obtiene información del propietario del espacio de trabajo mediante la API de InVideo.

    Parámetros:
        token (str): Token de autorización Bearer.

    Retorno:
        dict: Respuesta de la API en formato JSON.
    """
    # Configurar el endpoint y los headers
    url = "https://pro-api.invideo.io/graphql"
    headers = {
        "Host": "pro-api.invideo.io",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "accept": "*/*",
        "content-type": "application/json",
        "Origin": "https://ai.invideo.io",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ai.invideo.io/",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    # Configurar los datos del body
    data = {
        "operationName": "WorkspaceOwner",
        "variables": {},
        "query": """query WorkspaceOwner {
          workspaceOwner {
            id
            name
            handle
            displayHandle
            __typename
          }
        }"""
    }

    # Hacer la solicitud POST
    response = requests.post(url, headers=headers, json=data)

    # Verificar la respuesta
    if response.status_code == 200:
        print("Saltando pasos.", end="\rSaltando pasos.")
        #print("ACCESS_TOKEN", os.environ.get("ACCESS_TOKEN"))
        # Ejemplo de uso interactivo
        token = os.environ.get("ACCESS_TOKEN")
        # Llamar a la función
        campaign_id, question_id1, question_id2 = get_campaign_info(token)

        return response.json()  # Devolver la respuesta JSON
    else:
        return {"error": response.status_code, "message": response.text}  # Devolver error




def extract_and_return_ids(response_text):
    try:
        response_data = json.loads(response_text)

        campaign_id = None
        question_ids = []

        # Obtener Campaign ID
        if 'data' in response_data:
            campaign_id = response_data['data'].get('id', None)

            # Obtener Question IDs
            questions = response_data['data'].get('questions', [])
            for question in questions:
                question_id = question.get('id', None)
                if question_id:
                    question_ids.append(question_id)

        # Devolver Campaign ID y las Question IDs separadas
        return (campaign_id, *question_ids)

    except json.JSONDecodeError:
        print("Error al analizar el JSON.")
        return None

def get_campaign_info(token):

    # Configurar el endpoint y los headers
    url = f"https://pro-api.invideo.io/api/campaign?campaign_identifier=Waitlist"
    headers = {
        "Host": "pro-api.invideo.io",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "Windows",
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://ai.invideo.io",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ai.invideo.io/",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }

    # Hacer la solicitud GET
    response = requests.get(url, headers=headers)

    # Verificar la respuesta
    if response.status_code == 200:
        # Llamar a la función
        print("Saltando pasos..", end="\rSaltando pasos..")
        campaign_id, question_id1, question_id2 = extract_and_return_ids(response.text)

        # Imprimir las IDs para verificar
        #print(f"Campaign ID: {campaign_id}")
        #print(f"Question 1 ID: {question_id1}")
        #print(f"Question 2 ID: {question_id2}")

        #print("ACCESS_TOKEN", os.environ.get("ACCESS_TOKEN"))

        # Ejemplo de uso interactivo
        oken = os.environ.get("ACCESS_TOKEN")

        send_request(token, campaign_id, question_id1, question_id2)


        return campaign_id, question_id1, question_id2
    else:
        return {"error": response.status_code, "message": response.text}, None, None  # Devolver error


def send_request(authorization_token, campaign_id, question_id1, question_id2):
    url = f"https://pro-api.invideo.io/api/campaign/{campaign_id}/user_complete"
    headers = {
        "Authorization": f"Bearer {authorization_token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://ai.invideo.io",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ai.invideo.io/"
    }
    data = {
        "answers": [
            {
                "question_id": question_id1,
                "answer": {
                    "identifier": "google_search",
                    "name": "Google search",
                    "option": "D",
                    "type": "CHOICE"
                }
            },
            {
                "question_id": question_id2,
                "answer": {
                    "identifier": "other",
                    "name": "Other",
                    "option": "F",
                    "type": "CHOICE_TEXT",
                    "text": "GOOGLE"
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    print("FINISHED", end="\rFINISHED")






def extract_code(verification_code):

    # Analizar el HTML
    soup = BeautifulSoup(verification_code, 'html.parser')

    # Encuentra el título de la página
    title = soup.find('title').get_text()

    # Divide el título por el guion y toma el primer elemento
    number_text = title.split('-')[0].strip()

    if number_text:

        # Convierte el texto a un número entero
        try:
            number = int(number_text)
            return number
        except ValueError:
            print("No se pudo convertir el texto a un número entero.")
            return None
    else:
        print("No se encontró el elemento <span> con id 'email_ch_text'.")
        return None

def generar_nombre_completo():
    """Genera un nombre completo triplicando el nombre y apellido, junto con un número aleatorio de 3 dígitos."""
    nombres = ["Juan", "Pedro", "Maria", "Ana", "Luis", "Sofia", "Diego", "Laura", "Javier", "Isabel",
               "Pablo", "Marta", "David", "Elena", "Sergio", "Irene", "Daniel", "Alicia", "Carlos", "Sandra",
               "Antonio", "Lucia", "Miguel", "Sara", "Jose", "Cristina", "Alberto", "Blanca", "Alejandro", "Marta",
               "Francisco", "Esther", "Roberto", "Silvia", "Manuel", "Patricia", "Marcos", "Victoria", "Fernando", "Rosa",
               # Nombres comunes de EE.UU.
               "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas",
               "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
               "Kenneth", "Kevin", "Brian", "George", "Edward", "Ronald", "Timothy", "Jason", "Jeffrey", "Ryan",
               "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon",
               "Benjamin", "Samuel", "Frank", "Gregory", "Raymond", "Alexander", "Patrick", "Jack", "Dennis", "Jerry",
               "Tyler", "Aaron", "Henry", "Douglas", "Jose", "Peter", "Adam", "Zachary", "Nathan", "Walter",
               "Kyle", "Harold", "Carl", "Arthur", "Gerald", "Roger", "Keith", "Jeremy", "Terry", "Lawrence",
               "Sean", "Christian", "Ethan", "Austin", "Joe", "Jordan", "Albert", "Jesse", "Willie", "Billy"]

    apellidos = ["Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez", "Alonso", "Diaz",
                 "Martin", "Ruiz", "Hernandez", "Jimenez", "Torres", "Moreno", "Gomez", "Romero", "Alvarez", "Vazquez",
                 "Gil", "Lopez", "Ramirez", "Santos", "Castro", "Suarez", "Munoz", "Gomez", "Gonzalez", "Navarro",
                 "Dominguez", "Lopez", "Rodriguez", "Sanchez", "Perez", "Garcia", "Gonzalez", "Martinez", "Fernandez", "Lopez",
                 # Apellidos comunes de EE.UU.
                 "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                 "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                 "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
                 "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
                 "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
                 "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
                 "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
                 "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ward", "Cox", "Diaz", "Richardson", "Wood"]


    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    numero = random.randint(100000, 999999)

    nombre_completo = f"{nombre}_{apellido}_{numero}"
    return nombre_completo


def enviar_formulario():
    url = 'https://email-fake.com/'

    datos = {'campo_correo': 'ejemplo@dominio.com'}

    """Envía una solicitud POST a un formulario web."""
    response = requests.post(url, data=datos)
    return response.text

def extraer_dominios(response_text):
    """Extrae dominios de un texto utilizando expresiones regulares."""
    dominios = re.findall(r'id="([^"]+\.[^"]+)"', response_text)
    return dominios

def obtener_sitio_web_aleatorio(response_text):
    """Obtiene un sitio web aleatorio de los dominios extraídos."""
    dominios = extraer_dominios(response_text)
    sitio_web_aleatorio = random.choice(dominios)
    return sitio_web_aleatorio


def verify_session(email, code):
    uuids = os.environ.get("UUIDS")
    url = "https://pro-api.invideo.io/api/session/verify"
    headers = {
        "Host": "pro-api.invideo.io",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "\"Windows\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://ai.invideo.io",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ai.invideo.io/",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }
    data = {
        "email": email,
        "code": code,
        "rudderstack_anonymous_id": uuids,
        "meta_properties": {
            "page": {
                "name": "AuthPage",
                "url": "https://ai.invideo.io/signup",
                "path": "/signup",
                "source": "https://ai.invideo.io/signup"
            },
            "app": {
                "platform": "web",
                "source": "ivpro",
                "name": "iv-pro-web",
                "version": "7776980"
            },
            "browser": {
                "name": "Chrome",
                "version": "131.0.0.0"
            },
            "os": {
                "name": "Windows",
                "version": "10"
            },
            "device_info": {
                "tier": "MEDIUM",
                "cpu": "12",
                "ram": "8",
                "vendor": "na",
                "model": "na"
            },
            "screen": {
                "width": 1440,
                "height": 900,
                "resolution": "1440x900",
                "aspect_ratio": 1.6,
                "inner_height": 765,
                "inner_width": 1440,
                "inner_resolution": "1440x765",
                "inner_aspect_ratio": 1.88,
                "density": 2
            },
            "gpu_info": {
                "device": "amd radeon pro 555x",
                "renderer": "ANGLE (AMD, Radeon Pro 555X (0x000067EF) Direct3D11 vs_5_0 ps_5_0, D3D11)",
                "fps": "42",
                "tier": "MEDIUM"
            },
            "user_age_in_days": -1,
            "attribution": {
                "medium": "direct",
                "source": "direct",
                "campaign": "direct",
                "content": "na"
            }
        },
        "raw_attribution": {
            "medium": "direct",
            "source": "direct",
            "campaign": "direct",
            "content": "na",
            "utm_source": None,
            "utm_medium": None,
            "utm_campaign": None,
            "utm_term": None,
            "utm_content": None,
            "referrer": None,
            "domain_referrer": None,
            "matchtype": None,
            "creative": None,
            "placement": None,
            "campaign_id": None,
            "adset_id": None,
            "ad_id": None,
            "ref": None,
            "msclkid": None,
            "fbclid": None,
            "gclid": None,
            "ttclid": None,
            "gbraid": None,
            "wbraid": None,
            "user_referral": None,
            "irclickid": None,
            "mpid": None,
            "twclid": None,
            "fbp": None
        }
    }

    response = requests.post(url, headers=headers, json=data)
    #print(f"Response verify Code: {response.text}")
    if response.status_code == 200:
        try:
            response_data = response.json()
            refresh_token = response_data["data"]["refresh_token"]
            access_token = response_data["data"]["access_token"]
            return refresh_token, access_token
        except (KeyError, ValueError) as e:
            print("Error al procesar la respuesta:", e)
            return None, None
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None, None


COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Accept-Encoding': 'gzip, deflate'
}

def extract_verification_code(html_content):
    """
    Extrae el código de verificación de un contenido HTML dado.

    Args:
        html_content (str): El texto HTML que contiene el código de verificación.

    Returns:
        str: El código de verificación como una cadena, o None si no se encuentra.
    """
    pattern = r"Your verification code is ：(\d+)"
    match = re.search(pattern, html_content)
    if match:
        return match.group(1)  # Retorna solo el número
    return None  # Retorna None si no encuentra el código

def delete_temp_mail(username_email, dominios_dropdown, extracted_string):
    """Borra el correo temporal especificado."""
    EMAIL_FAKE_URL = 'https://email-fake.com/'
    url = f"{EMAIL_FAKE_URL}/del_mail.php"

    headers = {
        'Host': 'email-fake.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://email-fake.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Cookie': f'embx=%5B%22{username_email}%40{dominios_dropdown}%22%2C',
    }

    data = f'delll={extracted_string}'

    response = requests.post(url, headers=headers, data=data)

    if "Message deleted successfully" in response.text:
        #print("Temporary mail deleted...")
        return True
    else:
        print("Error deleting temporary email...")
        return False

def get_verification_code(username_email, dominios_dropdown):
    """Obtiene el código de verificación del correo y el identificador."""
    EMAIL_FAKE_URL = 'https://email-fake.com/'
    url = f"{EMAIL_FAKE_URL}/"

    headers = {
        'Host': 'email-fake.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        **COMMON_HEADERS,
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'Cookie': f'surl={dominios_dropdown}%2F{username_email}',
    }

    response = requests.get(url, headers=headers)

    #print(response.text)

    verification_code = extract_code(response.text)

    #verification_code = response.text

    # Utiliza una expresión regular para encontrar el identificador largo
    identifier_match = re.search(r'delll:\s*"([a-zA-Z0-9]+)"', response.text)
    #return identifier_match, verification_code

    # Extrae y retorna los valores si fueron encontrados
    if identifier_match:
        identifier = identifier_match.group(1)
        return verification_code, identifier
    else:
        return None, None, None

def create_new_user(email):
    correo = os.environ.get("USER_EMAIL_PIC")
    #password = os.environ.get("PASS_WORD_PIC")
    #print(correo)
    #print(password)
    uuids = str(uuid.uuid4())
    os.environ["UUIDS"] = uuids


    name, domain = correo.split('@')

    url = "https://pro-api.invideo.io/api/users/new"
    headers = {
        "Host": "pro-api.invideo.io",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": "\"Windows\"",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "Origin": "https://ai.invideo.io",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://ai.invideo.io/",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    }
    data = {
        "email_id": email,
        "token": None,
        "rudderstack_anonymous_id": uuids,
        "meta_properties": {
            "page": {
                "name": "AuthPage",
                "url": "https://ai.invideo.io/signup",
                "path": "/signup",
                "source": "https://ai.invideo.io/signup"
            },
            "app": {
                "platform": "web",
                "source": "ivpro",
                "name": "iv-pro-web",
                "version": "7776980"
            },
            "browser": {
                "name": "Chrome",
                "version": "131.0.0.0"
            },
            "os": {
                "name": "Windows",
                "version": "10"
            },
            "device_info": {
                "tier": "MEDIUM",
                "cpu": "12",
                "ram": "8",
                "vendor": "na",
                "model": "na"
            },
            "screen": {
                "width": 1440,
                "height": 900,
                "resolution": "1440x900",
                "aspect_ratio": 1.6,
                "inner_height": 765,
                "inner_width": 1440,
                "inner_resolution": "1440x765",
                "inner_aspect_ratio": 1.88,
                "density": 2
            },
            "gpu_info": {
                "device": "amd radeon pro 555x",
                "renderer": "ANGLE (AMD, Radeon Pro 555X (0x000067EF) Direct3D11 vs_5_0 ps_5_0, D3D11)",
                "fps": "42",
                "tier": "MEDIUM"
            },
            "user_age_in_days": -1,
            "attribution": {
                "medium": "direct",
                "source": "direct",
                "campaign": "direct",
                "content": "na"
            }
        },
        "raw_attribution": {
            "medium": "direct",
            "source": "direct",
            "campaign": "direct",
            "content": "na",
            "utm_source": None,
            "utm_medium": None,
            "utm_campaign": None,
            "utm_term": None,
            "utm_content": None,
            "referrer": None,
            "domain_referrer": None,
            "matchtype": None,
            "creative": None,
            "placement": None,
            "campaign_id": None,
            "adset_id": None,
            "ad_id": None,
            "ref": None,
            "msclkid": None,
            "fbclid": None,
            "gclid": None,
            "ttclid": None,
            "gbraid": None,
            "wbraid": None,
            "user_referral": None,
            "irclickid": None,
            "mpid": None,
            "twclid": None,
            "fbp": None
        }
    }

    response = requests.post(url, headers=headers, json=data)
    #print(f"Response nee creat: {response.text}")
    try:
        response_body = response.json()
        user_id = response_body.get('user', {}).get('id')
        #print(f"User ID: {user_id}")
        if user_id:
            print("Solicitud enviada con éxito. Buscando código de verificación...")

            attempts = 0
            verification_code, identifier = None, None

            # Reintentar hasta 6 veces
            while attempts < 6:
                verification_code, identifier = get_verification_code(name, domain)
                if verification_code:  # Si se obtiene el código, salir del bucle
                    break
                attempts += 1
                time.sleep(3)  # Esperar 3 segundos antes del siguiente intento

            if verification_code:
                #print("Código de verificación obtenido:", verification_code)
                #print("Identificador:", identifier)

                # Borrar el correo temporal asociado al identifier
                delete_temp_mail(name, domain, identifier)

                time.sleep(1)
                print("Correo:", email)
                #print("CODE", verification_code)
                time.sleep(5)
                # Registrar el usuario con el código de verificación
                #token, user_id = registrar_usuario(correo, password, verification_code)
                refresh_token, access_token = verify_session(email, str(verification_code))

                return refresh_token, access_token

    except ValueError:
        print("Error: Could not decode the response as JSON.")
        return None, None







def configurar_usuario():
    # Generar el nombre de usuario
    user_name = generar_nombre_completo()

    # Obtener el dominio de usuario
    domain_user = obtener_sitio_web_aleatorio(enviar_formulario())

    # Crear el correo electrónico del usuario
    user_emails = f"{user_name}@{domain_user}"

    # Contraseña (puede venir de otro lugar si es necesario)
    passwords = "c3b974a9b96984fabe65b5ee44a6a6cc"

    # Configurar las variables de entorno
    os.environ["USER_EMAIL_PIC"] = user_emails
    os.environ["PASS_WORD_PIC"] = passwords
    #print(user_emails)

    # Enviar código de registro
    refresh_token, access_token = create_new_user(user_emails)

    # Validar los resultados y configurar más variables de entorno
    if refresh_token and access_token:
        os.environ["REFRESH_TOKEN"] = refresh_token
        os.environ["ACCESS_TOKEN"] = access_token
        print("Registro con exito.")

        token = os.environ.get("ACCESS_TOKEN")
        first_name = generar_nombres()
        # Llamar a la función
        resultado = update_user_full_name(token, first_name)

    else:
        print("Error: No se obtuvieron valores válidos para el token o el user_idS.")