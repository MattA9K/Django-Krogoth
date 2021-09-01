# Django Krogoth

![alt text](https://raw.githubusercontent.com/MattA9K/Django-Krogoth/master/core_krogoth.jpg)

Start development of a single page web application within 20 minutes or less. Edit your web app straight from the Django Admin panel, or via the custom IDE. Save your changes and test within seconds (get rid of that `clear browser cache` addon).

----



## Krogoth Quickstart

Just three simple steps. *(Applies to any x86 machine that can run Docker)*


1. Install Docker

2. Clone Krogoth

3. Run Krogoth Installer


Step 1 applies specifically to Ubuntu 16. Ubuntu 16 uses less RAM out of the box and runs less services that utilize CPU resources as well, *(compared to later versions of Ubuntu)* but it really doesn't matter, so long as the Unix based OS can run docker, then you're good to launch. If you're running macOS, skip the first step and just install docker desktop, then proceed to step 2.

### Step 1. Install Docker

```bash
# apt-get install -y apt-transport-https 

# apt-get install -y ca-certificates 
# apt-get install -y curl 
# apt-get install -y gnupg-agent 
# apt-get install -y software-properties-common

# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
# add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# apt-get update
# apt install docker.io
```




### Step 2. clone

```bash
$ git clone https://github.com/MattAndrzejczuk/Django-Krogoth.git
```


### Step 3. install

BIG WARNING HERE, THIS INSTALLER AS OF RIGHT NOW WILL DESTROY ANY AND ALL DOCKER IMAGES CURRENTLY RUNNING. IT'S HIGHLY RECOMMENDED THAT YOU TRY THIS ON A FRESH VM WITH NO OTHER DOCKER IMAGES INSTALLED.

```bash
$ cd Django-Krogoth/docker
$ python3 install_all_in_one.py
```
----


## You're Now Live

whatever the IP of the machine is, the app is live and you can navigate to it. If you installed this locally, navigate to `http://localhost` and that's it. Kroogoth is now live and you can start adding and developing your AngularJS single page web app with ease `(the built in IDE makes this easy)`.

![alt text](https://raw.githubusercontent.com/MattAndrzejczuk/Django-Krogoth/master/krogoth.png)

Navigate to `http://SERVER_HOSTNAME/` and see the live app. 

### What Now?
Remember to create a super user using the following steps:
```bash
$ docker exec -it armprime bash
# ./manage.py createsuperuser
```

### Try The Built In IDE
Navigate to `http://0.0.0.0:8000/#!/Login` and log in as the superuser you've just created.

Then, navigate to `http://SERVER_HOSTNAME/#!/UltraEditorBrowse`

Click on `Primary`, `Required`, then finally `home`.

You should now be in the built-in IDE editor. from here, you can make changes to the AngularJS home page.
