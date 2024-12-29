import requests
import sys
import textwrap

class Client:
    def __init__(self, model='gpt-4o-mini'):
        self.url = 'http://198.105.124.251:10000/chat'
        self.model = model
        self.responses = 0

    def select_model(self):
        text = """
            Выберите модель: 
            1) gpt-4o
            2) o1-mini
            3) o1-preview
            4) gpt-4o-mini
        """
        print(textwrap.dedent(text).lstrip())
        sys.stdout.flush()
        choice = input('Введите номер варианта: ')
        if choice == '1':
            self.model = 'gpt-4o'
        elif choice == '2':
            self.model = 'o1-mini'
        elif choice == '3':
            self.model = 'o1-preview'
        elif choice == '4':
            self.model = 'gpt-4o-mini'
        else:
            print(f'Напечатайте только цифру от 1 до 4! Используется модель по умолчанию: {self.model}\n')

    def get_response(self, message):
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': message}]
        }
        response = requests.post(self.url, headers=headers, json=data)
        print(f'\033[1m{self.model}:\033[0m\n')
        print(response.json()['choices'][0]['message']['content'])

class ClientManager:
    _client_instance = None

    @classmethod
    def get_client(cls):
        if cls._client_instance is None:
            cls._client_instance = Client()
            cls._client_instance.select_model()
        return cls._client_instance

def ans(message):
    client = ClientManager.get_client() 
    return client.get_response(message)
