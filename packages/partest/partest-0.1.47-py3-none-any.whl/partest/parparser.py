import os

import yaml
import requests

class Parameter:
    """Class representing a parameter in an API path."""
    def __init__(self, name, param_type, required=False, description='', schema=None):
        self.name = name
        self.type = param_type
        self.required = required
        self.description = description
        self.schema = schema

    def __repr__(self):
        return f"Parameter(name={self.name}, type={self.type}, required={self.required}, description={self.description}, schema={self.schema})"


class RequestBody:
    """Class representing the request body of an API path."""
    def __init__(self, content):
        self.content = content

    @staticmethod
    def resolve_schema(schema_ref, swagger_dict):
        return OpenAPIParser.resolve_ref(schema_ref, swagger_dict)

    def __repr__(self):
        return f"RequestBody(content={self.content})"


class Response:
    """Class representing a response from an API path."""
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    @staticmethod
    def resolve_schema(schema_ref, swagger_dict):
        return OpenAPIParser.resolve_ref(schema_ref, swagger_dict)

    def __repr__(self):
        return f"Response(status_code={self.status_code}, content={self.content})"


class Path:
    """Class representing a path in an API."""
    def __init__(self, path, method, description, parameters, request_body, responses, deprecated=False):
        self.path = path
        self.method = method
        self.description = description
        self.parameters = parameters
        self.request_body = request_body
        self.responses = responses
        self.deprecated = deprecated  # Добавляем атрибут deprecated

    def __repr__(self):
        return f"Path(path={self.path}, method={self.method}, description={self.description}, parameters={self.parameters}, request_body={self.request_body}, responses={self.responses}, deprecated={self.deprecated})"


