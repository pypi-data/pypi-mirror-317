import requests
import sys
import textwrap
import time

class Client:
    def __init__(self, model='gpt-4o-mini'):
        self.url = 'http://198.105.124.251:10000/chat'
        self.model = model
        self.model_selected = False
        self.system_prompt = ('Всегда форматируй все формулы и символы в ASCII.'
                              'Не используй LaTeX, специальные символы или символы Unicode.'
                              'Пиши весь'
                              'Пиши по-русски.')

    def select_model(self, force=False):
        if not self.model_selected or force:
            text = """
            Выберите модель: 
            1) gpt-4o
            2) o1-mini
            3) o1-preview
            4) gpt-4o-mini
            """
            print(textwrap.dedent(text).lstrip(), flush=True)
            sys.stdout.flush()
            time.sleep(0.01)
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
                print(f'Напечатайте только цифру от 1 до 4! Используется модель по умолчанию {self.model}\n')

    def get_response(self, message):
        headers = {
            'Content-Type': 'application/json'
        }
        
        if self.model in ['o1-mini', 'o1-preview']:
            messages = [{'role': 'user', 'content': f"{self.system_prompt}\n{message}"}]
        else:
            messages = [
                {'role': 'system', 'content': self.system_prompt},
                {'role': 'user', 'content': message}
            ]

        data = {
            'model': self.model,
            'messages': messages
        }

        response = requests.post(self.url, headers=headers, json=data)
        
        return response.json()['choices'][0]['message']['content']


class ClientManager:
    _client_instance = None

    @classmethod
    def get_client(cls, skip_selection=False):
        if cls._client_instance is None:
            cls._client_instance = Client()
            if not skip_selection:
                cls._client_instance.select_model()
        return cls._client_instance

def answer(message, change=False):
    """
    Отправляет запрос к модели и выводит ответ в консоль.

    Параметры:
        message (str): Текст запроса, который нужно отправить модели.
        change (bool): Если True, позволяет повторно выбрать модель перед отправкой запроса.

    Возвращает:
        None: Ответ выводится в консоль.
    """
    client = ClientManager.get_client()
    if change and client.model_selected:
        client.select_model(force=True)
    client.model_selected = True
    response = client.get_response(message)
    print(f'\033[1m{client.model}:\033[0m\n')
    print(response)

def ask(message, m=4):
    """
    Отправляет запрос к модели и возвращает ответ.

    Параметры:
        message (str): Текст запроса, который нужно отправить модели.
        m (int): Номер модели, которую нужно использовать. 
                 Поддерживаемые значения:
                 1 - 'gpt-4o'
                 2 - 'o1-mini'
                 3 - 'o1-preview'
                 4 - 'gpt-4o-mini' (по умолчанию).

    Возвращает:
        str: Ответ модели на заданное сообщение.
    """
    model_map = {1: 'gpt-4o', 2: 'o1-mini', 3: 'o1-preview', 4: 'gpt-4o-mini'}
    client = ClientManager.get_client(skip_selection=True)
    if m in model_map:
        client.model = model_map[m]
    return client.get_response(message)