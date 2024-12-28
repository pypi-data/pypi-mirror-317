
import typing as _typing
import types as _types

try:
    from PyQt6.QtWidgets import QWidget
    from PyQt6.QtCore import QByteArray, QDateTime
except ImportError:
    pass

from .core import _EventTarget, Url
from enum import Enum

class __PyEngine_async:
    """
    Класс PyEngineAsync

    Асинхронный класс, содержащий методы для управления окнами и специфическими для языка Python функциями
    в контексте веб-страницы. Этот класс предназначен для интеграции с браузером и управления
    отображением пользовательского интерфейса в асинхронном контексте.
    """
PyEngine_async = __PyEngine_async()
class __PyEngine:
    """
    Класс PyEngine

    Класс, содержащий методы для управления окнами и специфическими для языка Python функциями
    в контексте веб-страницы. Этот класс предназначен для интеграции с браузером и управления
    отображением пользовательского интерфейса.
    """
    
    def setWidget(self, widget: 'QWidget') -> None: # type: ignore
        """
        Установка виджета страницы в окно браузера.

        Этот метод устанавливает указанный виджет в окно браузера, позволяя отображать
        интерфейс страницы в браузере. Виджет должен быть объектом типа QWidget и будет
        использоваться для представления интерфейса веб-страницы.

        :param widget QWidget: Виджет, представляющий интерфейс страницы.
        """
        ...
PyEngine = __PyEngine()







class __document_async:
    """
    Класс DocumentAsync

    Асинхронный класс, содержащий методы для управления заголовком и описанием страницы
    в контексте веб-страницы. Этот класс предназначен для интеграции с браузером
    и управления метаданными страницы в асинхронном контексте.
    """

    async def setTitle(self, title: str) -> None:
        """
        Асинхронная установка заголовка страницы.

        Этот метод асинхронно устанавливает указанный заголовок для веб-страницы.

        :param title str: Заголовок страницы.
        """
        ...

    async def setDescription(self, description: str) -> None:
        """
        Асинхронная установка описания страницы.

        Этот метод асинхронно устанавливает указанное описание для веб-страницы, которое
        может быть использовано для отображения в результатах поиска и для других
        мета-целей.

        :param description str: Описание страницы.
        """
        ...
document_async = __document_async()
class __document(_EventTarget):
    """
    Класс Document

    Класс, содержащий методы для управления заголовком и описанием страницы
    в контексте веб-страницы. Этот класс предназначен для интеграции с браузером
    и управления метаданными страницы.
    """

    def setTitle(self, title: str) -> None:
        """
        Установка заголовка страницы.

        Этот метод устанавливает указанный заголовок для веб-страницы.

        :param title str: Заголовок страницы.
        """
        ...

    def setDescription(self, description: str) -> None:
        """
        Установка описания страницы.

        Этот метод устанавливает указанное описание для веб-страницы, которое
        может быть использовано для отображения в результатах поиска и для других
        мета-целей.

        :param description str: Описание страницы.
        """
        ...
document = __document()

class __Console:
    """
    Класс Console

    Класс, предоставляющий методы для вывода логов и сообщений в консоль.
    Этот класс предназначен для интеграции с браузером и работы с выводом
    сообщений в консоль, аналогично объекту console в JavaScript.
    """

    def log(self, message: _typing.Any) -> None:
        """
        Выводит информационное сообщение в консоль.

        :param message _typing.Any: Сообщение, которое будет выведено в консоль.
        """
        ...

    def warn(self, message: _typing.Any) -> None:
        """
        Выводит предупреждающее сообщение в консоль.

        :param message _typing.Any: Сообщение, которое будет выведено в консоль.
        """
        ...

    def error(self, message: _typing.Any) -> None:
        """
        Выводит сообщение об ошибке в консоль.

        :param message _typing.Any: Сообщение, которое будет выведено в консоль.
        """
        ...

    def info(self, message: _typing.Any) -> None:
        """
        Выводит информационное сообщение в консоль.

        :param message _typing.Any: Сообщение, которое будет выведено в консоль.
        """
        ...
