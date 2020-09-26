#mqtt settings
mqtt_login = 'iunddsnu'
mqtt_password = '7FpJGsEHSxQA'
mqtt_broker = "hairdresser.cloudmqtt.com"
mqtt_port = 15636
mqtt_command_topic = 'smart_university/{}/execute_comand'
mqtt_response_topic = 'smart_university/response'
mqtt_keepalive = 60
#zoom settings
zoom_login = 'ozehnNDIS9WE9Ek9l8_PgA'
zoom_password = 'BREXJVzjypqFWUcRdXN6zNPDeCm35ueuUXf1'
path_to_zoom = r'C:\Users\Snowfall\AppData\Roaming\Zoom\bin\Zoom.exe'
len_zoom_meeting_id = 8
imgs_path = 'imgs//'
#lms settings
lms_user_login = 'st649687'
lms_user_password = 'andrey123'
#Message handler codes
MESSAGE_FORMAT_ERROR = 'Неверный формат сообщения'
UNSUPPORTED_COMMAND_ERROR = 'Данная команда не поддерживается'
ALREADY_RUNNING_ERROR = 'Сессия уже запущена'
ALREADY_CLOSED_ERROR = 'Сессия уже завершена'
SUCCESS_CODE = 'Успешно'
#Zoom error
BUTTON_ERROR = 'Возникли проблемы с кнопкой: {}'
WRONG_PATH_ERROR = 'Не правильно указан путь к Zoom'
MEETING_ID_ERROR = 'Неверно указано поле: ID конференции'
#Lms error
LOGGING_IN_WITHOUT_PARAMETERS_ERROR = 'Данные для входа в систуму LMS не предоставдены!'
WRONG_PARAMETERS_ERROR = 'Невправильно введены параметры входа'
DRIVER_NOT_FOUND_ERROR = 'Драйвер для запуска браузера не был найден'
ELEMENT_NOT_FOUND_ERROR = 'Ошибка при поиске элемента в браузере'
WRONG_LINK_ERROR = 'Неверная ссылка на трансляцию'
#Events
