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
#Message handler codes
MESSAGE_FORMAT_ERROR = 'invalid format of message'
UNSUPPORTED_COMMAND_ERROR = 'unsupported command'
ALREADY_RUNNING_ERROR = 'the session is already running'
#Zoom codes
BUTTON_ERROR = 'problem with button: {}'
WRONG_PATH_ERROR = 'wrong path to zoom, change the path'
SUCCESS_CODE = 'success'
ALREADY_CLOSED_ERROR = 'Is already closed'
#Lms error
LOGGING_IN_WITHOUT_PARAMETERS_ERROR = 'Данные для входа в систуму LMS не предоставдены!'
WRONG_PARAMETERS_ERROR = 'Incorrect login parameters'
DRIVER_NOT_FOUND_ERROR = 'The driver was not found'
ELEMENT_NOT_FOUND_ERROR = 'The required element was not found'
WRONG_LINK_ERROR = 'Wrong link'