console = __Console()
class __Console_async:
    """
    Класс ConsoleAsync

    Асинхронный класс, предоставляющий методы для вывода логов и сообщений в консоль.
    Этот класс предназначен для интеграции с браузером и работы с выводом
    сообщений в консоль в асинхронном контексте, аналогично объекту console в JavaScript.
    """

    async def log(self, message: _typing.Any) -> None:
        """
        Асинхронно выводит информационное сообщение в консоль.

        :param message _typing.Any: Сообщение, которое будет выведено в консоль.
        """
        ...

    async def warn(self, message: _typing.Any) -> None:
        """
        Асинхронно выводит предупреждающее сообщение в консоль.

        :param message _typing.Any: Сообщение, которое будет выведено в консоль.
        """
        ...

    async def error(self, message: _typing.Any) -> None:
        """
        Асинхронно выводит сообщение об ошибке в консоль.

        :param message _typing.Any: Сообщение, которое будет выведено в консоль.
        """
        ...

    async def info(self, message: _typing.Any) -> None:
        """
        Асинхронно выводит информационное сообщение в консоль.

        :param message _typing.Any: Сообщение, которое будет выведено в консоль.
        """
        ...
console_async = __Console_async()

class __window_async:
    """
    Класс WindowAsync

    Асинхронный класс, представляющий собой интерфейс для управления событиями и историей навигации
    в веб-странице. Этот класс предоставляет методы для асинхронной регистрации обработчиков событий,
    управления состоянием истории и имитации навигации назад и вперед в браузере.

    Класс WindowAsync работает аналогично объекту window в JavaScript, обеспечивая
    взаимодействие с ключевыми аспектами работы с окном браузера и историей навигации в асинхронном контексте.
    """
    def __init__(self) -> None:
        self.history = self.__history()
        self.location = self.__location()

    async def addEventListener(self, event: str, handler: _typing.Callable) -> None:
        """
        Асинхронно регистрирует обработчик для указанного события.

        Этот метод добавляет слушателя события для отслеживания определенного события,
        происходящего в окне браузера. Например, вы можете добавить обработчик для
        события "popstate", чтобы реагировать на изменения в истории навигации.

        :param event str: Название события, на которое регистрируется обработчик (например, "popstate").
        :param handler Callable: Функция-обработчик, которая будет вызвана при наступлении события.
        """
        ...

    class __history:
        """
        Вложенный класс HistoryAsync

        Асинхронный класс HistoryAsync предоставляет интерфейс для управления состояниями истории
        навигации в веб-странице. Он позволяет добавлять новые состояния, заменять
        текущие, а также имитировать переходы назад и вперед в истории браузера в асинхронном контексте.
        """

        async def pushState(self, state, title, url: str) -> None:
            """
            Асинхронно добавляет новое состояние в историю и изменяет URL.

            Этот метод позволяет асинхронно добавить новое состояние в стек истории браузера
            без перезагрузки страницы, а также изменить текущий URL. Он часто используется
            в одностраничных приложениях (SPA) для изменения состояния интерфейса
            без полной перезагрузки страницы.

            :param state: Объект состояния, который будет связан с новым элементом истории.
            :param title str: Заголовок страницы для нового состояния (может быть пустым).
            :param url str: Новый URL, который будет отображаться в адресной строке браузера.
            """
            ...

        async def replaceState(self, state, title, url: str) -> None:
            """
            Асинхронно заменяет текущее состояние в истории и изменяет URL.

            Этот метод асинхронно заменяет текущий элемент в истории браузера новым состоянием,
            сохраняя при этом позицию в истории. Это полезно, когда нужно обновить
            состояние или URL без добавления нового элемента в историю.

            :param state: Объект состояния, который заменит текущее состояние в истории.
            :param title str: Новый заголовок страницы для состояния (может быть пустым).
            :param url str: Новый URL, который будет отображаться в адресной строке браузера.
            """
            ...

        async def goBack(self) -> None:
            """
            Асинхронно имитирует нажатие кнопки "Назад" в браузере.

            Этот метод выполняет асинхронный переход на одну страницу назад в истории браузера,
            аналогично нажатию кнопки "Назад" пользователем. Полезно для программной
            навигации в веб-приложениях.
            """
            ...

        async def goForward(self) -> None:
            """
            Асинхронно имитирует нажатие кнопки "Вперед" в браузере.

            Этот метод выполняет асинхронный переход на одну страницу вперед в истории браузера,
            аналогично нажатию кнопки "Вперед" пользователем. Используется для
            программного управления навигацией, когда необходимо восстановить
            следующее состояние после перехода назад.
            """
            ...
    class __location:
        """
        Вложенный класс LocationAsync

        Асинхронный класс LocationAsync предоставляет методы для работы с URL страницы, включая получение текущего
        URL и другие операции, связанные с навигацией, в асинхронном контексте.
        """
        
