# use latest version of python image for running django
FROM python:latest

# set default working directory inside container, in this directory project will be copied.
WORKDIR /usr/src/app

# copy required files inside container
COPY requirements.txt ./

# noce required files copied, install them without using any cache, so it will intall latest dependency on new build
RUN pip install --no-cache-dir -r requirements.txt

# once all dependency installed then copy all your current project file to work directory inside the container.
COPY . .

# expose the port which can be used outside the container, currently it expose default port 80 as same as django run script.
EXPOSE 80

# Set the default command to run project when the container starts
CMD ["python", "./manage.py", "runserver", "0.0.0.0:80"]
