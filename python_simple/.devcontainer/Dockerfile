FROM nhandyal/base:latest

RUN curl -sSL https://install.python-poetry.org | python3 -

# Replace the appropriate values for your project. Remove after updating.
# {project_root} is the abs path of the project INSIDE the container.
# 
# RUN printf '\nexport PATH=$PATH:/worspaces/{project_name}/bin\n
RUN echo "Update PATH in Dockerfile" && \
    exit 1

# Can't do this because the code is not part of the image yet
# RUN cd '../' && \
#     pip3 install -r requirements.txt && \
#     npm i
