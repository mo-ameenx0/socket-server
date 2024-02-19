LOGGING_CONFIG = { 
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': { 
        'stdout': { 
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'server.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 1
        },
    },
    'loggers': {
        'server': { 
            'handlers': ['stdout', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    } 
}