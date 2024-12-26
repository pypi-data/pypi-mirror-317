
![Logo](https://i.ibb.co/Yb8zMzn/randompi-header.png)


# RandomPi

RandomPi is a simple package that uses the PyPi api to get a random python package.


## Authors

- [**Wyatt Johnson**](https://github.com/realendie)


## Install

```bash
  pip install RandomPi
```
    
## Demo

Input
```
C:\Users\RandomPi>get_random_pi
```
Output
```
pypi.org/project/RandomPi/
```


## PyPi Index Api

#### Get all packages

```http
   GET /simple/ HTTP/1.1
   Host: pypi.org 
   Accept: application/vnd.pypi.simple.v1+html
```


## License

[**Apache-2.0**](https://www.apache.org/licenses/LICENSE-2.0)

