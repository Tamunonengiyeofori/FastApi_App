# CREATING A DOCKER IMAGE

FROM python:3.9.7

# This is the directory where the code will be executed
WORKDIR /usr/src/app 

# Copy the dependencies required to the directory
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy all source code files to the directory of the docker image
COPY . . 

# RUN COMMAND TO START THE APPLICATION 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