window_async = __window_async()






class __window(_EventTarget):
    """
    Класс Window

    Класс представляет собой интерфейс для управления событиями и историей навигации
    в веб-странице. Этот класс предоставляет методы для регистрации обработчиков событий,
    управления состоянием истории и имитации навигации назад и вперед в браузере.

    Класс Window работает аналогично объекту window в JavaScript, обеспечивая
    взаимодействие с ключевыми аспектами работы с окном браузера и историей навигации.
    """
    def __init__(self) -> None:
        self.history = self.__history()
        self.location = self.__location()

    
        


    class __history:
        """
        Вложенный класс History

        Класс History предоставляет интерфейс для управления состояниями истории
        навигации в веб-странице. Он позволяет добавлять новые состояния, заменять
        текущие, а также имитировать переходы назад и вперед в истории браузера.
        """

        def pushState(self, state, title, url: str) -> None:
            """
            Добавляет новое состояние в историю и изменяет URL.

            Этот метод позволяет добавить новое состояние в стек истории браузера
            без перезагрузки страницы, а также изменить текущий URL. Он часто используется
            в одностраничных приложениях (SPA) для изменения состояния интерфейса
            без полной перезагрузки страницы.

            :param state: Объект состояния, который будет связан с новым элементом истории.
            :param title str: Заголовок страницы для нового состояния (может быть пустым).
            :param url str: Новый URL, который будет отображаться в адресной строке браузера.
            """
            ...

        def replaceState(self, state, title, url: str) -> None:
            """
            Заменяет текущее состояние в истории и изменяет URL.

            Этот метод заменяет текущий элемент в истории браузера новым состоянием,
            сохраняя при этом позицию в истории. Это полезно, когда нужно обновить
            состояние или URL без добавления нового элемента в историю.

            :param state: Объект состояния, который заменит текущее состояние в истории.
            :param title str: Новый заголовок страницы для состояния (может быть пустым).
            :param url str: Новый URL, который будет отображаться в адресной строке браузера.
            """
            ...

        def goBack(self) -> None:
            """
            Имитирует нажатие кнопки "Назад" в браузере.

            Этот метод выполняет переход на одну страницу назад в истории браузера,
            аналогично нажатию кнопки "Назад" пользователем. Полезно для программной
            навигации в веб-приложениях.
            """
            ...

        def goForward(self) -> None:
            """
            Имитирует нажатие кнопки "Вперед" в браузере.

            Этот метод выполняет переход на одну страницу вперед в истории браузера,
            аналогично нажатию кнопки "Вперед" пользователем. Используется для
            программного управления навигацией, когда необходимо восстановить
            следующее состояние после перехода назад.
            """
            ...
    class __location:
        """
        Вложенный класс Location

        Класс Location предоставляет методы для работы с URL страницы, включая получение текущего
        URL и другие операции, связанные с навигацией.
        """

        def currentPageUrl(self) -> Url:
            """
            Возвращает URL страницы.

            Этот метод возвращает обьект URL, представляющий URL веб-страницы.
            Этот метод отличается от currentUrl() в том, он возвращает конкретный начальный url страницы, а не адресную строку.

            :return Url: Текущий URL страницы.
            """
            ...
        def currentUrl(self) -> Url:
            """
            Возвращает текущий URL.

            Этот метод возвращает обьект URL, представляющий текущий URL адресной строки.
            Это полезно для получения информации о том, на каком адресе в данный момент
            находится пользователь.

            :return Url: Текущий URL страницы.
            """
            ...
        def changeUrl(self, url: _typing.Union[Url, str], complete: bool = True) -> None:
            """
            Переходит на новый URL.


            :param url:  новый URL.
            :param complete: Если True, дозаполнит относительный URL на полный URL, если он относительный.
            """
            ...
        def addTab(self, url: _typing.Union[Url, str]) -> None:
            """
            Этот метод добавляет новую вкладку с указанным URL.
            
            :param url: новый URL.
            """
            ...
        def replaceUrl(self, url: _typing.Union[Url, str]) -> None:
            """
            Этот метод заменяет текущий URL на новый.
            
            :param url: новый URL.
            """
            ...
        def reload(self) -> None:
            """
            Этот метод перезагружает текущую веб-страницу.
            """
            ...
        def completeUrl(self, url: _typing.Union[Url, str], originUrl: _typing.Optional[_typing.Union[Url, str]] = None) -> Url:
            """
            Дополняет URL недостающими частями из originUrl или текущего URL.

            Если в URL не хватает схемы или хоста, они будут взяты из originUrl. Если originUrl не указан, 
            используются данные из текущего URL страницы.

            Пример использования:

                complete_url = window.location.completeUrl('/some/path')
                # Дополнит схему и хост из текущего URL.

                complete_url = window.location.completeUrl('/some/path', originUrl='https://example.com')
                # Дополнит схему и хост из https://example.com.

            :param url _typing.Union[Url, str]: URL, который нужно дополнить.
            :param originUrl _typing.Optional[_typing.Union[Url, str]]: URL для дополнения недостающих частей. 
                                                        Если не указан, используется текущий URL.
            :return Url: Дополненный URL.
            """
            ...
