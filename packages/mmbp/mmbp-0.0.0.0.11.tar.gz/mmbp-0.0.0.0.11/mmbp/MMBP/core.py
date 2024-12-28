
import typing as _typing


class _EventTarget:
    @_typing.overload
    def addEventListener(self, event: str, handler: _typing.Callable) -> None:
        """
        Регистрирует обработчик для указанного события.

        Usage:

            def beforeunload_func() -> None:
                pass
                
            window.addEventListener('beforeunload', beforeunload_func)

        Этот метод добавляет слушателя события для отслеживания определенного события,
        происходящего в окне браузера.

        :param event str: Название события, на которое регистрируется обработчик.
        :param handler Callable: Функция-обработчик, которая будет вызвана при наступлении события.
        """
        ...
    @_typing.overload
    def addEventListener(self, event: str):
        """
        Регистрирует обработчик для указанного события.

        Usage:
        
            @window.addEventListener('beforeunload')
            def beforeunload_func() -> None:
                pass
                
        Этот метод добавляет слушателя события для отслеживания определенного события,
        происходящего в окне браузера.

        :param event str: Название события, на которое регистрируется обработчик.

        - beforeunload - Событие, вызывается перед завершением работы веб-страницы.

        
        """
        def wrapper(func): # пример
            return func
        return wrapper
    
    def addEventListener(self, event: str, handler: _typing.Optional[_typing.Callable] = None) -> None:
        ...
    def dispatchEvent(self, event: str, *args, **kwargs) -> bool:
        """
        Отправляет событие в окне браузера.
        
        Usage:
        
            window.dispatchEvent('load')
        
        Этот метод отправляет указанное событие в окне браузера и возвращает True, если событие было успешно отправлено,
        и False в противном случае.

        :param event str: Название события, которое требуется отправить.

        :return bool: True, если событие было успешно отправлено, и False в противном случае.
        """
        ...



class __LocalVault:
    """
    Well-protected local storage for storing data
    """
    def _get_caller_filename(self) -> str:
        ...
    @_typing.overload
    def add(self, key: str, model: tuple): ...
    @_typing.overload
    def add(self, key: str, data: _typing.Any = None, access_level: str = '', allowed_files: _typing.Union[str, _typing.List[str]] = None, denied_files: _typing.Union[str, _typing.List[str]] = None): ... # type: ignore

    def add(self, key: str, data: _typing.Any = None, access_level: str = '', allowed_files: _typing.Union[str, _typing.List[str]] = None, denied_files: _typing.Union[str, _typing.List[str]] = None, model: tuple = None): ... # type: ignore

    @_typing.overload
    def get(self, key: str) -> _typing.Any: ...
    @_typing.overload
    def get(self, model: tuple, default: _typing.Any) -> _typing.Any: ... # type: ignore

    def get(self, key: _typing.Optional[str] = None, model: _typing.Optional[tuple] = None, default: _typing.Optional[_typing.Any] = None) -> _typing.Any: # type: ignore
        ...
    def remove(self, key: str):
        ...
LocalVault = __LocalVault()




    





class Url:
    def __init__(self, url_str: _typing.Optional[str] = None):
        self.scheme: str
        self.hostname: str
        self.path: str
        self.query: str
        self.fragment: str
        self.params: dict

    def setUrl(self, url_str: str):
        """
        установка URL из строки
        """
        ...
    

    def getUrl(self, parts: _typing.List[_typing.Literal['scheme', 'hostname', 'path', 'params', 'fragment']] = ['scheme', 'hostname', 'path', 'params', 'fragment']) -> str:
        """
        Формирует и возвращает URL на основе указанных частей.

        Этот метод собирает URL из его составных частей, таких как схема, имя хоста, путь,
        параметры и фрагмент. Части, которые должны быть включены в конечный URL, передаются
        в виде списка. Если часть не указана в списке, она будет исключена из конечного результата.

        По умолчанию собираются все части: схема, имя хоста, путь, параметры и фрагмент.

        Пример использования:

            url = my_url.getUrl(parts=['scheme', 'hostname', 'path'])
            # Вернет URL, состоящий только из схемы, имени хоста и пути.

        :param parts List[Literal['scheme', 'hostname', 'path', 'params', 'fragment']]: 
            Список частей URL, которые должны быть включены в конечный результат. 
            Возможные значения:
            - 'scheme': Схема (например, 'https', 'http')
            - 'hostname': Имя хоста (например, 'example.com')
            - 'path': Путь (например, '/some/path')
            - 'params': Параметры запроса (например, '?param1=value1&param2=value2')
            - 'fragment': Фрагмент URL (например, '#section1')
        
        :return str: Полностью сформированный URL, включающий только указанные части.
        """
        ...
    def isSchemeSecure(self) -> bool:
        """
        Возвращает True, если схема URL является защищенной, и False в противном случае.
        """
        ...