class OpenAPIParser:
    """Class for parsing OpenAPI specifications."""
    def __init__(self, swagger_dict, base_path=''):
        self.swagger_dict = swagger_dict
        self.base_path = base_path

    @staticmethod
    def load_external_yaml(file_path):
        """Loads an external YAML file."""
        with open(file_path, 'r', encoding="utf8") as file:
            return yaml.safe_load(file)

    def resolve_ref(self, ref):
        """Разрешает ссылку на компонент в спецификации OpenAPI."""
        if isinstance(ref, dict):
            print("Обнаружен словарь вместо строки, пропускаем.")  # Отладочная информация
            return None  # Или можно вернуть какое-то значение по умолчанию

        print(f"Разрешение ссылки: {ref}")  # Отладочная информация

        # Проверка, является ли ссылка внешней
        if ref.startswith('./') or ref.startswith('../'):
            # Конструируем полный путь к внешнему файлу
            full_path = os.path.join(self.base_path, ref.split('#')[0])
            # Загружаем внешний YAML файл
            external_swagger_dict = self.load_external_yaml(full_path)
            # Разрешаем внутреннюю ссылку в загруженном файле
            internal_ref = ref.split('#')[1]  # Получаем часть после #
            return self.resolve_internal_ref(internal_ref, external_swagger_dict)
        else:
            # Обработка внутренних ссылок
            parts = ref.split('/')
            resolved = self.swagger_dict
            for part in parts[1:]:
                if part:  # Проверка, что часть не пустая
                    resolved = resolved.get(part)
                    if resolved is None:
                        print(
                            f"Ссылка '{ref}' не может быть разрешена в предоставленном словаре swagger, пропускаем.")  # Отладочная информация
                        return None  # Или можно вернуть какое-то значение по умолчанию
                else:
                    print("Обнаружена пустая часть ссылки, пропускаем.")  # Пропускаем пустую часть
            return resolved

    def resolve_internal_ref(self, internal_ref, swagger_dict):
        """Разрешает внутреннюю ссылку в данном словаре swagger."""
        if not internal_ref:
            raise ValueError("Внутренняя ссылка не может быть пустой.")

        parts = internal_ref.split('/')
        print(f"Разрешение внутренней ссылки: {internal_ref}")  # Отладочная информация
        resolved = swagger_dict
        for part in parts:
            print(f"Текущая часть: '{part}'")  # Отладочная информация
            if part:  # Проверка, что часть не пустая
                resolved = resolved.get(part)
                if resolved is None:
                    raise KeyError(
                        f"Ссылка '{internal_ref}' не может быть разрешена в предоставленном словаре swagger.")
            else:
                print("Обнаружена пустая часть ссылки, пропускаем.")  # Пропускаем пустую часть

        return resolved

    @classmethod
    def load_swagger_yaml(cls, source_type, file_path=None):
        """Loads the Swagger YAML file from a local file or a URL."""
        if source_type == 'local':
            base_path = os.path.dirname(file_path)  # Get the base path for resolving external references
            with open(file_path, 'r', encoding="utf8") as file:
                swagger_dict = yaml.safe_load(file)
            return cls(swagger_dict, base_path)  # Pass the base path to the parser
        elif source_type == 'url':
            response = requests.get(file_path)
            response.raise_for_status()
            swagger_dict = yaml.safe_load(response.text)
            return cls(swagger_dict)  # No base path for URLs
        else:
            raise ValueError("Invalid source type. Use 'local' or 'url'.")

    def extract_paths_info(self):
        """Extracts path information from the Swagger specification."""
        paths = self.swagger_dict.get('paths', {})
        result = []

        for path, methods in paths.items():
            for method, details in methods.items():
                # Убедитесь, что details - это словарь
                if isinstance(details, dict):
                    parameters = self.extract_parameters(details)
                    request_body = self.extract_request_body(details)
                    responses = self.extract_responses(details)
                    description = self.safe_get_description(details)
                    deprecated = details.get('deprecated', False)  # Получаем значение deprecated
                    result.append(Path(
                        path=path,
                        method=method.upper(),
                        description=description,
                        parameters=parameters,
                        request_body=request_body,
                        responses=responses,
                        deprecated=deprecated  # Передаем значение deprecated
                    ))
                else:
                    print(
                        f"Warning: Expected details to be a dict, but got {type(details)} for path {path} and method {method}")

        return result

    def extract_parameters(self, details):
        """Extracts parameters from the method details."""
        parameters = []
        if 'parameters' in details:
            for param in details['parameters']:
                resolved_param = self.resolve_param(param)
                parameters.append(resolved_param)
        return parameters

    def extract_request_body(self, details):
        """Extracts the request body from method details."""
        if 'requestBody' in details:
            content = details['requestBody'].get('content', {})
            if 'application/json' in content:
                if 'schema' in content['application/json'] and '$ref' in content['application/json']['schema']:
                    schema_ref = content['application/json']['schema']['$ref']
                    resolved_schema = RequestBody.resolve_schema(schema_ref, self.swagger_dict)
                    content['application/json']['schema'] = resolved_schema
                return RequestBody(content['application/json'])
        return None

    def extract_responses(self, details):
        """Извлекает ответы из деталей метода."""
        responses = {}
        if 'responses' in details:
            for code, response in details['responses'].items():
                if 'content' in response and 'application/json' in response['content']:
                    content = response['content']['application/json']
                    if 'schema' in content and '$ref' in content['schema']:
                        schema_ref = content['schema']['$ref']
                        print(f"Обнаружена схема: {schema_ref}")  # Отладочная информация
                        resolved_schema = Response.resolve_schema(schema_ref, self.swagger_dict)
                        content['schema'] = resolved_schema
                    responses[code] = Response(code, response)
        return responses

    def resolve_param(self, param):
        """Разрешает определение параметра."""
        if '$ref' in param:
            # Убедитесь, что вы передаете строку
            ref_value = param['$ref']
            resolved_param = self.resolve_ref(ref_value)  # Передаем строку
            return Parameter(
                name=resolved_param['name'],
                param_type=resolved_param['in'],
                required=resolved_param.get('required', False),
                description=resolved_param.get('description', ''),
                schema=resolved_param.get('schema')  # Возвращаем схему, если она присутствует
            )
        else:
            # Обработка обычных параметров
            return Parameter(
                name=param['name'],
                param_type=param['in'],
                required=param.get('required', False),
                description=param.get('description', ''),
                schema=param.get('schema')  # Возвращаем схему, если она присутствует
            )

    def safe_get_description(self, details):
        """Safely retrieves the description from details."""
        if isinstance(details, dict):
            return details.get('description', '')
        elif isinstance(details, list) and details:
            return details[0].get('description', '') if isinstance(details[0], dict) else ''
        return ''


class SwaggerSettings:
    """Class for managing Swagger settings and loading Swagger files."""

    def __init__(self, swagger_files):
        self.local_files = []
        self.swaggers = []
        self.paths_info = []
        self.add_swagger(swagger_files)

    def add_swagger(self, swagger_dict):
        """Adds swagger definitions from a dictionary to the swaggers list."""
        for name, (source_type, path) in swagger_dict.items():
            self.swaggers.append((source_type, path))

    def load_swagger(self):
        """Loads swagger definitions and returns their data."""
        all_extracted_data = []
        for source_type, path in self.swaggers:
            parser = OpenAPIParser.load_swagger_yaml(source_type, path)
            extracted_data = parser.extract_paths_info()
            all_extracted_data.extend(extracted_data)
        return all_extracted_data

    def collect_paths_info(self):
        """Collects path information from all swagger definitions."""
        extracted_data = self.load_swagger()
        self.paths_info = []

        # Collecting paths from each extracted data
        for item in extracted_data:
            # Проверяем, является ли эндпоинт устаревшим
            if not item.deprecated:  # Используем атрибут deprecated
                self.paths_info.append({
                    'description': item.description,
                    'path': item.path,
                    'method': item.method,
                    'parameters': item.parameters
                })

        # Debugging output to see the collected paths
        print("Collected Paths Info:")
        for path_info in self.paths_info:
            print(path_info)

        return self.paths_info