window = __window()




class __files(_EventTarget):
    """
    Класс Files

    Класс, содержащий методы для загрузки файлов с сайтов, а также для загрузки и управления
    библиотеками с сайтов. Класс предназначен для синхронной загрузки данных с удаленных источников.
    """
    def load(self, url: _typing.Union[Url, str], savePath: str = '/', fileName: _typing.Optional[str] = None, unpack: bool = False, version: str = '0.0.1') -> _typing.Optional[str]:
        """
        Загрузка файла с указанного URL.

        Этот метод загружает файл по указанному URL и возвращает путь к локально сохраненному файлу.

        Usage:

            path = files.load('https://example.com/file.txt')
            path = files.load('https://example.com/file.txt', '/site_name/images')

        :param url str: URL файла, который необходимо загрузить.
        :param savePath str: Необязательный путь для сохранения файла.
                             Если не указан, используется путь из `self.getCurrentFilePath()`.
        :return str: Путь к локально сохраненному файлу, или None, если файл не уладось загрузить.
        """
        ...
    def getCurrentPath(self) -> str:
            """
            Возвращает текущий путь для сохранения файлов.
            :return str: Текущий путь для сохранения файлов.
            """
            ...
Files = __files()

class __libs:
        """
        Вложенный класс Libs

        Класс предоставляет методы для загрузки библиотек с сайтов или по имени. Предназначен
        для работы с внешними Python-библиотеками, загружаемыми с удаленных источников.
        """
        def get(self, name: str) -> _typing.Optional[_types.ModuleType]:
            """
            Загрузка библиотеки с указанного URL или по имени.

            Этот метод загружает библиотеку из lib.sourse.gw по имени и возвращает загруженный модуль,
            если он был найден и успешно загружен.

            Usage:

                module = files.libs.load('lib_name')

            :param name str: имя библиотеки для загрузки.
            :return typing._typing.Optional[types.ModuleType]: Загруженная библиотека в виде модуля, или None, если библиотека не найдена.
            """
            ...
Libs = __libs()


