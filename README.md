# CAMPUS E-RAKSHA SEVA
![Campus-Saathi-logo](https://github.com/anuran-roy/hacknpitch/blob/main/media/forum/images/ic_launcher.png "CAMPUS OWL : ALWAYS GUARDING THE CAMPUS 💯 🥇 👍🏻 ")
 
### Hack 'N' Pitch Project on Campus E-Governance.

# Requirements
Any Windows/Linux 4.14+ kernel/MacOS with Python 3.8.10 or above.
```bash
sudo apt-get install python3 # for Debian & Ubuntu based Systems
sudo yum install python3-devel.x86_64 # for RPM bases Systems
sudo  pacman -S glib2-devel pacman -U python-3.8.10 # for Arch Systems
```
For Windows 10 ,Mac,Android Download from offical site of Python and run their respective binaries .
```bash
python # in Windows 11 Terminal for installing python
```
## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install E-Governance Django App.

```bash
pip3 install requirements.txt
python3 manage.py runserver [specify port] #for Linux Systems
```
For Windows Environment 
```bash
pip install requirements.txt
python manage.py runserver [specify port] #for Linux Systems
```
Note:- Virtualenv needs to be configured and activated for production server. WSGL and other workers , Static_files aswell as Allowed_Hosts needs to be configured in settings.py for final deployment over the net.

## Usage

```python
Performing system checks...

System check identified no issues (0 silenced).
September 20, 2021 - 17:09:32
Django version 2.0, using settings 'ChatApp.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
MIT License

Copyright (c) 2021 Team n00bs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
[LICENSE](https://github.com/anuran-roy/hacknpitch/blob/main/LICENSE)
