DATABASE_SETTINGS = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'skyeye_database',  # Database 이름
        'USER': 'skysys',  # 데이터베이스에서 사용할 계정
        'PASSWORD': 'tmzkdl11@!',  # 계정의 비밀번호
        'HOST': '192.168.88.20',  # 데이테베이스 주소
        'PORT': '3306',  # 데이터베이스 포트, mysql 디폴트값은 3306
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}