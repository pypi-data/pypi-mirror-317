from setuptools import setup

# README.md 파일을 불러오는 기능
with open('README.md', encoding='utf-8') as f:
  long_description = f.read()

setup(
  name='wrtn', # 등록할 패키지 이름 (PyPI에 등록되는 이름)
  version='1.1.3', # 패키지 버전
  description='unoffical wrtn api', # 패키지의 짧은 설명
  long_description=long_description, # 패키지의 상세 설명
  long_description_content_type = 'text/markdown', # long_description의 형식
  author='sickwrtn', # 패키지 작성자 이름
  author_email='sillo154265@gmail.com', # 패키지 작성자 이메일
  url='https://github.com/sickwrtn/unoffical_wrtn_api', # 프로젝트의 공식 URL
  license='MIT', # 패키지의 라이선스 정보
  python_requires='>=3.7', # 패키지가 지원하는 Python 버전
  install_requires=["requests==2.32.3",
    "setuptools==75.6.0",], # 패키지가 의존하는 외부 라이브러리 목록
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
  ] # 패키지 분류
)