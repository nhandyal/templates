FROM nhandyal/base:latest

# Replace the appropriate values for your project. Remove after updating.
# {project_root} is the abs path of the project INSIDE the container.
# 
# RUN printf '\nexport PATH=$PATH:/worspaces/{project_name}/bin\n
RUN echo "Update PATH in Dockerfile" && \
    exit 1

RUN pushd '../' && \
    pip3 install -r requirements.txt && \
    npm i