class __user:
    """
    Класс User

    Класс, предоставляющий методы для работы с текущим пользователем в контексте веб-страницы.
    Этот класс обеспечивает доступ к информации о пользователе, такой как его ID, никнейм, токен и тд.
    Информация берется из текущего окна и активной сессии пользователя.
    """
    def getUserId(self) -> _typing.Optional[int]:
        """
        Получение ID пользователя.

        Этот метод возвращает идентификатор текущего пользователя, если пользователь аутентифицирован.
        Если пользователь не найден или не аутентифицирован, метод возвращает None.

        :return _typing.Optional[int]: Идентификатор пользователя или None, если пользователь не аутентифицирован.
        """
        ...
    def getNickname(self) -> _typing.Optional[str]:
        """
        Получение никнейма пользователя.

        Этот метод возвращает никнейм (username) текущего пользователя, если пользователь аутентифицирован.
        Если пользователь не найден или не аутентифицирован, метод возвращает None.

        :return _typing.Optional[str]: Никнейм пользователя или None, если пользователь не аутентифицирован.
        """
        ...
    def getToken(self) -> _typing.Optional[str]:
        """
        Получение токена пользователя.

        Этот метод возвращает токен текущего пользователя, если пользователь аутентифицирован.
        Если пользователь не найден или не аутентифицирован, метод возвращает None.

        :return _typing.Optional[str]: Токен пользователя или None, если пользователь не аутентифицирован.
        """
        ...
User = __user()






