from setuptools import setup, find_packages

setup(
    name='Mustpy',  # اسم المكتبة (يجب أن يكون فريدًا في PyPI)
    version='0.1.0',
    packages=find_packages(),
    description='A simple Python library for math and string utilities',
    author='Mustaid',  # ضع اسمك
    author_email='amust5175@gmail.com',  # ضع بريدك الإلكتروني
    url='https://github.com/yourusername/my_library',  # اختياري: رابط GitHub
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)