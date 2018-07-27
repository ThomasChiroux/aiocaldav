import pytest


def pytest_addoption(parser):
    parser.addoption('--no-backend-radicale', action='store_true',
                     help='remove radicale from the tested backend')
    parser.addoption('--no-backend-davical', action='store_true',
                     help='remove davical from the tested backend')
    parser.addoption('--no-backend-xandikos', action='store_true',
                     help='remove xandikos from the tested backend')
    parser.addoption('--no-backend-cyrus', action='store_true',
                     help='remove cyrus from the tested backend')
    
    parser.addoption('--only-backend-radicale', action='store_true',
                     help='only test against radicale backend')
    parser.addoption('--only-backend-davical', action='store_true',
                     help='only test against davical backend')
    parser.addoption('--only-backend-xandikos', action='store_true',
                     help='only test against xandikos backend')
    parser.addoption('--only-backend-cyrus', action='store_true',
                     help='only test against cyrus backend')
    
    parser.addoption('--only-direct-backend-radicale', action='store_true',
                     help='only test against radicale backend in direct mode')
    parser.addoption('--only-direct-backend-davical', action='store_true',
                     help='only test against davical backend in direct mode')
    parser.addoption('--only-direct-backend-xandikos', action='store_true',
                     help='only test against xandikos backend in direct mode')
    parser.addoption('--only-direct-backend-cyrus', action='store_true',
                     help='only test against cyrus backend in direct mode')
    