class Cookie:
    class SameSite(Enum):
        Default = 0
        None_ = 1
        Lax = 2
        Strict = 3

    class DnsType(Enum):
        Www = 0
        """Www: World Wide Web (default)"""

        Gw = 1
        """GW"""

    class RawForm(Enum):
        NameAndValueOnly = 0
        Full = 1

    @_typing.overload
    def __init__(self, cookie: 'Cookie') -> None: ...

    @_typing.overload
    def __init__(self, name: str, value: _typing.Any) -> None: ...

    @_typing.overload
    def __init__(self, name: _typing.Union['QByteArray', bytes, bytearray, memoryview] = b"", 
                 value: _typing.Union['QByteArray', bytes, bytearray, memoryview] = b"") -> None: ...

    def __init__(self,  # type: ignore
                 name_or_cookie: _typing.Union['QByteArray', bytes, bytearray, memoryview, 'Cookie', str] = b"", 
                 value: _typing.Union['QByteArray', bytes, bytearray, memoryview, _typing.Any] = b"") -> None:
        """
        Инициализирует объект cookie с заданным именем и значением,
        или создает копию другого объекта `Cookie`.

        :param name_or_other: Имя cookie или другой объект `Cookie`.
        :param value: Значение cookie (если используется имя).
        """
        ...
    def setSameSitePolicy(self, sameSite: 'Cookie.SameSite') -> None:
        """
        Устанавливает политику SameSite для cookie.

        :param sameSite: Политика SameSite.
        """
        ...

    def sameSitePolicy(self) -> 'Cookie.SameSite':
        """
        Возвращает текущую политику SameSite для cookie.

        :return: Политика SameSite.
        """
        ...

    def normalize(self, url: Url) -> None:
        """
        Нормализует cookie в соответствии с заданным URL.

        :param url: URL для нормализации.
        """
        ...

    def hasSameIdentifier(self, cookie: 'Cookie') -> bool:
        """
        Проверяет, имеет ли cookie такой же идентификатор, как и другой cookie.

        :param other: Другой объект `Cookie`.
        :return: True, если идентификаторы совпадают, иначе False.
        """
        ...

    def swap(self, other: 'Cookie') -> None:
        """
        Обменивает содержимое текущего cookie с другим объектом `Cookie`.

        :param other: Другой объект `Cookie`.
        """
        ...

    def setHttpOnly(self, enable: bool) -> None:
        """
        Устанавливает флаг `HttpOnly` для cookie.

        :param enable: True для включения, False для отключения.
        """
        ...

    def isHttpOnly(self) -> bool:
        """
        Проверяет, является ли cookie HttpOnly.

        :return: True, если HttpOnly, иначе False.
        """
        ...

    @staticmethod
    def parseCookies(cookieString: _typing.Union['QByteArray', bytes, bytearray, memoryview]) -> _typing.List['Cookie']:
        """
        Разбирает строку cookie и возвращает список объектов `Cookie`.

        :param cookieString: Строка cookie для разбора.
        :return: Список объектов `Cookie`.
        """
        ...

    def toRawForm(self, form: 'Cookie.RawForm' = RawForm.Full) -> 'QByteArray':
        """
        Преобразует cookie в строковое представление.

        :param form: Формат представления (NameAndValueOnly или Full).
        :return: Строковое представление cookie.
        """
        ...

    def setValue(self, value: _typing.Union['QByteArray', bytes, bytearray, memoryview, _typing.Any]) -> None:
        """
        Устанавливает значение cookie.

        :param value: Значение cookie.
        """
        ...

    def value(self) -> _typing.Union['QByteArray', bytes, bytearray, memoryview, _typing.Any]:
        """
        Возвращает значение cookie.

        :return: Значение cookie.
        """
        ...

    def setName(self, cookieName: _typing.Union['QByteArray', bytes, bytearray, memoryview, str]) -> None:
        """
        Устанавливает имя cookie.

        :param cookieName: Имя cookie.
        """
        ...

    @_typing.overload
    def name(self) -> str:
        ...
    @_typing.overload
    def name(self, returntype: str) -> str:
        ...
    @_typing.overload
    def name(self, returntype: 'QByteArray') -> 'QByteArray':
        ...

    def name(self, returntype: _typing.Union['QByteArray', 'str'] = 'str') -> _typing.Union[str, 'QByteArray']:
        """
        Возвращает имя cookie.

        :return: Имя cookie.
        """
        ...
    
    def setDnsType(self, dnsType: 'DnsType') -> None:
        """
        Устанавливает DNS-тип cookie.
        :param dnsType: DNS-тип cookie ('internet' или 'gw').
        """
        ...

    def dnsType(self) -> 'DnsType':
        ...

    def setPath(self, path: _typing.Optional[str]) -> None:
        """
        Устанавливает путь cookie.

        :param path: Путь для cookie.
        """
        ...

    def path(self) -> str:
        """
        Возвращает путь cookie.

        :return: Путь cookie.
        """
        ...

    def setDomain(self, domain: _typing.Optional[str]) -> None:
        """
        Устанавливает домен cookie.

        :param domain: Домен для cookie.
        """
        ...

    def domain(self) -> str:
        """
        Возвращает домен cookie.

        :return: Домен cookie.
        """
        ...

    def setExpirationDate(self, date: _typing.Union['QDateTime', _typing.Any]) -> None:
        """
        Устанавливает дату истечения срока действия cookie.

        :param date: Дата истечения срока действия.
        """
        ...

    def expirationDate(self) -> _typing.Optional['QDateTime']:
        """
        Возвращает дату истечения срока действия cookie.

        :return: Дата истечения срока действия или None, если cookie сессионный.
        """
        ...

    def isSessionCookie(self) -> bool:
        """
        Проверяет, является ли cookie сессионным.

        :return: True, если сессионный, иначе False.
        """
        ...

    def setSecure(self, enable: bool) -> None:
        """
        Устанавливает флаг безопасности (Secure) для cookie.

        :param enable: True для включения, False для отключения.
        """
        ...

    def isSecure(self) -> bool:
        """
        Проверяет, является ли cookie безопасным (Secure).

        :return: True, если Secure, иначе False.
        """
        ...

class __CookieStore:
    @_typing.overload
    def setCookie(self, cookie: Cookie) -> None: ...

    @_typing.overload
    def setCookie(self, name: str, value: str) -> None: ...

    @_typing.overload
    def setCookie(self, name: str, value: str, path: str = "/") -> None: ...

    def setCookie(self, name_or_cookie: _typing.Union[Cookie, str], value: _typing.Optional[str] = None, path: str = "/") -> None: # type: ignore
        """Сохраняет или обновляет cookie в LocalVault и синхронизирует с QWebEngine."""
        ...

    def getCookie(self, domain: str, name: str) -> _typing.Optional[Cookie]:
        """Получает cookie из LocalVault."""
        ...

    @_typing.overload
    def removeCookie(self, cookie: Cookie) -> None: ...

    @_typing.overload
    def removeCookie(self, name: str) -> None: ...

    def removeCookie(self, name_or_cookie: _typing.Union[Cookie, str]) -> None: # type: ignore
        """Удаляет cookie из LocalVault и синхронизирует с QWebEngine."""
        ...
CookieStore = __CookieStore()