# Django UnitTest

This is example of Django UnitTest using Selenium. 

* Functional Test using Selenium
* Unit Test using Django

## Usage

to use Selenium, navigate to project directory then create virtual environment
```sh
virtualenv -p python3.8 env
source env/bin/activate

pip install -r hashthat/requirements.txt
```
now download [Selenium](https://github.com/mozilla/geckodriver/)

```sh
wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz

tar -xzvf geckodriver-v*-linux64.tar.gz
```
then link the binary to environment binary
```bash
ln -s ./geckodriver env/bin/
```
to test it
```bash
cd hashthat/
python manage.py test
```
the expected output should be like:
```
Found 9 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........
----------------------------------------------------------------------
Ran 9 tests in 14.140s

OK
Destroying test database for alias 'default'...
```

