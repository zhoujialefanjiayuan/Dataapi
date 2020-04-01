import requests
from flask import current_app, request, Blueprint

from app.error import INVALID_PARAMETER_ERROR
from app.validator import mobile_online_validator


def istokopedia(mobile_no):
    url = 'https://gql.tokopedia.com/'
    headers = {
        'cookie': '_abck=B963277A8FFF461C398AD58069DCC8D2~0~YAAQgZZUaFaJcJ5wAQAAn1u45wNBp66rRoMiU/v9fxQH+oN3pPdO2QC5mozEithnkjoju11B7xW860q7ygKq6yMMKIxRyENalRH865tbrMY1dyfuIkE0Fy6jf+IgyBc7lSzDoDQbxIchXvRb77glilnXPjRtQYGfyaNXm9Hz9zQ2lMbMcFOOQlaBV2WaUZ2FonC9O1n551Udw0/6hk92m+Ys4bwH+tiXajBxzUCwRlLycYdIt0o8HGxYn0HA0DtfkymBoejJ/x7DRgzBp4wJrXhsXVZQZktYLslwDxOAN9Vu/wycXvzGlcnPzC/mr7sFn2UWiCEutCcmWw==~-1~-1~-1; DID=96c9643136522dd245d5673a0687ad562c74e47afd392aa1277611b18ee4f848d5e3f0eca60f9d9e2f1482ff45d1f418; DID_JS=OTZjOTY0MzEzNjUyMmRkMjQ1ZDU2NzNhMDY4N2FkNTYyYzc0ZTQ3YWZkMzkyYWExMjc3NjExYjE4ZWU0Zjg0OGQ1ZTNmMGVjYTYwZjlkOWUyZjE0ODJmZjQ1ZDFmNDE447DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=; _gcl_au=1.1.739123696.1584435583; __auc=2dacece6170e7b85843f2179b67; _ga=GA1.2.53470112.1584435584; _gid=GA1.2.531671573.1584435584; _fbp=fb.1.1584435585052.999039682; _jx=a75fec80-682d-11ea-ae63-9b88358d3316; CSHLD_SID=c88b1a581af0bd731b072458f9dc32d68a73aa873c3fd3ec428ed1cc5ba7cf67; lang=id; isWebpSupport=true; _ID_autocomplete_=009dc670121e4a159e3b4adf7d8a6b7c; bm_sz=0192EB4B76DDCD009A2F8BC4A02C0DD3~YAAQgZZUaLwGdJ5wAQAA11eW6wfYHZAsvV8F9Ewjkrqm0tjmcFUa+fD/Ywzay5KRQDXWGIVN7AVcqRa3Hcd4zWvNOuQlteBRBvg94n/GJQJABh0gExaQbRvIZl5aAQQt0Ah7UliROflPCHmd1yyPUSRv6IrJZo0JZGtPhPZY0BuigBbyZy0hnnKxTappTW+Qcckv; ak_bmsc=7853DCD1FEC859A2D82AD7E3DE33D870685496815D150000EF8E715EB85B4764~plVY55Fb4NEW5nOY2wEmoTTJdPL221/MAUru/XQPKjd1pgk6GqD8GQF0v3vEfH0xEJAeR2bI0WQnmF73gSmhAiOo9nvlsCmp8zaU1Es3SgDC0lJ5T/qcIry01eeuBgmBzMUMdXMa3bIiQhyfQewX2REkKH21lEptauV5Kc9e+rJkojY1Up0oyVdwpI+kGj2e9dS6AErSgp2h2oJzviwAsI80ylbHRMeZclcbr8Eh+d5SAKhvDOpgr2qD49oWo9YhgVXOU5+teaKWVgU7W8AC681Otm00o0aJwJY6PYw9t+qlW+bn1BskBJK6+8oRbOXE4vQLDKS5t27qKxS2KdSc5FIA==; _SID_Tokopedia_=XCGs0Z7Afw_uf4ZHsnpXb71vwqGHJ9eoz6WQHsPIN3PsS0eJiGI3dKWWskfyTVpLXXa52FSjA1K_gxyLPyiALDoB0JyuCrzKswtpgnutmwoX3k6IKP8PJmuxvMa4tH01; __asc=dcb28299170eb96570c45bafbf8; _jxs=1584500464-a75fec80-682d-11ea-ae63-9b88358d3316; state=eyJyZWYiOiJodHRwczovL3d3dy50b2tvcGVkaWEuY29tLyIsInV1aWQiOiJhN2EyNDIyYS1jMTE0LTQ5Y2UtOTYyOS02MTM2NjY2ZDJhY2IiLCJwIjoiaHR0cHM6Ly93d3cudG9rb3BlZGlhLmNvbSJ9; bm_sv=F6683F207D6D24FDE1C63CE442CD3E6B~LGMpezWvkdKDUZfNIFlI17wmTlFUynXY658T9wA++pUYgipIkg0maS8Y3OQqVmt2nwSEWm0QYjv4uG4aIboYzZ1B3ZTCbOGhq4qpAEkO5gOZ3jP9gtMANwrbrm5c+SRxwRxuHM/yyV0Nsgm83jeRGXRz7+p8VCOShesX2GHNWmQ=; RT="z=1&dm=tokopedia.com&si=be7c09c1-2331-47df-b55d-f3d3d8f129aa&ss=k7wqnx97&sl=0&tt=0&bcn=%2F%2F684fc537.akstat.io%2F"; _dc_gtm_UA-9801603-1=1; _gat_UA-9801603-1=1',
        'origin': 'https://www.tokopedia.com',
        'referer': 'https://www.tokopedia.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'x-source': 'tokopedia-lite',
        'x-tkpd-lite-service': 'zeus'}

    data = [{'operationName': "CheckRegisterMutation", 'variables': {'id': mobile_no},'query': "mutation CheckRegisterMutation($id: String!) {  registerCheck(id: $id) {    isExist    errors    __typename  }}"}]
    re = requests.post(url,json=data,headers=headers).json()[0]
    return re['data']['registerCheck']["isExist"]

istokopedia_blue = Blueprint("istokopedia_blue", __name__, url_prefix="/api")

@istokopedia_blue.route('/istokopedia', methods=['POST'])
def istokopedia_check():
    istokoprice = current_app.config.get('ISTOKO')
    params = request.json
    try:
        mobile_online_validator(params)
    except Exception as e:
        INVALID_PARAMETER_ERROR['message'] = str(e)
        return INVALID_PARAMETER_ERROR
    mobile_no = params.get('mobile_no')[1:]
    re = istokopedia(mobile_no)
    return {'istokopedia':re,'paied':istokoprice}