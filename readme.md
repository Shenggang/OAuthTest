# Prerequisites #
You'll need:

* Python 3.5+

* The `pip` package management tool

* The Google APIs Client Library for Python:

  `pip install --upgrade google-api-python-client`

* The google-auth-oauthlib and google-auth-httplib2 libraries for user authorization.

  `pip install --upgrade google-auth-oauthlib google-auth-httplib2`

* TKinter, check if installed
  ```
  import tkinter
  tkinter._test()
  ```
  otherwise check https://tkdocs.com/tutorial/install.html for installation details.
 
 # Installation #
 ```
 git clone https://github.com/Shenggang/OAuthTest
 git pull
 cd oauth_test
 pip install --editable .
```

# Configuration #
To run the program, you need to create at least one project at Google developer's console at https://console.developers.google.com/.
Add 'Youtube Data API v3' to your project library https://console.developers.google.com/apis/library .
Configure your OAuth Consent Screen, by filling in mandatory entries https://console.developers.google.com/apis/credentials/consent .
In the consent screen page, publish your project.
Then, create a Client secret in Credentials page https://console.developers.google.com/apis/credentials.
Select your client type to be 'Desktop App'
Download your client secret as json, copy and paste the content into 'client_secret.json' in your project directory. 
If you have multiple client secrets, separate each by Enter comma Enter, e.g.
```
{secret 1}
,
{secret 2}
```
Create at least one API_key and save it in 'api_key.txt' in your project directory.

# Run #
 If your Python is managed by Anaconda, just double click the 'run.bat' file.
 Or go into project directory and run
 `python oauth_test/__main__.py`
  
===================================================================================================
# 需要 #
* Python 3.5+， Windows用户推荐安装Anaconda3，便于管理。 https://www.anaconda.com/products/individual

* pip，用于管理Python包， Anaconda自带

* 谷歌Python API库：
 `pip install --upgrade google-api-python-client`
 `pip install --upgrade google-auth-oauthlib google-auth-httplib2`
 
* TKinter图形库，一般Python自带，可以进入python检查：
  ```
  import tkinter
  tkinter._test()
  ```
  若没有安装，请参考 https://tkdocs.com/tutorial/install.html。
  
 # 安装 #
 ```
 git clone https://github.com/Shenggang/OAuthTest
 git pull
 cd oauth_test
 pip install --editable .
```

# 配置 #
运行程序需要在 谷歌控制台 登录你的谷歌账号并创建至少一个项目。https://console.developers.google.com/
在你的新项目，添加 'Youtube Data API v3'到你的库中。https://console.developers.google.com/apis/library
配置 OAuth同意屏幕，填上必填项即可。https://console.developers.google.com/apis/credentials/consent
在相同的页面，发布你的程序。
然后在凭据界面创建一个 OAuth客户端ID， 应用类型选择桌面应用。https://console.developers.google.com/apis/credentials.
在凭据界面下载刚才创建的凭据，并复制其内容到点踩机路径的 'client_secret.json' 文件里。
当你有多个 OAuth客户端 凭据时，用 回车 逗号 回车 分割每个凭据，比如：
```
{secret 1}
,
{secret 2}
```
至少创建一个 API密钥 并保存至 'api_key.txt'。

# 运行 #
若你使用的是Anaconda, 可以直接双击运行 “run.bat” 文件。
如果你的Python在环境变量里，则可以在项目路径里直接运行
```python oauth_test/__main__.py```


   
